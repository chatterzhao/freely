---
schema_version: '1'
local_id: raw-20261103T132556Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132556Z-A
platform_ids:
  github:
    issue_id: '4152'
    url: https://github.com/chatterzhao/freely/issues/4152
    synced_at: ''
  gitee:
    issue_id: IKSPQ7
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ7
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20261103T132556Z/issues/I-20261103T132556Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:25:56Z'
updated_at: '2026-11-08T09:30:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132556Z-A
source_candidate: ''
completed_at: '2026-11-08T09:30:00Z'
closeout_note: ''
---

# fix: ACP bridge 按 session 路由避免越权代答

workflow_kind: fix

## 根因
一个 `(project, base_tool)` 只有一个 bridge 进程，它把 ACP server 的每条通知广播给所有已连接客户端；客户端也从不比对 `params.sessionId`。路由责任在两层之间被同时放弃。

## 证据
- 单点：`docs/system/workspace/scripts/runtime/acp-bridge.py:58-60`（一个 socket）、`freely:22850-22878`（只按 base_tool 去重，eager 只起 manager 的）。
- 广播：`acp-bridge.py:497-510` docstring 即 `Forward server notification to all connected clients`，实现为 `for sock in self.clients: sock.send(data)`；注册列表 `:630-632`（本次复核确认）。
- 客户端不筛：`docs/system/workspace/scripts/runtime/run-acp-prompt.py:218-226` 只按 `method` 分派；`_handle_session_update:232-247` 把 `agent_message_chunk` 直接 `sys.stdout.write`；`_handle_permission_request:250-260` 不看 session，`mode=="auto"` 时优先选 `allow_always / allow_once`。
- 权限面放大：`acp-bridge.py:45-50` 默认 `bypassPermissions`。
- 与文档冲突：`docs/system/workspace/acp-session-architecture.md:41-43` 声称「Worker-A/B 各自独立 session，互不干扰」。

## 影响
两个 worker 并发时，A 的 `agent_message_chunk` 被写进 B 的 stdout → 污染 B 的证据与日志解析（B 的「我的输出」里混入 A 的话）；更严重的是任一客户端会替别的 session 回答权限请求，且答案是 allow。这是已知唯一的「并发正确性 + 权限越界」双料缺陷。

## 修复方案
1. 最小修法（两层都加过滤）：`acp-bridge.py:497` 按 `params.sessionId` 定向投递（未知 session 丢弃并记日志，不广播）；`run-acp-prompt.py:218-226` 在 handle 前比对 `params.sessionId != self.session_id → drop`，权限请求同理（不匹配则不应答，让真正的主人答）。
2. `_handle_permission_request` 的 `auto` 模式改为「必须 session 匹配才应答」，不匹配时不应答且不默认 allow。
3. `bypassPermissions` 默认值改为显式 opt-in（启动参数或 env 明确开启），默认不放大权限面。
4. 彻底修法（可选）：每 session 一个 bridge 或一条连接，需先评估进程数（当前一个项目 ≥6 常驻进程）。
5. 前置条件：先抓一次真实流量确认 `session/update` 总带 `sessionId`（报告 U6），否则过滤会丢消息。

## 验收标准
- RED：起一个 bridge + 两个 `run-acp-prompt.py`（session A/B），server 只向 A 发 `agent_message_chunk`：当前 B 的 stdout 也会出现该文本；修复后 B 不得出现。
- RED：向 A 发 `session/request_permission`，B 不得应答；当前 B 以 `allow_always` 应答（隔离 mock server 验证，不调真实平台）。
- GREEN：`grep -n "sessionId" run-acp-prompt.py` 至少一处出现在**入站过滤**路径（当前只出现在出站请求参数里）。
- GREEN：`bypassPermissions` 默认不再为真，默认路径下权限请求必须 session 匹配。

---
schema_version: '1'
local_id: raw-20261104T075857Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T075857Z-A
platform_ids:
  github:
    issue_id: '4161'
    url: https://github.com/chatterzhao/freely/issues/4161
    synced_at: ''
  gitee:
    issue_id: IKSW8X
    url: https://gitee.com/zhaoquan/freely/issues/IKSW8X
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/issues/I-20261104T075857Z-A.md
last_synced_comment_at:
  github: '2026-11-11T11:58:37Z'
  gitee: '2026-11-11T11:58:37Z'
hash: ''
created_at: '2026-11-04T07:58:57Z'
updated_at: '2026-11-11T11:58:42Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T075857Z-A
source_candidate: ''
completed_at: '2026-11-11T11:58:36Z'
closeout_note: ''
---

# refactor: 收口 Bash 与 Python 的跨进程数据契约

workflow_kind: feature

## 根因
编排/会话/worktree/daemon 在 Bash，A2A/DB/ACP/scan 在 Python；两侧通过 Unix socket JSON-RPC、env 文件、temp 文件、stdout 文本互相传递，没有统一的序列化契约与错误模型。

## 证据
- 规模：Bash 约 31K 行、Python 约 17K 行。
- 边界样本：`bin/issue-sync:338-342` 用位置参数调 `gitee-issue.py`，被调侧 argparse 只接受子命令 + 具名 flag → 退出码 2 被 `|| echo '{"ok":false}'` 吞成合法 JSON。
- 状态传递：`.freely/run/*.env` 由 `source` 读入（可执行语义），`workcell-state.env`/`manager-worker-launch-state.env` 同族。
- 错误模型：Bash 侧靠退出码与文本 grep，Python 侧抛异常或返回 dict，两侧无共同错误码。

## 影响
- 参数错配、字段缺失都表现为「空结果」而非失败。
- 测试碎片化：552 个脚本测试，Bash 侧几乎没有单元测试。
- 换实现语言时无法保证语义不变。

## 修复方案
1. 定义跨边界契约：每个调用点声明输入 schema、输出 schema、错误码；统一为 `{"ok":bool,"code":str,"data":...}`。
2. 所有 Bash→Python 调用改为「子命令 + 具名参数 + JSON 输出」，禁止位置参数与文本 grep。
3. 状态文件统一为不可执行格式（`KEY<TAB>value` 或 JSON），读侧用白名单解析，禁止 `source`。
4. 为 3 个高频边界（issue-sync、scan、db-cli）补契约测试。

## 验收标准
- RED：给 `gitee-issue.py` 传错参数，调用方必须显式失败；当前被 `|| echo` 吞掉。
- GREEN：三个边界的输入/输出 schema 有单页文档并被测试引用。
- GREEN：`grep -rn "source .*\\.env"` 为 0。
- GREEN：新增边界契约测试 ≥3 条，覆盖字段缺失、类型错误、超时。

### comment-20261111T115836Z
- source: system
- event: promote_finalized
- children: ["I-20261104T075857Z-A"]

拆解为以下任务:
1. [I-20261104T075857Z-A](will-be-updated)

---
candidate_id: C-20261103T132556Z-A
status: promoted
source_raw: raw-20261103T132556Z
created_at: 2026-11-08
milestone: M-20261103T132556Z-A
---

# Candidates

被否决方案（每 session 一 bridge、未知 session 丢弃、裸默认无 opt-in 翻转）见 brainstorms.md，均经证伪后收窄，不另立 candidate。

## C-20261103T132556Z-A: 两层 session 路由 + 裸默认显式 opt-in

- candidate_format_version: v2
- title: 客户端 `ACPClient` 绑定自身 session 并按 positively-mismatched `params.sessionId` 过滤入站 `session/update`/`session/request_permission`；bridge 维护 client→session 映射做定向投递（未知/缺失回退广播）；`bypassPermissions` 裸默认改为显式 opt-in
- status: promoted
- decision_reason: 一个 (project,base_tool) 单 bridge 广播 + 客户端零 session 校验，导致 worker A 输出污染 B 的 stdout、B 越权代答 A 的权限请求。客户端知道自己唯一的 session，是最可靠的过滤点；bridge 定向投递是纵深防御。缺省/缺失 sessionId 一律保留旧行为（U6），不丢消息。
- next_action: 建 AT-001（4 静态 + 15 行为：客户端 4 场景 + 权限 3 场景 + bridge 4 场景 + 权限默认 3 场景），改 `run-acp-prompt.py` 与 `acp-bridge.py`。
- revisit_trigger: 若引入 `acp_bridge_v2.py`（SDK 版）或把 ACP server 换成不带 `sessionId` 的实现，两层路由都需复核；若 `acp` SDK 上线，需确认 v2 是否同样定向投递。
- acceptance_criteria:
  - RED(baseline `35ce56765`)：B 的 stdout 出现 A 的 chunk；B 对 A 的权限请求以 allow 应答；bridge 把 A 的通知也发给 B；裸默认为 bypassPermissions。
  - GREEN：`sessionId` 出现在 `run-acp-prompt.py` 入站过滤路径；`bypassPermissions` 裸默认不再为真且权限请求必须 session 匹配。
  - 不退化：own-session / 无 sessionId / 未知自身 session / 未知 session 广播 / 空注册表 / 显式 opt-in / `CLAUDE_CODE_PERMISSION_MODE` 权威，全部保持。
  - 相关回归：`test-prompt-manifest-integration.py` 通过；4 个 cc 预存红测试与 develop 基线退出码一致（归 #4151）。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate + 人工四层 TDD review
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复核 execv/SDK 运行时路径、bridge 广播实现、client sessionId 分布、permission-mode 生产注入链；证伪 3 个高风险字面方案并收窄；AT-001 在 develop 基线快照 9 ok/10 failed → 工位 19 ok/0 failed。
  - verdict: pass
- promoted_issue_id: I-20261103T132556Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20261103T132556Z/issues/I-20261103T132556Z-A.md
- milestone: M-20261103T132556Z-A
- session_refs: []

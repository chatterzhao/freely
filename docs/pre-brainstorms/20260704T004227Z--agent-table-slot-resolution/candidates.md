---
candidate_id: C-20260704T004227Z-A
status: promoted
source_raw: raw-20260704T004227Z
created_at: 2026-07-04
milestone: M-20260704T004227Z-A
---

# Candidates

## C-20260704T004227Z-A: 修复 agent-id 子串匹配 bug

- candidate_format_version: v2
- title: 修复 _startup 中 agent-id 解析的子串匹配 bug
- status: promoted
- decision_reason: develop 路径 `.../freely` 是 worktree 路径 `.../freely-worktrees/...` 的子串，grep -F 误匹配导致 develop 上 resolve 出 worker_01。这是明确的代码 bug，修复范围小、风险低。
- next_action: 修改 `grep -F "$(pwd)"` 为精确匹配（锚定路径分隔符或行尾），然后走 dev-loop。
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - develop 上 `_my_id` 正确解析为 `manager_01`
  - worktree 路径上 `_my_id` 仍正确解析为对应 worker_id
  - 不影响 agent-id.env 中其他行的解析
- promotion_gate: 代码修改正确，grep 模式改为精确行尾匹配
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 agent-id.env 的 grep 子串匹配问题，确认修复方案正确
  - verdict: pass
- promoted_issue_id: I-20260704T004227Z-A
- promoted_issue_path: docs/epics/{epic-name}/{story-name}/raw-20260704T004227Z/issues/I-20260704T004227Z-A.md
- milestone: M-20260704T004227Z-A
- session_refs: []

---

## C-20260704T004227Z-B: 诊断并修复 slot 模型不匹配

- candidate_format_version: v2
- title: 诊断 agent-table slot 配置与实际推理模型不匹配的根因
- status: needs_research
- decision_reason: 根因尚未确定。三个可能方向需逐一验证：OPENCODE_CONFIG 未被 opencode ACP 正确读取、acp-bridge.py SDK 硬编码、环境变量污染。不可在未确认根因前盲目修改代码。
- next_action: 启动 freely 并开启 debug trace，捕获 bridge launch 时的环境变量和 opencode ACP server 的实际行为，确定模型错配发生在哪个环节。
- revisit_trigger: 根因确定后重新评估 scope；若根因在外部依赖则可能标记为 blocked 等待上游修复。
- acceptance_criteria:
  - 确认根因：哪个环节导致 deepseek-v4-pro 被使用而非 deepseek-v4-flash-free
  - 修复方案经过 B2 设计阶段评审
  - 修复后 agent-table 配置的 slot 与实际推理一致
- promotion_gate: 根因已确认，修复方案已设计
- open_questions:
  - OPENCODE_CONFIG env var 是否被 opencode ACP server v1.17.13 正确读取？
  - acp-bridge.py 的 session/set_mode 是否覆盖了模型配置？
  - daemon 进程环境是否有残留 ANTHROPIC_* 变量？
- milestone: M-20260704T004227Z-A
- session_refs: []

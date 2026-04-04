# Code Review - checkpoint-and-fleet-verification

- issue_id: `I-20260318-0930`
- date: `2026-03-18`
- reviewer_tool: `codex`
- reviewer_session_id: `current-thread`

## Scope

- `docs/system/workspace/scripts/quality/checkpoint-guard`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/scripts/tests/test-checkpoint-guard`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Findings

- no blocking findings

## Verified Behavior

- `checkpoint-guard` 能同时覆盖 clean tree、mixed control/product planes 与 staged-only 阻断。
- `wt-fleet-status` 与 `freely fleet-status` 已按工位读取 runtime 摘要；缺少结构化 phase/issue 时保持 `unavailable`，不伪造 milestone 状态。
- `freely baseline-status` 已暴露 `last_project_dirty_entries`、`last_worktree_summary_total`、`last_worktree_summary_dirty`、`checkpoint_required` 与 `checkpoint_reasons`。
- 首跳 prompt 已携带项目级工位快照，并要求主管模式先做排班、冻结、集成与 cleanup 判断；同工具场景继续第二跳而不是只停在 handoff。
- 受保护分支上的首跳 prompt 现在会进入 `MANAGER_MODE=true`，明确限制主管工位只做监督、委派与 continuity，不在 `develop/main/test-pre-merge-*` 直接执行第二跳实现。

## Tests

- `bash docs/system/workspace/scripts/tests/test-checkpoint-guard`
- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/start-lead-agent.sh --project /Users/zhaoyu/Downloads/code/my-freely/freely --intent /Users/zhaoyu/Downloads/code/my-freely/freely/docs/PROJECT_INTENT.md --constitution /Users/zhaoyu/Downloads/code/my-freely/freely/docs/CONSTITUTION.md --ai codex:auto`

## Residual Risks

- 当前只完成到 `in_verification`，还没有 promote / cleanup 证据。
- `I-20260307-1201` 与 `I-20260308-0101` 的收口仍需在后续轮次完成。

# Issue: worktree-maintenance-governance

- issue_id: `I-20260320-1405`
- title: Worktree maintenance governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-maintenance-governance`
- issue-name: `worktree-maintenance-governance`
- source_candidate: `docs/B1-docs/raw-20260320T174500Z/candidates.md#c-20260320-1410-a`
- source_brainstorm: `docs/B1-docs/raw-20260320T174500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 现有技能已经覆盖：

- how to create worktrees
- how to watch dirty/checkpoint/runtime state
- how to cleanup after verified retirement

但没有一条能力专门负责 worktree 创建后的维护：

- 单棵树真实状态审计
- 多棵树 merge-prep 顺序与冲突面
- companion / obsolete worktree 的 salvage_then_retire

这会让主管在 worktree 积累后反复用 milestone、issue、review、tests、git ancestry 和聊天上下文临时拼判断。

## Scope

1. 新增 `skill:worktree-maintenance-governance`
2. 在 skill 中定义三种模式：
   - `audit`
   - `merge_prep`
   - `retirement_handoff`
3. 更新主管真源与首跳提示，让主管在合适时候调用该 skill
4. 增加最小脚本级回归，锁定首跳提醒

## Acceptance

- 存在专门 skill 处理 worktree 维护问题，而不是继续依赖 ad hoc 判断
- skill 明确区分 `audit / merge_prep / retirement_handoff`
- `lead-agent`、`manager-agent` 和 `start-lead-agent.sh` 知道何时调用该 skill
- `test-routing-foundation-loop` 锁定这条提示

## Completion

- `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/audit.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/merge-prep.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/retirement-handoff.md`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Next

- 这条治理能力已落盘完成；后续如果要把 merge-prep 自动化成 CLI 或 runtime owner contract，再从同一主题开新 candidate，不在本 issue 扩 scope。

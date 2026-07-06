# Pre-tests: worktree-maintenance-governance

1. `skill:worktree-maintenance-governance` 明确区分 `audit / merge_prep / retirement_handoff`
2. `lead-agent` 和 `manager-agent` 都把 worktree maintenance 当作主管级能力，而不是临时经验
3. `start-lead-agent.sh` 明确提示在 worktree 审计、merge 顺序或 retirement handoff 场景下读取该 skill
4. `test-routing-foundation-loop` 锁住上述提示

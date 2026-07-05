# Pre-tests: manager-delegation-after-sufficient-patrol-evidence-governance

## Pre-merge acceptance

1. `manager-agent` 明确写出：
   - stable disposition 后优先 delegate
   - 只有 blocker / missing fact 时才继续 patrol
2. `auto-loop-orchestrator` 明确写出：
   - project-level patrol 完成后进入具体 execution routing
   - 不能只停在 manager continuity
3. `multi-worktree-supervision` 明确写出：
   - `retire-only / retire-now / continue-dev` 的默认下一跳是 worker execution

## Post-merge acceptance

1. 继续在 `develop` 上使用 `freely chat` 做主管巡检时，观察主管是否更快地进入 worker delegation，而不是无限续写 patrol 证据。

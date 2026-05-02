# Brainstorm: runtime-startup-root-cause-packet-governance

## Goal

把 `20260413-0420` 预研的 root-cause 结论和分流策略，以一个 develop-bound 文档型 owner 固化下来，避免后续实现 lane 再依赖临时 feature worktree 上的 candidate-only truth。

## Frozen Conclusions

1. `startup authority` 是 promote-ready 的实现 owner 边界，应由后续实现 lane 负责：
   - launch identity
   - startup truth publication
   - daemon ready semantics
   - ghost-supervisor cleanup truth
2. `manager handoff contract` 仍需研究，不应混入本轮启动 authority 修复。
3. 当前 worktree 的职责是记录 split，而不是抢跑实现。

## Routing Decision

- `C-20260413-0420-A` 保持 `implementation_ready: true`，但仍等待 dedicated implementation worktree 开 owner。
- `C-20260413-0420-B` 保持 `needs_research`，继续作为 manager continuity/manager_ready follow-on 的入口。
- `C-20260413-0420-C` 吸收这次 packet split，并承担 develop-bound canonicalization。

## Guardrails

1. 不在本 owner 内宣称 fake-supervisor、daemon readiness 或 continuity gap 已修复。
2. 不把 packet split 伪装成 implementation done。
3. develop absorb 通过后，当前 feature worktree 应进入 retire-only closeout，而不是继续扩 scope。

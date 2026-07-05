# Brainstorms - 20260404-0119--governance-merge-gate-milestone-status-followthrough

## Context

`feature/sandbox-compatible-runtime-bootstrap-and-operator-state-20260403-2245` 已经把 `/bin/ps` 不可用时的 runtime attach fallback 修到可验证状态，但在 replay 到 canonical `develop` 前又被 `governance-merge-gate` 拦住了一次。这次不是 runtime owner 本身缺 lifecycle，而是 merge gate 对 `docs/milestones.md` 的解析出了层级错误。

## Trigger

真实报错是：

- `C-20260403-2245-A ... has status 'promoted', but declared milestone M-20260306-workspace-routing-foundation has status 'needs_research'.`

但 `docs/milestones.md` 里 `M-20260306-workspace-routing-foundation` 的顶层状态实际是 `active`。误判发生在 `parse_milestones()`：它把 queue item 内部的 `- status:` 也当成 milestone 顶层状态读进了 `current_milestone_status`。

## Verified Repo Facts

1. `docs/milestones.md` 当前确实允许 queue item 带自己的 `status`，例如 `candidate_issues` 下的 `needs_research` 条目。
2. `docs/system/workspace/scripts/quality/governance-merge-gate` 的 `parse_milestones()` 目前在进入 queue 之后，仍会对任何缩进层级的 `- status:` 直接改写 `current_milestone_status`。
3. 这会把真正 `active` 的 milestone 误读成 queue item 的 `needs_research`，进而错误阻断 develop-bound replay。
4. 这条问题属于 merge-gate parser residual regression，不属于 runtime bootstrap owner 本身。

## Boundary

这条 followthrough 只处理：

1. `parse_milestones()` 只读取 milestone 顶层 `- status:`，不再吞掉 queue item 的 `status`。
2. `test-governance-merge-gate` 增加一条 focused regression，锁住“milestone active + nested candidate status needs_research”仍能通过的场景。
3. 为 develop-bound replay 补齐最小 candidate / issue / progress / verification owner。

这条 followthrough 不处理：

1. runtime `/bin/ps` fallback 本身的实现边界
2. milestone 排程策略重设计
3. `governance-check` 的 milestone 解析重写
4. 任何 broader merge-gate policy widening

## Why A New Narrow Owner

`protected-branch-merge-receipt-hardening` 已经完成，并且明确写了：之后若再出现 merge-gate residual regression，应开更窄的 follow-on owner，而不是去改写已完成 owner。当前问题正符合这条规则：

- 它是真实 replay 暴露出的 parser bug
- 范围只是一处层级解析与一条 focused regression
- 继续把它塞回更宽的 break-glass / receipt owner 只会重新混淆已关闭 contract

## Working Conclusion

应 materialize 一个新的、窄到只承接 milestone-status parser bug 的 followthrough owner，挂回 `workspace-routing-foundation`，并以 `in_verification` 方式直接完成实现与验证，不再额外扩展 runtime 或 milestone policy 讨论。

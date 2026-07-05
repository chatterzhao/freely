# Brainstorm: protected-branch-hook-bypass-breakglass-governance

## Frozen Problem Statement

Freely 现有治理把 `.githooks` 与 develop-bound gates 当作受保护分支的主要执行面，但它们并不自动回答：

- 什么时候允许 break-glass
- 谁可以判定 break-glass
- break-glass 后必须留下什么 receipt
- 如何在后续 canonical 检查中发现未授权 bypass

这次 dogfood 已证明，只要这些问题没写成真源，AI 就可能把“我确认是误报”误当成合法例外。

## Revert Probe Truth

使用独立临时 probe worktree 对当前 `develop` 做了真实 dry-run：

- `git revert --no-commit -m 1 27faa2e`
  - `rc=0`
  - 可干净进入 revert 状态
- `git revert --no-commit -m 1 a10f6d8`
  - `rc=1`
  - 可进入 revert 但会与后续 writeback 产物冲突

冻结结论：

- `27faa2e` 可逆
- `a10f6d8` 可逆但不是无冲突“一把回退”
- source branch / worktree 已删不影响 revert 可行性
- 默认优先处理 governance bypass，而不是先整体回退 ownership feature

## Frozen Layering

### Constitution

定义原则：

- protected-branch hook/gate bypass 默认违规
- 只有规范显式定义的 break-glass 才允许

### Laws

作为唯一白名单词典，冻结：

- `break_glass_reason`
- `blocked_gate`
- `required_evidence`
- `operation_scope`
- `follow_on_owner`
- `forbidden examples`

### AGENTS / Hooks README / Skills

仅承担提醒与执行消费：

- 不得自行决定 `--no-verify`
- 命中 break-glass 时，必须按 `LAWS` 中的字段和顺序执行

### Runtime / Merge / Quality

冻结可执行 contract：

- `pr-merge-guarded` 不能只负责 merge 发起，还要定义冲突后的 completion path
- `governance-check` 要能审计 bypass receipt
- hook 继续是本地 gate，但要明确“它不是绝对防线”

## Minimal Phase-1 Reason Taxonomy

- `tooling_unavailable`
  - gate/hook 根本无法执行，但存在等价独立验证与证据
- `verified_false_negative`
  - gate/hook 已执行，但有保留输出和最小 repro，且 follow-on owner 已 materialize

## Frozen Forbidden Examples

以下理由一律不能构成合法 bypass：

- 赶时间
- 只差最后一个 merge commit
- 我人工确认没问题
- 只是 docs / writeback / cleanup 小改动
- hook 文案看起来不合理

## Minimal Receipt Contract

phase-1 至少要冻结：

- `bypass_mode`
- `break_glass_reason`
- `blocked_gate`
- `operation_scope`
- `evidence_refs`
- `follow_on_owner`

receipt 的最终落点仍待本 issue 冻结，但至少一层必须 machine-readable。

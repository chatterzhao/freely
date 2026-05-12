# Protected Branch Break-Glass Receipts

本文件是 protected-branch break-glass 事后审计 ledger。

使用规则：
- 只记录已经落到 protected branch merge commit 的 break-glass receipt
- 不记录普通 `merge-guarded` / `merge-guarded-complete`
- 每条 receipt 都必须能被 `governance-check` 从 merge commit trailer 回溯到本文件
- 允许 break-glass 不等于允许自由 bypass；白名单与最小作用域以 `docs/LAWS.md` §2D 为准

最小字段：
- `audit_effective_date`
- `source_policy_effective_date`（可选；用于定义 develop/test-pre-merge source-branch 新语义的生效日期）
- merge commit hash 标题
- `target_branch`
- `source_branch`
- `receipt_mode`（可选；默认 `trailer_parity`，历史补录可显式标记 `legacy_backfill`）
- `bypass_mode`
- `break_glass_reason`
- `blocked_gate`
- `operation_scope`
- `follow_on_owner`
- `evidence_refs`

- audit_effective_date: `2026-04-02`
- source_policy_effective_date: `2026-04-06`

## Receipt Contract

本文件是 protected-branch break-glass merge 的 post-merge receipt ledger。它不授予绕过权限；权限边界仍由 `docs/CONSTITUTION.md` 与 `docs/LAWS.md` §2D 定义。

记录要求：
- 只记录 `Freely-Bypass-Mode: break_glass` 的 protected-branch merge commit
- 每条 receipt 必须与 merge commit trailer 一一对应，至少写出：
  - merge commit hash
  - `target_branch`
  - `source_branch`
  - `receipt_mode`
  - `bypass_mode`
  - `break_glass_reason`
  - `blocked_gate`
  - `operation_scope`
  - `follow_on_owner`
  - `evidence_refs`
- phase-1 的 `operation_scope` 只允许 `merge_completion_only`
- `receipt_mode: trailer_parity` 表示该 merge commit 自己带有 canonical Freely trailer，`governance-check` 必须校验 trailer 与 ledger 字段逐项一致
- `receipt_mode: legacy_backfill` 只用于历史补录：当 merge commit 发生在当前 canonical trailer contract 之前，允许 ledger 单独留痕，但不得拿它掩盖今天的 trailer-bearing break-glass merge
- `governance-check` 会以 `audit_effective_date` 当日零点为起点，扫描之后的 protected-branch merge commit；凡是 break-glass merge，都必须能在本 ledger 里找到匹配 receipt
- 若声明 `source_policy_effective_date`，新的 protected-branch source-branch 语义只从该日期开始强制；更早的 break-glass receipt 仍按当时模型作为 grandfathered 历史处理

来源关系：
- runtime handshake env 由 `merge-guarded complete ... --break-glass` 设置，并由 `pre-merge-commit` 验证
- merge commit trailer 是提交时的即时 receipt
- 本 ledger 是 post-merge canonical writeback，用来说明 why this break-glass was accepted and who owns the follow-on repair；对于 `legacy_backfill` receipt，它同时承担 grandfathered 历史补录角色

## Receipt: 27faa2e5349dbc0e21a0a52def78a4271d60ebbc

- target_branch: `develop`
- source_branch: `feature/worktree-exclusive-ownership-postmerge-writeback-20260402-1700`
- receipt_mode: `legacy_backfill`
- bypass_mode: `break_glass`
- break_glass_reason: `verified_false_negative`
- blocked_gate: `governance-merge-gate`
- operation_scope: `merge_completion_only`
- follow_on_owner: `I-20260402-0020-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
  - `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/brainstorms.md`

## Receipt: a10f6d878774d44def570d9b8a4de60b9d089fba

- target_branch: `develop`
- source_branch: `feature/worktree-exclusive-ownership-governance-20260402-0455`
- receipt_mode: `legacy_backfill`
- bypass_mode: `break_glass`
- break_glass_reason: `tooling_unavailable`
- blocked_gate: `pre-commit`
- operation_scope: `merge_completion_only`
- follow_on_owner: `I-20260402-0020-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
  - `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/brainstorms.md`

## Receipt: 3a3e87e2f04039ad5a3d4d8e4913e88f64b2c38b

- target_branch: `develop`
- source_branch: `hotfix/I-20260501-0000-A-scan-pr-platform-config`
- receipt_mode: `trailer_parity`
- bypass_mode: `break_glass`
- break_glass_reason: `verified_false_negative`
- blocked_gate: `governance-merge-gate`
- operation_scope: `merge_completion_only`
- follow_on_owner: `I-20260501-0000-A`
- evidence_refs:
  - `docs/issues/raw-20260501-0000/issue.md`

## Receipt: bc6a1dcb5ebd1ad6e90ac49ee5225eb6816d53c3

- target_branch: `develop`
- source_branch: `feature/raw-20260508T120000Z-wt-create-fix`
- receipt_mode: `trailer_parity`
- bypass_mode: `break_glass`
- break_glass_reason: `verified_false_negative`
- blocked_gate: `governance-merge-gate`
- operation_scope: `merge_completion_only`
- follow_on_owner: `I-20260508T120000Z-A`
- evidence_refs:
  - `docs/epics/wt-create-fix/code-reviews/closeout-review.md`
  - `docs/epics/wt-create-fix/verification/pre-tests.md`
  - `docs/issues/raw-20260508T120000Z/issue.md`

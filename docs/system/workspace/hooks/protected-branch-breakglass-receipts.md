# Protected Branch Break-Glass Receipts

本文件是 protected-branch break-glass 事后审计 ledger。

使用规则：
- 只记录已经落到 protected branch merge commit 的 break-glass receipt
- 不记录普通 `merge-guarded` / `merge-guarded-complete`
- 每条 receipt 都必须能被 `governance-check` 从 merge commit trailer 回溯到本文件
- 允许 break-glass 不等于允许自由 bypass；白名单与最小作用域以 `docs/LAWS.md` §2D 为准

最小字段：
- `audit_effective_date`
- merge commit hash 标题
- `target_branch`
- `bypass_mode`
- `break_glass_reason`
- `blocked_gate`
- `operation_scope`
- `follow_on_owner`
- `evidence_refs`

- audit_effective_date: `2026-04-02`

## Receipt Contract

本文件是 protected-branch break-glass merge 的 post-merge receipt ledger。它不授予绕过权限；权限边界仍由 `docs/CONSTITUTION.md` 与 `docs/LAWS.md` §2D 定义。

记录要求：
- 只记录 `Freely-Bypass-Mode: break_glass` 的 protected-branch merge commit
- 每条 receipt 必须与 merge commit trailer 一一对应，至少写出：
  - merge commit hash
  - `target_branch`
  - `bypass_mode`
  - `break_glass_reason`
  - `blocked_gate`
  - `operation_scope`
  - `follow_on_owner`
  - `evidence_refs`
- phase-1 的 `operation_scope` 只允许 `merge_completion_only`
- `governance-check` 会以 `audit_effective_date` 为起点，扫描之后的 protected-branch merge commit；凡是 break-glass merge，都必须能在本 ledger 里找到匹配 receipt

来源关系：
- runtime handshake env 由 `merge-guarded complete ... --break-glass` 设置，并由 `pre-merge-commit` 验证
- merge commit trailer 是提交时的即时 receipt
- 本 ledger 是 post-merge canonical writeback，用来说明 why this break-glass was accepted and who owns the follow-on repair

## Receipt: 27faa2e5349dbc0e21a0a52def78a4271d60ebbc

- target_branch: `develop`
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
- bypass_mode: `break_glass`
- break_glass_reason: `tooling_unavailable`
- blocked_gate: `pre-commit`
- operation_scope: `merge_completion_only`
- follow_on_owner: `I-20260402-0020-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
  - `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/brainstorms.md`

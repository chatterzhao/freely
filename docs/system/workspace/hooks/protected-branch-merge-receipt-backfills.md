# Protected Branch Merge Receipt Backfills

本文件记录普通 protected-branch merge 缺 canonical trailer 时的事后 backfill 证据。

使用规则：
- 只记录普通 `merge-guarded` / `merge-guarded-complete` merge commit 的 receipt gap
- 不记录 break-glass merge；break-glass 仍使用 `protected-branch-breakglass-receipts.md`
- 只用于“merge 已经发生，历史不可改写，但 canonical trailer 缺失”的例外修复
- 不能把本 ledger 当成未来正常 merge 缺 trailer 的常规入口

最小字段：
- `audit_effective_date`
- merge commit hash 标题
- `target_branch`
- `source_branch`
- `canonical_merge_path`
- `canonical_bypass_mode`
- `follow_on_owner`
- `evidence_refs`

- audit_effective_date: `2026-04-04`

## Contract

- `governance-check` 会从 `audit_effective_date` 当日零点开始扫描 protected-branch merge ancestry
- 普通 protected merge 若已经带 canonical Freely trailer，则不得在本 ledger 中声明 backfill
- 普通 protected merge 若缺 canonical Freely trailer，则必须在本 ledger 有 matching backfill entry
- backfill entry 只修复 auditability，不授予 bypass 权限

## Receipt Gap: 908a6ad9f96a1a76a22f1f44f3b5438e23f6c6e0

- target_branch: `develop`
- source_branch: `feature/governance-merge-gate-milestone-status-followthrough-20260404-011904`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`

## Receipt Gap: 5da463c9d2ddd284ddc45f085a789cb8b092c1a8

- target_branch: `develop`
- source_branch: `feature/governance-1100-closeout-20260404-0648`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`

## Receipt Gap: eec65f3a00586f64d47ecd441779690b3f729719

- target_branch: `develop`
- source_branch: `feature/protected-branch-merge-receipt-backfill-20260404-0710`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-protected-branch-merge-receipt-gap-followthrough-verification.md`

## Receipt Gap: dfbca95b4066cb562f093ad16c83d687f47f9aa6

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: 3de9c27009ac2cf52c7a17b7bf559f8eb22d6943

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: ec36ebe0d5215315c18c6081f854b60b0a712cf2

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: 9e35ed77f37a3f9ab77ff1e033c10bb376d6aac3

- target_branch: `develop`
- source_branch: `feature/cli-output-style-optimization-20260405-1000`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260405-cli-output-style-A`
- evidence_refs:
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`

## Receipt Gap: c20c6bd4a09112287a8b2ec6bd9148981946b86b

- target_branch: `develop`
- source_branch: `feature/cli-output-style-optimization-20260405-1000`
- canonical_merge_path: `merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260405-cli-output-style-A`
- evidence_refs:
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`

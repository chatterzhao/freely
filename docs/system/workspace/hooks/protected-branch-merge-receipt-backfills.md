# Protected Branch Merge Receipt Backfills

本文件记录普通 protected-branch merge 缺 canonical trailer 时的事后 backfill 证据。

使用规则：
- 只记录普通 `pr-merge-guarded` / `pr-merge-guarded-complete` merge commit 的 receipt gap
- 不记录 break-glass merge；break-glass 仍使用 `protected-branch-breakglass-receipts.md`
- 只用于“merge 已经发生，历史不可改写，但 canonical trailer 缺失”的例外修复
- 不能把本 ledger 当成未来正常 merge 缺 trailer 的常规入口

最小字段：
- `audit_effective_date`
- `source_policy_effective_date`（可选；用于定义 develop/test-pre-merge source-branch 新语义的生效日期）
- merge commit hash 标题
- `validation_mode`（可选；默认 `subject_match`）
- `target_branch`
- `source_branch`
- `canonical_merge_path`
- `canonical_bypass_mode`
- `follow_on_owner`
- `evidence_refs`

`validation_mode: subject_match`（默认）继续使用现有 contract，并从 merge subject `Merge branch '<source>' into <target>` 恢复 source/target 语义。

`validation_mode: unparseable_subject_ancestry` 只用于 generic-subject ancestry gap，并额外要求：
- `protected_batch_branch`
- `absorbing_protected_merge`
- `bounded_issue`
- `verification_ref`

- audit_effective_date: `2026-04-04`
- source_policy_effective_date: `2026-04-06`

## Contract

- `governance-check` 会从 `audit_effective_date` 当日零点开始扫描 protected-branch merge ancestry
- 若声明 `source_policy_effective_date`，`governance-check` 只从该日期开始强制新的 protected-branch source-branch 语义；更早的历史 merge 继续按 receipt 完整性审计，不 retroactively 重判 promote model
- 普通 protected merge 若已经带 canonical Freely trailer，则不得在本 ledger 中声明 backfill
- 普通 protected merge 若缺 canonical Freely trailer，则必须在本 ledger 有 matching backfill entry
- `validation_mode: subject_match` 仍要求 merge subject 可解析并与 ledger `source_branch` / `target_branch` 一致
- `validation_mode: unparseable_subject_ancestry` 必须显式声明 absorbing protected merge、protected batch branch、bounded owner issue 和 verification artifact；不得退化为 hash-only 例外
- backfill entry 只修复 auditability，不授予 bypass 权限

## Receipt Gap: 17556ba9d970b4bae03edf2fd4b679395125b8bd

- target_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260418`
- source_branch: `feature/runtime-lifecycle-receipt-followthrough-20260418`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260418-runtime-lifecycle-receipt-followthrough-verification.md`

## Receipt Gap: 890e24d5f971ad95a5b91b565911e5c432112bf3

- target_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260418`
- source_branch: `feature/runtime-lifecycle-receipt-followthrough-20260418`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260418-runtime-lifecycle-receipt-followthrough-verification.md`

## Receipt Gap: b05d485923c49bbef4412b32596e8d8596999ee9

- target_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260418`
- source_branch: `feature/runtime-lifecycle-receipt-followthrough-20260418`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260418-runtime-lifecycle-receipt-followthrough-verification.md`

## Receipt Gap: 9cb3236d2c297e3b8b36bb4613c3f0d8dbb69e98

- target_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260418`
- source_branch: `feature/runtime-lifecycle-receipt-followthrough-20260418`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260418-runtime-lifecycle-receipt-followthrough-verification.md`

## Receipt Gap: dc436573e5f3f995ed936e7b21c65f9440fffae9

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260424-runtime-lifecycle-receipt-closeout-reconcile-verification.md`

## Receipt Gap: f7145cc889c3919cbe21b1162f96d14d736b83b7

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260418-1900-A`
- evidence_refs:
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/B2-docs/runtime-lifecycle-receipt-followthrough-governance/code-reviews/20260424-runtime-lifecycle-receipt-closeout-reconcile-verification.md`

## Receipt Gap: f3dcbbd8fe4da12377f7e533dc162c649792bc69

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `test-pre-merge-runtime-lifecycle-20260419`
- source_branch: `feature/runtime-process-leak-20260417`
- protected_batch_branch: `feature/runtime-process-leak-20260417`
- absorbing_protected_merge: `48a4224750bbc4131ea8eb86a6213252417aa7ca`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- bounded_issue: `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- verification_ref: `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: 8674e717fd4c8d5a4dde465cd01d9dd34ecbbad2

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `test-pre-merge-runtime-lifecycle-20260419`
- source_branch: `feature/runtime-process-leak-20260417`
- protected_batch_branch: `feature/runtime-process-leak-20260417`
- absorbing_protected_merge: `48a4224750bbc4131ea8eb86a6213252417aa7ca`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- bounded_issue: `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- verification_ref: `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`
## Receipt Gap: 3e226fa9865973d5964e0bd5ec8a124452c49118

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: ad339d264c87ae382e8398ecbcd5de01802e3372

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: 8cb050abdead5c338d7dd4a5e3d0cbc0a98d809e

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: c4de46907e4acfff31e2454c1aff592f7b1631ad

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/runtime-process-leak-20260417`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: ee5b7073eba487cdefca39b0f6ff07b5ad82c980

- target_branch: `test-pre-merge-runtime-lifecycle-20260417`
- source_branch: `feature/lifecycle-trace-debuggability-20260416`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260417-0445-A`
- evidence_refs:
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Receipt Gap: 908a6ad9f96a1a76a22f1f44f3b5438e23f6c6e0

- target_branch: `develop`
- source_branch: `feature/governance-merge-gate-milestone-status-followthrough-20260404-011904`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`

## Receipt Gap: 5da463c9d2ddd284ddc45f085a789cb8b092c1a8

- target_branch: `develop`
- source_branch: `feature/governance-1100-closeout-20260404-0648`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`

## Receipt Gap: eec65f3a00586f64d47ecd441779690b3f729719

- target_branch: `develop`
- source_branch: `feature/protected-branch-merge-receipt-backfill-20260404-0710`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-protected-branch-merge-receipt-gap-followthrough-verification.md`

## Receipt Gap: dfbca95b4066cb562f093ad16c83d687f47f9aa6

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: 3de9c27009ac2cf52c7a17b7bf559f8eb22d6943

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: ec36ebe0d5215315c18c6081f854b60b0a712cf2

- target_branch: `develop`
- source_branch: `feature/develop-push-governance-blocker-triage-20260404-0745`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`

## Receipt Gap: 9e35ed77f37a3f9ab77ff1e033c10bb376d6aac3

- target_branch: `develop`
- source_branch: `feature/cli-output-style-optimization-20260405-1000`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260405-cli-output-style-A`
- evidence_refs:
  - `docs/B2-docs/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
  - `docs/B2-docs/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`

## Receipt Gap: c20c6bd4a09112287a8b2ec6bd9148981946b86b

- target_branch: `develop`
- source_branch: `feature/cli-output-style-optimization-20260405-1000`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260405-cli-output-style-A`
- evidence_refs:
  - `docs/B2-docs/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
  - `docs/B2-docs/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`

## Receipt Gap: 9fa8ec35bb9532235bd8cb51b6e20c6730836d7c

- target_branch: `develop`
- source_branch: `feature/slot-switch-startup-preflight-governance-20260404-2138`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-2148-A`
- evidence_refs:
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-verification.md`
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-canonical-closeout-verification.md`

## Receipt Gap: 6969be7e02ea0c380a9e9fc892b5184168d261fb

- target_branch: `develop`
- source_branch: `feature/slot-switch-startup-preflight-closeout-20260404-2335`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-2148-A`
- evidence_refs:
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-verification.md`
  - `docs/B2-docs/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-canonical-closeout-verification.md`

## Receipt Gap: 01e3263d6382c6b35a8714c44db9bd2c01b9a5e8

- target_branch: `develop`
- source_branch: `feature/worktree-tool-boundary-bootstrap-closeout-20260405-1700`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260404-0640-A`
- evidence_refs:
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/B2-docs/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260405-worktree-bootstrap-closeout-merge-receipt-gap-verification.md`
  - `docs/B2-docs/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
  - `docs/B2-docs/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/code-reviews/20260405-worktree-tool-boundary-bootstrap-canonical-closeout-verification.md`

## Receipt Gap: 01e3263d6382c6b35a8714c44db9bd2c01b9a5e8

- target_branch: `develop`
- source_branch: `feature/worktree-tool-boundary-bootstrap-closeout-20260405-1700`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260403-2041-A`
- evidence_refs:
  - `docs/B2-docs/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
  - `docs/B2-docs/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/code-reviews/20260405-worktree-tool-boundary-bootstrap-canonical-closeout-verification.md`

## Receipt Gap: 63c9e509e9b2cb5ba99969622527a560d02f56cc

- target_branch: `test-pre-merge-20260408-verification-and-develop-push`
- source_branch: `feature/develop-push-followthrough-escalation-20260408-1200`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260408-1200-A`
- evidence_refs:
  - `docs/B2-docs/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`
  - `docs/B2-docs/develop-push-followthrough-escalation-governance/code-reviews/20260408-develop-push-followthrough-escalation-verification.md`

## Receipt Gap: 357c18bb39286580a9c07856d0a1858867dd7d58

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

## Receipt Gap: 8069bced62af4dc1e6c46387fa715613628f291a

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

## Receipt Gap: 497c474abd9ecb4776462aa9416b59f7cc45a1f8

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

## Receipt Gap: c235976621a36a1f89db5dda83676d3b4370278d

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

## Receipt Gap: ae09968a60d722deb11e59ca43b1239dab694c5c

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

## Receipt Gap: 88dd9eaabbcda45b2b7127da7dea9ec3f68e4df2

- validation_mode: `unparseable_subject_ancestry`
- target_branch: `develop`
- source_branch: `test-pre-merge-20260410-preferred-auth-fix`
- protected_batch_branch: `test-pre-merge-20260410-preferred-auth-fix`
- absorbing_protected_merge: `aeca22048b2b63e2a5a3a4318e912dd0f71ee368`
- canonical_merge_path: `pr-merge-guarded`
- canonical_bypass_mode: `forbidden`
- follow_on_owner: `I-20260411-0217-A`
- bounded_issue: `docs/B2-docs/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_ref: `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`
- evidence_refs:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
  - `docs/B2-docs/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md`

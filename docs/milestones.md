# Milestones

本文件是 Freely 自举开发时的主动扫描入口，用来承接已进入活跃范围的 candidate / issue。

## Milestone Policy

milestone_status_policy_version: v2

candidate_policy:
- dropped: remove from active milestone queues
- needs_research: keep in candidate_issues with `next_action` and `revisit_trigger`, and route back to pre-brainstorms or issue-bound brainstorm; do not silently drop it from active scans
- promoted: bind to a milestone immediately; do not leave as long-term unbound state
- blocked: keep visible with blocker, next action, and revisit trigger

queue_policy:
- committed_issues: sequencing is clear and the item is the next active batch
- candidate_issues: contains unresolved candidates plus `todo_ibm` candidate mirrors for already-materialized issues; when `promoted_issue_path` is concrete, execution authority remains in `committed_issues`
- completed_issues: delivered work kept for traceability within the same milestone

phase_state_policy:
- `phase_state=in_ibm`: keep the issue visible in `committed_issues` with `issue_path` and `next_action`; do not require `progress`
- `phase_state=done_ibm`: keep the issue visible in `committed_issues` with `issue_path` and a clear handoff into dev-loop
- `phase_state=in_dev`: keep the issue visible in `committed_issues` and require matching `progress`
- `phase_state=blocked_dev`: keep the issue visible with blocker, next action, and current execution context
- `phase_state=in_verification`: keep the issue visible until completion evidence is written back
- `phase_state=completed`: move the issue to `completed_issues` with evidence
- `phase_state=todo_ibm`: candidate mirror only; issue has already been materialized and remains authoritative in `committed_issues`. Do not route execution from the candidate mirror when `promoted_issue_path` is concrete.

session_policy:
- full `session_refs` live in candidate / issue / progress / recovery artifacts
- milestone may keep `active_session_ref` as a summary, but `issue_path` is the canonical detail pointer

sequencing_policy:
- ordered_by: dependency_then_control_plane
- allow_unordered_candidates: true

routing_policy:
- no_issue_path: stay in pre-brainstorms or continue doc-loop materialization
- issue_path_present: route by `phase_state` into issue-bound brainstorm, IBM, continuation, dev-loop, or completion verification
- unresolved candidate or issue never disappears just because the current round chose another priority; keep it in the appropriate queue with an explicit restart condition

## M-20260306-workspace-routing-foundation

- title: Workspace routing foundation for Freely dogfooding
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/candidates.md`
- intent: 把首跳路由治理候选正式纳入 milestone，避免 Freely 自己继续依赖悬空 candidate 工作
- why_now: 这批项定义 Freely 如何发现上下文、读取 milestone、并路由到下一跳 skill；如果 milestone 自身不先落盘，Freely 的狗粮链路就是断的

### committed_issues

3. `I-20260405-1415-A`
- title: ai-switch-cli extraction threshold and skeleton disposition governance
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition/candidates.md`
- next_action: Keep this owner parked as the canonical IBM handoff for standalone extraction timing. Do not open an extraction worktree until the Codex-first owner is merged and a concrete follow-on lane can prove the extraction-start checklist is satisfied.
- revisit_trigger: Re-open only if the Codex-first owner is reopened and invalidates the threshold/boundary package, or if a second tool reaches verified parity quickly enough to change the extraction economics.

2. `I-20260406-0408-A`
- title: CLI help and dry-run contract followthrough governance
- milestone_state: committed
- phase_state: `in_dev`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-cli-help-and-dry-run-contract-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- next_action: Repair the audited help/usage exit-code contracts plus the bounded `ai switch codex --dry-run` JSON summary path, then replay the focused CLI-first verification set before promotion.
- revisit_trigger: Re-open only if the owner proves too narrow to keep help semantics and dry-run summary semantics aligned, or if canonical replay exposes another first-hop command contract outside this bounded set.

### candidate_issues

1. `C-20260407-0817-A`
- title: Source inbox, routing absorption boundary, and manager/worker audit contract
- milestone_state: candidate
- phase_state: `needs_research`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260407-0817--source-ledger-routing-and-manager-audit-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260407-0817--source-ledger-routing-and-manager-audit-boundary/candidates.md`
- next_action: Finish the current-state durable-source inventory, lock the default durable families to `human interruption` and `external issue`, treat review/test/runtime anomaly as discovery mechanisms by default, and decide whether the first bounded implementation should stay a human-interruption/local-intake slice with unresolved-index removal backstop instead of a repo-wide source-ledger rollout.
- revisit_trigger: Revisit when a concrete first-slice proposal exists for the first source family and its storage boundary, or when another dogfooding incident proves the current visibility gap cannot be solved by strengthening existing pre-brainstorm/milestone/routing truth alone.

1. `C-20260407-0023-A`
- title: Codex auto switch keeps probing saved apikey slots after all-unavailable OAuth sweep
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260407-0023--codex-auto-switch-probe-apikey-fallback/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260407-0023--codex-auto-switch-probe-apikey-fallback/candidates.md`
- next_action: Candidate mirror only. `I-20260407-0023-A` is now the canonical owner for the saved-apikey fallback after an `all_unavailable:*` account sweep.
- revisit_trigger: Re-open only if canonical replay proves this follow-on owner is too narrow.

1. `C-20260406-1829-A`
- title: Codex current-live apikey bootstrap without saved-slot inventory
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-current-live-apikey-bootstrap-without-saved-slot-governance/issues/codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1829--codex-current-live-apikey-bootstrap-without-saved-slot/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1829--codex-current-live-apikey-bootstrap-without-saved-slot/candidates.md`
- next_action: Candidate mirror only. `I-20260406-1829-A` is now the canonical owner for the no-saved-slot current-live Codex apikey bootstrap boundary.
- revisit_trigger: Re-open only if canonical replay proves the owner boundary is too narrow.

2. `C-20260406-1851-A`
- title: Codex interactive login and API-key input flow
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/candidates.md`
- next_action: Candidate mirror only. `I-20260406-1851-A` is now the canonical owner for Codex-first interactive login mode selection and API-key input/materialization UX.
- revisit_trigger: Revisit if a future owner tries to widen this bounded UX slice into current-live bootstrap, watchdog semantics, or standalone backend extraction.

3. `C-20260406-0715-A`
- title: Codex live auth identity reconciliation and probe timeout boundary
- milestone_state: candidate
- phase_state: `needs_research`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260406-0715--codex-live-auth-identity-and-probe-lock-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-0715--codex-live-auth-identity-and-probe-lock-boundary/candidates.md`
- next_action: Finish landing the stale live-slot reconciliation and probe-timeout cleanup slice, then decide whether the remaining live `codex exec` timeout evidence warrants a separate issue instead of reopening the completed 20260405 Codex API-key owner.
- revisit_trigger: Revisit if canonical replay shows this boundary is fully absorbed by an existing owner, or if the unresolved timeout evidence proves the real follow-on is upstream `codex exec` stall diagnosis rather than more slot identity work.

2. `C-20260406-0901-A`
- title: Codex reconnect probe fast-fail and runtime network classification alignment
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-0901--codex-reconnect-probe-fast-fail/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-0901--codex-reconnect-probe-fast-fail/candidates.md`
- next_action: Candidate mirror only. `I-20260406-0901-A` is now the canonical owner for reconnect fast-fail and runtime network classification alignment.
- revisit_trigger: Re-open only if canonical replay proves the issue boundary is too narrow, or if upstream Codex semantics change enough that string-matched reconnect evidence is no longer the right boundary.

1. `C-20260404-0119-A`
- title: Governance merge gate milestone status followthrough
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0119--governance-merge-gate-milestone-status-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0119--governance-merge-gate-milestone-status-followthrough/candidates.md`
- next_action: This candidate is now materialized as `I-20260404-0119-A`. Keep the owner scoped to milestone-level status parsing so the merge gate stops reading nested queue item status lines as milestone truth.
- revisit_trigger: Re-open only if active-milestone validation still misreads nested queue metadata after this parser-bound followthrough lands.

2. `C-20260406-0045-A`
- title: Governance-check protected-merge history source policy
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/candidates.md`
- next_action: Candidate mirror only. `I-20260406-0045-A` is the canonical owner for first-parent protected merge history auditing.
- revisit_trigger: Re-open only if the issue boundary proves too narrow to keep ordinary receipt and break-glass receipt audits aligned.

3. `C-20260406-1105-A`
- title: Milestone completed-queue closeout
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1105--milestone-completed-queue-closeout/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1105--milestone-completed-queue-closeout/candidates.md`
- next_action: Candidate mirror only. `I-20260406-1105-A` is the canonical owner for repairing completed-owner queue drift and binding the missing baseline audit.
- revisit_trigger: Re-open only if canonical governance-check still misses milestone queue/phase drift after this owner closes.

2. `C-20260405-1615-A`
- title: Feature-owned test-pre-merge family promotion model
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1615--feature-owned-test-pre-merge-family/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1615--feature-owned-test-pre-merge-family/candidates.md`
- next_action: Candidate mirror only. `I-20260405-1615-A` is authoritative and now parked at `completed`; use the owner package to guide follow-on enforcement and lifecycle owners instead of reopening raw pre-brainstorm debate.
- revisit_trigger: Revisit if a future owner tries to widen gate implementation or lifecycle automation without consuming `I-20260405-1615-A`, or if a second `test-pre-*` prefix is proposed.

3. `C-20260405-1805-A`
- title: Test-pre-merge family promotion gate enforcement
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1805--test-pre-merge-family-promotion-gate-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1805--test-pre-merge-family-promotion-gate-enforcement/candidates.md`
- next_action: Candidate mirror only. `I-20260405-1805-A` is authoritative and now parked at `completed`; use this owner for synchronized truth-source update and gate enforcement rather than splitting them again.
- revisit_trigger: Revisit if someone proposes separate owner lifecycles for constitutional truth and gate semantics, or if lifecycle automation is widened into this enforcement owner.

4. `C-20260405-1914-A`
- title: Test lane routing and enforcement
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1914--test-lane-routing-and-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1914--test-lane-routing-and-enforcement/candidates.md`
- next_action: Candidate mirror only. `I-20260405-1914-A` is authoritative and now parked at `completed`; use this owner for explicit lane truth, machine enforcement, and regression alignment instead of leaving `test-lane` as an unowned implementation.
- revisit_trigger: Revisit if lane enforcement is widened into implicit auto-routing, or if a future owner tries to hide lane mismatches behind generic “run tests anywhere” semantics.

5. `C-20260404-0232-A`
- title: Governance merge gate review-aware regression alignment
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/candidates.md`
- next_action: This candidate is now materialized as `I-20260404-0232-A`. Keep the owner scoped to making the mixed unresolved-candidate implementation regression review-aware and restoring same-file borrowed-owner blocking after staged review artifacts became mandatory.
- revisit_trigger: Re-open only if a future guard again causes this mixed unresolved-candidate implementation regression to fail before it reaches the current allowed path, or if same-file borrowed-owner regressions start passing again.

6. `C-20260404-0640-A`
- title: Protected-branch merge receipt gap followthrough
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/candidates.md`
- next_action: This candidate is now materialized as `I-20260404-0640-A`. Keep the owner scoped to ancestry receipt-gap backfill and audit for ordinary protected merges only.
- revisit_trigger: Re-open only if another ordinary protected merge is found without canonical trailers or the ancestry audit still misses such gaps after this followthrough lands.

7. `C-20260404-1545-A`
- title: Bound runtime supervision when websocket permission-denied failures block manager continuity and intake claim
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-1545--runtime-websocket-permission-denied-recovery-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-1545--runtime-websocket-permission-denied-recovery-governance/candidates.md`
- next_action: Candidate mirror only. `I-20260405-2136-A` is now the canonical owner for prompt-visible-but-unclaimed runtime supervision; use the issue package for blocked intake / continuity truth and keep this candidate only as the discovery mirror.
- revisit_trigger: Revisit only if canonical `develop` proves the blocked supervision family belongs entirely inside an existing owner, or if the same prompt-visible-but-unclaimed evidence disappears without needing a dedicated lifecycle.

8. `C-20260404-2148-A`
- title: Bound startup governance for stale or ambiguous codex slot-switch lock
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-2148--slot-switch-lock-startup-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-2148--slot-switch-lock-startup-governance/candidates.md`
- next_action: This candidate is now materialized as `I-20260404-2148-A`. Keep the owner scoped to startup preflight and minimal lock observability; do not widen it back into blocked-intake supervision.
- revisit_trigger: Re-open only if a future runtime change proves the startup/status lock contract still lacks a dedicated owner after this issue closes.

9. `C-20260405-1215-A`
- title: Runtime audio notifier and sound semantics
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1215--runtime-audio-notifier-and-sound-semantics/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1215--runtime-audio-notifier-and-sound-semantics/candidates.md`
- next_action: This candidate is now materialized as `I-20260405-1215-A`. Keep the owner scoped to canonical audio cue events, four standard bundled sounds, and frontend/Tauri playback only.
- revisit_trigger: Re-open only if future work adds blocked/failed/interruption semantics, native notice adapters for more tools, or headless/OS fallback playback.
10. `C-20260405-0027-A`
- title: Codex API-key slot bundle and provider-aware probe governance
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe/candidates.md`
- next_action: Candidate mirror only. `I-20260405-0027-A` is now the canonical completed owner for the Codex auth+config bundle contract; future work should route through a new follow-on owner rather than reopening candidate-stage IBM.
- revisit_trigger: Revisit if another active owner absorbs the full auth+config slot bundle contract or if official Codex provider/auth semantics shift enough to invalidate the current slot-kind split.

11. `C-20260405-2055-A`
- title: Restart slot-switch preflight preserves active runtime governance
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/candidates.md`
- next_action: Candidate mirror only. `I-20260405-2055-A` is now the canonical completed owner for restart-time slot-switch preflight ordering, preserved-runtime failure behavior, and the bounded adjacent durability hardenings required by that contract.
- revisit_trigger: Revisit if canonical `develop` regresses the preserved-runtime restart contract or if a future owner absorbs this exact restart-only boundary.

12. `C-20260405-1415-A`
- title: ai-switch-cli extraction threshold and skeleton disposition governance
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition/candidates.md`
- next_action: Candidate mirror only. `I-20260405-1415-A` is authoritative and now parked at `done_ibm`; use the committed owner as the canonical handoff package when a future extraction lane is justified.
- revisit_trigger: Revisit once the Codex-first lane is merged or once a second tool reaches verified backend-worthy maturity.

13. `C-20260405-2358-C`
- title: CLI wrapper packaging and regression-surface audit
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- next_action: Candidate mirror only. `I-20260405-2358-C` is now the canonical owner for CLI packaging, clean help output, and deterministic regression-surface repair.
- revisit_trigger: Revisit if canonical `develop` later proves the same defects belong to a broader bootstrap/runtime owner instead of this packaging lane.

14. `C-20260405-2358-B`
- title: Runtime control-plane CLI stability after full command audit
- milestone_state: candidate
- phase_state: `needs_research`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- next_action: Keep this candidate visible under `workspace-routing-foundation`, then split the current evidence into restart/readiness semantics versus intake/chat state-accounting before materializing the narrow runtime/control-plane owner.
- revisit_trigger: Revisit if canonical runtime commands still require stale-child cleanup, readiness babysitting, or contradictory intake state explanation.

15. `C-20260405-2358-D`
- title: CLI help and dry-run contract followthrough after canonical audit
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- next_action: Candidate mirror only. `I-20260406-0408-A` is now the canonical owner for audited help/usage contracts and bounded `ai switch --dry-run` result alignment.
- revisit_trigger: Revisit if help invocations still carry side effects or non-obvious exit semantics, or if `ai switch --dry-run` remains inconsistent with the saved auth inventory on canonical `develop`.

### completed_issues
1. `I-20260407-0023-A`
- title: Codex auto switch probe apikey fallback governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-auto-switch-probe-apikey-fallback-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260407-0023--codex-auto-switch-probe-apikey-fallback/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260407-0023--codex-auto-switch-probe-apikey-fallback/candidates.md`
- evidence:
  - `develop` merge `1b33131`
  - `docs/progress/workspace-routing-foundation/p-codex-auto-switch-probe-apikey-fallback-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`
  - `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-all-unavailable-falls-back-to-exec`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
  - `./bin/governance-check`
- completion_note: `Canonical develop now carries the bounded saved-apikey fallback after an all-unavailable account sweep, so this owner should no longer remain in committed_issues.`

2. `I-20260406-1829-A`
- title: Codex current-live apikey bootstrap without saved-slot inventory governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-current-live-apikey-bootstrap-without-saved-slot-governance/issues/codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1829--codex-current-live-apikey-bootstrap-without-saved-slot/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1829--codex-current-live-apikey-bootstrap-without-saved-slot/candidates.md`
- evidence:
  - `develop` merge `4b6e0a9`
  - `docs/progress/workspace-routing-foundation/p-codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-current-live-apikey-bootstrap-without-saved-slot-governance/code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/codex-current-live-apikey-bootstrap-without-saved-slot-governance/code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-verification.md`
  - `docs/epics/workspace-routing-foundation/codex-current-live-apikey-bootstrap-without-saved-slot-governance/code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`
  - `./bin/governance-check`
- completion_note: `Canonical develop now carries the bounded current-live apikey bootstrap repair without saved-slot inventory, so this owner should no longer remain in committed_issues.`

3. `I-20260406-1851-A`
- title: Codex interactive login and API-key input flow governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-interactive-login-and-apikey-input-flow-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/candidates.md`
- evidence:
  - `develop` merge `7dc4074`
  - `docs/progress/workspace-routing-foundation/p-codex-interactive-login-and-apikey-input-flow-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-verification.md`
  - `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-interactive-mode-selection`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-interactive`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-direct-args`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-empty-input-fails`
  - `./bin/governance-check`
- completion_note: `Canonical develop now carries the bounded Codex-first interactive login and API-key input flow repair, so this owner should no longer remain in committed_issues.`

4. `I-20260406-0901-A`
- title: Codex reconnect probe fast-fail and runtime network classification governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-0901--codex-reconnect-probe-fast-fail/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-0901--codex-reconnect-probe-fast-fail/candidates.md`
- evidence:
  - `develop` merge `7674bc3`
  - `docs/progress/workspace-routing-foundation/p-codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-verification.md`
  - `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-network-failure-before-timeout`
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-network-failure-cleans-child-process`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-status-live-apikey-network-failure`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-live-apikey-network-failure`
  - `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
  - `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
  - `./bin/governance-check`
- completion_note: `Canonical develop now carries the reconnect fast-fail and runtime network-classification repair, while the unrelated interruption-manager readiness patch remains explicitly out of scope for this completed owner.`

1. `I-20260406-1105-A`
- title: Milestone completed-queue closeout governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-milestone-completed-queue-closeout-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-1105--milestone-completed-queue-closeout/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-1105--milestone-completed-queue-closeout/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-milestone-completed-queue-closeout-governance.md`
  - `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-milestone-phase-queue-alignment`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
  - `./bin/governance-check`
- completion_note: `Canonical milestone truth no longer leaves completed owners in committed_issues, and baseline governance-check now audits milestone queue placement against the referenced issue phase so historical queue drift is no longer silent.`

2. `I-20260406-0045-A`
- title: Governance-check protected-merge history source policy governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-check-protected-merge-history-source-policy-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260406-0045--governance-check-protected-merge-history-source-policy/candidates.md`, `docs/pre-brainstorms/20260406-0055--governance-check-nested-test-pre-merge-receipt-audit/candidates.md`
- evidence:
  - `develop` merge `f58cf65`
  - `docs/progress/workspace-routing-foundation/p-governance-check-protected-merge-history-source-policy-governance.md`
  - `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-verification.md`
  - `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `./bin/governance-check`
- completion_note: `Canonical develop now audits protected-branch merge receipts by effective target branch, so nested feature -> test-pre-merge ancestry no longer poisons develop source-policy checks while direct invalid feature -> develop receipts still fail.`

3. `I-20260405-2358-C`
- title: CLI wrapper packaging and regression-surface governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-cli-wrapper-packaging-and-regression-surface-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- evidence:
  - `develop` merge `8e0985b`
  - `docs/progress/workspace-routing-foundation/p-cli-wrapper-packaging-and-regression-surface-governance.md`
  - `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`
  - `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-canonical-closeout-verification.md`
- completion_note: `Canonical develop has already absorbed the bounded wrapper packaging and regression-surface repair, so this owner belongs only in completed_issues.`

4. `I-20260405-2136-A`
- title: Runtime blocked intake and continuity truth governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-blocked-intake-and-continuity-truth-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-1545--runtime-websocket-permission-denied-recovery-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-1545--runtime-websocket-permission-denied-recovery-governance/candidates.md`
- evidence:
  - `develop` merge `fd1907b`
  - `docs/progress/workspace-routing-foundation/p-runtime-blocked-intake-and-continuity-truth-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-verification.md`
  - `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/code-reviews/20260405-runtime-blocked-intake-continuity-canonical-closeout-verification.md`
- completion_note: `Canonical develop already carries the blocked-intake and continuity truth surface, so this owner should not remain in committed_issues.`

5. `I-20260405-1914-A`
- title: Test lane routing and enforcement governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1914--test-lane-routing-and-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1914--test-lane-routing-and-enforcement/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/code-reviews/20260405-test-lane-routing-and-enforcement-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/code-reviews/20260405-test-lane-routing-and-enforcement-verification.md`
  - `./bin/governance-check`
- completion_note: `Explicit lane routing, executable wrappers, and lane misuse enforcement are already frozen as completed historical truth and no longer belong in committed_issues.`

6. `I-20260405-1805-A`
- title: Test-pre-merge family promotion gate enforcement governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1805--test-pre-merge-family-promotion-gate-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1805--test-pre-merge-family-promotion-gate-enforcement/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-verification.md`
  - `./bin/governance-check`
- completion_note: `The synchronized truth-source and promotion-gate contract is already frozen as completed governance, so the owner belongs only in completed_issues.`

7. `I-20260405-1615-A`
- title: Feature-owned test-pre-merge family promotion model governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1615--feature-owned-test-pre-merge-family/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1615--feature-owned-test-pre-merge-family/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-verification.md`
  - `./bin/governance-check`
- completion_note: `The canonical test-pre-merge family promote model has already been frozen as completed handoff truth and should no longer remain in the active committed queue.`

8. `I-20260404-0640-A`
- title: Protected-branch merge receipt gap followthrough
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-gap-followthrough.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/candidates.md`
- evidence:
  - `develop` merge `0c9701f`
  - `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews/20260404-develop-push-triage-merge-receipt-gap-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `./bin/governance-check`
- completion_note: `Canonical develop now audits trailerless protected-ancestry merges by their actual merge subject, so gap 70ef97d and the same-day receiptless ancestry set pass under the ordinary backfill ledger. The blocker-triage branch/worktree was retired after post-merge verification passed.`
9. `I-20260404-2148-A`
- title: Slot-switch startup preflight and lock observability governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-slot-switch-startup-preflight-and-lock-observability-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-2148--slot-switch-lock-startup-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-2148--slot-switch-lock-startup-governance/candidates.md`
- evidence:
  - `develop` merge `9fa8ec3`
  - `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
  - `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-verification.md`
  - `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-canonical-closeout-verification.md`
  - `docs/progress/workspace-routing-foundation/p-slot-switch-startup-preflight-and-lock-observability-governance.md`
  - `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
  - `bash docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`
  - `./bin/governance-check`
- completion_note: `Canonical develop now enforces bounded slot-switch startup preflight and lock observability, and the closeout lane recorded the ordinary protected-merge receipt gap repair plus post-merge verification before retirement.`
3. `I-20260405-1215-A`
- title: Runtime audio notifier and sound semantics governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-audio-notifier-and-sound-semantics-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1215--runtime-audio-notifier-and-sound-semantics/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1215--runtime-audio-notifier-and-sound-semantics/candidates.md`
- evidence:
  - `develop` merge `a9eba5b`
  - `docs/progress/workspace-routing-foundation/p-runtime-audio-notifier-and-sound-semantics-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-verification.md`
  - `docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-canonical-closeout-verification.md`
  - `bun test src/frontend_probe_v0`
  - `bun run typecheck`
  - `bun run build`
  - `cargo test --manifest-path src-tauri/Cargo.toml`
  - `bun run tauri:validate:probe`
  - `git diff --check`
  - `./bin/governance-check`
- completion_note: `Canonical develop now emits stable AudioCueRequested events for the bounded manager/worker start-and-complete matrix, and the bundled probe host ships the four standard wav assets without widening into fallback playback or transcript-listener semantics.`
4. `I-20260405-0027-A`
- title: Codex API-key slot bundle and provider-aware probe governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe/candidates.md`
- evidence:
  - `develop` merge `c5e0b85`
  - `docs/progress/workspace-routing-foundation/p-codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-verification.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-canonical-closeout-verification.md`
  - `git diff --check`
  - `./bin/governance-check`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- completion_note: `Canonical develop now treats Codex auth as a bundle of auth truth plus provider-aware config fragment, preserves cross-kind account/apikey switching semantics, and keeps exec-only apikey probing separate from OAuth-backed account inventory without widening into non-Codex parity or standalone extraction.`
5. `I-20260405-2055-A`
- title: Restart slot-switch preflight preserves active runtime governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/candidates.md`
- evidence:
  - `develop` merge `255d6dd`
  - `docs/progress/workspace-routing-foundation/p-restart-slot-switch-preflight-preserves-active-runtime-governance.md`
  - `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-verification.md`
  - `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-canonical-closeout-verification.md`
  - `git diff --check`
  - `./bin/governance-check`
  - `bash -n docs/system/workspace/scripts/runtime/freely`
  - `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
  - `bash docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
  - `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-triggers-auth-change-wake`
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`
  - `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
  - `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
- completion_note: `Canonical develop now resolves shared slot-switch preflight before restart stops a live project runtime, preserves the active supervisor and AI child on bounded preflight failure, and keeps the restart-adjacent relaunch/session-state hardenings aligned with that contract without widening into broader watchdog redesign.`

1. `I-20260402-0020-A`
- title: Hook bypass break-glass governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-hook-bypass-breakglass-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/candidates.md`
- completion_note: `Canonical develop absorbed protected-branch break-glass governance through receipt-bearing merge 52f55c0, and the closeout lane recorded both historical break-glass receipts and post-merge verification evidence.`
2. `I-20260403-1100-A`
- title: Governance chain legacy repair for develop push unblock
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-chain-legacy-repair.md`
- source_brainstorm: `docs/pre-brainstorms/20260403-1100--governance-chain-legacy-repair/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260403-1100--governance-chain-legacy-repair/candidates.md`
- evidence:
  - `develop` merge `1d87824`
  - `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
  - `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/child-slice-status.md`
  - `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/code-reviews/20260403-governance-chain-legacy-repair-implementation-decision.md`
  - `docs/progress/workspace-routing-foundation/p-governance-chain-legacy-repair.md`
- completion_note: The 2026-04-04 truth-repair merge restored the missing `1100` owner artifacts, retired deleted `1200/1201/1202/1203` slices to historical status, and cleared dangling canonical references. Any future governance-chain backfill must reopen from current `develop` as a new lifecycle instead of reviving `1100` as an active owner.
3. `I-20260403-2245-A`
- title: Sandbox-compatible runtime bootstrap and operator-state governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/candidates.md`
- evidence:
  - `develop` merge `1eddbcd`
  - `develop` merge `45bed28`
  - `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
  - `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/code-reviews/20260403-sandbox-compatible-runtime-bootstrap-and-operator-state-verification.md`
  - `docs/progress/workspace-routing-foundation/p-sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-sandbox-operator-state-bootstrap-fallback`
  - `bash docs/system/workspace/scripts/tests/test-freely-status-degrades-when-ps-is-unavailable`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-refuses-unverified-attach-when-ps-is-unavailable`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-rejects-foreign-pids-when-ps-is-unavailable`
  - `bash docs/system/workspace/scripts/tests/test-freely-stop-ignores-foreign-pids-when-ps-is-unavailable`
  - `./bin/governance-check`
- completion_note: Canonical `develop` absorbed the sandbox-compatible operator-state fallback and the degraded PID ownership followthrough through merges `1eddbcd` and `45bed28`; this closeout lane only writes back completed lifecycle truth so future sandbox/runtime gaps reopen as new owners on current `develop`.
4. `I-20260404-0119-A`
- title: Governance merge gate milestone status followthrough governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-merge-gate-milestone-status-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0119--governance-merge-gate-milestone-status-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0119--governance-merge-gate-milestone-status-followthrough/candidates.md`
- evidence:
  - `develop` merge `908a6ad`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/tasks.md`
  - `docs/progress/workspace-routing-foundation/p-governance-merge-gate-milestone-status-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/code-reviews/20260404-governance-merge-gate-milestone-status-followthrough-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
- completion_note: Canonical `develop` absorbed the narrow `parse_milestones()` queue-scope repair through merge `908a6ad`; this closeout lane only writes back completed lifecycle truth so any future nested-field parser regressions reopen as new owners on current `develop`.
5. `I-20260404-0232-A`
- title: Governance merge gate review-aware regression alignment governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-merge-gate-review-aware-regression-alignment-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/candidates.md`
- evidence:
  - `develop` merge `0bb78ce`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/tasks.md`
  - `docs/progress/workspace-routing-foundation/p-governance-merge-gate-review-aware-regression-alignment-governance.md`
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
- completion_note: Canonical `develop` absorbed the review-aware mixed-regression fixture refresh and the same-file borrowed-owner block restoration through merge `0bb78ce`; this closeout lane only writes back completed lifecycle truth so future merge-gate residuals reopen as new owners on current `develop`.
6. `I-20260404-1405-A`
- title: Manager bootstrap prompt publication without continuity materialization governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization/candidates.md`
- evidence:
  - `develop` merge `8d29609`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-verification.md`
  - `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- completion_note: Canonical `develop` absorbed the bounded bootstrap grace fix and the `## Worker Dispatch` continuity parser repair through merge `8d29609`; this closeout lane only realigns milestone, issue, and progress truth so future restart-churn work reopens as a new owner instead of reviving `1405`.
1. `I-20260402-0455-A`
- title: Worktree exclusive ownership and promotion lease governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0455--worktree-exclusive-ownership-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0455--worktree-exclusive-ownership-governance/candidates.md`
- evidence:
  - `develop` merge `a10f6d8`
  - `docs/progress/workspace-routing-foundation/p-worktree-exclusive-ownership-and-promotion-lease-governance.md`
  - `docs/epics/workspace-routing-foundation/worktree-exclusive-ownership-and-promotion-lease-governance/code-reviews/20260402-worktree-exclusive-ownership-and-promotion-lease-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-hard-stale-intent-reclaim`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-merge-guarded`
  - `./bin/governance-check`
- completion_note: Canonical `develop` now has a shared phase-1 ownership truth for runtime status, manager launch/recovery, cleanup followthrough, and promotion gating, so duplicate mutate intents no longer rely on PID-only courtesy checks.

2. `I-20260401-2354-A`
- title: Implementation decision notes in issue-bound review artifacts
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-2354--implementation-decision-notes-in-review-artifacts/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-2354--implementation-decision-notes-in-review-artifacts/candidates.md`
- evidence:
  - `develop` merge `d4c9474`
  - `develop` merge `5537a7e`
  - `docs/progress/workspace-routing-foundation/p-implementation-decision-notes-in-issue-review-artifacts-governance.md`
  - `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews/20260401-implementation-decision-notes-in-review-artifacts-verification.md`
  - `docs/epics/workspace-routing-foundation/runtime-human-readable-time-display-governance/code-reviews/20260402-runtime-human-readable-time-display-verification.md`
  - `docs/epics/workspace-routing-foundation/runtime-loop-log-timezone-label-followthrough-governance/code-reviews/20260402-runtime-loop-log-timezone-label-followthrough-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
- completion_note: The decision-note gate is now closed on canonical `develop`: implementation-bearing develop-bound diffs require a staged owner review artifact, and post-gate owners such as `runtime-human-readable-time-display` and `runtime-loop-log-timezone-label-followthrough` prove that the complete note path works end to end.

2. `I-20260401-1831-A`
- title: Worker reactivation and local reentry residual runtime governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/worker-reactivation-and-local-reentry-residual-runtime-governance/issues/worker-reactivation-and-local-reentry-residual-runtime-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1831--worker-reactivation-reentry-residual-runtime-gaps/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1831--worker-reactivation-reentry-residual-runtime-gaps/candidates.md`
- evidence:
  - `develop` commit `e3cce23`
  - `docs/progress/workspace-routing-foundation/p-worker-reactivation-and-local-reentry-residual-runtime-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-reactivation-and-local-reentry-residual-runtime-governance/code-reviews/20260401-worker-reactivation-and-local-reentry-residual-runtime-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
  - `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
  - `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
  - `./bin/governance-check`
- completion_note: The bounded worker residual owner is now closed on canonical `develop`: attach-reuse false-success and local reentry predicate drift are both frozen into runtime truth, and future worker-runtime drift must reopen as narrower follow-on owners instead of lingering in verification.

1. `I-20260402-0540-A`
- title: Runtime loop log timezone label followthrough governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-loop-log-timezone-label-followthrough-governance/issues/runtime-loop-log-timezone-label-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0540--runtime-loop-log-timezone-label-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0540--runtime-loop-log-timezone-label-followthrough/candidates.md`
- evidence:
  - `develop` merge `5537a7e`
  - `docs/progress/workspace-routing-foundation/p-runtime-loop-log-timezone-label-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-loop-log-timezone-label-followthrough-governance/code-reviews/20260402-runtime-loop-log-timezone-label-followthrough-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-cooldown-falls-back-to-active-slot`
  - `./bin/governance-check`
- completion_note: The final runtime time-display tail is now closed on `develop`: loop log headers remain host-local and now carry timezone labels, while stored truth and UTC naming truth stay unchanged.

1. `I-20260401-1545-A`
- title: ACP optional adapter boundary governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/candidates.md`
- evidence:
  - `develop` commit `a0f9a48`
  - `docs/progress/workspace-routing-foundation/p-acp-optional-adapter-boundary-governance.md`
  - `./bin/governance-check`
- completion_note: ACP adapter boundary is now canonical on `develop`: ACP stays an optional communication-layer adapter, `direct` remains the first-class path, and governance concerns remain in Freely rather than being collapsed into ACP.

2. `I-20260401-2245-A`
- title: Build artifact exposure and release allowlist audit governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-2245--build-artifact-exposure-and-release-allowlist-capability/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-2245--build-artifact-exposure-and-release-allowlist-capability/candidates.md`
- evidence:
  - `develop` commit `e085bda`
  - `docs/progress/workspace-routing-foundation/p-build-artifact-exposure-and-release-allowlist-audit-governance.md`
  - `docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/code-reviews/20260401-build-artifact-exposure-and-release-allowlist-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit`
  - `bash docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate`
  - `bun run build`
- `./bin/governance-check`
- completion_note: Canonical truth now enforces automation-first release artifact safety: forbidden build outputs and non-allowlisted files fail the audit, `freely doctor` replays that audit when build output exists, and production sourcemaps are explicitly disabled by default in repo builds.

3. `I-20260402-0308-A`
- title: Runtime human-readable time display governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-human-readable-time-display-governance/issues/runtime-human-readable-time-display-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0308--runtime-status-time-display-audit/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0308--runtime-status-time-display-audit/candidates.md`
- evidence:
  - `develop` commit `af0be7c`
  - `develop` commit `eca4c79`
  - `docs/progress/workspace-routing-foundation/p-runtime-human-readable-time-display-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-human-readable-time-display-governance/code-reviews/20260402-runtime-human-readable-time-display-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-develop-push-status-time-display`
  - `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
  - `./bin/governance-check`
- completion_note: Human-readable runtime status surfaces now render in the host system timezone with timezone labels across the original runtime slice and the residual baseline/live status tail fields, while UTC naming truth and RFC3339/epoch machine truth stay unchanged; `frontend-probe-v0` remains limited to the Probe display slice.

3. `I-20260401-0115-A`
- title: Supply-chain baseline and install-intake audit governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/issues/supply-chain-baseline-and-install-intake-audit-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-0115--supply-chain-baseline-and-install-intake-audit-capability/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-0115--supply-chain-baseline-and-install-intake-audit-capability/candidates.md`
- evidence:
  - `develop` commit `1d082fc`
  - `docs/progress/workspace-routing-foundation/p-supply-chain-baseline-and-install-intake-audit-governance.md`
  - `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/code-reviews/20260401-supply-chain-baseline-and-install-intake-audit-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`
  - `bash docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
  - `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
  - `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
  - `./bin/governance-check`
- completion_note: Supply-chain baseline is now canonical on `develop`: lockfile presence, disallowed direct dependency intake, explicit install lifecycle allowlist enforcement, mutable workflow pin rejection, and shared `doctor` replay no longer depend on reviewer memory; `freely init` also seeds the repo-scoped lifecycle allowlist so new repos start aligned with the baseline.

3. `I-20260401-1308-A`
- title: Agent execution safety review and security decision support
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/candidates.md`
- evidence:
  - `develop` merge `e72ff86`
  - `docs/progress/workspace-routing-foundation/p-agent-execution-safety-review-and-security-decision-support.md`
  - `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/code-reviews/20260401-agent-execution-safety-review-and-security-decision-support-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
  - `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-security-review-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
  - `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
  - `bin/pretests-gate --issue docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
  - `./bin/governance-check`
- completion_note: The first advisory-only security review capability slice is now canonical on `develop`: project-local execution-boundary truth, machine-readable `security-review-brief` guidance, and the workspace skill expose reviewer/committee escalation evidence without rewriting launch blocking, approval posture, or fallback behavior. A real reviewer committee runtime remains a follow-on owner rather than unfinished scope inside this slice.

2. `I-20260401-1703-A`
- title: Runtime adapter axis and per-tool adapter selection
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1703--runtime-adapter-axis-and-per-tool-adapter-selection/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1703--runtime-adapter-axis-and-per-tool-adapter-selection/candidates.md`
- evidence:
  - `develop` commit `a0f9a48`
  - `docs/progress/workspace-routing-foundation/p-runtime-adapter-axis-and-per-tool-adapter-selection.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
- completion_note: The runtime now has a canonical adapter axis on `develop`, including adapter truth, adapter policy, adapter-aware dispatch, managed mutation, and a per-tool supported-adapter matrix.

3. `I-20260401-1545-A-01`
- title: Codex ACP fresh-path prototype
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/issues/codex-acp-fresh-path-prototype.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/candidates.md`
- evidence:
  - `develop` commit `a0f9a48`
  - `docs/progress/workspace-routing-foundation/p-codex-acp-fresh-path-prototype.md`
  - `docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/code-reviews/20260401-codex-acp-fresh-path-prototype-verification.md`
- completion_note: The first real `codex + adapter=acp` prototype is now merged on `develop` for `fresh` and `fresh_with_handoff`; direct path still owns the strongest explicit `resume` contract, so parity work must reopen as a new owner.

1. `I-20260328-2105-A`
- title: Codex verified resume evidence governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260328-2105--resume-evidence-strength-and-false-positive-resume-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260328-2105--resume-evidence-strength-and-false-positive-resume-governance/candidates.md`
- evidence:
  - `develop` commit `20574fa`
  - `docs/progress/workspace-routing-foundation/p-codex-verified-resume-evidence-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-verified-resume-evidence-governance/code-reviews/20260330-codex-verified-resume-evidence-feature-verification.md`
- completion_note: verified-resume evidence contract 已进入主线：`codex` 只有在 rollout/jsonl evidence 可追踪时才会继续 explicit `resume`，单独观察到的 `session_id` 不再被误升格为可恢复 truth，也不会继续制造 false-positive resume storm。

1. `I-20260325-0333-B`
- title: Story-level pre-tests quality gate governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260325-0333--testing-evidence-ladder-and-real-environment-gates/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260325-0333--testing-evidence-ladder-and-real-environment-gates/candidates.md`
- evidence:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
  - `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/code-reviews/20260325-story-level-pre-tests-quality-gate-governance-verification.md`
- completion_note: Story-level `pre-tests.md` 质量 gate 已进入 capability truth，最小 blocker taxonomy 已冻结为 `definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`，verification 已 pass

1. `I-20260331-2012-A`
- title: Active milestone placement and consumption gate governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260331-2012--active-milestone-placement-and-consumption-gate/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260331-2012--active-milestone-placement-and-consumption-gate/candidates.md`
- evidence:
  - `develop` commits `79f8bba`, `b279330`, `8972f7c`
  - `docs/progress/workspace-routing-foundation/p-active-milestone-placement-and-consumption-gate-governance.md`
  - `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/code-reviews/20260331-active-milestone-placement-gate-verification.md`
- completion_note: active milestone placement correctness 已经进入 canonical gate truth。`governance-check` 与 `governance-merge-gate` 现在共同拦截 unresolved candidate 的 `unassigned` / `pending://...` / wrong milestone / completed milestone placement，并允许同一 governance owner 吸收 unresolved placement metadata 修正；这条 owner 不再保留在 verification。

1. `I-20260331-1840-A`
- title: Multi-tool availability manager governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md`
- evidence:
  - `develop` commits `7252ed8`, `f5addf3`, `795fe8d`, `12a56bc`
  - `docs/progress/workspace-routing-foundation/p-multi-tool-auto-switch-v1-codex-fallback-governance.md`
  - `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`
- completion_note: ordered fallback v1 已经落到 canonical runtime truth：current tool same-tool recovery first、cross-tool fallback 从 `AI_FALLBACK_TOOLS` 最左侧重新开始、Kiro live path 不再被 stale default model 或 supervisor teardown race 卡住。更广的 all-tools slot parity 已移交 `I-20260401-0840-A` 并完成，不再由本 owner 持续占用 verification。

1. `I-20260401-0840-A`
- title: All-tools unified slot contract governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/candidates.md`
- evidence:
  - `develop` commit `e8b5e0a`
  - `docs/progress/workspace-routing-foundation/p-all-tools-unified-slot-contract-governance.md`
  - `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
- completion_note: unified slot contract 已进入主线：所有工具进入统一 `~/.ai-auth/<tool>-<slot>/` inventory、runtime 维护 generic current-slot truth、每个 fallback tool 先扫 own slots，再继续跨工具，并且 canonical `develop` live validation 已确认 `kiro-cli` 不可用 + dead Codex slot 时仍能落到后续可用 Codex slot。

1. `I-20260330-2358-A`
- title: Runtime network failure taxonomy and bounded recovery governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/candidates.md`
- evidence:
  - `develop` commit `1a632bd`
  - `docs/progress/workspace-routing-foundation/p-runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/code-reviews/20260401-runtime-network-failure-taxonomy-and-bounded-recovery-verification.md`
- completion_note: execution-time network failure taxonomy 已被 narrow runtime owner 吸收：`execution_network_transient` / `execution_network_persistent` / `proxy_config_invalid` 不再落回 generic `ai_exit_rc_*`，也不会误触发 slot/tool fallback，而是在当前 `tool + slot` 上执行 bounded retry/cooldown。

1. `I-20260331-1830-A`
- title: Kiro CLI runtime availability failure governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/issues/kiro-cli-runtime-availability-failure-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260331-1830--kiro-cli-monthly-request-limit-runtime-loop-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260331-1830--kiro-cli-monthly-request-limit-runtime-loop-governance/candidates.md`
- evidence:
  - `develop` commit `3a6b0e0`
  - `docs/progress/workspace-routing-foundation/p-kiro-cli-runtime-availability-failure-governance.md`
  - `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/code-reviews/20260331-kiro-cli-runtime-availability-verification.md`
- completion_note: Kiro monthly-limit / subscription-status-service-error 这条已证实 failure family 已被 narrow runtime owner 吸收：runtime 不再把它们记成 `ai_exit_rc_0`，而是写入 canonical Kiro availability reason 并停止本地盲目 relaunch。更广的 same-tool slot recovery 或 cross-tool fallback 继续留给后续 lifecycle，不回灌本 owner。

1. `I-20260330-2318-A`
- title: Manager attach reuse missing-AI repair governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260330-2318--live-status-already-running-attach-regression/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260330-2318--live-status-already-running-attach-regression/candidates.md`
- evidence:
  - `develop` merge `9b89fb3`
  - `docs/progress/workspace-routing-foundation/p-manager-attach-reuse-missing-ai-repair-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/code-reviews/20260401-manager-attach-reuse-missing-ai-verification.md`
- completion_note: `develop` real recovery validation now confirms the manager attach path no longer rewrites runtime truth to `already_running_attach` when only the supervisor is present. On the same `kiro_monthly_request_limit -> codex` chain that previously reproduced the bug, runtime now records `tool_auto_switch_selected` followed by `ai_launch_begin tool=codex` without `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager`; worker attach reuse remains unchanged.

1. `I-20260321-1835-A`
- title: Develop merge issue binding and C/M/I gate governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1835--lifecycle-complete-before-merge-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1835--lifecycle-complete-before-merge-governance/candidates.md`
- evidence:
  - `develop` commit `5e3ec97`
  - `develop` merge replay `544e1dd`
  - `docs/progress/workspace-routing-foundation/p-develop-merge-issue-binding-and-cmi-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/code-reviews/20260330-develop-merge-cmi-gate-verification.md`
- completion_note: strengthened gate 现在不仅在 focused regressions 与 hook wrapper 路径上通过，还在真实 runtime closeout merge 中阻断了 completed-owner / absorbed-candidate misuse，并在修正为 same-line execution owner 后放行；因此本 owner 已完成 closeout。

1. `I-20260324-0415`
- title: Application-native runtime observation contract and observability planes
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
- source_brainstorm: `docs/pre-brainstorms/20260324-0415--application-native-observability-planes/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260324-0415--application-native-observability-planes/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-application-native-runtime-observation-contract-and-observability-planes.md`
  - `docs/epics/workspace-routing-foundation/application-native-runtime-observation-contract-and-observability-planes/code-reviews/20260324-application-native-runtime-observation-contract-and-observability-planes-verification.md`
- completion_note: application-native runtime observation contract、observability plane 分层与共享状态卡片 deep refs 已在 canonical issue/progress/verification 栈中闭合；当前缺口只是 milestone 编排写回，非 IBM/dev 真源缺失

1. `I-20260327-0651`
- title: Project-scoped network proxy configuration and launcher inheritance governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/code-reviews/20260327-project-scoped-network-proxy-verification.md`
- completion_note: project-scoped proxy config truth、shared resolver、OAuth inheritance 与 no-arg switch refresh contract 已合到同一能力面；后续前端只需改 `.freely/config.env` 即可驱动同一网络策略。

2. `I-20260327-0701`
- title: Pre-tests evidence binding and completion gate governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews/20260327-pretests-gate-feature-verification.md`
- completion_note: 第一阶段 issue-bound completed gate 已在 `develop` 吸收；后续 active worktree 在 issue 进入 `completed` 时会被同一 gate 约束，retirement enforcement 留给 follow-on lifecycle。

3. `I-20260327-1115`
- title: OAuth slot inventory sweep and launch-time confirmation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/code-reviews/20260327-oauth-sweep-launch-confirmation-verification.md`
- completion_note: OAuth `wham/usage` sweep 已成为 canonical inventory truth surface；status、switch auto、ensure-manager 共用 cache/sweep/launch-time-confirmation contract，旧的全量串行真实 probe 不再是主路径

1. `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260316-first-hop-second-hop-verification.md`
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260326-source-routing-canonical-replay-verification.md`
- completion_note: 首跳来源分层、IBM/progress 边界、derived worktree 规则与同工具第二跳 contract 已收口；旧 dirty sibling blocker 已被 canonical 4-tree fleet truth 消除，不再构成未完成项

2. `I-20260319-0018`
- title: Token-efficient session continuity and rotation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/code-reviews/20260326-token-efficient-session-continuity-and-rotation-canonical-verification.md`
- completion_note: continuity trigger matrix、manager-vs-worker continuity targets、fallback-only session evidence refs 与 warn/rotate/fresh-with-handoff 边界已共同写回 canonical truth sources；后续官方 compaction primitive 或 continuity schema 演进另开 lifecycle

3. `I-20260319-0148`
- title: Context-compaction continuity guard salvage
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/context-compaction-continuity-guard-salvage/issues/context-compaction-continuity-guard-salvage.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-context-compaction-continuity-guard-salvage.md`
  - `docs/epics/workspace-routing-foundation/context-compaction-continuity-guard-salvage/code-reviews/20260326-context-compaction-continuity-guard-salvage-canonical-verification.md`
- completion_note: 旧 context-compaction 分支独有的 continuity guard 字段、prompt 提醒与测试锁定已被 canonical `develop` 吸收；本地也不再保留旧 feature branch，后续 continuity 演进回到主线 issue family

2. `I-20260321-0217`
- title: Claude Code tool profiles and Codex MCP session evidence governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/candidates.md`, `docs/pre-brainstorms/20260321-0148--cc-codex-session-evidence-resolution/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/code-reviews/20260321-cc-codex-runtime-governance-verification.md`
  - `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/code-reviews/20260326-cc-codex-runtime-canonical-replay-verification.md`
- completion_note: `cc` / `cc-use-codex-cli` fixed top-level profiles、双层 session evidence 与 focused regressions 已在当前 develop-facing absorption owner 上保持通过；后续 protected replay 属于 sweep-level promote，不再阻塞 issue 完成

3. `I-20260321-1745`
- title: Active lifecycle boundary and dogfooding capability discovery
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1745--active-lifecycle-boundary-and-dogfooding-capability-discovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1745--active-lifecycle-boundary-and-dogfooding-capability-discovery/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/code-reviews/20260321-active-lifecycle-boundary-and-dogfooding-capability-discovery-verification.md`
  - `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/code-reviews/20260326-active-lifecycle-boundary-canonical-replay-verification.md`
- completion_note: active-vs-historical lifecycle 边界与狗粮能力发现原则已稳定写回 `three-loop-capability-lifecycle` 和 `PROJECT_INTENT`；后续更高层产品架构讨论另开 lifecycle，不回灌此 issue

4. `I-20260322-1801`
- title: pre-test-merge responsibility, usage, and lifecycle governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- evidence:
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
  - `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/code-reviews/20260322-pre-test-merge-responsibility-usage-and-lifecycle-governance-verification.md`
- completion_note: 历史 issue/path 仍沿用 `pre-test-merge` 命名，但当前 canonical 真义已收敛为 `test-pre-merge-*` 测试批次前缀族；其职责边界、stale / retire / rebuild 语义与 canonical promote / receipt 追溯策略已写回真源，后续 lifecycle management capability 保持独立，不与职责定义混成同一 issue

5. `I-20260321-1515`
- title: Remote branch retirement governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1515--remote-branch-retirement-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1515--remote-branch-retirement-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260321-remote-branch-retirement-governance-verification.md`
  - `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260326-remote-branch-retirement-canonical-replay-verification.md`
- completion_note: remote branch disposition 已并入 cleanup/retirement contract，并在当前 absorption owner 上继续通过 focused interruption cleanup regression；后续 status surface 扩展另开 lifecycle

6. `I-20260321-0257`
- title: Worktree fleet governance closure
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/code-reviews/20260321-worktree-fleet-governance-closure-verification.md`
  - `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/code-reviews/20260326-worktree-fleet-governance-closure-canonical-replay-verification.md`
- completion_note: `fleet_closure` 能力与 canonical inventory writeback 已稳定收敛到 4-tree / dirty=0 / all stopped；retained-vs-retired judgement 已冻结为 protected/control、retained research owner、active develop-facing absorption owner 三类，后续 research materialization 不再阻塞本 issue 完成

7. `I-20260329-2045-A`
- title: AI auth-change wake command lifecycle governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/issues/ai-auth-change-wake-command-lifecycle-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle/candidates.md`
- evidence:
  - `develop` commit `44bb13c`
  - `docs/progress/workspace-routing-foundation/p-ai-auth-change-wake-command-lifecycle-governance.md`
  - `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/code-reviews/20260330-ai-auth-change-wake-command-lifecycle-verification.md`
- completion_note: `switch/login` success-path wake lifecycle 已收口到“成功后及时退出 + suppress watchdog self-reentry”，且本轮未执行真实登录或 slot 删除。

8. `I-20260329-2155-A`
- title: Sensitive local artifact ignore governance
- milestone_state: completed
- phase_state: `completed`
- priority: P2
- issue_path: `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/issues/sensitive-local-artifact-ignore-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260329-2155--sensitive-local-artifact-ignore-governance/candidates.md`
- evidence:
  - `develop` commit `208c591`
  - `docs/progress/workspace-routing-foundation/p-sensitive-local-artifact-ignore-governance.md`
  - `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/code-reviews/20260330-sensitive-local-artifact-ignore-verification.md`
- completion_note: 保守 sensitive-local-artifact ignore contract 与 focused regression 已合入 `develop`，并清除了根目录 stray `auth.json`。

9. `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/candidates.md`
- evidence:
  - `develop` merge `b93efd2`
  - `docs/progress/workspace-routing-foundation/p-project-command-semantics-and-restore-work-governance.md`
  - `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md`
- completion_note: project command family taxonomy、verification cleanup hardening 与 closeout 写回已完成；后续 global restart 继续留在拆分 owner。

10. `I-20260327-2006-A-global-restart`
- title: Global restart restore memory governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-2006--start-restart-control-plane-semantics/candidates.md`
- evidence:
  - `develop` commit `8441b92`
  - `develop` merge `2467cc7`
  - `docs/progress/workspace-routing-foundation/p-global-restart-restore-memory-governance.md`
  - `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`
- completion_note: explicit global restart restore-memory owner 已完成，实现覆盖 manifest durability、retention 与 fleet restore selection。

7. `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/candidates.md`, `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/code-reviews/20260326-global-ai-account-watchdog-canonical-replay-verification.md`
  - `docs/progress/workspace-routing-foundation/p-global-ai-account-watchdog-and-manager-bootstrap.md`
- completion_note: global watchdog/bootstrap contract 已在 canonical `develop` 通过 replay，slot-sweep-first recovery、no-launch gate、all-unavailable hold、inventory-change wake、slot-only identity、dispatcher-ready gate 与 timeout/deactivated-workspace artifact 全部稳定；scheduler retained research 与更广义 interruption followthrough 另由后续 lifecycle 承接

2. `I-20260326-1815`
- title: IBM pre-tests executable acceptance quality governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1733--ibm-pretests-real-environment-acceptance-quality/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1733--ibm-pretests-real-environment-acceptance-quality/candidates.md`
- evidence:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
  - `docs/progress/workspace-routing-foundation/p-ibm-pretests-executable-acceptance-quality-governance.md`
  - `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/code-reviews/20260326-ibm-pretests-executable-acceptance-quality-governance-verification.md`
- completion_note: IBM 真源现在要求 `pre-tests.md` 默认写出可恢复的 executable acceptance contract，并对 Freely 自治能力明确 integration、application-native real-environment、end-to-end dogfood 三类 post-merge 验收面；verification review 模板统一与 machine-readable schema 继续留给后续 lifecycle

3. `I-20260326-1915`
- title: Deep-refactor fleet sequencing governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1825--deep-refactor-fleet-sequencing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1825--deep-refactor-fleet-sequencing/candidates.md`
- evidence:
  - `AGENTS.md`
  - `docs/progress/workspace-routing-foundation/p-deep-refactor-fleet-sequencing-governance.md`
  - `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/code-reviews/20260326-deep-refactor-fleet-sequencing-governance-verification.md`
- completion_note: broad/deep refactor 前的 fleet sequencing audit 已固定为开发 Freely 的入口 gate，并已用真实 stop、merge-prep 与 governance-check 结果验证；后续若要升级成自动化或更高等级规则，应由新的 lifecycle 承接

4. `I-20260326-1835`
- title: Manager owner stance and source-patrol completeness governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1705--manager-owner-stance-and-source-patrol/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1705--manager-owner-stance-and-source-patrol/candidates.md`
- evidence:
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
  - `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
  - `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
  - `docs/progress/workspace-routing-foundation/p-manager-owner-stance-and-source-patrol-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/code-reviews/20260326-manager-owner-stance-and-source-patrol-governance-verification.md`
- completion_note: 已把开发治理输入与运行期能力真源的边界写清，并把 manager owner stance、advisory interruption semantics、以及 interruption / milestone / progress / pre-brainstorm 的 standing-source completeness 直接收敛进产品能力真源；后续若要继续把这套 contract 扩成更强的 runtime 事务面，应通过新 lifecycle 承接。

3. `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260326-latest-manager-continuity-worker-consumption-canonical-replay-verification.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260404-latest-manager-continuity-worker-consumption-missing-run-dir-guard-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260404-latest-manager-continuity-worker-consumption-missing-run-dir-guard-verification.md`
- completion_note: canonical `develop` 已重新对齐 latest continuity / latest worker prompt generated-consumed truth，并继续吸收 2026-04-04 的 same-family missing-run-dir parser/status guard 修复；更大的 websocket blocked-intake / supervision contract 仍需独立 lifecycle 承接

3a. `I-20260405-1505-A`
- title: Manager semantic-loop active-worker suppression governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1505--manager-semantic-loop-active-worker-suppression/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1505--manager-semantic-loop-active-worker-suppression/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-semantic-loop-active-worker-suppression-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-implementation-decision.md`
  - `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-verification.md`
- completion_note: semantic-loop monitoring 重新回到 conservative contract；一旦 runtime 仍能看到 active worker truth，无论来自当前 PID 发现还是 launch-state 记录，`live-status` / `fleet-status` 都不会把现场误报成 manager semantic loop。更广的 active-worker stall recovery 仍按独立 lifecycle 推进。

4. `I-20260326-0445`
- title: Manager-delegated intake absorption closure governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-0445--manager-delegated-intake-absorption-closure/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-0445--manager-delegated-intake-absorption-closure/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-delegated-intake-absorption-closure-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/code-reviews/20260326-manager-delegated-intake-absorption-closure-verification.md`
- completion_note: manager-owned delegated intake absorbed closure 已进入 canonical `develop`，focused regressions 与 live-status surface 均未回退；worker-side delegated lifecycle 仍按既有 issue family 独立推进

5. `I-20260328-0745-A`
- title: Live-status current runtime state reconciliation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/issues/live-status-current-runtime-state-reconciliation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260328-0745--live-status-current-runtime-state-reconciliation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260328-0745--live-status-current-runtime-state-reconciliation/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-live-status-current-runtime-state-reconciliation-governance.md`
  - `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`
- completion_note: `live-status` current-state surface 现在会把确认存活的 project-owned supervisor / AI PID 与 `last_*` 字段对齐，不再在 active AI 场景下同时显示 `ai_active` 与 `last_ai_state: down`；修复保持只读，不改变 recovery 持久化语义

6. `C-20260324-0405-A`
- title: Watchdog restart-storm and process-churn signal implementation
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/issues/watchdog-restart-storm-and-process-churn-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-watchdog-restart-storm-and-process-churn-governance.md`
  - `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/code-reviews/20260324-watchdog-restart-storm-and-process-churn-verification.md`
- completion_note: restart-storm / process-churn signal 的 runtime helper、`session-state.env` 真相面、manager escalation 与 `live-status` / `fleet-status` 暴露已在 same-family issue 中完成并验证；该 candidate 不再保留为 active dev handoff

7. `I-20260320-1945`
- title: Watchdog live status surface and manager supervision
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- completion_note: `freely live-status` 的主管监督接线与 status surface 已进入 canonical truth；后续若继续扩 JSON / watch / scoring，应新开 lifecycle

8. `I-20260320-2105`
- title: Baseline-status command and status family governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-2105--status-family-baseline-rename-and-future-aggregation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-2105--status-family-baseline-rename-and-future-aggregation/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- completion_note: `baseline-status` 命名迁移与 `status` family 聚合入口已经完成；后续 JSON family 输出或 watch 模式应通过新 lifecycle 承接

8. `I-20260324-0405`
- title: 三个 loop 的并列关系与 terminal governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/candidates.md`, `docs/pre-brainstorms/20260323-0241--three-loop-lifecycle-dictionary-and-worktree-completion/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-three-loops-sibling-relationship-and-terminal-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/code-reviews/20260324-three-loops-sibling-relationship-verification.md`
- completion_note: active truth、agent / skill 与 runtime-facing contract 已统一到 `auto-loop` outer + `doc-loop` / `dev-loop` sibling 的模型；继续把它留在 `in_dev` 会制造假待办

9. `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-cli-first-entrypoint-and-observability-surface-unification.md`
  - `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
- completion_note: shared front-door submit helper 与 CLI-first backend contract 已完成并验证；后续若继续扩 Tauri 渲染层，应新开 lifecycle

10. `I-20260322-0135`
- title: Integration-acceptance-first IBM and verification governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0135--integration-acceptance-first-ibm-and-verification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0135--integration-acceptance-first-ibm-and-verification/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-integration-acceptance-first-verification-governance.md`
  - `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/code-reviews/20260322-integration-acceptance-first-verification-governance-verification.md`
- completion_note: `pre-tests.md` 作为 issue-level acceptance 控制面与 integration-first 口径已收回真源；结构化 verification review 模板若继续扩展，应另开 lifecycle

11. `I-20260322-0228`
- title: Manager delegation after sufficient patrol evidence governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0228--manager-delegation-after-sufficient-patrol-evidence/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0228--manager-delegation-after-sufficient-patrol-evidence/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-delegation-after-sufficient-patrol-evidence-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/code-reviews/20260322-manager-delegation-after-sufficient-patrol-evidence-governance-verification.md`
- completion_note: patrol evidence 充足后必须切 concrete worker delegation 的阈值语义已经稳定落盘；后续若 runtime 仍出现只巡检不委派，应进入新的 delegation-mechanism lifecycle

12. `I-20260322-0412`
- title: Worker active reentry for manager-delegated continuation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0412--worker-active-reentry-for-manager-delegated-continuation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0412--worker-active-reentry-for-manager-delegated-continuation/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/code-reviews/20260322-worker-active-reentry-for-manager-delegated-continuation-verification.md`
- completion_note: active-worker local reentry 修复、脚本级验收与 post-merge acceptance 已完成；后续 consumed-id 可见性增强应通过新 lifecycle 承接

13. `I-20260318-0930`
- title: Checkpoint commit and multi-worktree supervision governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260318-checkpoint-and-fleet-verification.md`
  - `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260326-checkpoint-and-fleet-canonical-replay-verification.md`
- completion_note: checkpoint-guard、staged scope gate、fleet summary 与 baseline dirty-budget 暴露已经在 canonical `develop` 通过 replay；旧 dirty worktree snapshot 不再构成未完成项

14. `I-20260318-1408`
- title: Manager self-supervision and autonomous recovery
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/code-reviews/20260326-manager-self-supervision-canonical-replay-verification.md`
- completion_note: manager self-supervision alert、runtime-owned recovery、PID ownership 与 account-boundary contract 已在 canonical `develop` 通过 replay；更外层 manager ensure / watchdog 由 `I-20260318-1630` 继续承接

15. `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260316-state-sync-verification.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260317-lead-agent-reentry-verification.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260326-state-sync-canonical-replay-verification.md`
- completion_note: 状态词典、session evidence 传播与 milestone handoff policy 已在 canonical truth 中稳定存在；旧 dirty snapshot 与当时的环境兼容性问题不再构成未完成项

16. `I-20260318-1825`
- title: Worktree hygiene supervision control plane
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/worktree-hygiene-supervision-control-plane/code-reviews/20260326-worktree-hygiene-canonical-replay-verification.md`
- completion_note: hygiene skill、checkpoint drift escalation 与 manager hygiene alert 已在 canonical `develop` 通过 replay；若需专门 hygiene worker delegation flow，应通过新 lifecycle 承接

17. `I-20260321-0345`
- title: Manager reactivation and fleet patrol governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/issues/manager-reactivation-and-fleet-patrol-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-0345--manager-reactivation-and-fleet-patrol/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-0345--manager-reactivation-and-fleet-patrol/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260321-manager-reactivation-and-fleet-patrol-verification.md`
  - `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260326-manager-reactivation-and-fleet-patrol-canonical-replay-verification.md`
- completion_note: manager reactivation 后先 patrol fleet 的协议、reference 与首跳提示已在 canonical truth 中稳定存在；真正脚本级巡检/自动派单应通过新 lifecycle 承接

18. `I-20260321-1045`
- title: Stacked worktree merge-chain governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1045--stacked-worktree-merge-chain-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1045--stacked-worktree-merge-chain-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/stacked-worktree-merge-chain-governance/code-reviews/20260326-stacked-merge-chain-canonical-replay-verification.md`
- completion_note: stacked merge-chain 的 skill/reference/prompt truth 已在 canonical truth 中稳定存在；CLI/脚本级自动决策属于后续增量，不再阻塞当前 issue 收口

### candidate_issues

1. `C-20260331-1840-A`
- title: Materialize ordered multi-tool fallback v1 with Codex slot parity
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md`
- next_action: This candidate is now materialized as `I-20260331-1840-A`. The active owner restores same-tool-first recovery, ordered `AI_FALLBACK_TOOLS` scanning, and explicit all-tools-unavailable waiting truth while keeping per-tool capability gaps explicit.
- revisit_trigger: Re-open only if the completed ordered-fallback v1 regresses; all-tools unified slot parity now belongs to `C-20260401-0840-A`.

3. `C-20260401-0840-A`
- title: Materialize unified slot contract across all runtime tools
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/candidates.md`
- next_action: This candidate is now materialized as `I-20260401-0840-A`. The active owner absorbs unified slot inventory, current-slot truth, generic slot-first scheduling, and earliest tool+slot waiting truth.
- revisit_trigger: Re-open candidate-level research only if generic slot inventory proves insufficient and a structured auth-material schema is required.

4. `C-20260330-2318-A`
- title: Live-status false already-running-attach regression
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260330-2318--live-status-already-running-attach-regression/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260330-2318--live-status-already-running-attach-regression/candidates.md`
- next_action: This candidate is now materialized as `I-20260330-2318-A`. The active owner keeps the slice narrow: manager attach reuse now requires a confirmed AI child before writing attach success, while worker attach reuse stays unchanged.
- revisit_trigger: Re-open candidate-level research only if the manager-only attach gate repair still leaves stale optimistic truth and forces a broader `live-status` or observability redesign.

5. `C-20260327-1115-A`
- title: Promote OAuth parallel sweep to canonical slot inventory truth
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/candidates.md`
- next_action: 已提升为新的 follow-on issue；后续由 `I-20260327-1115` 承接 issue-bound IBM closeout 与 dev-loop 执行

6. `C-20260323-1435-A`
- title: Interactive init bootstrap and fine-grained force/skip governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://interactive-init-bootstrap-and-force-governance`
- source_brainstorm: `docs/pre-brainstorms/20260323-1435--interactive-init-bootstrap-and-force-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1435--interactive-init-bootstrap-and-force-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结 `init` 的 step graph、bootstrap commit 豁免边界，以及每个 managed item 的 skip/force contract；在这些边界稳定前，不直接往现有 `init` 继续堆局部 patch
- revisit_trigger: 当 `init` 的交互入口、repo bootstrap 语义与细粒度 skip/force 输出 contract 可以被冻结成独立 issue scope 时，重新进入 materialization 判断

7. `C-20260318-0715-A`
- title: `commit-first after checkpoint-ready` 自治治理
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结 3 个边界：`checkpoint-ready` 的结构化输出、`LAWS/runtime/checkpoint-guard/supervisor` 的职责分层、以及进入 IBM 前的 promotion gate；在这些边界稳定前不得直接写成 IBM issue 或塞回 `I-20260318-0930`
- revisit_trigger: 当 `checkpoint-ready` 的结构化输出、supervisor 职责边界与 promotion gate 可以被稳定写成最小 issue contract 时，重新进入 materialization 判断

8. `C-20260319-0402-01`
- title: 定义 Freely 的 harness engineering 分层与缺口图
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先验证 Freely 是否需要一份更明确的 harness 分层与缺口图；若边界稳定，再 materialize 成 issue，而不是直接把外部文章结论塞进现有主线
- revisit_trigger: 当 harness 分层、缺口图与 Freely 自身的最小吸收面可以冻结成独立 issue contract 时，重新进入 materialization 判断

9. `C-20260319-0402-02`
- title: 把 worktree 级验证信号统一暴露成 agent 可消费接口
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 继续 pre-brainstorm，先盘点现有 status / wt-status-all / runtime 输出，再决定要不要 materialize 成统一 machine-readable 汇总接口
- revisit_trigger: 当 worktree 级验证信号的 canonical 输入、输出与 machine-readable summary contract 可以被冻结成 issue scope 时，重新进入 materialization 判断

8. `C-20260319-0402-03`
- title: 建立文档园艺与 AI 残渣清理的周期性后台循环
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P2
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 保持 `needs_research`，等前两个更基础的 harness 候选边界稳定后，再决定是否 materialize
- revisit_trigger: 当 harness 分层图与 worktree 级验证接口都已稳定，且后台园艺循环不再扩大当前 scope 时，重新进入 materialization 判断

10. `C-20260401-1545-A`
- title: Materialize ACP as an optional adapter boundary between Freely and external code agents
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/candidates.md`
- next_action: This candidate is now materialized as `I-20260401-1545-A`. The issue freezes `ACP = optional adapter layer`, `direct = first-class path`, and the follow-on implementation order: extract adapter axis before any first-tool ACP prototype.
- revisit_trigger: Re-open candidate-level research only if issue-bound materialization fails to hold a stable ACP adapter boundary, or if ACP no longer fits Freely's external code-agent integration layer.

11. `C-20260401-1703-A`
- title: Materialize runtime adapter axis and per-tool adapter selection
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1703--runtime-adapter-axis-and-per-tool-adapter-selection/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1703--runtime-adapter-axis-and-per-tool-adapter-selection/candidates.md`
- next_action: This candidate is now materialized as `I-20260401-1703-A`. The owner isolates `adapter axis` extraction as the first implementation slice before any ACP bridge work.
- revisit_trigger: Re-open candidate-level research only if `adapter axis` extraction proves inseparable from a broader runtime redesign, or if the ACP boundary assumptions materially change.

12. `C-20260322-1615-A`
- title: Protected post-merge acceptance route and promotion guard governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://protected-post-merge-acceptance-route-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260322-1615--protected-post-merge-acceptance-route-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1615--protected-post-merge-acceptance-route-governance/candidates.md`
- next_action: 继续 pre-brainstorm，但已冻结两条硬规则：历史文案中的 `pre-test-merge` 现在一律按 `test-pre-merge-*` canonical 测试批次前缀族解释；`develop` 不承担主线前预测试，develop-bound promote 必须先经过当前权威 `test-pre-merge-*` 批次。剩余要收口的是 `develop-only completion verification` 与测试批次 acceptance 的分流、raw `git add` 无法 hook 时的最小可靠兜底，以及主环境验收发现问题后的 source receipt / cleanup 证据模型；在这些边界稳定前不得直接写成 issue 或只靠 skill 文案宣告完成
- revisit_trigger: 当 protected verification environment 的 replay policy、failure reroute、machine-readable evidence 与最小 guard 落点可以被冻结成独立 issue contract 时，重新进入 materialization 判断

13. `C-20260402-0455-A`
- title: Worktree exclusive ownership and promotion lease governance
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0455--worktree-exclusive-ownership-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0455--worktree-exclusive-ownership-governance/candidates.md`
- next_action: This candidate materialized as `I-20260402-0455-A`, and the owner is now closed on canonical `develop` via merge `a10f6d8`. Reopen candidate-level research only if a follow-on owner must extend ownership semantics beyond the completed phase-1 slice.
- revisit_trigger: Re-open candidate-level research only if the phase-1 ownership contract proves inseparable from a broader runtime orchestration redesign, or if cleanup/promotion ownership cannot be expressed with the proposed occupancy + lease split.

10. `C-20260325-0525-A`
- title: Retire cooldown-driven recovery and make slot sweep canonical
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/candidates.md`
- completion_note: 当前 candidate 生命周期已通过 pre-brainstorm 收口为 same-family supporting evidence；不新开平行 issue，直接把 “cooldown 退出主恢复 contract、failure-driven full slot sweep 成为 canonical” 的边界改写回 `I-20260318-1630`

11. `C-20260322-1801-B`
- title: pre-test-merge lifecycle management capability for Freely
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://pre-test-merge-lifecycle-management-capability`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- next_action: 继续 pre-brainstorm，但 scope 已收窄为 `stale test-pre-merge batch governance`；历史候选名仍保留 `pre-test-merge`，语义上一律指向 `test-pre-merge-*` 前缀族。先冻结三块 machine-readable contract：`stale state truth surface`、`manager-owned lifecycle transaction`、`runtime consumption gate`；同时补齐 `replay source manifest / replay order / retire evidence`，把 `Issue + Brainstorm + PRD -> pre-tests.md` 派生链桥接成固定的 `acceptance_contract_state/source/blocker` 字段，并把 testing closeout 的集成测试 / application-native real-environment testing evidence bar 写死，在这些真源稳定前不进入实现
- revisit_trigger: 当 stale state 的 canonical 落点、manager lifecycle transaction 字段、runtime gate 消费路径、replay/retire manifest、`acceptance_contract_state/source/blocker` 桥，以及 testing closeout evidence bar 都能冻结成独立 issue contract 时，重新进入 materialization 判断

12. `C-20260322-1801-C`
- title: worker self-loop exit and scheduler closeout governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://worker-self-loop-exit-and-scheduler-closeout-governance`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- next_action: 继续 pre-brainstorm，单独冻结 `phase progress`、`loop stall`、`manager handback`、`capacity release / supersede` 规则；同时补清 lane 回交后如何识别“其实是上游 `Issue + Brainstorm + PRD -> pre-tests.md` acceptance 面不完整”以及“其实还没完成 integration / application-native real-environment testing closeout”；这里提到的 stale `pre-test-merge` gate 同样按 `test-pre-merge-*` 前缀族解释，在 machine-readable 阈值稳定前，不把两条能力线绑在一起实现
- revisit_trigger: 当 low-value self-loop 的判据、manager 回交 contract、容量释放规则，以及与 IBM/`Issue + Brainstorm + PRD -> pre-tests.md` 缺口和 testing closeout 缺口的分流条件都能冻结成独立 issue contract 时，重新进入 materialization 判断

14. `C-20260319-0500-01`
- title: 为 Freely 补一份更强的 orchestrator executable spec
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先确认 Freely 是否真的缺一份更集中、可执行的 orchestrator spec；若结论稳定，再 materialize 成 issue，而不是直接把 Symphony 当成架构模板
- revisit_trigger: 当 orchestrator executable spec 的缺口、职责边界与最小验收可以冻结成独立 issue contract 时，重新进入 materialization 判断

15. `C-20260319-0500-02`
- title: 统一 issue-level continuity artifact 设计
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先确认哪些 continuity 信息必须跨环持续存在、哪些仍应按 loop 分层存放；未稳定前不要 materialize
- revisit_trigger: 当 issue-level continuity artifact 的最小字段、跨环写回边界与 canonical 落点可以被冻结成 issue scope 时，重新进入 materialization 判断

16. `C-20260319-0500-03`
- title: 评估远程 worker / SSH 执行扩展对 Freely 的适用性
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P2
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，优先只收集远程 worker 对 workspace ownership、cleanup、resume、host health 的新增要求
- revisit_trigger: 当远程 worker / SSH 扩展的 ownership、cleanup、resume 与 host health 新约束可以冻结成最小 issue contract 时，重新进入 materialization 判断

17. `C-20260310-0056-A`
- title: Evolver Sidecar for Freely Strategy Evolution
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/candidates.md`
- next_action: 继续 pre-brainstorm，先把本地可选 sidecar 的最小职责边界、review / validation / rollback gate 和不接管主 runtime 的约束写稳，再决定是否 materialize 成独立 issue
- revisit_trigger: 当 sidecar 的职责边界、review/validation/rollback gate 与“不接管主 runtime”约束可以被冻结成最小 issue contract 时，重新进入 materialization 判断

9. `C-20260310-0056-B`
- title: Delay EvoMap Hub Integration Until Single-Node Autonomy Is Stable
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/candidates.md`
- next_action: 保持在 pre-brainstorm，先把单机自治、自我优化原型与本地策略资产模型跑稳，再决定是否还需要外部 Hub / worker 网络方向
- revisit_trigger: 当单机自治闭环已稳定，且外部协作语义、成本与 review gate 可以被冻结成独立 issue contract 时，重新进入 materialization 判断

10. `C-20260320-1745-A`
- title: Dirty worktree gate redesign for multi-worktree autonomy
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-1745--dirty-worktree-governance-redesign/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-1745--dirty-worktree-governance-redesign/candidates.md`
- next_action: 保持 pre-brainstorm candidate；先继续冻结 `target_clean / fleet_busy / fleet_dirty_unrelated` 的最小 contract，再决定是否 materialize 成独立治理 issue
- revisit_trigger: 再次出现 unrelated dirty tree 阻断 cleanup / audit / merge-prep，或需要为 `wt-status-all` / cleanup 增加显式绕过语义时

11. `C-20260327-parked-worktree-retirement`
- title: Milestone-coupled parked worktree retirement planning
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结“parked issue allows retirement”的最小契约，再决定是否 materialize 成 follow-on issue
- revisit_trigger: 当某个 worktree 的剩余动作已退化为 milestone 排序维护，而不是近程 issue continuation 时重新唤起

12. `C-20260303-001`
- title: Ring + SSOT 规则契约化
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260303-0000--ai-consistency-closed-loop-freely-alignment/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260303-0000--ai-consistency-closed-loop-freely-alignment/candidates.md`
- next_action: 保持在 pre-brainstorm，先把 Ring/SSOT 冲突决议规则与检查点清单收敛成当前治理链可消费的最小 contract
- revisit_trigger: 当规则契约与检查点清单可以冻结成独立 issue contract 时，重新进入 materialization 判断

14. `C-20260303-002`
- title: 独立监理 Gate 接入 auto-loop
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260303-0000--ai-consistency-closed-loop-freely-alignment/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260303-0000--ai-consistency-closed-loop-freely-alignment/candidates.md`
- next_action: 保持在 pre-brainstorm，先定义最小独立审查放行边界，再判断是否值得进入正式治理 issue
- revisit_trigger: 当独立监理 gate 的输入输出、放行条件与 owner 边界可以被冻结成 issue scope 时，重新进入 materialization 判断

14. `C-20260304-605`
- title: Sub-agent 批次编排器
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260304-0000--research-redo-owner-tool-alignment/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260304-0000--research-redo-owner-tool-alignment/candidates.md`
- next_action: 保持在 pre-brainstorm，继续判断当前 dispatch metadata、queue/frozen queue 与失败回退是否已足够，还是仍需要独立 batch orchestration owner
- revisit_trigger: 当并发批次等待、失败回退与审计记录 contract 无法继续由现有 dispatch truth 承接时，重新进入 materialization 判断

15. `C-20260305-703`
- title: Governance UI for Hooks/Worktree Constraints
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260305-0000--freely-dogfooding-governance-worktree-policy/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260305-0000--freely-dogfooding-governance-worktree-policy/candidates.md`
- next_action: 继续 pre-brainstorm，先判断 CLI-first 配置内核是否已经足够稳定，再决定是否值得补 UI 层
- revisit_trigger: 当 hook/worktree 约束已有稳定 machine-readable config 面，且确实需要用户可视化治理入口时重新唤起

16. `C-20260309-2003-C`
- title: Review Alignment Recovery and Loop Boundary Governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260309-2003--document-skill-boundary-planning/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260309-2003--document-skill-boundary-planning/candidates.md`
- next_action: 保持在 pre-brainstorm，继续收敛 review 分流、直接修补 vs 重开、以及 worktree 续用/新建的统一 gate
- revisit_trigger: 当 review alignment 与 loop boundary 的最小治理 contract 可以冻结成独立 issue scope 时，重新进入 materialization 判断

9. `C-20260322-0715-A`
- title: Detect and recover pre-test-merge manager acceptance stalls after delegated continuation
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://pre-test-merge-acceptance-stall-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/candidates.md`
- next_action: 保持 active candidate；先依赖测试批次治理 issue 冻结 protected-env 生命周期语义。历史文案中的 `pre-test-merge` 统一按 `test-pre-merge-*` 前缀族理解，并在真实 dogfood 中跑满 watchdog 阈值；只有 delegated continuation 已进 prompt 且超过阈值仍无新 manager continuity/decision 时，才 materialize 成独立 runtime/orchestration issue
- revisit_trigger: 当治理 issue 稳定 `test-pre-merge-*` 边界后，或真实 post-merge acceptance 再次在超过 watchdog 阈值后仍复现 delegated continuation stall 时，重新进入 issue materialization 判断

10. `C-20260323-1835-A`
- title: Detect and recover active worker delegated-continuation stalls
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://worker-delegated-continuation-active-stall-recovery-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260323-1835--worker-delegated-continuation-active-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1835--worker-delegated-continuation-active-stall-recovery/candidates.md`
- next_action: 保持 active candidate；先让 manager watchdog 能识别并恢复 active worker delegated-continuation stall，再继续真实 dogfood 验证 retained worker 能否自动收口、cleanup 并回到 next patrol
- revisit_trigger: 当再次复现 active worker 已收到 delegated continuation 但 cycle log / closeout 长时间不推进，或当前 runtime 补丁验证稳定后需要冻结独立 issue contract 时，重新进入 materialization 判断

### committed_issues

### candidate_issues

8. `C-20260319-0018-B`
- title: session evidence references as fallback, not prompt payload
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/candidates.md`
- next_action: Keep this supporting candidate visible while the same-family continuity owner narrows the fallback-reference contract.
- revisit_trigger: Revisit when the owner issue either absorbs the fallback-reference contract explicitly or proves it unnecessary as a separate candidate.

9. `C-20260319-1105-A`
- title: 三层循环能力映射、owner 边界与生命周期真源收敛
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先验证 `docs/system/workspace/three-loop-capability-lifecycle.md` 是否足以成为唯一细节真源；若仍需更多行为约束，再 materialize 为独立 IBM issue，而不是继续把细节散落到 `CONSTITUTION`、`PROJECT_INTENT` 和多个 skills 中
- revisit_trigger: 当 lifecycle 真源之外仍出现新的行为约束必须落到独立 issue，或 manager/doc/dev-loop 继续出现无法由当前真源解释的冲突时，重新进入 materialization 判断
11. `C-20260320-0252-A`
- title: Signal restart-point routing across interruption, review, test, and recovery
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://restart-point-routing-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/candidates.md`
- next_action: M1-M3 的 interruption 最小 slice 已落盘：主管 triage 已改成抽象 routing contract，且 `cleanup` followthrough 已形成第一条完整 event 链。下一步继续 pre-brainstorm，把同一 contract 扩到 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan，再决定是否 materialize 为统一 routing issue
- revisit_trigger: 当 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan 已共享同一 restart-point routing contract 时，重新进入 materialization 判断

12. `C-20260320-0908-A`
- title: Unresolved research candidate persistence and revisit governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先把“不能收口时必须显式保持在 candidate/blocked 队列并写清重启条件”的规则写入 lifecycle、lead prompt 与 doc-loop reference，再决定是否 materialize 为独立治理 issue
- revisit_trigger: 当后续 worktree 审查再次发现 unresolved candidate 仍会在队列层被跳过，或当前规则需要更强的 issue-bound enforcement 时，重新进入 materialization 判断
13. `C-20260320-0605-A`
- title: Agent state time-machine and shared continuity control plane
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://state-snapshot-fork-and-shared-continuity-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0605--agent-state-time-machine-and-shared-continuity/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0605--agent-state-time-machine-and-shared-continuity/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结四个边界：Freely 当前哪些关键状态不在 Git/worktree 治理内、哪些状态必须一起 snapshot/rollback、共享连续性与 worker 私有状态如何分层、以及最小实现是否应先从本地 snapshot index / continuity metadata 开始；在这些边界稳定前不要把 PGFS 或 PostgreSQL 直接定成默认架构
- revisit_trigger: 当 Freely 的多设备或多人协作场景需要统一共享连续性控制面，且本地 snapshot index 方案边界稳定后，再进入 IBM。

14. `C-20260325-0333-A`
- title: Testing evidence ladder and real-environment gates for Freely
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://testing-evidence-ladder-and-real-environment-gates`
- source_brainstorm: `docs/pre-brainstorms/20260325-0333--testing-evidence-ladder-and-real-environment-gates/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260325-0333--testing-evidence-ladder-and-real-environment-gates/candidates.md`
- next_action: Keep the umbrella candidate visible while the first story-level `pre-tests.md` quality gate owner closes, then choose the next testing slice.
- revisit_trigger: Revisit once `C-20260325-0333-B` closes and writes back whether the next slice should be evidence ladder mapping, real-environment harness, or another testing governance cut.

15. `C-20260331-1837-A`
- title: Worker first-hop role boundary regression in prompt generation and follow-on reentry
- milestone_state: candidate
- phase_state: `needs_research`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260331-1837--worker-first-hop-role-boundary-regression/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260331-1837--worker-first-hop-role-boundary-regression/candidates.md`
- next_action: Trace the worker prompt-generation path and the worker follow-on relaunch path together, then decide whether this becomes one focused repair issue or two narrower runtime-facing fixes.
- revisit_trigger: Revisit immediately if another worker lane writes manager-only artifacts, performs project-level patrol after delegated completion, or `MANAGER_MODE=false` prompts still enter `lead-agent` without a worker-only second hop boundary.

16. `C-20260402-0020-A`
- title: Hook bypass break-glass governance
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0020--hook-bypass-breakglass-governance/candidates.md`
- next_action: Candidate is already materialized as `I-20260402-0020-A`; keep this mirror only for source traceability and route execution from the issue/progress pair.
- revisit_trigger: Revisit immediately if protected-branch work uses `--no-verify` again, if a gate false negative again leaves no canonical bypass receipt, or if merge conflict completion still falls back to raw `git commit`.

17. `C-20260402-1912-A`
- title: Protected-branch merge receipt hardening
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-1912--protected-branch-merge-receipt-hardening/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-1912--protected-branch-merge-receipt-hardening/candidates.md`
- next_action: Candidate is already materialized as `I-20260402-1912-A`; keep this mirror only for source traceability and route execution from the issue/progress pair.
- revisit_trigger: Revisit immediately if protected-branch completion semantics are widened beyond merge-completion-only, if receipt trailer and ledger truth drift apart, or if root `develop` again accumulates unowned merge-governance hardening.

18. `C-20260405-0425-A`
- title: Develop guarded merge entrypoint enforcement
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-0425--develop-guarded-merge-entrypoint-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-0425--develop-guarded-merge-entrypoint-enforcement/candidates.md`
- next_action: Candidate is already materialized as `I-20260405-0425-A`; keep this mirror only for source traceability and route execution from the issue/progress pair.
- revisit_trigger: Revisit immediately if raw `git merge` on `develop` still reaches a merge commit without canonical guarded state, or if entrypoint enforcement suppresses governance/promotion gates after handshake validation.

### committed_issues

### completed_issues

1. `I-20260405-0425-A`
- title: Develop guarded merge entrypoint enforcement governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-develop-guarded-merge-entrypoint-enforcement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-0425--develop-guarded-merge-entrypoint-enforcement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-0425--develop-guarded-merge-entrypoint-enforcement/candidates.md`
- evidence:
  - `develop` commit `f1965d3`
  - `docs/progress/workspace-routing-foundation/p-develop-guarded-merge-entrypoint-enforcement-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews/20260405-develop-guarded-merge-entrypoint-enforcement-verification.md`
  - `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews/20260405-develop-guarded-merge-entrypoint-canonical-closeout-verification.md`
- completion_note: canonical `develop` now enforces `./bin/merge-guarded` as the required merge entrypoint; later expansion to other protected branch families should reopen as a narrower follow-on.

2. `I-20260402-1912-A`
- title: Protected-branch merge receipt hardening
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-hardening.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-1912--protected-branch-merge-receipt-hardening/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-1912--protected-branch-merge-receipt-hardening/candidates.md`
- completion_note: protected-branch merge receipt hardening is absorbed on canonical `develop`; any later receipt gap beyond parity audit, guarded completion handshake hardening, or the frozen staged merge-gate boundary must reopen as a narrower follow-on.

2. `I-20260323-1705-A`
- title: Manager delegated continuation stall recovery governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-delegated-continuation-stall-recovery-governance/issues/manager-delegated-continuation-stall-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/candidates.md`, `docs/pre-brainstorms/20260328-0154--manager-stall-reentry-false-positive-supervision-thrash/candidates.md`
- evidence:
  - `develop` commit `ce17a17`
  - `docs/progress/workspace-routing-foundation/p-manager-delegated-continuation-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegated-continuation-stall-recovery-governance/code-reviews/20260328-manager-delegated-continuation-stall-recovery-verification.md`
- completion_note: manager delegated continuation stall recovery 的 idle-safe repair 已进入主线；older continuity、stale runtime refs、missing prompt target 不再把坏态伪装成 lawful wait，stale queued worker prompts 也会重新回到 launchable recovery。

2. `I-20260401-1035-A`
- title: Materialize develop push-pending governance after protected-branch merge
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/develop-push-pending-guard-governance/issues/develop-push-pending-guard-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1035--develop-push-pending-guard-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1035--develop-push-pending-guard-governance/candidates.md`
- evidence:
  - `develop` commits `08fb096`, `8feae13`, `11f310b`
  - `docs/progress/workspace-routing-foundation/p-develop-push-pending-guard-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-push-pending-guard-governance/code-reviews/20260401-develop-push-pending-guard-verification.md`
- completion_note: develop push followthrough truth 已进入 canonical status/patrol surfaces；`push_pending` / `push_deferred` 现在是显式 machine-readable state，而不是 merge 之后的隐式本地遗忘窗口。
- revisit_trigger: Re-open candidate-level research only if `develop`-scoped push debt proves too narrow and the state model must expand to other protected branch families.

3. `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`, `docs/progress/workspace-routing-foundation/p-cli-first-entrypoint-and-observability-surface-unification.md`, `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
- cleanup_gate: `merged-pending-verify`
- branch: `feature/cli-first-observability-surfaces-20260322`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-cli-first-observability-surfaces`
- local_branch_disposition: `retained-with-reason`
- remote_branch_disposition: `deleted`
- completion_note: issue 实现能力已被 `develop` 吸收，当前 feature branch 也已 rebase 到最新 `develop` 之上，但 branch tip 仍保留未被主线吸收的 canonical closure writeback。`2026-03-22` 的 post-merge acceptance 再次确认：milestone 队列已经保持 canonical `completed_issues`，远程同名 branch 仍不存在，但 `git rev-list --left-right --count feature/cli-first-observability-surfaces-20260322...develop` 仍为 `3 0`，因此当前 disposition 继续是 `retire-only`，cleanup gate 只能保持 `merged-pending-verify`；先把这些收口提交吸收到 canonical `develop`，再由 supervisor/runtime 在 worktree 外执行最终 branch/worktree 删除。

4. `I-20260321-1925`
- title: Manager chat reentry and cleanup misrouting governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/interruption-manager-handler`, `docs/system/workspace/scripts/tests/test-interruption-manager-handler`, `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`, `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/code-reviews/20260321-manager-chat-reentry-and-cleanup-misrouting-verification.md`
- completion_note: broad supervisor chat signal 已不再默认误落 cleanup followthrough；纯 cleanup 请求仍保持 worker cleanup 路径，主管级广义巡检请求则回到 `handoff://continuation` 与 manager ownership

5. `I-20260322-0049`
- title: Manager continuation handoff consumption governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/candidates.md`
- evidence: `docs/progress/workspace-routing-foundation/p-manager-continuation-handoff-consumption-governance.md`, `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/code-reviews/20260322-manager-continuation-handoff-consumption-verification.md`, `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/code-reviews/20260322-manager-continuation-handoff-consumption-cleanup-verification.md`
- completion_note: 当前 worktree 已确认 `retire-only`，历史 anomaly 仅保留追溯语义，不再 materialize 新实现 scope；milestone 队列已纠正到 `completed_issues`。fresh session after `context_compacted` 已再次复核 canonical closeout，结论未变：当前分支还保留一个已被 `feature/completed-worktree-closeout-merge-prep-20260322` 吸收的 cleanup/closure 提交且无远程同名分支；本地 branch/worktree 删除应走 closeout chain，而不是重新打开本 issue 的实现范围

6. `I-20260322-0245`
- title: Runtime worker launch linkage and stall recovery governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/runtime/manager-watchdog.sh`, `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`, `docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`, `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/code-reviews/20260322-runtime-worker-launch-linkage-and-stall-recovery-verification.md`
- completion_note: manager-generated worker handoff 已可直接转成 target worker continuation launch，stall recovery 也已进入 runtime-owned 控制面；当前 issue 已完成 verification closure，本轮 canonical writeback 固化后工位会恢复 clean，但本地 docs-only closure commits 仍待经 develop-facing 路径吸收，因此 cleanup gate 继续为 `retained-with-reason`

7. `I-20260321-2010`
- title: Explicit session-addressed resume governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/runtime/tool-launchers.sh`, `docs/system/workspace/scripts/monitor-ai-cli.sh`, `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`, `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/code-reviews/20260321-explicit-session-addressed-resume-verification.md`
- completion_note: 显式 session-addressed resume 已成为 Freely 的 canonical continuity model；`codex` 默认路径不再依赖 `--last`，worker-scoped target evidence 与 preemption fallback 也已闭环

8. `I-20260321-1715`
- title: Manager watchdog trigger and drift reconcile governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/candidates.md`, `docs/pre-brainstorms/20260321-1430--external-drift-and-out-of-band-reconcile/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-watchdog-trigger-and-drift-reconcile-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/code-reviews/20260321-manager-watchdog-trigger-and-drift-reconcile-verification.md`
  - `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/code-reviews/20260326-manager-watchdog-trigger-and-drift-reconcile-canonical-replay-verification.md`
- completion_note: cleanup reroute contract 已在 canonical `develop` 通过 replay，cleanup-only signal 保持 `handoff://cleanup`，broad supervisor signal 保持 manager-owned continuation reentry；authoritative fleet truth 也已稳定到 4-tree / dirty=0 / all stopped。scheduler retained research owner 继续独立保留，不并入本条完成判断

7. `I-20260328-0335-A`
- title: Manager supervision quiet-period stall-signal governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/issues/manager-supervision-quiet-period-stall-signal-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260328-0335--operator-stop-runtime-stall-recovery-semantics/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260328-0335--operator-stop-runtime-stall-recovery-semantics/candidates.md`
- evidence:
  - `develop` commit `82ea1e6`
  - `docs/progress/workspace-routing-foundation/p-manager-supervision-quiet-period-stall-signal-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/code-reviews/20260328-manager-supervision-quiet-period-stall-signal-verification.md`
- completion_note: quiet-period false-positive stall recovery 的最小行为修复已完成；restart-storm 与 observability 区分留作 follow-on。

4. `I-20260321-1706`
- title: Chat-triggered worker runtime reactivation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1706--chat-triggered-worker-runtime-reactivation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1706--chat-triggered-worker-runtime-reactivation/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`, `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/code-reviews/20260321-chat-triggered-worker-runtime-reactivation-verification.md`
- completion_note: worker 工位在 `operator_stop` 后的 `freely chat` 现在会通过 delegated handoff gate 重新拉起本工位主循环；脚本级与真实狗粮验证均已通过

5. `I-20260319-1715`
- title: CLI-first human chat intake and manager delegation loop
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`, `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/code-reviews/20260320-human-chat-intake-and-manager-delegation-verification.md`, `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- completion_note: CLI-first human chat intake、manager queue scanning、claim/resolve/absorption writeback 与专项测试已闭环；companion canonical 分支已挂起，不再阻塞主线完成

6. `I-20260319-2315`
- title: CLI TUI interruption input box for Freely
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-tui-human-interruption-input/issues/cli-tui-human-interruption-input.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- completion_note: `freely tui` 已收口为 interruption presentation shell，并补齐中文与多行提交回归，输入仍统一落到既有 durable intake 链路

7. `I-20260320-1405`
- title: Worktree maintenance governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-1410--worktree-maintenance-skill-taxonomy/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-1410--worktree-maintenance-skill-taxonomy/candidates.md`
- evidence: `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`, `docs/system/workspace/agents/lead-agent.md`, `docs/system/workspace/agents/manager-agent.md`, `docs/system/workspace/scripts/start-lead-agent.sh`, `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- completion_note: 已把 worktree 创建后的维护能力收敛成专门 skill，明确 `audit / merge_prep / retirement_handoff` 三种模式，并接入主管真源与首跳测试

8. `I-20260318-1222`
- title: Mem9 shared memory evaluation for Freely continuity plane
- milestone_state: completed
- phase_state: `completed`
- priority: P2
- issue_path: `docs/epics/workspace-routing-foundation/mem9-continuity-bridge/issues/mem9-continuity-bridge.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1222--mem9-shared-memory-fit-for-freely/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1222--mem9-shared-memory-fit-for-freely/candidates.md`
- completion_note: mem9 已明确收束为可选连续性增强层，不是 Freely 的治理真源；对应边界已 materialize 为 `skill:mem9-continuity-bridge`，并保持本地治理事实源优先

9. `C-20260306-1101`
- title: `lead-agent.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/lead-agent-bootstrap.md`
- evidence: `docs/system/workspace/agents/lead-agent.md`
- completion_note: 已落地首跳中枢代理职责与首跳协议

10. `C-20260306-1102`
- title: `context-source-skill.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/context-source-skill-bootstrap.md`
- evidence: `docs/system/workspace/skills/context-source-skill/SKILL.md`
- completion_note: 已落地来源判定、milestone 扫描与 usable issue 决策规则

5. `C-20260306-1103`
- title: `doc-pre-brainstorm-execution.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-pre-brainstorm-execution-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- completion_note: 已落地 docs 前置收敛环，负责 pre-brainstorm 产物与 milestone 原子同步

6. `C-20260306-1104`
- title: `doc-ibm-execution.md` 与 `dev-loop-execution.md` 的外循环接驳边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-loop-dev-loop-handoff-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已收紧 issue-bound `IBM+G` 与 `DDD` 的接驳边界，状态交换统一回流给 auto-loop

7. `C-20260306-1105`
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/auto-loop-orchestrator-bootstrap.md`
- evidence: `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`, `docs/system/workspace/scripts/README.md`, `docs/system/workspace/scripts/tests/test-routing-foundation-loop`, `docs/system/workspace/hooks/pre-commit.sh`
- completion_note: 已把 `system/workspace` 真源、`scripts` / `hooks` 与运行时投影映射写回 orchestrator，并补齐最小闭环测试

6. `I-20260308-1631`
- title: 阶段前缀式主进度标识治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/candidates.md`
- evidence: `docs/LAWS.md`, `docs/PROJECT_INTENT.md`, `docs/milestones.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已把 `phase_state` 收敛为 Freely 自举阶段的主执行标识，并统一 `done_ibm -> in_dev` handoff 与 milestone 路由口径

7. `I-20260308-1931`
- title: 业务阻塞状态与系统崩溃恢复定位治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`, `docs/milestones.md`
- completion_note: 已明确分层业务阻塞与系统崩溃恢复，禁止用 `blocked_*` 伪造系统事件交接，并统一恢复定位顺序与最小字段口径

8. `C-20260319-0220-A`
- title: Watchdog umbrella term and sub-control-plane taxonomy
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- evidence: `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`, `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`, `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`, `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- completion_note: umbrella taxonomy 已由 `watchdog-control-plane` 与现有 availability / runtime / continuity issue 主线吸收，不再单独 materialize

9. `I-20260320-0512`
- title: Milestone planning and state maintenance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/candidates.md`
- completion_note: milestone planning 与 state maintenance 已作为独立治理能力物化并验证，收口为 `completed`

11. `C-20260319-0220-C`
- title: Historical watchdog productization worktree retirement handoff
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/pre-brainstorms/CONVERGENCE.md`, `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/brainstorms.md`
- completion_note: 旧 watchdog 产品化工位的 `materialize_then_retire` handoff、cleanup 结果与 retirement heuristic 已完成留痕；该候选归档，不新开 IBM

12. `I-20260316-1801`
- title: Auto-run session lifecycle rotation and handoff governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260303-0000--cli-orchestration-architecture/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260303-0000--cli-orchestration-architecture/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/monitor-ai-cli.sh`, `docs/system/workspace/scripts/tests/test-freely-session-rotation`, `bin/test-freely-session-rotation`
- completion_note: 已把 `resume` 与 `fresh_with_handoff` 区分为显式 runtime 行为，并固定 Codex 默认模型为 `gpt-5.4`、默认 reasoning effort 为 `medium`

11. `I-20260320-0018`
- title: Default project resolution and authorized project memory for CLI-first interruption entrypoints
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0018--default-project-resolution-and-authorized-project-memory/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0018--default-project-resolution-and-authorized-project-memory/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-project-resolution-defaults`
- completion_note: 默认项目解析已由共享 runtime resolver 覆盖，并通过 cwd auto-resolution 与单一已授权项目回退回归锁定；后续如需多项目切换能力，应从新的 candidate materialize，不要继续扩大本条 completed issue
11. `I-20260320-0500`
- title: Candidate acceptance review governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0500--candidate-acceptance-review-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0500--candidate-acceptance-review-governance/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`, `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/tasks.md`, `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`, `docs/system/workspace/scripts/quality/governance-check`
- completion_note: future candidate v2 schema、独立 acceptance review、IBM acceptance deepening 与治理门禁已稳定落盘；高风险 candidate 的双审策略保留为后续治理演进，不阻塞当前 issue 完成

12. `C-20260323-2045-A`
- title: Add capacity-aware queueing for manager worker prompt sets
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260323-2045--manager-worker-scheduler-capacity-and-queueing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-2045--manager-worker-scheduler-capacity-and-queueing/candidates.md`
- evidence:
  - `AGENTS.md`
  - `docs/system/workspace/scripts/start-lead-agent.sh`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-capacity-queue`
  - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-busy-worker-queue`
  - `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- completion_note: 当前 candidate 的旧 blocker 已被 canonical `develop` 否定并吸收：dispatch metadata 已成为 runtime contract，固定 numeric launch cap 已退场，parallel-safe prompts 会直接 launch，queue 只保留给 same-lane busy、单 wave 非并行限制与 `write_scope` 冲突。后续若要继续做更强的 scheduler fairness / quota / transaction 语义，应新开 lifecycle，而不是复活这条已收口的 research。

## M-20260312-control-surface-runtime-convergence

- title: Control surface, runtime, and intervention architecture convergence
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- intent: 把跨 pre-brainstorm / 跨 feature 分支的架构结论收敛进单一里程碑，停止悬空讨论，再按 milestone 顺序创建后续专用 worktree 落 IBM 与实现；该收敛批次以前置 issue `I-20260308-1245` 的边界复评结论为基础，不替代它。
- why_now: Freely 正在吃自己的狗粮开发自己；如果架构、控制面、standalone/OpenClaw、human intervention 等候选持续分散在多个分支和 pre-brainstorm 中，auto-loop 与人工协作都会缺少统一编排入口，同时也会与现有 frontend-probe milestone 的边界复评形成重复编排。

### committed_issues

### candidate_issues

1. `C-20260312-0011-E`
- title: AI Team Control Surface and Multi-Worktree Visibility
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 待 contract 边界初步冻结后进入 IBM，定义 day-1 control surface 的信息架构、worktree visibility 和 team timeline
- revisit_trigger: 当需要设计控制面首页、多 worktree lanes 或团队态势视图时重新唤起

2. `C-20260312-0011-G`
- title: Standalone Runtime Baseline Without OpenClaw
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在引入任何外部 runtime profile 前，先把 Freely standalone mode 的最小组件、状态面和未闭合点写成正式 IBM 产物
- revisit_trigger: 当要证明 Freely 可以在不依赖 OpenClaw 的情况下独立运行时重新唤起

3. `C-20260312-0011-H`
- title: Human Intervention Transport Across Auto-Run CLIs
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在当前 `SendChatIntervention` 协议语义下，先冻结 `resume_with_intervention` 的 day-1 控制链与最小依赖字段
- revisit_trigger: 当 human interruption transport 需要正式进入 IBM 或无法继续停留在临时 transport 约定时重新唤起

4. `C-20260312-0011-B`
- title: Frontend Manifest Boundary and Runtime Capability Layering
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 contract 与 standalone 基线明确后进入 IBM，收紧 frontend/backend/AI tool/integration 的 manifest 与真源分层
- revisit_trigger: 当 manifest 分层必须落地到可执行依赖文件时重新唤起

5. `C-20260312-0011-D`
- title: Event Log and Snapshot Reconstruction Contract
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 作为 boundary contract 的补充，单独冻结 event/snapshot 的 reconstruction 语义，服务 UI、恢复和 team visibility
- revisit_trigger: 当事件日志、快照重建或恢复语义出现实现歧义时重新唤起

6. `C-20260312-0011-F`
- title: Skill-first Capability Exposure with OpenClaw Workspace Projection
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 standalone baseline 清晰后再进入 IBM，定义哪些 Freely 能力先以 skill 暴露，再映射到 OpenClaw workspace/profile
- revisit_trigger: 当需要把 Freely 能力投影到 OpenClaw workspace 或 hooks 时重新唤起

7. `C-20260312-0011-C`
- title: Runtime Independence with OpenClaw Profile as Optional Adapter
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 standalone mode 与 skill projection 明确后进入 IBM，正式定义 OpenClaw 只作为 optional adapter/profile 的边界
- revisit_trigger: 当 OpenClaw 借力边界必须被正式冻结或替换时重新唤起

### completed_issues

1. `I-20260312-0011`
- title: Backend Service Contract and Adapter Taxonomy
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/issues/backend-service-contract-and-adapter-taxonomy.md`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- evidence:
  - `docs/progress/control-surface-runtime-convergence/p-backend-service-contract-and-adapter-taxonomy.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260320-backend-service-contract-and-adapter-taxonomy-ibm-completion.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260326-backend-service-contract-and-adapter-taxonomy-canonical-verification.md`
- completion_note: contract layer 与 adapter layer 的冻结已经成为下游 frontend-probe architecture / boundary contract 的引用真源；因此本 issue 已从单纯 IBM 包提升为 canonical completion，后续 control surface、standalone runtime 与 intervention transport 直接复用该边界，不再阻塞在 `done_ibm`

2. `C-20260304-501`
- title: Freely-on-OpenClaw profile 最小落地
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/issues/backend-service-contract-and-adapter-taxonomy.md`
- source_brainstorm: `docs/pre-brainstorms/20260304-0000--openclaw-workspace-freely-feasibility/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260304-0000--openclaw-workspace-freely-feasibility/candidates.md`
- completion_note: 这条候选的独立 owner 价值已被后续架构真源吸收；当前 canonical 边界明确 OpenClaw 只是 optional adapter/profile，而不是 Freely 主定义

## M-20260326-freely-product-architecture

- title: Freely product architecture convergence
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260326-1810--freely-layered-architecture-and-tooling-topology/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1810--freely-layered-architecture-and-tooling-topology/candidates.md`
- intent: 把 Freely 自身的产品/系统分层拓扑收敛进正式 milestone，避免高层架构 issue 只有 pre-brainstorm/issue 真源而没有主动扫描入口
- why_now: `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md` 的高层分工已经通过独立 issue 写回，需要 milestone 保留同一条 canonical traceability

### committed_issues

1. `I-20260405-1235-A`
- title: Tool authorization bootstrap and post-consent materialization governance
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P1
- issue_path: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization/candidates.md`
- next_action: Keep this owner parked as the canonical IBM handoff for post-consent authorization/bootstrap semantics. Future work should open narrower follow-on owners for persisted state, per-tool repair/materialization cleanup, or adapter-specific drift rather than widening this architecture owner.

### completed_issues

1. `I-20260406-1905-A`
- title: Fresh-project bootstrap and baseline scoping followthrough governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- evidence:
  - `develop` merge `65553c9`
  - `docs/progress/freely-product-architecture/p-fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
  - `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`
  - `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
  - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
  - `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-status-family`
  - `./bin/governance-check`
  - `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1935-test-pre-merge-fresh-project-bootstrap-baseline-scoping-followthrough --issue docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
  - `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
  - `git diff --check`
- completion_note: `Canonical develop now keeps fresh-project sync-tooling bootstrap scoped to the target project, rematerializes .githooks for follow-on init, and preserves baseline/status target pinning through premerge and post-merge followthrough.`

2. `I-20260403-2041-A`
- title: Worktree tool boundary bootstrap governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-worktree-tool-boundary-bootstrap-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260403-2041--worktree-tool-boundary-bootstrap/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260403-2041--worktree-tool-boundary-bootstrap/candidates.md`
- evidence:
  - `develop` merge `eaddfc8`
  - `docs/progress/freely-product-architecture/p-worktree-tool-boundary-bootstrap-governance.md`
  - `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/code-reviews/20260403-worktree-tool-boundary-bootstrap-verification.md`
  - `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/code-reviews/20260405-worktree-tool-boundary-bootstrap-canonical-closeout-verification.md`

2. `I-20260405-2302-A`
- title: Worktree helper shell source compatibility governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/issues/worktree-helper-shell-source-compatibility-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-worktree-helper-shell-source-compatibility-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2302--worktree-helper-shell-source-compatibility/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2302--worktree-helper-shell-source-compatibility/candidates.md`
- evidence:
  - `develop` merge `3e0c8b9`
  - `docs/progress/freely-product-architecture/p-worktree-helper-shell-source-compatibility-governance.md`
  - `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/code-reviews/20260405-worktree-helper-shell-source-compatibility-verification.md`
- completion_note: `Canonical develop now preserves the documented sourced worktree helper contract in default zsh and bash, while keeping protected-branch add blocking, existing-worktree re-entry, and dated sibling naming intact.`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `bash docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`
  - `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
  - `bash docs/system/workspace/scripts/tests/test-signal-intent-handler-cc`
  - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
  - `bash docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
  - `bash docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`
  - `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
  - `git diff --check`
  - `./bin/governance-check`
- completion_note: `Canonical develop now rematerializes managed tool boundaries into sibling worktrees through sync-tooling plus standard worktree entrypoints, while keeping project root as the integration surface and reserving wrapper or launch-time boundary extension for tools that still lack a verified project-local config surface.`

2. `I-20260405-cli-output-style-A`
- title: AGENTS project entry and output style governance
- milestone_state: completed
- phase_state: `completed`
- priority: P2
- issue_path: `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-agents-cli-output-style-experiment-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1000--cli-output-conciseness-and-token-efficiency/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1000--cli-output-conciseness-and-token-efficiency/candidates.md`
- evidence:
  - `develop` merge `e79e182`
  - `docs/progress/freely-product-architecture/p-agents-cli-output-style-experiment-governance.md`
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`
  - `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/code-reviews/20260405-agents-cli-output-style-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
  - `git diff --check`
  - `./bin/governance-check`
- completion_note: `Canonical develop still treats the output-style change as a narrow AGENTS-only experiment and explicitly points at the already-existing project-level AGENTS bootstrap/read-order contract, without widening this owner into reusable capability truth.`

3. `I-20260405-1130-A`
- title: Project-level AGENTS bootstrap and management contract governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/freely-product-architecture/project-level-agents-bootstrap-and-management-contract-governance/issues/project-level-agents-bootstrap-and-management-contract-governance.md`
- progress_path: `docs/progress/freely-product-architecture/p-project-level-agents-bootstrap-and-management-contract-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1130--project-level-agents-bootstrap-and-management/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1130--project-level-agents-bootstrap-and-management/candidates.md`
- evidence:
  - `docs/progress/freely-product-architecture/p-project-level-agents-bootstrap-and-management-contract-governance.md`
  - `docs/epics/freely-product-architecture/project-level-agents-bootstrap-and-management-contract-governance/code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-governance-verification.md`
  - `docs/epics/freely-product-architecture/project-level-agents-bootstrap-and-management-contract-governance/code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-canonical-closeout-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
  - `git diff --check`
  - `./bin/governance-check`
- completion_note: `Canonical develop now treats project-level AGENTS bootstrap and management as reusable capability truth: init creates AGENTS only when missing, preserves project-owned files when present, and runtime consumption still reads the project root entrypoint before reusable workspace capability docs.`

3. `I-20260402-0403-A`
- title: Canonical product posture bootstrap reconciliation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/issues/canonical-product-posture-bootstrap-reconciliation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/candidates.md`
- evidence:
  - `develop` commit `25aed6d`
  - `develop` commit `77e1c76`
  - `docs/progress/freely-product-architecture/p-canonical-product-posture-bootstrap-reconciliation-governance.md`
  - `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/code-reviews/20260402-canonical-product-posture-bootstrap-reconciliation-governance-verification.md`
  - `./bin/freely init --project /Users/zhaoyu/Downloads/code/my-freely/freely --intent /Users/zhaoyu/Downloads/code/my-freely/freely/docs/PROJECT_INTENT.md --constitution /Users/zhaoyu/Downloads/code/my-freely/freely/docs/CONSTITUTION.md --ai codex:gpt-5.4:auto --accept-default-autonomy --force`
  - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `./bin/freely doctor --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `./bin/governance-check`
- completion_note: Canonical `develop` now matches the already-frozen autonomy posture contract: tracked `.codex/config.toml` carries `approval_policy=never`, local bootstrap proof records activation consent in managed `.freely/config.env`, canonical `live-status` and `doctor` both report an aligned execution-boundary audit, and `freely init --force` preserves the canonical sibling `freely-worktrees` root even when invoked from a feature worktree.

1. `I-20260326-1810`
- title: Freely layered architecture and tooling topology
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/freely-product-architecture/freely-layered-architecture-and-tooling-topology/issues/freely-layered-architecture-and-tooling-topology.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1810--freely-layered-architecture-and-tooling-topology/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1810--freely-layered-architecture-and-tooling-topology/candidates.md`
- evidence:
  - `docs/epics/freely-product-architecture/freely-layered-architecture-and-tooling-topology/code-reviews/20260326-freely-layered-architecture-and-tooling-topology-verification.md`
- completion_note: Freely 自身产品架构、command family、observability semantic、host shell / form factor、external AI tooling layer 与 loop/lifecycle 真源的分层职责已在高层真源中完成首轮收敛；后续若继续泛化成通用产品形态方法，必须另开 lifecycle

2. `I-20260401-2316-A`
- title: CC ACP init autonomy consent test followthrough governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/freely-product-architecture/cc-acp-init-autonomy-consent-test-followthrough-governance/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-2316--cc-acp-init-autonomy-consent-test-followthrough/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-2316--cc-acp-init-autonomy-consent-test-followthrough/candidates.md`
- evidence:
  - `develop` merge `d5b7080`
  - `docs/progress/freely-product-architecture/p-cc-acp-init-autonomy-consent-test-followthrough-governance.md`
  - `docs/epics/freely-product-architecture/cc-acp-init-autonomy-consent-test-followthrough-governance/code-reviews/20260401-cc-acp-init-autonomy-consent-test-followthrough-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `./bin/governance-check`
- completion_note: Canonical `develop` now matches the already-frozen activation-consent contract on the `cc:auto + adapter=acp` init path; this owner closed as a strict test-only followthrough without reopening runtime semantics or ACP scope.

3. `I-20260401-1303-A`
- title: Default autonomy activation consent and posture truth governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1303--freely-product-security-baseline-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1303--freely-product-security-baseline-governance/candidates.md`
- evidence:
  - `develop` commit `3f462c6`
  - `docs/progress/freely-product-architecture/p-default-autonomy-activation-consent-and-tool-policy-governance.md`
  - `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/code-reviews/20260401-default-autonomy-activation-consent-verification.md`
  - `./bin/governance-check`
- completion_note: The bounded product contract is now canonical on `develop`: Freely defaults to unattended automatic approval, activation consent is the explicit blocking posture gate, safeguard guidance remains strongly recommended but non-blocking by default, and runtime decision escalation stays AI-first rather than reverting to user step approvals.

4. `I-20260401-1303-A-2`
- title: Freely tool autonomy policy materialization governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/issues/freely-tool-autonomy-policy-materialization-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260401-1303--freely-product-security-baseline-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260401-1303--freely-product-security-baseline-governance/candidates.md`
- evidence:
  - `develop` commit `641cb55`
  - `docs/progress/freely-product-architecture/p-freely-tool-autonomy-policy-materialization-governance.md`
  - `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/code-reviews/20260401-freely-tool-autonomy-policy-materialization-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
  - `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
  - `./bin/governance-check`
- completion_note: The first tool materialization slice is now canonical on `develop`: project-local Codex posture, launch-time auto injection, and Claude/Claude-via-Codex launcher semantics are explicitly separated from the higher-level product contract instead of remaining an implicit split.

### candidate_issues

1. `C-20260405-cli-output-style`
- title: CLI Output Style Optimization
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P2
- promoted_issue_path: `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1000--cli-output-conciseness-and-token-efficiency/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1000--cli-output-conciseness-and-token-efficiency/candidates.md`
- next_action: This candidate is now materialized as `I-20260405-cli-output-style-A`. Keep the owner narrow: the current change freezes an `AGENTS.md` experiment for developer-facing CLI/chat output while also documenting the already-existing project-level `AGENTS.md` generation/consumption contract; it does not introduce a new Freely capability.
- revisit_trigger: Re-open only if the AGENTS-only experiment proves insufficient or later needs to become a higher-priority canonical product/capability contract.

2. `C-20260405-1130-A`
- title: Project-level AGENTS bootstrap and management contract
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/freely-product-architecture/project-level-agents-bootstrap-and-management-contract-governance/issues/project-level-agents-bootstrap-and-management-contract-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1130--project-level-agents-bootstrap-and-management/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1130--project-level-agents-bootstrap-and-management/candidates.md`
- next_action: This candidate is now materialized as `I-20260405-1130-A`. Keep the first slice narrow: freeze the reusable project-level AGENTS contract, add preserve-existing-AGENTS coverage, and document the self-hosting boundary without widening into richer template customization.
- revisit_trigger: Re-open only if the first capability-contract slice proves insufficient or future project template management needs a broader product/capability split.

3. `C-20260405-1235-A`
- title: Tool authorization bootstrap and post-consent materialization contract
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization/candidates.md`
- next_action: This candidate is now materialized as `I-20260405-1235-A`. Keep the owner documentation-first: freeze the layer split, per-tool matrix, degradation semantics, and backend contract boundary before opening narrower implementation follow-ons.
- revisit_trigger: Re-open only if the IBM slice proves too broad, overlaps older owners, or new tool surfaces require a separate owner family instead of a follow-on implementation lane.

4. `C-20260405-2358-A`
- title: Fresh-project bootstrap and baseline scoping followthrough after CLI audit
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P1
- promoted_issue_path: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260405-2358--cli-command-audit-regressions/candidates.md`
- next_action: This candidate is now materialized as `I-20260406-1905-A`. Keep the owner narrow: repair `sync-tooling` retargeting plus `.githooks` rematerialization, prove `baseline-status` / `status --view baseline` stay pinned to the target project, and keep `ensure-interruption-dispatch` as a non-regression guard rather than reopening runtime control-plane work.
- revisit_trigger: Revisit if fresh-project bootstrap still requires manual `.githooks` copying, baseline/status scoping still drifts from the target project, or another project-targeted CLI command regresses the current doc-gate semantics.

- none right now; the 20260401-1303 product-security candidate is now closed across `I-20260401-1303-A` and `I-20260401-1303-A-2`, while reusable security-capability follow-ons continue as separate owners instead of being carried implicitly inside this completed split.
  - `I-20260401-2245-A` owns build artifact exposure and release allowlist audit.
  - `I-20260401-0115-A` owns supply-chain baseline and install-intake audit.
  - `I-20260402-0403-A` owns the narrower canonical repo bootstrap reconciliation follow-on for already-completed autonomy/consent posture truth.

## M-20260308-frontend-probe-dogfooding-loop

- title: Frontend probe + backend increment dogfooding loop
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- intent: 把“backend-core-first + frontend-probe-from-day-1”收敛为 Freely 自举开发自己的正式候选批次，避免继续只有后端结论、没有产品面验证闭环
- why_now: Freely 的目标本身就是防止 AI 跑偏；如果自举开发中每个后端增量都不能立刻被前端观察、打断和回放，狗粮链路仍然不完整

### committed_issues

1. `I-20260317-1003`
- title: Incremental Dogfooding Gate for Backend Increments
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/issues/incremental-dogfooding-gate-for-backend-increments.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: 这条验证门禁先保持 parked completed-IBM owner，作为后续 backend increment review gate 复用；当前不需要单独挂住 research worktree。等活跃 `in_dev` 主线逼近该成本窗口时，再决定是否补 canonical closeout 或 issue-bound continuation。

### candidate_issues

1. `C-20260304-202`
- title: 多项目 UI 隔离规则实现
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260304-0000--architecture-backend-first-and-frontend-decoupling/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260304-0000--architecture-backend-first-and-frontend-decoupling/candidates.md`
- next_action: 继续 pre-brainstorm，先判断 frontend probe 当前是否需要真正的多项目工作台，再决定是否 materialize
- revisit_trigger: 当 frontend/control-surface 确认需要 `activeProject` 隔离、Focus/Overview 与项目级输入隔离 contract 时，重新进入 materialization 判断

2. `C-20260317-1101`
- title: Frontend Runtime Baseline for Probe
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- next_action: 已提升为独立 issue，且其 absorption closeout 已由 `I-20260317-1004` 写回 completed；此处只保留 candidate provenance

### completed_issues

1. `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-internal-frontend-backend-architecture-review.md`
  - `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/code-reviews/20260326-internal-frontend-backend-architecture-canonical-verification.md`
- completion_note: frontend/backend 总体边界、状态归属矩阵、协议分层、输入仲裁与 MVP autonomy milestone 已被下游 boundary contract 与 control-surface issue 直接复用，故本 issue 已完成 canonical closeout；后续 probe / bridge / runtime 实现沿该边界推进，不再回灌为总论争议

2. `I-20260317-1001`
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/code-reviews/20260326-frontend-backend-boundary-contract-v1-canonical-verification.md`
- completion_note: Probe day-1 boundary contract 已冻结到 object family、error surface、ordering 与 adapter compatibility 字段面，并被 `frontend-probe-v0` 与 `rust-tauri-probe-bridge-v1` 直接复用；因此本 issue 已完成 canonical closeout，后续真实宿主与 bridge 联调留给 active `in_dev` 主线承接

3. `I-20260317-0332`
- title: Rust/Tauri Probe Bridge v1
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-rust-tauri-probe-bridge-v1.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/code-reviews/20260401-rust-tauri-probe-bridge-host-validation-verification.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/code-reviews/20260401-rust-tauri-probe-bridge-real-interaction-verification.md`
- completion_note: Rust/Tauri Probe bridge 的 day-1 contract、真实宿主启动验证、以及真实 `Transport=tauri` 下的最小 `start -> create/resume session -> chat intervention` 闭环已写成 live evidence 并随实现吸收到 `develop`；其 day-1 下游 frontend host integration / UX 收口随后也已由 `I-20260308-1244-03` 完成，bridge beyond day-1 subset 若需扩展则另开 lifecycle

4. `I-20260308-1244-03`
- title: Frontend Probe v0
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-frontend-probe-v0.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/code-reviews/20260401-frontend-probe-v0-terminal-attach-validation.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/code-reviews/20260402-frontend-probe-v0-closeout-verification.md`
- completion_note: Frontend Probe v0 的 day-1 product surface、真实 `Transport=tauri` 下的 `start -> create/resume session -> attach terminal -> chat intervention` 闭环、以及 Recent Activity 的本地时区显示层都已吸收到 `develop`；后续更宽的 frontend UX、multi-project shell 与复用 gate enforcement 若需推进，另开 lifecycle

5. `I-20260317-1004`
- title: Frontend Runtime Baseline for Probe
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- evidence:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/code-reviews/20260402-frontend-runtime-baseline-for-probe-absorption-verification.md`
- completion_note: frontend host entry、renderer mount、runtime injection 与最小 build/test baseline 已被 `frontend-probe-v0` 和 `rust-tauri-probe-bridge-v1` 的真实 develop 实现吸收，因此本 owner 不再作为 parked committed issue 保留；若未来再出现新的宿主/runtime 基线缺口，另开 lifecycle


## M-20260318-url-content-intake-skill-and-wechat-fetch-governance

- status: completed
- linked_issue: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- intent: 把公众号链接抓取研究转成可分享的 skill、脚本和最小测试
- why_now: 研究已经证明本地浏览器 UA 抓取可行；如果不把脚本放进 skill，分享 skill 时能力仍然是不完整的

### committed_issues

- none currently

### candidate_issues

- none currently

### completed_issues

1. `I-20260318-1246`
- title: URL 内容摄取 skill 与微信公众号抓取治理
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/candidates.md`
- evidence:
  - `develop` commits `fb1044f`, `232b273`
  - `docs/progress/workspace-routing-foundation/p-url-content-intake-skill-and-wechat-fetch-governance.md`
  - `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/code-reviews/20260401-url-content-intake-skill-verification.md`
- completion_note: `url-content-intake` skill 已在 canonical `develop` 提供 bundled fetch/extract scripts 与最小回归，微信公众号与通用 HTTP(S) URL 的 bounded intake contract 已 materialize；更广的 URL routing/browser fallback 另开 lifecycle。

- none currently

## M-20260321-ai-native-doc-loop

- title: AI-native doc-loop artifacts for Freely
- status: active
- linked_issue: `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/candidates.md`
- intent: 把“AI 时代的 PRD 应该是什么”从 chat 讨论收敛为 Freely 自己可执行的 IBM 产物
- why_now: Freely 自己的 `prd.md` 还偏向人类摘要，而用户已经明确提出要在 Freely 流程里回答“AI 生成 PRD 应该长什么样”；如果不先给出 canonical 结构，后续 doc-loop 仍会沿用旧范式

### committed_issues

- none currently

### completed_issues

1. `I-20260321-1530`
- title: Agent-ready PRD architecture for Freely IBM flow
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/candidates.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`, `docs/system/workspace/scripts/quality/governance-check`, `docs/system/workspace/scripts/tests/test-doc-ibm-prd-quality-bar`
- completion_note: 已把 AI-ready PRD 的最小质量门槛接入 `doc-ibm-execution` 真源，并补齐 governance-check 与回归测试，确保 IBM 产物中的 `prd.md` 不再只停留在人类摘要

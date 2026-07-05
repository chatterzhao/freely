# Candidates - 20260410-1835--codex-limit-triggered-slot-recovery-and-real-bin-ai-verification

## Context
- Source brainstorm: `docs/B1-docs/raw-20260410-1835/brainstorms.md`
- Status: promoted
- Reopens: `I-20260407-0023-A` and the surrounding Codex switch/recovery lineage through a new bounded follow-on owner

## Candidates

### C-20260410-1835-B
- candidate_format_version: `v2`
- title: Codex real exec switch and after-failure recovery governance
- problem: `freely start` and related Codex switch surfaces were still mixing inventory truth, manual sweep semantics, and after-failure recovery semantics. That left real limit/network failures able to stall on the failed current slot, let `status` mutate auth unexpectedly, and kept the command surface insufficiently verified against real `bin/ai` and `freely start` execution.
- why_now: Dogfooding with a real limited slot proved the runtime path and command surface had to be tightened to `codex exec` truth and validated with real commands, not URL/OAuth-only evidence.
- acceptance_criteria:
  - `freely start` uses the current slot directly, then after a real failure skips the failed current slot and stops at the first later usable slot
  - Manual `bin/ai switch codex` keeps full-sweep semantics and does not blindly skip the current slot
  - Network/certificate failures during slot testing kill the current test child quickly and advance to the next saved slot
  - Real `bin/ai xx` command-surface verification and bad-slot startup recovery are executed and restored on a dedicated feature worktree
- fix_approach: Make real `codex exec` the primary runtime truth across switch/start/watchdog paths, separate manual sweep from after-failure recovery semantics, kill slot-test children promptly on slot-local network failures, and replay both focused regressions and real command-surface validation.
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260410-1835-B`
- promoted_issue_path: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/issues/codex-real-exec-switch-and-after-failure-recovery-governance.md`
- source_brainstorm: `docs/B1-docs/raw-20260410-1835/brainstorms.md`
- session_refs: []
- next_action: Land the bounded follow-on owner with real command-surface evidence, then merge through `test-pre-merge-20260410-codex-switch-real-env`.

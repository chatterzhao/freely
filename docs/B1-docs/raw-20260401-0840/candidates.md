# 候选：all-tools-unified-slot-contract-governance

- id: `C-20260401-0840-A`
- candidate_format_version: `v2`
- title: Materialize unified slot contract across all runtime tools
- source_brainstorm: `docs/B1-docs/raw-20260401-0840/brainstorms.md`
- problem: Freely now has ordered cross-tool fallback, but same-tool slot recovery truth is still effectively Codex-specific. As a result, runtime state mixes `current` and `last` semantics, non-Codex tools cannot participate in a uniform slot-first scheduler, and the final contract requested by users remains unmaterialized.
- why_now:
  - `I-20260331-1840-A` already restored ordered cross-tool fallback and explicit waiting truth, but it intentionally stopped short of all-tools slot parity.
  - current docs and code still overstate generic availability-manager scope while the implementation truth remains Codex-heavy.
  - the next capability slice is no longer “whether fallback exists”, but “whether every tool can enter the same slot-first scheduler model”.
- acceptance_criteria:
  - freeze `~/.ai-auth/<tool>-<slot>/` as the canonical slot inventory contract for every tool
  - introduce runtime truth that distinguishes current tool/current slot from last-successful history
  - make same-tool slot sweep generic: whenever a tool has slot inventory and auto-slot is enabled, manager recovery must attempt that tool's slots before cross-tool fallback
  - preserve `codex` probe-first / switch-lock / no-launch invariants instead of weakening them to match weaker tools
  - when a tool lacks mature probe parity, keep that capability gap explicit but still let it participate in unified slot inventory and current-slot state
  - when all tools and all slots are unavailable, pin the earliest-known recovery target as `tool + slot`, not just tool
- promotion_gate:
  - close `I-20260331-1840-A` as the v1 ordered-fallback slice instead of silently widening it post hoc
  - keep generic slot inventory truth separate from per-tool readiness/probe parity
  - do not claim cross-tool resume equivalence
  - prove at least one live chain where current tool fails, Codex current slot is dead, and manager still reaches a usable later slot before relaunch
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - close the old multi-tool owner as v1
  - establish generic slot inventory/current-slot truth for all tools
  - implement slot-first scheduler semantics across tool boundaries
  - keep Codex-specific watchdog strength without forcing fake parity on weaker tools
- next_action:
  - materialize a new owner that narrows old v1 scope and carries forward the final all-tools slot-first acceptance contract
- revisit_trigger:
  - revisit only if a stronger persistent config schema or per-tool auth material format is required beyond the generic slot inventory API

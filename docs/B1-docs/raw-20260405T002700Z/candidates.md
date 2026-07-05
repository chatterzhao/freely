# Candidates - 20260405-0027--codex-apikey-slot-bundle-and-provider-aware-probe

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260405T002700Z-A: legacy issue
- candidate_format_version: `v2`
- title: Codex API-key slot bundle and provider-aware probe governance
- problem: Freely currently saves and switches Codex slots as if `auth.json` were the only live truth. That model breaks for real API-key/provider usage where slot usability depends on both `auth.json` and `config.toml`, including provider-scoped `base_url`, auth mode, and provider selection.
- why_now: Dogfooding has already reached a state where local Codex auth is API-key based rather than ChatGPT-account based, and the user explicitly wants API keys to become first-class saved slots compatible with `switch`, `login`, and `delete`, while preserving Freely's existing auto-check-and-auto-switch behavior.
- acceptance_criteria:
  - the slot-bundle filesystem shape and manifest vocabulary remain reusable across all supported tools rather than becoming a Codex-only special case
  - generic slot commands (`login/save/switch/delete/status/list`) are separated from per-tool live materialization/probe adapters
  - the research explicitly decides whether Freely should keep those adapters in-process long term or stage them toward a standalone CLI-first backend
  - Codex supports kind-prefixed saved slot ids under the existing inventory root, at minimum `account-*` and `apikey-*`
  - API-key slots store enough slot-local truth to restore provider behavior without relying on one mutable global singleton config
  - cross-kind switch semantics are frozen for `account -> apikey` and `apikey -> account`
  - live materialization treats `~/.codex/auth.json` and `~/.codex/config.toml` as one atomic pair
  - Codex probe selection is frozen by slot kind: `account-*` may keep the current OAuth inventory path, while `apikey-*` must use the existing non-interactive `codex exec` probe path rather than the OAuth/curl sweep
  - probe/status truth distinguishes auth, quota, endpoint, network, and config failures rather than treating copy-success as usability
- promotion_gate:
  - keep the owner scoped to Codex runtime slot bundle/probe/switch behavior rather than reopening global slot scheduler semantics
  - define how non-Codex tools reuse the generic slot bundle vocabulary without claiming false probe parity
  - freeze a per-tool capability tier table so inventory-only tools do not masquerade as switchable/probeable
  - decide whether `ai-switch-cli` should become the long-term tool auth/switch backend for Freely, and if so, what stays in Freely versus moves out
  - define the abstraction boundary between generic slot inventory semantics and per-tool live file mutation
  - preserve compatibility with the canonical inventory root `~/.ai-auth/<tool>-<slot>/`
  - define how legacy unprefixed Codex slots are interpreted or lazily migrated
  - define the minimum write-preserving TOML mutation rule so unrelated sections are not damaged
  - keep `cc-switch` as reference evidence only, not as Freely architecture or UX scope
- open_questions:
  - should the first API-key slice support both `auth.json`-backed keys and `env_key`-backed providers, or stage them separately behind one bundle contract
  - what is the minimum provider-aware lightweight probe that gives reliable classification without needing a full Codex launch
  - should `login codex` remain account-only while API-key onboarding enters through `save`/`add`, or is an explicit `--auth-mode apikey` path worth adding in the first slice
  - when switching back to `account-*`, do we restore a saved account config slice or clear only the API-key-specific provider overrides
  - should `apikey-*` inventory truth always use `codex exec hi`, or is there a later provider-specific lower-cost probe worth adding once correctness is proven
  - which non-Codex tools can be promoted immediately to `switchable` based on verified live config surfaces (`iflow`, `opencode`) versus staying `inventory_only` (`cc`, `cc-use-codex-cli`, `kiro-cli`)
  - for Codex account slots, is an explicit saved `config-auth.toml` fragment required from day 1, or can the first slice represent account-mode restore as a targeted clear/set rule plus optional fragment
  - at what maturity point should the tool-specific adapter layer be extracted into standalone `ai-switch-cli`, and should Freely `init` prefer that backend when installed
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The architecture boundary is stable. This now needs a narrower runtime owner rather than more architecture wording. The owner should stay Codex-specific and provider-aware, not reopen completed all-tools slot or OAuth sweep owners.`
    verdict: `ready_for_ibm`
- priority: P1
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason: The remaining work is no longer "should Freely support this" but "what exact runtime contract should land first without breaking the existing slot scheduler". That is a separate implementation owner family under workspace routing/runtime capability, not a continuation of the architecture-only bootstrap owner.
- decision_reason: The slot-bundle shape should be generic enough for `codex`, `cc`, `opencode`, `iflow`, and other supported tools, but Codex remains the first stronger slice because it has the clearest official auth/config/provider surfaces and existing watchdog truth.
- decision_reason: Generic command compatibility does not imply equal runtime maturity; the first slice should explicitly preserve weaker non-Codex tools as `inventory_only` or `switchable` until verified probe/materialization adapters exist.
- promoted_issue_path: `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- next_action: Candidate mirror only. `I-20260405T002700Z-A` is now the canonical completed owner for the Codex auth+config bundle contract; future work should route through a new follow-on owner rather than reopening candidate-stage IBM.
- revisit_trigger: Revisit if another existing owner absorbs the full `auth+config bundle` contract, or if official Codex auth/provider semantics change enough to invalidate the proposed slot-kind split.
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`

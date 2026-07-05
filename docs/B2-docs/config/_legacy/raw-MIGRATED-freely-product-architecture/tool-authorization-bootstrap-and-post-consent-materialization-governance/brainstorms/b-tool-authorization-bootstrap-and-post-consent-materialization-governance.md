# IBM Brainstorm: tool-authorization-bootstrap-and-post-consent-materialization-governance

## Focus

Freeze the first product-architecture contract for project authorization bootstrap after user consent, without pretending all tools now have full auto-managed trust/config parity.

## Narrowing Decisions

1. Keep activation consent as an existing sibling truth; this owner only defines the next layer after that consent exists.
2. Treat authorization bootstrap as backend contract truth reused by CLI, TUI, GUI, and future settings mutation.
3. Require a per-tool matrix before implementation so launch-time injection is not mislabeled as persistent authorization.
4. Keep home-level trust/config changes manual unless an official project-scoped surface and explicit user-approved flow are verified.
5. Record runtime refactor seams, but defer implementation to narrower follow-on owners.

## Confirmed Runtime Evidence

1. `require_default_autonomy_activation_consent()` is already a blocking gate in `cmd_init()`, but there is no separate persisted truth yet for “project authorization bootstrap accepted”.
2. `cmd_init()` currently mixes:
   - consent gate
   - `AGENTS.md` bootstrap
   - hooks enablement
   - config writeback
   - tool-local config materialization
   - wrapper/bootstrap file generation
   - registry writeback
   - runtime state reset
3. `cmd_set_tool()` and `cmd_sync_tooling()` can rematerialize project-local tooling surfaces after init, so post-consent mutation is already real behavior rather than hypothetical future scope.
4. `submit_human_frontdoor_message()` is already shared by `chat` and `tui`, so future authorization/bootstrap repair flows should reuse the same backend contract rather than inventing UI-specific semantics.
5. Current runtime and tests still expose at least one material drift:
   - `test-freely-init-cc-config` allows `AI_TOOL_ADAPTER="acp"` for `cc`
   - `tool_supported_adapters()` still reports `cc` as `direct` only

## Frozen Per-Tool Matrix

### codex

- project-local managed config:
  - verified project-local baseline exists
- launch-time managed posture:
  - additional runtime posture is injected at launch
- manual followthrough:
  - home-level auth/config may still need repair or completion
- known gaps:
  - project bootstrap and home-level readiness are not equivalent
  - alternate adapter paths still have parity gaps

### cc

- project-local managed config:
  - wrapper-managed project baseline exists
- launch-time managed posture:
  - stronger posture is primarily launch-time today
- manual followthrough:
  - native trust/settings remain manual until a stable project surface is verified
- known gaps:
  - config/runtime drift still exists for `cc + acp`
  - persistent project-local trust remains weaker than launch-time posture

### cc-use-codex-cli

- project-local managed config:
  - mixed wrapper baseline exists, but it spans more than one tool family
- launch-time managed posture:
  - runtime posture is assembled at launch across the composed tool path
- manual followthrough:
  - underlying tool trust can still remain manual if missing
- known gaps:
  - top-level tool-native settings are not yet frozen as one persistent contract
  - should not be described as full dual-tool authorization parity

### iflow

- project-local managed config:
  - wrapper-managed project baseline exists
- launch-time managed posture:
  - boundary extension is currently launch-time oriented
- manual followthrough:
  - any stronger trust/permission setup remains manual
- known gaps:
  - wrapper-only posture is not a full authorization bootstrap contract
  - continuity and project-local control remain weaker than Codex/Claude

### kiro-cli

- project-local managed config:
  - only a thin project wrapper baseline is verified
- launch-time managed posture:
  - trust posture is largely launch-time today
- manual followthrough:
  - user must still complete any non-wrapper trust/config path manually
- known gaps:
  - no verified project-local writable-root/trust surface
  - current flow is the weakest fit for “silent bootstrap after consent”

## Frozen Degradation Semantics

1. If activation consent is missing, `init` remains blocked before any downstream authorization/bootstrap work.
2. If activation consent exists but project authorization bootstrap is not completed for a given tool, Freely must explain the downgrade explicitly rather than silently pretending success.
3. Launch-time injection alone must be described as temporary execution posture, not as persistent tool trust.
4. When a tool lacks verified project-local config/trust surface, Freely must degrade to:
   - official non-interactive CLI if supported and explicitly approved
   - otherwise wrapper plus clear manual followthrough
5. CLI, TUI, GUI, and future settings must report the same degradation categories and not invent separate wording or hidden repair paths.

## Runtime Refactor Seams

1. Split activation consent recording from project authorization bootstrap recording.
2. Split tool-selection persistence from tooling materialization/rematerialization.
3. Split project entry bootstrap (`AGENTS.md`, hooks, allowlist) from per-tool authorization/bootstrap actions.
4. Expose one backend repair/materialization primitive reused by `init`, `set-tool`, `sync-tooling`, and future settings mutation.
5. Keep UI submit surfaces thin; `chat`, `tui`, and future GUI should call backend contract functions instead of branching semantics locally.

## Delegated Backend Detail

1. This brainstorm confirms that Codex API-key/provider mode is real product evidence that “project bootstrap completed” and “home-level tool auth/config is healthy” are different states.
2. It does not retain the detailed bundle, naming, probe, or cross-kind switch mechanics here. Those are now delegated to:
   - `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
   - `docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
3. The architecture-layer takeaway is narrower:
   - one cross-tool inventory/repair contract should exist
   - only tools with verified official surfaces may claim stronger switch/probe/auto-rotation parity
   - future standalone backend timing is a follow-on owner concern, not something re-opened in this product contract
4. `cc-switch` remains reference-only. Its value here is limited to demonstrating that config mutation and provider-aware editing can be tool-private backend concerns instead of architecture-level truth.

## Proposed Follow-on Families

1. Persisted `project authorization bootstrap accepted` truth and status surfacing.
2. Tool-auth backend work owned by workspace-routing follow-on owners, including Codex richer slot/auth handling and any generic backup discipline they require.
3. Per-tool bootstrap/repair execution path cleanup for `init` / `set-tool` / `sync-tooling`.
4. `cc + acp` drift resolution as a narrow adapter/materialization followthrough.
5. Future GUI/TUI/settings authorization repair flows only after the backend contract is canonical.

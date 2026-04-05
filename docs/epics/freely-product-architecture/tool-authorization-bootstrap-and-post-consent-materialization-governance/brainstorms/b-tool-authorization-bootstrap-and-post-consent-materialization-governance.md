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
  - `.codex/config.toml`
  - `.freely/bin/codex`
  - `.freely/tool-boundary-bootstrap.md`
- launch-time managed posture:
  - `--dangerously-bypass-approvals-and-sandbox`
  - `--add-dir <project-worktrees-root>`
- manual followthrough:
  - user home-level Codex trust still may need manual completion
- known gaps:
  - project-local baseline exists, but home-level trust is not equivalent to “Freely fully finished authorization bootstrap”
  - ACP path currently does not provide resume parity

### cc

- project-local managed config:
  - `.freely/config.env`
  - `.freely/bin/claude`
  - no frozen Claude-native project config truth yet
- launch-time managed posture:
  - `--permission-mode bypassPermissions`
  - `--session-id`
  - `--add-dir <project-worktrees-root>`
- manual followthrough:
  - any future Claude-native trust/settings flow remains manual until a stable project-scoped surface is verified
- known gaps:
  - config/runtime drift still exists for `cc + acp`
  - current authorization story is mostly launch-time, not persistent project-local trust

### cc-use-codex-cli

- project-local managed config:
  - `.freely/config.env`
  - `.freely/bin/claude`
  - project-local `.codex/config.toml` for embedded Codex capability posture
- launch-time managed posture:
  - Claude `--permission-mode bypassPermissions`
  - Claude `--session-id`
  - Claude `--add-dir <project-worktrees-root>`
  - fixed Codex capability injection for model/sandbox/approval/cwd policy
- manual followthrough:
  - Codex home-level trust can still remain manual if missing
- known gaps:
  - top-level Claude still lacks a separately frozen native project settings contract
  - should not be described as “Claude and Codex are both fully auto-authorized”

### iflow

- project-local managed config:
  - `.freely/config.env`
  - `.freely/bin/iflow`
  - no verified iflow-native project trust/config truth
- launch-time managed posture:
  - `--add-dir <project-worktrees-root>`
- manual followthrough:
  - any stronger trust/permission setup remains manual
- known gaps:
  - wrapper + add-dir is boundary extension, not a complete authorization bootstrap contract
  - continuity and project-local control remain weaker than Codex/Claude

### kiro-cli

- project-local managed config:
  - `.freely/config.env`
  - passthrough wrapper only
- launch-time managed posture:
  - trust posture currently relies on launch flags such as `--trust-all-tools`
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

## Proposed Follow-on Families

1. Persisted `project authorization bootstrap accepted` truth and status surfacing.
2. Per-tool bootstrap/repair execution path cleanup for `init` / `set-tool` / `sync-tooling`.
3. `cc + acp` drift resolution as a narrow adapter/materialization followthrough.
4. Future GUI/TUI/settings authorization repair flows only after the backend contract is canonical.

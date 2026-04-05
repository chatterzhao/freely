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

## Codex API-Key Findings

1. Official Codex already models provider auth as a first-class config concern rather than a pure login-email concern.
2. Official evidence currently relevant to Freely:
   - Codex README says users can sign in with ChatGPT or use an API key with additional setup.
   - OpenAI Codex auth docs say `auth.json` stores login details and is updated when the preferred auth method changes.
   - OpenAI Codex config schema defines `model_providers`, `base_url`, `env_key`, `openai_base_url`, and `requires_openai_auth`.
   - The schema description says `requires_openai_auth = true` stores login preference and token/key in `auth.json`, while `false` skips login UI and expects the key from `env_key`.
3. Therefore Freely must not equate “Codex slot” with “email-bearing ChatGPT account” any longer.
4. Current live-machine evidence confirms this is not theoretical:
   - `~/.codex/auth.json` only contains `OPENAI_API_KEY`
   - `~/.codex/config.toml` contains `model_provider = "custom"` and provider-scoped `base_url`
5. Current Freely `ai-cli` Codex slot code is too narrow because it:
   - copies only `auth.json`
   - treats slot identity as account/email when possible
   - verifies switch success by re-reading `auth.json`
6. That verification model fails for API-key/provider slots because success may depend on provider/base-url/config truth that lives in `config.toml`.

## Proposed Codex Slot Bundle Contract

1. Keep the existing `tool + slot` scheduler model; do not invent a second scheduling system just for Codex.
2. Upgrade Codex slot payload from `saved auth.json directory` to a bundle with explicit metadata.
3. Proposed minimum bundle contents:
   - `manifest.json`
   - optional `auth.json`
   - optional `config.toml` fragment or canonical provider slice
4. Proposed manifest fields:
   - `slot_kind`: `chatgpt_login | api_key_profile`
   - `auth_source`: `auth_json | env_key`
   - `provider_id`
   - `requires_openai_auth`
   - `base_url`
   - `openai_base_url`
   - `preferred_auth_method`
   - `probe_strategy`
5. Compatibility rule:
   - existing auth-only Codex slots should continue to load as implicit `chatgpt_login` bundles
   - new API-key slots use the richer manifest without breaking older saved slots
   - canonical inventory root stays `~/.ai-auth/<tool>-<slot>/`; type discrimination should happen in the slot id plus manifest, not by inventing a second root
6. Write rule:
   - active live Codex state must be treated as `auth.json + config.toml`
   - switching writes both or neither
7. Config rule:
   - preserve unrelated TOML sections
   - update active provider section first
   - only fall back to top-level `base_url` when there is no active provider truth

## Proposed Slot Naming Contract

1. Keep the existing directory contract:
   - `~/.ai-auth/codex-<slot_id>/`
2. Freeze `slot_id` as kind-prefixed so the directory name itself is machine-classifiable:
   - `account-<normalized-name>`
   - `apikey-<normalized-name>`
3. Proposed first-pass regex:
   - `^account-[a-z0-9][a-z0-9-]*$`
   - `^apikey-[a-z0-9][a-z0-9-]*$`
4. Examples:
   - `~/.ai-auth/codex-account-user-example-com/`
   - `~/.ai-auth/codex-apikey-openai-prod/`
   - `~/.ai-auth/codex-apikey-custom-caowo-xin/`
5. Compatibility rule for older saved slots with no prefix:
   - treat as legacy `account`-like Codex slots unless manifest says otherwise
   - allow lazy migration when the slot is next saved or rewritten
6. Recommended bundle contents by kind:
   - `account-*`: `manifest.json`, `auth.json`, optional config restore slice
   - `apikey-*`: `manifest.json`, optional `auth.json`, provider config slice, optional env metadata stub

## Switch Direction Matrix

1. `account -> account`
   - replace live `auth.json`
   - restore the slot's saved account-compatible config slice or clear stale API-key-only provider overrides
   - publish active slot only after probe succeeds
2. `account -> apikey`
   - replace or clear live `auth.json` according to the slot's `auth_source`
   - apply provider/base-url/preferred-auth/config slice for the API-key slot
   - preserve unrelated `projects.*`, `mcp_servers.*`, notices, and preferences
   - publish active slot only after provider-aware probe succeeds
3. `apikey -> apikey`
   - atomically swap provider/auth/config bundle
   - refresh availability classification and cooldown truth
4. `apikey -> account`
   - replace live `auth.json` with the account slot's auth payload
   - remove or overwrite API-key-only provider overrides introduced by the previous slot
   - restore the account slot's saved config slice so Codex does not stay pinned to the previous custom provider/base URL
5. Shared invariant:
   - active live state is the pair `~/.codex/auth.json + ~/.codex/config.toml`
   - no switch path may claim success after touching only one of them

## Login Save Delete Expectations Under The New Slot Kinds

1. `login codex`
   - creates or refreshes an `account-*` slot after official ChatGPT login
2. API-key add/save flow
   - creates or refreshes an `apikey-*` slot bundle
   - stores key/provider/base-url semantics in the slot directory instead of relying on one mutable global singleton state
3. `delete codex <slot>`
   - deletes only `~/.ai-auth/codex-<slot_id>/`
   - if deleting an active `apikey-*` slot, Freely must either switch to another verified slot first or refuse without explicit force
   - if deleting an active `account-*` slot, the same rule applies; do not leave a half-cleared live Codex state behind

## Proposed CLI Semantics

1. `freely ai login codex`
   - remains the ChatGPT login path
   - on success, save a `chatgpt_login` slot bundle
2. `freely ai save codex <slot>`
   - if live Codex state is email/login flavored, save as `chatgpt_login`
   - if live Codex state is API-key/provider flavored, save as `api_key_profile`
3. future explicit API-key add flow should accept enough information to build a slot without forcing the user to hand-edit live files first:
   - slot name
   - provider id
   - base URL when needed
   - whether auth comes from `auth.json` or `env_key`
4. `freely ai switch codex <slot>`
   - acquire switch lock
   - atomically apply auth + config
   - probe and classify result
   - publish active slot only after successful materialization
5. `freely ai delete codex <slot>`
   - removes saved bundle
   - if active, either require `--force` plus fallback decision or auto-switch to another verified usable slot before deletion

## Availability And Auto-Switch Design

1. Freely should keep its current stronger-than-cc-switch behavior:
   - probe first
   - classify reason
   - auto-switch only when policy says rotation is warranted
2. `cc-switch` is useful for config mutation technique, not as Freely’s availability truth.
3. Proposed API-key slot probe ladder:
   - validate manifest completeness
   - validate TOML syntax for the config slice
   - resolve effective provider, base URL, and auth source
   - verify required secret exists (`auth.json` key or expected env var)
   - perform provider-aware lightweight auth probe
4. Proposed classification set:
   - `usable`
   - `auth_invalid`
   - `quota_or_rate_limited`
   - `provider_endpoint_invalid`
   - `provider_network_transient`
   - `provider_network_persistent`
   - `config_invalid`
5. Rotation policy:
   - rotate on `auth_invalid`
   - rotate on `quota_or_rate_limited`
   - do not immediately rotate on network-local transient failures
   - keep current no-launch truth when every slot is bad, and expose earliest credible reset target
6. Lock policy:
   - startup, watchdog, manual switch, and probe all serialize on the same Codex switch lock family
   - the critical section must now protect `auth.json + config.toml` together

## Lessons Imported From cc-switch

1. `cc-switch` correctly treats Codex live state as both `auth.json` and `config.toml`.
2. Its `toml_edit` approach is worth copying because it preserves unrelated sections and comments.
3. Its provider-aware `base_url` editing is directly relevant to Freely.
4. Its semantics are still weaker than Freely needs because it does not own runtime launch blocking, cooldown truth, or auto-rotation policy.

## Proposed Follow-on Families

1. Persisted `project authorization bootstrap accepted` truth and status surfacing.
2. Codex API-key slot bundle materialization, atomic switch, and provider-aware probing.
3. Per-tool bootstrap/repair execution path cleanup for `init` / `set-tool` / `sync-tooling`.
4. `cc + acp` drift resolution as a narrow adapter/materialization followthrough.
5. Future GUI/TUI/settings authorization repair flows only after the backend contract is canonical.

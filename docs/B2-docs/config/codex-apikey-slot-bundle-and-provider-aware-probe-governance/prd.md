# PRD: codex-apikey-slot-bundle-and-provider-aware-probe-governance

## Goal

把 Codex 的 API-key/provider 模式收敛成 Freely 的一等 slot contract，使 `login/save/switch/delete/status/list` 可以在不破坏既有 account-slot behavior 的前提下，正确管理 `account-*` 与 `apikey-*` 两类 saved slot。

## Why Now

当前 dogfood 现场已经出现真实的 API-key/provider 使用，而 Freely 现有 contract 还停留在：

- slot inventory 是通用的
- Codex probe 和 auto-rotate 是强的
- 但 Codex save/switch 仍只保存和恢复 `auth.json`

这导致 runtime 的强治理和 live auth truth 出现断层。若不先冻结 auth+config bundle contract，后续实现很容易把：

- API key
- provider selection
- `base_url`
- `preferred_auth_method`
- `requires_openai_auth`

散落到一个无法安全切换、无法安全探测的全局 singleton 里。

## Product Surface

- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/tools.md`
- future standalone backend: `ai-switch-cli`
- future AI-facing skill: `ai-switch-skill`
- `~/.ai-auth/<tool>-<slot>/` inventory contract
- Codex live surfaces:
  - `~/.codex/auth.json`
  - `~/.codex/config.toml`

## Non-Goals

- non-Codex tool probe parity
- Claude/OpenCode/iFlow/Kiro live auth materialization landing
- whole-file `config.toml` replacement
- new global fallback scheduler semantics
- immediate publication or packaging of a standalone `ai-switch-cli` app

## Non-Negotiables

- `apikey` is a first-class slot kind, not a singleton mode bolted onto global Codex config
- Codex live materialization is atomic across `auth.json` and auth-relevant config mutation
- switch success is probe-backed, not copy-backed
- directory name remains a fast routing hint, but manifest is the stronger truth for compatibility and migration
- generic slot command surface remains shared across tools, while materializer/probe implementations stay tool-specific

## Canonical Contract Frame

### Generic layer

Must own:

1. inventory root
2. slot id
3. slot kind
4. active-slot pointer
5. generic manifest vocabulary
6. delete/list/status command semantics
7. staged extraction boundary toward a standalone CLI backend

Must not own:

1. tool-specific live file layouts
2. provider-specific config mutation logic
3. tool-specific probe execution

### Codex layer

Must own:

1. slot-local `auth.json`
2. slot-local auth/provider fragment such as `config-auth.toml`
3. syntax-preserving mutation of live `~/.codex/config.toml`
4. slot-kind-aware probe routing
5. cross-kind stale-field clearing rules

### Freely control-plane layer

Long term, Freely should prefer a CLI-first contract rather than permanently embedding every tool's live-file mutation logic.

That means Freely should ultimately own:

1. tool priority / fallback order
2. watchdog recovery policy
3. no-launch / cooldown / bounded retry decisions
4. when to ask a backend for `probe`, `best`, `switch`
5. project-local UX such as whether a newly logged-in tool should be inserted into priority order

And a standalone backend such as `ai-switch-cli` should own:

1. tool-native login flow
2. slot save/delete/switch implementation
3. tool-specific live config mutation
4. tool-specific probe execution
5. JSON machine-readable output consumed by Freely

## `ai-switch-cli` Minimal Command Surface

The extracted backend should expose one stable shared contract across tools:

1. `ai-switch-cli list <tool> [--json]`
2. `ai-switch-cli current <tool> [--json]`
3. `ai-switch-cli login <tool> [account|apikey] [--slot <slot_id>] [--json]`
4. `ai-switch-cli save <tool> [--slot <slot_id>] [--json]`
5. `ai-switch-cli switch <tool> <slot_id|auto> [--json]`
6. `ai-switch-cli delete <tool> <slot_id> [--json]`
7. `ai-switch-cli probe <tool> [<slot_id>|--current] [--json]`
8. `ai-switch-cli best <tool> [--json]`
9. `ai-switch-cli status [<tool>] [--json]`

Rules:

1. `login` must support interactive and non-interactive invocation. When auth mode is omitted, the backend may prompt for `account` vs `apikey`.
2. `switch <tool> auto` means "choose and activate the best usable slot under that tool's probe contract", not "pick the latest saved slot".
3. `best` is read-only selection. It must never mutate live files.
4. `status` is the machine-facing discovery surface for installed tools, current slots, capability tiers, and backend health.
5. Unsupported actions must fail explicitly and machine-readably instead of silently degrading into partial behavior.

## JSON Envelope

Whenever `--json` is requested, the top-level response must include:

- `ok`
- `backend`
- `tool`
- `requested_action`
- `capability_tier`
- `slot_id`
- `slot_kind`
- `current_slot_id`
- `provider_id`
- `probe_method`
- `mutated_live_surfaces`
- `reason_code`
- `message`

Command-specific extensions:

1. `list` adds `slots[]`.
2. `current` adds `slot`.
3. `probe` adds `probe_result`, `latency_ms`, `evidence`.
4. `best` adds `selected_slot`, `selection_reason`, `candidates_considered`.
5. `status` adds `tools[]` and backend-install state.

## `ai-switch-skill` Boundary

The backend should ship with an AI-facing integration skill, tentatively `ai-switch-skill`.

The skill must explain:

1. command meanings and expected JSON fields
2. when to use `probe` versus `best` versus `switch auto`
3. auth-mode differences between `account` and `apikey`
4. which commands mutate live state and which are read-only
5. failure handling and retry boundaries

Freely should eventually consume the CLI through this documented contract rather than relying on hidden in-process adapter knowledge.

## Capability Tier Table

Current verified contract:

| Tool | Tier now | Verified truth |
| --- | --- | --- |
| `codex` | `auto_rotatable` | Generic inventory, auth+config bundle materialization, and proactive probe routing are real and dogfooded. |
| `cc` | `inventory_only` | Generic slot inventory can represent saved slots, but this owner does not verify Claude live auth materialization or proactive probe parity. |
| `cc-use-codex-cli` | `inventory_only` | Some Codex project-config bridging exists, but this owner does not verify Claude auth bundle switching. |
| `opencode` | `inventory_only` | Reference evidence shows provider-specific config mutation elsewhere, but Freely has not yet frozen or verified equivalent live materialization. |
| `iflow` | `inventory_only` | No verified live auth bundle switch or probe contract is owned here. |
| `kiro-cli` | `inventory_only` | No verified live auth bundle switch or probe contract is owned here. |

This table is binding for this lane: no IBM or implementation artifact may claim stronger parity without new verified evidence.

## Staged Extraction Plan

### Stage A: prove the contract in Freely

Use the current owner to freeze:

1. generic manifest vocabulary
2. Codex account/apikey bundle semantics
3. slot-kind-aware probe contract
4. multi-tool capability tiers

### Stage B: extract tool-switch backend

Once the contract is stable, extract the tool-specific adapter layer into standalone `ai-switch-cli`:

1. Freely continues to own orchestration
2. `ai-switch-cli` owns tool auth/switch/probe implementation
3. Freely prefers the CLI backend when installed, but may keep an internal fallback during migration

### Stage C: init/login UX integration

When `ai-switch-cli` is mature enough, `freely init` should:

1. detect whether `ai-switch-cli` is installed
2. ask whether to use/install it
3. persist backend choice in project-local config
4. preserve an explicit "backend unavailable" state instead of silently falling back to stale embedded logic

And `freely ai login <tool> <auth-mode>` should:

1. complete login through the active backend
2. check whether the tool is already present in the project tool priority list
3. if missing, prompt to insert it
4. default Enter behavior inserts it at the front of the list
5. preserve the relative order of other tools unless the user explicitly reorders them

This preserves CLI-first decoupling while keeping routing/fallback truth in Freely.

## First Slice

1. manifest + slot bundle format
2. kind-prefixed naming and legacy compatibility
3. auth+config fragment extraction/materialization helpers
4. slot-kind-aware probe routing
5. focused tests for save/switch/probe/status
6. minimal `ai-switch-cli` command and JSON contract freeze
7. `ai-switch-skill` boundary freeze
8. explicit decision that the long-term backend direction is standalone `ai-switch-cli`, with Freely as a CLI-first consumer

## Eval Plan

Success:

- Codex API-key slot can be saved without losing provider/base-url truth
- switching `account-*` <-> `apikey-*` leaves no stale live config residue
- watchdog/status/switch use the correct probe truth per slot kind
- non-Codex tools remain explicitly weaker instead of being silently over-promised
- the docs make the `Freely control plane` vs `tool-switch backend` split unambiguous
- `freely init` and `freely ai login` have a frozen backend-detection and priority-list insertion contract that does not require implementation guesswork

Failure:

- implementation still treats `auth.json` as complete truth
- `apikey-*` slot availability remains gated on OAuth sweep
- account/apikey cross-switch leaves old provider selection or base URL behind
- docs or code imply `cc`/`iflow`/`opencode` already have equal parity
- extracted CLI shape remains too vague for Freely to consume it without hidden tool-specific knowledge

## Revisit Triggers

- official Codex auth/provider schema changes materially
- a verified lower-cost API-key probe becomes available
- another tool reaches verified switchable/probeable parity and should be folded into the same generic contract

## Dev-Loop Handoff

实现阶段优先集中在 `ai-cli` 和 `availability-watchdog.sh`，先把 Codex contract 做对。若 IBM 结论确认 `ai-switch-cli` 是长期方向，则实现时应避免把新 adapter 逻辑继续深埋进 Freely，而要按可抽离 backend 的边界组织代码。

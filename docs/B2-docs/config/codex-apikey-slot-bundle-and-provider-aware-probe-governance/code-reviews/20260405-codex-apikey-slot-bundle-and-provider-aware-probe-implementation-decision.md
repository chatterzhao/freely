# Implementation Decision: codex-apikey-slot-bundle-and-provider-aware-probe-governance

- issue_id: `I-20260405-0027-A`
- issue_path: `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- branch: `feature/tool-authorization-bootstrap-research-20260405-0335`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0335-feature-tool-authorization-bootstrap-research`
- decision_date: `2026-04-05`
- author: `codex`

## Implementation Decision Note

- decision: `Treat Codex slot truth as a slot-local bundle of auth payload, provider-aware config fragment, and manifest metadata; route watchdog probing by slot kind instead of assuming OAuth inventory is authoritative for every saved slot; and require a shared timestamped backup helper before rewriting untracked home-level config such as ~/.codex/config.toml.`
- why_this: `Real Codex API-key mode lives across both ~/.codex/auth.json and ~/.codex/config.toml. Saving only auth.json loses base_url/provider/auth-mode truth, while probing only through OAuth sweep blocks usable API-key slots. Because config.toml lives in the user home and is not Git-tracked, safe materialization also needs a rollback copy before mutation. The narrow bundle, slot-kind probe split, and shared backup helper fix the observed dogfood failures without pretending other tools already have the same materializer maturity.`
- alternatives_considered: `Considered storing the whole ~/.codex/config.toml per slot and doing full-file replacement on switch, and considered leaving the switch path auth-only while adding an API-key-specific probe exception. Whole-file replacement would trample unrelated project/user config, while auth-only switching would keep stale provider residue and broken cross-kind materialization.`
- boundary_non_goals: `Do not widen this owner into full multi-tool parity, standalone ai-switch-cli extraction, or generic provider mutation for every supported tool. Do not claim Codex account/apikey semantics automatically generalize to cc/opencode/iflow/kiro-cli before dedicated evidence exists.`
- residual_risk: `The live config writer still normalizes TOML formatting instead of preserving comments/order byte-for-byte, and the current slice only proves Codex. Future backend extraction should isolate tool-native mutation behind ai-switch-cli so Freely consumes a single JSON contract instead of carrying more per-tool file knowledge, while any tool that rewrites home-level config consistently consumes the same backup primitive.`

## Why

- Codex account slots and API-key/provider slots are both first-class in the user environment, but they do not share the same live truth surface.
- The owner already froze `account-*` / `apikey-*` naming, bundle semantics, and probe routing in IBM docs; the implementation follows that frozen boundary rather than creating a second implicit contract in shell code.
- Slot manifests keep backward compatibility for legacy/unprefixed slots while adding enough metadata for kind-aware switch, status, and watchdog behavior.

## Alternatives Considered

- keep using `auth.json` as the only saved truth and add a special-case env override at probe time
  - rejected because it still leaves switch-time provider/base-url residue behind in live config
- save/restore the entire `~/.codex/config.toml`
  - rejected because unrelated tables such as project trust settings must survive slot changes
- continue treating OAuth inventory as the only canonical availability source
  - rejected because API-key slots can be usable even when OAuth/curl inventory is unreachable

## Non-Goals

- no generic per-tool bundle materializer for every tool in this lane
- no new scheduler or priority-order redesign in Freely control plane
- no standalone packaging/release work for `ai-switch-cli` yet

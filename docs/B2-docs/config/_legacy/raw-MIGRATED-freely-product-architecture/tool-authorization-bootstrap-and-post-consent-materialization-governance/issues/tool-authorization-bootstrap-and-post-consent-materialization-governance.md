# Issue: tool-authorization-bootstrap-and-post-consent-materialization-governance

- issue_id: `I-20260405-1235-A`
- title: Tool authorization bootstrap and post-consent materialization governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `tool-authorization-bootstrap-and-post-consent-materialization-governance`
- issue-name: `tool-authorization-bootstrap-and-post-consent-materialization-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-1235-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
  - `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
  - `docs/B2-docs/config/packaging/issues/project-level-agents-bootstrap-and-management-contract-governance.md`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经冻结了 activation consent、默认自治 posture、以及一部分 per-tool materialization，但还缺一条独立 owner 来回答更具体的产品问题：

1. 用户在 `freely init`、`set-tool`、future settings mutation 中，是否显式同意了“为当前项目做 tool authorization bootstrap”。
2. Freely 对每个工具到底能自动做什么，不能自动做什么，哪些仍需 manual trust / CLI followthrough。
3. adapter 路径、tool trust、project authorization bootstrap 三者如何分层，避免 ACP 或 wrapper 被误写成“授权已完成”。
4. CLI、TUI、GUI 与 future settings 面板如何复用同一 backend contract，而不是各自发明一套同意/修复语义。

当前这层缺口已经不是 wording 问题，而是产品 contract 缺口。现有 runtime 代码已经会在 `init` / `set-tool` / `sync-tooling` 中改写 tool-local surface，但系统还没有单独真源来定义这些动作属于哪一层授权、哪些只是 launch-time posture、哪些仍需用户继续完成。

## Scope

1. 冻结 `activation consent`、`project authorization bootstrap`、`tool trust / permission surface`、`adapter surface` 的边界。
2. 冻结一份 per-tool authorization/bootstrap matrix，至少覆盖：
   - `codex`
   - `cc`
   - `cc-use-codex-cli`
   - `iflow`
   - `kiro-cli`
3. 明确 `freely init`、`set-tool`、`sync-tooling`、future settings mutation 在“用户未同意 / tool 未完成 bootstrap”时必须如何解释退化行为。
4. 冻结 CLI-first backend contract，要求未来 TUI / GUI / settings 复用同一 authorization/bootstrap truth。
5. 明确 runtime refactor seam，解释为什么 `cmd_init()` 不应继续承载 consent、AGENTS bootstrap、tooling materialization、registry writeback、runtime reset 的混合职责。

## Non-Goals

1. 不在本条 issue 中直接实现新的 tool bootstrap 流程或自动化写配置。
2. 不把用户 home 级 trust/config 改写面默认纳入 Freely 自动执行范围。
3. 不把 ACP 重新定义成 trust/authorization owner；它仍只是 adapter/transport 轴。
4. 不在本条 issue 中设计一套独立的 GUI/TUI 语义；只冻结 backend contract。
5. 不在 contract 未稳定前声称 `cc + acp` 或其他工具组合已经获得完整 direct parity。

## Boundary Guardrails

1. 本 owner 只定义“用户显式授权后，Freely 如何按工具能力完成 bootstrap/materialization，以及哪些步骤仍必须用户手工完成”的 contract，不重写默认自治 posture 或 activation consent 文案。
2. 本 owner 消费 `default-autonomy-activation-consent-and-tool-policy-governance` 已冻结的上位边界，而不是重开它。
3. 本 owner 不重开 `project-level-agents-bootstrap-and-management-contract-governance`；项目级 `AGENTS.md` 仍只是项目入口，不承担外部工具 trust/bootstrap 真相。
4. 本 owner 只收口 per-tool 三分法：`project-local managed config`、`launch-time injection only`、`manual-only followthrough`；不得把 home-level trust 或未验证 surface 伪装成已自动完成。
5. 本 owner 可以引用 adapter 轴差异，但不把 ACP parity、session continuity 或新 adapter runtime 实现一起吃成 umbrella。

## Acceptance

1. issue 明确区分 activation consent 与 project authorization bootstrap，二者不再复用为一个模糊总开关。
2. issue 明确列出 per-tool matrix：project-local managed config、launch-time managed posture、manual followthrough、unsupported/unknown surface。
3. issue 明确规定 adapter 选择不会自动代表 tool trust 或项目授权 bootstrap 已完成。
4. issue 明确写出未同意 / 未完成 bootstrap 时的 degradation semantics，避免 CLI/TUI/GUI 各说各话。
5. issue 明确写出 runtime refactor seam，让后续实现可以把 consent、bootstrap、repair、tool materialization 解耦为同一 backend contract。
6. lifecycle artifacts 保持 documentation-first，不假装本轮已经进入实现。

## Frozen Degradation Contract

1. Missing activation consent remains a hard blocker for `init`.
2. Existing activation consent does not imply per-tool authorization/bootstrap is complete.
3. Project-local managed config, launch-time injection, and manual followthrough must be surfaced as distinct states.
4. If a tool lacks verified project-local trust/config surface, Freely must either:
   - use an official non-interactive CLI path with explicit consent, or
   - fall back to wrapper plus manual followthrough
5. Future CLI/TUI/GUI/settings flows must report the same degradation categories and backend truth.

## Current Evidence

1. `docs/system/workspace/scripts/runtime/freely#cmd_init` currently mixes consent, project bootstrap, tool materialization, registry writeback, and runtime reset in one path.
2. `docs/system/workspace/scripts/runtime/freely#cmd_set_tool` and `docs/system/workspace/scripts/runtime/freely#cmd_sync_tooling` already prove post-init rematerialization is a real capability surface.
3. `docs/system/workspace/scripts/runtime/freely#submit_human_frontdoor_message` and `docs/system/workspace/scripts/runtime/freely#cmd_tui` already show CLI/TUI frontdoor unification at the submit layer.
4. `docs/system/workspace/scripts/runtime/tool-launchers.sh#tool_supported_adapters` still reports `cc` as `direct` only.
5. `docs/system/workspace/scripts/tests/test-freely-init-cc-config` still allows `cc + adapter=acp` to be persisted in project config, proving a config/runtime drift that this owner must classify but not prematurely “solve” in architecture docs.
6. Codex has now proven a concrete product-layer case where project bootstrap and home-level auth/config truth are not the same thing; the detailed slot bundle, provider-aware probe, and cross-kind switch contract are owned by `I-20260405-0027-A`.
7. The extraction timing for a future standalone backend is no longer operator memory; it is owned by `I-20260405-1415-A` and must not be re-decided in this architecture owner.

## Delegated Tool-Auth Backend Truth

This owner freezes the product boundary only. The following implementation-shaped truths are delegated and must be consumed by reference rather than redefined here:

1. Codex `account-*` / `apikey-*` slot bundle shape, slot naming, cross-kind switch matrix, provider-aware probe routing, and backup-before-mutation behavior are owned by `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`.
2. The threshold and repository disposition for any future standalone `ai-switch-cli` backend are owned by `docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`.
3. This architecture owner only requires that any backend chosen by follow-on owners preserve one cross-tool contract family:
   - slot inventory remains tool-keyed rather than tool-specific ad hoc roots
   - stronger capabilities such as switch, probe, and auto-rotation are claimed only when official tool surfaces are verified
   - CLI, TUI, GUI, and future settings flows consume the same backend truth instead of inventing UI-local semantics

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- `docs/B2-docs/config/packaging/brainstorms/b-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- `docs/B2-docs/config/packaging/prd.md`
- `docs/B2-docs/config/packaging/pre-tests.md`
- `docs/B2-docs/config/packaging/tasks.md`
- `docs/progress/freely-product-architecture/p-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`

## Verification

- `./bin/governance-check`
- wording review confirming:
  - activation consent, authorization bootstrap, tool trust, and adapter policy are distinct layers
  - per-tool automation claims do not outrun verified tool surfaces
  - CLI/TUI/GUI/settings reuse the same backend contract instead of inventing separate semantics

## IBM Handoff

- implementation_scope_summary:
  - `I-20260405-1235-A` now freezes the product-layer contract for post-consent tool authorization/bootstrap, including the layer split between activation consent, project authorization bootstrap, tool trust, and adapter policy.
  - The canonical IBM package now includes the per-tool matrix, shared degradation semantics, and runtime refactor seams required before any narrower implementation owner is opened.
  - Follow-on work must consume this owner as architecture truth rather than reopening umbrella product-boundary debate inside runtime lanes.
- required_doc_refs:
  - `docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
  - `docs/B2-docs/config/packaging/brainstorms/b-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
  - `docs/B2-docs/config/packaging/prd.md`
  - `docs/B2-docs/config/packaging/pre-tests.md`
  - `docs/B2-docs/config/packaging/tasks.md`
  - `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`

## Next

## Closeout

- Canonical `develop` already carries this bounded architecture contract for post-consent authorization/bootstrap semantics.
- `2026-04-09` closeout verification reconfirmed that downstream implementation owners should continue consuming this package rather than reopening it for tool-specific implementation.
- Future work should open only narrower follow-on owners for persisted state, repair/materialization cleanup, or adapter-specific drift correction.

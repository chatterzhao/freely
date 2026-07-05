# Issue: ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance

- issue_id: `I-20260405-1415-A`
- title: ai-switch-cli extraction threshold and skeleton disposition governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance`
- issue-name: `ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-1415-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经在当前 Codex owner 中冻结了长期方向: tool auth/switch/probe 应逐步抽成 standalone `ai-switch-cli` backend，而 Freely 保持 control plane / orchestration / priority / recovery policy。现在缺的不是“是否要拆”，而是：

- 何时才算达到可拆分门槛
- 哪些 helper 必须先从 Freely 内部的 inline script 中收敛成可迁移的 generic surface
- 当前本机已有的 `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch` 空骨架应如何处理

如果不先把这条边界冻结，后续很容易出现两类治理退化：

1. 过早拆分，导致 Freely 和 standalone repo 双份维护仍在变化的 tool-private file knowledge
2. 一直不拆，导致 Freely 持续吸收 backend-specific config mutation/probe logic，反而把 control plane 和 backend boundary重新混在一起

因此需要一个新的 milestone-owned owner，专门冻结 extraction threshold、repo skeleton disposition 和 first extraction lane 的 boundary，而不是继续在 Codex verification lane 中顺手决定。

## Scope

1. 冻结 `ai-switch-cli` extraction 的准入门槛，包括命令面、JSON envelope、至少一个强工具 contract、以及 generic helper surface 的成熟条件。
2. 冻结 Freely control plane 与 future backend 的职责边界，避免 extraction 后出现 prompt/CLI/runtime 三份平行真相。
3. 冻结现有本地 skeleton `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch` 的处置规则。
4. 冻结 extraction owner 启动前，Freely 内部应先抽离哪些 generic helper，例如 config backup、generic slot inventory plumbing。
5. 冻结是否允许“原地 rename skeleton”与“丢弃后新建仓库”两种路径，以及各自进入条件。

## Non-Goals

1. 不在本 owner 内直接实现 standalone `ai-switch-cli` 发布、安装或打包。
2. 不在本 owner 内把当前 `ai-cli` 逻辑整体迁出 Freely。
3. 不重开 Codex slot bundle / provider-aware probe 的已冻结 contract。
4. 不在没有 verified evidence 的情况下宣称第二工具已经达到 backend-worthy parity。
5. 不把空 skeleton 目录误当成已经存在的 canonical backend。

## Acceptance

1. extraction threshold 至少明确要求：
   - command surface 冻结
   - JSON envelope 冻结
   - 至少一个工具具备 verified save/switch/probe/materialization truth
   - generic helper surfaces 不再只是 tool-local inline logic
2. Freely control plane 与 backend 的职责边界能直接指导后续 extraction owner，不需要再从聊天记录恢复。
3. 本地 skeleton 仓库的处置规则明确说明：
   - 何时允许 rename 为 `ai-switch-cli`
   - 何时应直接丢弃并新建
   - 在 first real commit 前必须改写哪些命名与文档真相
4. 文档明确说明当前仍未开始 standalone extraction，避免误把本地 skeleton 当成 active backend。
5. issue IBM 文档能直接约束 follow-on implementation owner，且不把 extraction timing 留在 operator memory。

## Completion

- `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/brainstorms/b-ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/prd.md`
- `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/tasks.md`
- milestone / candidate writeback showing this is the canonical owner for extraction timing and skeleton disposition

## IBM Handoff

- implementation_scope_summary:
  - `I-20260405-1415-A` 已冻结 standalone extraction 的 start gate、Freely/backend boundary、以及本地 skeleton disposition。
  - 后续若真的开 extraction owner，不再重复研究“要不要拆”；只允许判断 threshold 是否已满足，以及第一刀迁移哪个 backend-owned slice。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
  - `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/brainstorms/b-ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
  - `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/tasks.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`

## Closeout

- Canonical `develop` already carries this bounded extraction-threshold and skeleton-disposition owner as the handoff package for any future standalone backend lane.
- `2026-04-09` closeout verification reconfirmed the owner remains documentation/governance-only and that lifecycle drift, not implementation debt, was the only missing work.
- Future work should open a new owner only when threshold conditions are truly ready to be exercised; do not reopen this owner merely because the local skeleton still exists.

## Verification

- `./bin/governance-check`
- review `docs/B1-docs/raw-20260405/brainstorms.md`
- review `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/prd.md`
- confirm the resulting docs do not claim standalone extraction has already started

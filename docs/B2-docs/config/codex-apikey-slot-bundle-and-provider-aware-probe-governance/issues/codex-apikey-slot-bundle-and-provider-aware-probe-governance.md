# Issue: codex-apikey-slot-bundle-and-provider-aware-probe-governance

- issue_id: `I-20260405-0027-A`
- title: Codex API-key slot bundle and provider-aware probe governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-apikey-slot-bundle-and-provider-aware-probe-governance`
- issue-name: `codex-apikey-slot-bundle-and-provider-aware-probe-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-0027-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
  - `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把 slot inventory、slot-first recovery、OAuth inventory sweep、launch-time confirmation 和 bounded network taxonomy 分别冻结为 canonical contract，但 Codex live auth truth 仍停留在 `~/.codex/auth.json` copy-in/copy-out。这个模型无法覆盖已经真实存在的 API-key/provider 模式，因为可用性与切换正确性同时依赖：

- `~/.codex/auth.json`
- `~/.codex/config.toml`
- provider-scoped `base_url` / `env_key` / auth-mode truth

如果不把 `apikey` 提升为一等 slot，Freely 就会在 dogfood 环境里继续误判：

- `save` 只能保存残缺 truth
- `switch` 会把旧 provider residue 留在 live config
- watchdog 会把 OAuth sweep 误当成 API-key slot 的可用性来源

因此需要一个新的 follow-on owner，专门收敛 Codex `account-*` / `apikey-*` slot bundle、跨类型切换和 provider-aware probe contract，而不是重开更宽的全局 slot 或 OAuth sweep owner。

## Scope

1. 冻结 Codex kind-prefixed slot contract，至少覆盖 `account-*`、`apikey-*` 与 legacy unprefixed slot compatibility。
2. 定义 Codex slot bundle shape，使 slot 目录能保存 auth truth 与 provider-aware config fragment，而不是只保存 `auth.json`。
3. 定义 `account -> apikey`、`apikey -> account`、`apikey -> apikey`、`account -> account` 的 cross-kind live materialization 语义。
4. 定义 slot-kind-aware probe routing：
   - `account-*` 继续允许 OAuth inventory sweep + exec confirmation
   - `apikey-*` 直接走 exec-based usability truth
5. 冻结 generic slot manifest 与 per-tool materializer/probe adapter 的边界，确保其他工具可以复用 command surface，但不冒充与 Codex 等级相同。
6. 冻结这条能力未来是否应提炼成 standalone `ai-switch-cli` backend，以及 Freely runtime 对该 backend 的 CLI-first 集成边界。
7. 冻结 `ai-switch-skill` 作为 AI-facing integration layer 的职责，确保任何 AI 工具都可通过统一 CLI contract 接入。

## Non-Goals

1. 不把本 owner 扩写成所有工具都立即支持 auth bundle switch。
2. 不复制 `cc-switch` 的架构、UI 或配置管理层级。
3. 不在本 owner 内同时落地非 Codex 工具的 probe parity。
4. 不重写全局 scheduler、公平性或 cross-tool fallback semantics。
5. 不把整个 `~/.codex/config.toml` 粗暴存进 slot 并在 switch 时整文件覆盖。
6. 不在本 owner 内直接实现完整独立应用发布流程；这里只冻结拆分阶段与 integration contract。

## Acceptance

1. Codex slot bundle contract 明确要求 live truth 按 `auth.json + auth-relevant config fragment` 成对处理，而不是继续假设 `auth.json` 单文件足够。
2. kind-prefixed slot naming、legacy slot compatibility、manifest vocabulary 和 active-slot routing 规则都已冻结，可直接指导 `login/save/switch/delete/status/list` 的实现。
3. cross-kind switch contract 明确说明从 account 与 apikey 两类 slot 互切时需要写哪些 live surfaces，以及哪些 stale provider/auth residue 必须清理。
4. probe selection 按 slot kind 分流：
   - `account-*` 可继续复用 OAuth inventory sweep 作为 inventory truth
   - `apikey-*` 不再依赖 OAuth/curl sweep，而以 non-interactive `codex exec` probe 为 canonical truth
5. per-tool capability tier table 明确区分 `inventory_only`、`switchable`、`probeable`、`auto_rotatable`，并明确当前只有 Codex 具备第一轮强 contract。
6. 文档明确说明 Freely 的长期方向是否是通过 standalone `ai-switch-cli` 以 CLI-first 方式消费 tool auth/switch/probe 能力，并写清与 Freely watchdog/orchestration 的职责边界。
7. 本 issue 的 IBM 文档能直接约束第一实现切片，且不把非 Codex 工具误写成当前已具备 live auth materialization 或 proactive probe。
8. `ai-switch-cli` 的最小命令面、JSON envelope、`freely init` backend-detection flow、以及 `freely ai login` priority-list insertion flow 都已冻结到足以直接开 dev-loop。

## Completion

- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/prd.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-verification.md`
- milestone / candidate writeback showing this is now the canonical owner
- issue-owned IBM contract freezing the future `ai-switch-cli` / `ai-switch-skill` boundary

## Verification

- `./bin/governance-check`
- review `docs/B1-docs/raw-20260405/brainstorms.md`
- review `docs/system/workspace/scripts/runtime/ai-cli`
- review `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- confirm the IBM docs do not claim non-Codex probe/materialization parity without verified evidence
- pass `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
- pass `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
- pass `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- pass `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- pass `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- treat the two existing protected-merge receipt gaps on `develop` as historical governance debt unless this lane changes those merge commits

## Next

- Completed on canonical `develop` via guarded merge `c5e0b85`.
- Post-merge closeout verification is recorded in `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-canonical-closeout-verification.md`.
- Reopen only if Codex auth/config bundle materialization, slot-kind-aware probe routing, or provider residue cleanup regresses on canonical `develop`.

# Issue: frontend-runtime-baseline-for-probe

- issue_id: `I-20260317-1004`
- title: Frontend Runtime Baseline for Probe
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `frontend-runtime-baseline-for-probe`
- issue-name: `frontend-runtime-baseline-for-probe`
- source_candidate: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md#c-20260317-1101`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/pre-tests.md`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

`Frontend Probe v0` 在实现中已经暴露出一个独立基础设施缺口：缺少真实 frontend build/runtime baseline，导致后续工作无法从骨架阶段进入可运行宿主阶段。

## Scope

1. 明确 frontend 宿主入口与 React renderer 挂载基线。
2. 明确 Tauri runtime 注入路径与最小 host wiring。
3. 明确 day-1 build/test baseline 的最小约束。
4. 明确该 baseline 与 `Frontend Probe v0` 的依赖边界。

## Acceptance

- 文档明确 frontend 宿主入口、React renderer 与 runtime 注入的最小基线。
- 文档明确 build/test baseline 的最小要求，不再让 dev-loop 只停在样板代码。
- 文档明确 `Frontend Probe v0` 如何依赖该 baseline，而不是继续把它混在 Probe issue 内。

## Minimal baseline

### Host entry

- 提供统一 default entry，负责读取宿主 runtime 能力
- 提供 bootstrap / mount / host helper，避免调用方手写接线

### React renderer

- 宿主必须提供明确的 render/root 接口
- Probe app 不直接依赖外部全局 renderer 细节，而通过 host helper 统一挂载

### Tauri runtime injection

- 宿主需提供 `invoke`
- 宿主需提供 `listen`
- 两者共同驱动 adapter 的 command / event 双通道

### Minimal build/test baseline

- 至少需要一个 frontend host entry 文件
- 至少需要一个 renderer/mount 路径
- 至少需要一个可验证 adapter 注入的最小运行方式
- 若正式测试基线尚未存在，需在 issue/progress/continuity 中显式记录缺失，而不是假装已可运行

## IBM Handoff

- implementation_scope_summary:
  - 把 `Frontend Probe v0` 中暴露出来的基础设施缺口独立成专门 issue，避免继续污染当前 UI issue 的边界。
  - 当前阶段仍是 issue-bound IBM 收敛，不进入实现代码。
- required_doc_refs:
  - `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/brainstorms/b-frontend-runtime-baseline-for-probe.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/prd.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/pre-tests.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/tasks.md`

## Next

- 当前 owner 已完成 absorption closeout；后续若 Probe 或其他 frontend shell 再暴露新的宿主/build/runtime 基线缺口，应另开新 lifecycle，而不是重新挂住本 owner。

## Closeout

- 当前 owner 的作用是把 frontend host entry、renderer mount、runtime injection 与最小 build/test baseline 从 `Frontend Probe v0` 中拆出来单独冻结边界。
- 这些基线现在已经不再停留在 IBM 文档层：`src/frontend_probe_v0/`、`index.html`、`vite.config.ts`、根目录 `package.json` 与 `src-tauri/` 的真实宿主/bridge 路径都已在 `develop` 存在，并被 `I-20260308-1244-03` 与 `I-20260317-0332` 实际消费。
- 因此本 owner 不再需要继续作为 parked committed issue 占住近程执行窗；它的边界已经被下游实现吸收，当前合适的生命周期动作是 canonical closeout。

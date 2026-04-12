# Brainstorm: pretests-gate-and-network-proxy-config

- brainstorm_id: `20260327-0651--pretests-gate-and-network-proxy-config`
- created_at: `2026-03-27`
- status: `active`
- related_signals:
  - Freely 当前已经把 `pre-tests.md` 写成 issue-level acceptance 控制面，但 closeout/retire 仍可能在没有真实环境证据的情况下发生，说明 gate 还没有真正消费 `pre-tests.md`
  - OAuth slot sweep 这类能力在真实环境里暴露出 `codex exec` 和 `curl` 走的是两套网络语义，其中 `codex` 路径甚至仍带 `http://127.0.0.1:7890` 硬编码
  - Freely 未来会有前端配置面，因此代理、网络出口和测试验收状态都不应只埋在 shell 实现里，必须有可配置、可恢复、可 machine-readably 消费的项目能力面

## Problem

这次不是两个独立小问题，而是同一类产品化缺口的两个表现：

1. `pre-tests.md` 仍主要是“写出来供人阅读”，还不是 completion / merge / worktree retirement 的强门禁输入。
2. runtime 网络配置还没有成为 Freely 的统一能力，导致不同执行路径各自偷偷继承或硬编码代理语义。

最终结果是：

- 真实环境测试要求容易变成摆设，因为 gate 不知道该检查哪个 issue 的哪些验收项、证据是否足够、证据等级是否满足
- 同一个项目里，`codex exec`、`curl`、watchdog、status、switch 可能走不同代理路径
- 前端以后即使想提供“代理配置”界面，也找不到一个单一真源去读写

## Current Truth

### 已经存在但还不够的 pre-tests 真源

1. `story-level-pre-tests-quality-gate-governance`
- 已冻结：`pre-tests.md` 最低质量线，要求 acceptance target / testing layer / target environment / required evidence / blocker taxonomy
- 未冻结：如何把 issue 绑定到自己的 `pre-tests.md`，以及如何把验收状态和证据等级变成 machine-readable completion gate

2. `ibm-pretests-executable-acceptance-quality-governance`
- 已冻结：对 Freely 自治能力，集成、真环境、端到端狗粮默认都应成为必答面
- 未冻结：如何产出 artifact、如何判断 real-env 是否真的跑过、如何阻止“mock 过了就 closeout”

3. `pre-test-merge-responsibility-usage-and-lifecycle-governance`
- 已冻结：worktree/test batch 的生命周期边界
- 未冻结：retirement 前如何强制检查 pre-tests evidence completeness

### 已经存在但还不够的配置真源

1. `.freely/config.env`
- 已是项目级 runtime 配置真源
- 目前承载 AI tool / model / cadence / restart 等字段
- 现在已吸收 project-scoped proxy config defaults，但其他 active worktree 仍需跟进新的 completed gate 后再进入 closeout

2. runtime network resolver
- 现在已在 dedicated proxy lane materialize 为统一 resolver
- 目标是让 `codex exec`、`curl`/OAuth、watchdog 与 future tooling launcher 共用同一组 `inherit` / `explicit` / `disabled` 语义

## Desired Outcome

形成两条可衔接的 Freely 能力线：

### 能力线 A：pre-tests acceptance gate

让 `pre-tests.md` 不再只是“文档写没写够”，而变成：

- 每个 active issue 都能显式绑定自己的 `pre-tests.md`
- gate 只检查当前 issue 的 acceptance contract，而不是扫描全仓库所有 `pre-tests.md`
- 每条 acceptance 都有 machine-readable 状态、证据等级、证据落点
- 未满足 real-env 的 issue 不能被宣称 `completed`，也不能退休 worktree

### 能力线 B：project-scoped network proxy capability

让代理配置不再埋在 shell 补丁里，而变成：

- 项目级 Freely 配置的一部分
- 同时服务 `codex exec`、`curl`、watchdog、status、switch、future frontend
- 支持地址、端口、完整 URL 或禁用模式，而不是写死 localhost:7890
- 后续 UI 只需要读写同一份 Freely config，就能驱动全部网络调用

## Tensions

1. 不能让 gate 去“扫描所有 `pre-tests.md`”；必须从当前 issue 出发找到唯一绑定的 `pre-tests.md`
2. 不能把 pre-tests 直接变成纯 JSON schema，否则会和现有 IBM/doc-loop 断层；更现实的是先在 Markdown 中冻结 machine-readable 最小字段，再补 artifact manifest
3. 不能让代理配置只服务 Codex；Freely 未来会编排更多 tooling，网络出口应是 project-scoped capability，而不是 codex 私货
4. 不能把代理默认值继续硬编码在实现里，否则前端再做配置面仍然会被底层实现绕开

## Working Hypothesis

### A. pre-tests gate 的最小可执行结构

最小链路应该是：

`issue -> pre_tests_path -> verification_artifact_dir -> gate verdict`

其中：

- issue 文档显式声明 `pre_tests_path`
- `pre-tests.md` 以固定 acceptance item 记录：
  - `id`
  - `requirement`
  - `evidence_level`
  - `status`
  - `artifact_ref`
- 真实验证命令产出 `.freely/verification/<issue-id>/...` 之类的 artifact
- gate 根据 issue phase transition 和 worktree retirement 动作去检查这个 artifact 面

### B. 代理配置的最小可执行结构

最小 contract 应该是项目级配置先行，例如在 `.freely/config.env` 中冻结：

- `FREELY_NETWORK_PROXY_MODE`
  - `inherit`
  - `explicit`
  - `disabled`
- `FREELY_NETWORK_PROXY_URL`
- `FREELY_ALL_PROXY`
- `FREELY_HTTP_PROXY`
- `FREELY_HTTPS_PROXY`
- `FREELY_NO_PROXY`

然后由一个统一 resolver 负责：

1. 从项目配置读出网络策略
2. 归一化生成执行环境变量
3. 同一套注入到 `codex exec`、`curl`、watchdog probe、OAuth sweep、future tooling launcher

这样前端未来只需修改 `.freely/config.env` 或其等价 managed surface，不必知道脚本内部调用细节。

## Concrete Questions

1. `pre-tests` gate 是应作为 `story-level-pre-tests-quality-gate-governance` 的 follow-on，还是新 issue 专门处理 machine-readable binding + retirement gate？
2. issue 文档里是否需要新增固定字段：
   - `pre_tests_path`
   - `verification_artifact_dir`
3. gate 应卡哪些时机最合理：
   - `phase_state -> completed`
   - merge 到 `develop`
   - worktree retirement
4. 代理配置字段是直接进 `.freely/config.env`，还是补一层 `network.env` / structured config 再由 `config.env` 指向？
5. 对未来前端来说，哪种形态最稳：
   - 继续使用 env 风格键值对
   - 增加结构化配置文件，但保持 env 兼容镜像

## Likely Landing Zones

- `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/*`
- `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/**`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/**`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`

## Initial Direction

这条研究入口现在已经拆成两条后续生命周期：

1. `I-20260327-0701` 负责 issue-bound pre-tests evidence gate，并已先把 `phase_state=completed` 的第一阶段 gate 合入 `develop`
2. `I-20260327-0651` 负责 project-scoped network proxy configuration and launcher inheritance，并在当前 lane 继续推进实现、验证与 closeout

## Status Reconcile

- reconcile_status: `deferred_split`
- why: `这条预研把 pre-tests gate 愿景和 network proxy capability 放在同一入口里；后续 owner 已经把两条能力拆开推进，因此“completion / merge / retirement 全链一次性落地”不再是当前 owner 的真实承诺。`
- stale_statement:
  - `把 completion / merge / retirement 全链门禁与 project-scoped network proxy capability 继续当成同一个 earliest owner 的已承诺范围。`
- canonical_truth:
  - `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- deferred_scope:
  - `retirement auto-check / cleanup followthrough gate 是 follow-on owner scope；即使后续已有独立 owner，也不应回写成最早 pretests gate owner 已完成范围。`
  - `network proxy capability 仍由独立 owner 继续推进，不能把其未完成面误报成 pre-tests gate regression。`
- follow_on_owner:
  - `docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- reconcile_note: `此条仍保留原始愿景的产品化价值，但后续评审必须按拆分后的 owner 边界判断“已完成”“deferred”“另案推进”，而不是拿混合入口去要求单一 owner 覆盖全部能力。`

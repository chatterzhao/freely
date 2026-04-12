# Brainstorm - 20260411-1414--launch-time-verification-contract-hard-gate

一句话范围：本预研只处理 launch-time verification contract 的硬门禁缺口，目标是把晚门禁问题前移到 manager dispatch 时刻，不在本条预研里扩展到 adequacy schema 全量升级或 cleanup/retirement 自动化。

## Problem

Freely 已经把 `pre-tests.md` 定义为 issue 的测试真源，也已经在 `pretests-gate` 与 develop merge 路径中消费该真源；但 worker launch 入口仍允许缺 verification metadata 的委派继续执行。结果是：

1. 规则在文档层很强，执行层在 launch 时仍放宽。
2. 问题经常在 completion/merge gate 才被拦截，形成晚门禁体验。
3. manager/worker handoff 不能稳定恢复本轮最小测试契约，导致“跑了测试”与“跑够测试”混淆。

## Confirmed Facts

1. 顶层真源并不缺测试要求：
   - 宪法/法律/IBM 体系已要求 issue-bound `pre-tests.md` 承载成功标准与测试任务，并随开发推进持续补全。
   - 项目当前不引入并行 `tests.md`，`pre-tests.md` 就是同一份逐步补全的测试真源。
2. `test-pre-merge-* -> develop` 的 merge gate 已消费 owner issue 绑定的 `pre-tests.md`，不是“没有门禁”。
3. runtime 在 launch 处会解析 verification metadata，并记录 `VERIFICATION_METADATA_MISSING_FIELDS`。
4. 但 runtime 当前不会因 missing fields 拒绝 worker launch，缺口只被记录，不被前置阻断。
5. 现有测试也主要验证“能解析并记录缺字段”与“自然语言 prompt 仍可 launch”，而不是“缺字段必须拒绝 launch”。

## Why This Is Not An AGENTS/Constitution/Laws Prompting Gap

本问题更接近执行层 materialization 缺口，而不是提示不足：

1. 上层规范已经给出清晰方向：`pre-tests.md` 单一真源、lane 约束、merge/completion 门禁。
2. 当前失败模式发生在 launch-time enforcement：有 contract 语义，但未形成硬阻断。
3. 因此改进重点应放在 runtime/manager dispatch 入口，而不是继续加提示文案。

## Current Runtime Gap (Launch-Time)

当前行为是：

1. manager prompt 被解析后，runtime 提取 worktree/branch 与 verification metadata。
2. 若 verification metadata 不完整，runtime 记录 missing fields。
3. worker 仍被 launch，后续再依赖 gate 或人工评审纠偏。

这使得“执行前 contract 校验”缺位，无法把风险前移到最早可判定节点。

## Minimal Correct Design

第一阶段只做 launch-time hard gate，最小正确设计如下：

1. manager dispatch 前置检查 verification contract 必填字段。
2. 任何必填字段缺失时，拒绝 launch worker，并返回 machine-readable missing-fields 诊断。
3. 保留现有 missing-fields 写入状态能力，支持恢复与审计。
4. 对字段完整的 prompt 保持现有成功 launch 路径，不引入行为回退。
5. 坚持单一真源：不新增 `tests.md`，继续消费 issue-bound `pre-tests.md`。

建议的最小必填集合：

- `Owner-Issue`
- `Pre-Tests-Path`
- `Verification-Artifact-Dir`
- `Required-Test-Lanes`
- `Required-Acceptance-Item-Ids`
- `Minimum-Evidence-Level`
- `Target-Environment`
- `Closeout-Gate`

## Non Goals

1. 不在本 owner 首阶段扩展 `pretests-gate` 到完整 adequacy item schema（`surface_kind`/`target_lane`/`case_design` 等）。
2. 不在本 owner 同时实现 cleanup/retirement 的 `pre-tests.md` 自动门禁。
3. 不新增第二份测试真源文档（如 `tests.md`）。
4. 不把 merge/completion gate 语义重写为 launch-time 语义；本条只补 launch 入口硬门。

## Possible Landing Zones

1. Runtime launch path：
   - `docs/system/workspace/scripts/runtime/freely`
2. Manager/worker contract truth：
   - `docs/system/workspace/agents/manager-agent.md`
   - `docs/system/workspace/agents/worker-agent.md`
3. Lead/dispatch script contract sink：
   - `docs/system/workspace/scripts/start-lead-agent.sh`
4. Tests：
   - `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
   - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
   - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`

## Owner Candidates

建议主 owner 与 follow-ons 分离，避免 scope 膨胀：

1. 主 owner：`launch-time-verification-contract-hard-gate-governance`
   - 目标：缺 verification metadata 即拒绝 launch，完整 metadata 保持现有成功路径。
2. follow-on A：`pretests-adequacy-item-schema-materialization-governance`
   - 目标：把 richer adequacy 字段接入 gate 可执行层。
3. follow-on B：`pretests-cleanup-retirement-enforcement-governance`
   - 目标：把 cleanup/retirement 统一纳入 `pre-tests.md` 消费链。

## Recommendation

建议立刻 materialize 主 owner，并在 dedicated feature worktree 上先落 launch-time hard gate。该方向收益最高、范围最窄，且最符合“不要功能回退”的执行约束。

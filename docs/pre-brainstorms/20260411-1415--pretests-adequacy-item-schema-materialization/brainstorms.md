# 预研头脑风暴：pretests-adequacy-item-schema-materialization

## 一句话范围

把 `pre-tests.md` 的 adequacy item 从“最小结构可过门”升级到“可判定是否跑够”，并保持单一真源，不引入新的 `tests.md` 平行文档。

## 问题陈述

当前治理链已经把 `pre-tests.md` 定义为 issue 的测试真源，但可执行 gate 仍主要消费最小字段五件套：

- `id`
- `requirement`
- `evidence_level`
- `status`
- `artifact_ref`

这能判断“有没有跑、有没有证据”，却不能稳定判断“是否覆盖了该 issue 在该 lane 的必需测试面”，导致：

- `run some tests` 与 `run enough tests` 在 gate 侧无法区分
- manager/worker 可以在正确 lane 上执行，却仍然在 adequacy 上欠账
- 风险经常推迟到 merge followthrough 或 dogfood 才暴露

## 现状与事实

1. richer schema 诉求已经在预研与 owner 里出现，典型字段包括：
   - `surface_kind`
   - `target_lane`
   - `promotion_gate`
   - `task_refs`
   - `case_design`
2. 当前 gate 实施面仍以最小五件套为主，尚未把上述 richer 字段纳入 machine enforcement。
3. lane 路由与分支模型已存在，但 lane 合法不等于 adequacy 充分。
4. 本项目明确 `pre-tests.md` 是“提前写成功标准并持续补全”的唯一文件，不再增加 `tests.md` 冗余面。

## 根因判断

问题不是顶层缺“测试重要”的表述，而是 contract materialization 的阶段性缺口：

1. 文档先定义了 richer adequacy contract。
2. 可执行 gate 只 materialize 了最小闭环。
3. 结果是结构可校验、充分性不可判定。

## 目标

1. 保持 `pre-tests.md` 单一真源，不新增并行测试文档。
2. 让 acceptance item 可表达“为何该项足够支持当前 promote/closeout 决策”。
3. 让 gate 至少能区分：
   - 未跑
   - 跑了但不够
   - 跑够并有证据
4. 采用渐进升级，避免一次性打爆历史 owner。

## 非目标

1. 不在本条预研中重做 runtime 调度或 worker 启动逻辑。
2. 不要求一次迁移全仓历史 `pre-tests.md`。
3. 不把 gate 变成自动设计测试计划的系统。
4. 不引入 `tests.md`、`acceptance-tests.md` 等第二真源。

## 渐进升级策略

### Phase 0 - Schema 冻结与兼容声明

1. 冻结 adequacy item v2 字段集：
   - 必选仍保留最小五件套
   - 新增字段先声明为可选但建议
2. 明确兼容策略：
   - 旧 item 不立刻失败
   - 新 owner/新 issue 先按 v2 写

### Phase 1 - 诊断先行，不阻断

1. gate 新增 adequacy diagnostics：
   - 缺 `surface_kind`/`target_lane` 等 richer 字段给 warning
   - `promotion_gate` 与当前 lane 不匹配给 warning
2. 输出 machine-readable 分类，便于 review 与 followthrough 消费。

### Phase 2 - 面向新 owner 的软强制

1. 对新 materialized owner（按 issue 时间窗或显式标记）要求 v2 字段完整。
2. 老 owner 保持 warning，不立即 hard fail。

### Phase 3 - 核心字段硬门禁

1. 对 develop-bound promote 的 required items，硬要求：
   - `surface_kind`
   - `target_lane`
   - `promotion_gate`
2. `task_refs`/`case_design` 先保持强建议，待样本稳定后再评估硬化。

## 建议的 adequacy item v2 语义

1. `surface_kind`
   - 描述测试面：`unit`/`integration`/`end_to_end`/`real_environment`/`post_merge_followthrough`
2. `target_lane`
   - 声明该 item 计划在哪条 lane 执行：`feature-local`/`premerge-integration`/`post-merge-followthrough`
3. `promotion_gate`
   - 说明该 item 用于哪个门：`completion`/`develop_merge`/`retirement`
4. `task_refs`
   - 绑定 issue 的任务/验收条目 id，减少“测试项与任务脱节”
5. `case_design`
   - 最小可执行描述（前置条件、动作、预期信号），减少“标题式测试”

## Landing Zones

1. `docs/system/workspace/scripts/quality/pretests-gate`
   - 增加 v2 字段读取、诊断与阶段化强制逻辑
2. `docs/system/workspace/scripts/quality/governance-merge-gate`
   - develop promote 场景下消费 adequacy 判定结果
3. `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
   - 固化 `pre-tests.md` item v2 写作要求
4. `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
5. `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
6. `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
7. `docs/system/workspace/scripts/tests/test-pretests-gate`
8. `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## 后续 owner 候选

1. `pretests-adequacy-item-schema-materialization-governance`
   - owner 主责：把 v2 schema 从文档诉求 materialize 到 gate 可执行语义
2. `pretests-adequacy-derivation-and-lane-binding-governance`
   - follow-on：加强 `task_refs` 与 lane 派生一致性
3. `pretests-cleanup-retirement-adequacy-governance`
   - follow-on：把 adequacy item 与 retirement gate 串联

## 风险与控制

1. 风险：一次性硬化导致历史 issue 大面积失败。
   - 控制：分 phase 上线，先 warning 后 hard fail。
2. 风险：字段增加但语义漂移成样板文字。
   - 控制：`case_design` 采用最小结构模板并配回归样例。
3. 风险：并行引入第二测试真源。
   - 控制：明确禁止新增 `tests.md`，所有成功标准继续沉淀于同一份 `pre-tests.md`。

## 结论

这条预研应进入 owner materialization。它解决的是“充分性不可判定”而非“有没有测试文档”，并且能在不回退现有流程的前提下，渐进收紧 `pre-tests.md` 的 machine-enforce 质量线。

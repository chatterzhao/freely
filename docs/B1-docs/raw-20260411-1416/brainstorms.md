# 预研头脑风暴：pre-tests cleanup/retirement enforcement

## 背景与问题

Freely 已经把 `pre-tests.md` 作为 IBM 阶段的成功标准与测试任务真源；随着开发推进，这份文档会持续补全直到形成完整测试任务集。

当前状态存在一个结构性不一致：

- `completed` 前的 issue 级证据检查已具备（`pretests-gate`）
- `test-pre-merge-* -> develop` 的 guarded merge 已消费 owner `pre-tests.md`
- 但 `cleanup_governance` / `retire_worktree` 仍未统一消费同一份 `pre-tests.md`

这导致 completion 与 merge 可以被较强约束，但 cleanup/retirement 仍可能主要依赖流程信号与人工裁决，未形成同一测试真源驱动的闭环。

## 已确认事实（来自既有预研与 owner）

1. 早期预研已明确提出“`pre-tests.md` 不应只用于可读文档，应进入 completion / merge / retirement gate”：
- `docs/B1-docs/20260327-0651--pretests-gate-and-network-proxy-config/brainstorms.md`

2. owner `pre-tests-evidence-binding-and-completion-gate-governance` 明确只先实现 completion gate，并把 retirement auto-check 设为后续：
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/prd.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/pre-tests.md`

3. merge 侧 gate 已对 `test-pre-merge-* -> develop` 消费 owner `pre-tests.md`：
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/quality/pretests-gate`

4. cleanup lifecycle 真源已强调“completed 不等于 lifecycle closed”，retire 需要 cleanup evidence 与 closure：
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`

## 结论：这是“真实缺口 + 明确 deferred”，不是回退

该缺口为真实缺口，因为系统还没有把 cleanup/retirement 的可判定条件统一绑定到 owner `pre-tests.md`。

该缺口也是明确 deferred，因为既有 owner 的 PRD 与 pre-tests 已把 retirement auto-check 排除在当前批次之外，属于分阶段 materialization 策略，而非规则失效或功能回退。

## 最小正确设计（本预研建议）

目标是“统一消费同一份 `pre-tests.md`”，不是新增 `tests.md` 或平行测试真源。

最小能力边界：

1. 增加 `pretests-retirement-gate`（名称可在 owner 固化）
- 输入：`--project`、`--issue`、`--worktree-path`、`--retire-intent`
- 来源：仅读取 issue 绑定的 `pre_tests_path`
- 判定：对 cleanup/retirement 所需 acceptance items 与 evidence level 做 machine-readable 检查

2. cleanup/retirement 路由接入点
- `cleanup_governance` 做 retire decision 前调用该 gate
- `retire_worktree` 执行前再次检查（防止 stale state）

3. 判定输出要求
- machine-readable 错误码（例：`pretests_retirement_blocked`、`acceptance_item_pending`）
- 缺口定位到 item id，避免仅返回文本失败

4. 兼容策略
- 先支持最小字段集合，不在第一批强推 adequacy schema 扩展
- 不破坏现有 completion gate 与 merge gate 行为

## 与 worktree retirement / fleet closure 的关系

该能力不是单独测试规则，而是 `auto-loop` cleanup closure 的输入真源补齐。

- 若 completion/merge 已通过但 cleanup gate 失败，tree 进入 retained/followthrough，而非直接 retirement
- fleet closure 需要能区分“可删树”与“证据未闭环不可删树”，并能追溯到 owner `pre-tests.md` item 缺口
- 对 `test-pre-merge-*`，rebuild/retire 的治理决策也应引用同一测试真源，避免 stale batch 被误当作完成态

## 非目标（首批明确排除）

1. 不新增 `tests.md` 或其他平行测试契约文件
2. 不在本批次同时完成 item-level adequacy schema 全量升级
3. 不在本批次重写 manager/worker 全链路 dispatch contract
4. 不做全仓扫描式 pre-tests 审计，仍坚持 issue-bound 单一绑定

## Landing Zones

实现与真源落区建议：

- gate 脚本：`docs/system/workspace/scripts/quality/`
- hook/入口胶水：`docs/system/workspace/hooks/` 与 runtime cleanup route
- 生命周期真源：`docs/system/workspace/three-loop-capability-lifecycle.md`
- cleanup 技能真源：`docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- owner 文档：`docs/epics/workspace-routing-foundation/<new-owner>/`

## 后续 owner 候选

首选 owner 名称建议：

- `pre-tests-cleanup-and-retirement-enforcement-governance`

该 owner 的 phase-1 验收建议：

1. cleanup/retirement 前必须消费 issue-bound `pre-tests.md`
2. gate 失败时禁止 retire，并写 machine-readable 缺口
3. 不引入 `tests.md`，不改变 `pre-tests.md` 作为唯一测试真源的原则
4. completion/merge 现有 gate 不回退

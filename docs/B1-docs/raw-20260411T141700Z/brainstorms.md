# Brainstorm - 20260411-1417--stale-prebrainstorm-truth-reconcile

一句话范围：本预研只处理 pre-brainstorm 与 canonical truth 漂移导致的审计误判问题，目标是建立最小纠偏策略，不做全仓文档大清洗。

## Problem

当前多条 pre-brainstorm 在后续 owner issue、gate 脚本、hook、测试落地后，局部陈述已经过时。  
过时文本会把后续审计导向错误结论，例如把“已落地但文档未更新”误判成“门禁未实现”，或把“明确 deferred 的能力”误判成“实现回退”。

这会直接影响三类治理判断：

1. 错误立项：重复创建已经有 owner 或已闭环的工作
2. 错误归因：把执行层硬约束缺失归咎为顶层规则没写
3. 错误排期：把应先做的 runtime/gate hardening 让位给低价值文档重写

## Scope

1. 明确哪些 pre-brainstorm 里的具体陈述已被 canonical truth 推翻或淘汰
2. 解释 stale truth 如何误导审计与治理决策
3. 定义最小正确修复原则：
   - 只改被 canonical truth 明确推翻的旧描述
   - 不改仍属开放探索或明确 deferred 的段落
4. 给出 landing zones 与后续 owner 候选
5. 保持 `pre-tests.md` 单一命名，不引入 `tests.md` 冗余面

## Out Of Scope

- 不在本条预研中直接改 runtime、hook 或 quality gate 逻辑
- 不做 pre-brainstorms 全量风格统一或历史术语重写
- 不把已拆分 owner 的 deferred scope 强行回填到当前 owner
- 不做 `docs/B1-docs/raw-INDEX.md`、`docs/milestones.md` 或其他共享索引的批量重写；若 owner materialization 依规范必须追加注册条目，只允许最小 append

## Confirmed Stale Or Superseded Statements

### 1) `20260408-1205--verification-contract-and-premerge-adequacy`

- 过时点：文档写到 merge gate 不会在 `test-pre-merge-* -> develop` 路径消费 `pre-tests.md`
- canonical truth：
  - `.githooks/pre-merge-commit` 路由到 `docs/system/workspace/hooks/pre-merge-commit.sh`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`
- 结论：该陈述已被实现与回归测试推翻

### 2) `20260406-0055--governance-check-nested-test-pre-merge-receipt-audit`

- 过时点：被当作持续开放问题使用
- canonical truth：预研自身已记录“fix absorbed, no independent follow-on needed”
- 结论：该条应视为历史收敛，不应继续作为活跃缺口输入

### 3) `20260327-0651--pretests-gate-and-network-proxy-config`

- 易误读点：早期文字同时提 completion/merge/retirement 全链门禁愿景
- canonical truth：后续 owner 明确将 retirement auto-check 作为 deferred
- 结论：不是实现回退，而是 owner 边界收窄；若不标注会被误解为“门禁失效”

### 4) `20260405-1615--feature-owned-test-pre-merge-family`

- 易误读点：把 family lifecycle automation 视作已完成范围
- canonical truth：后续 owner 只先落 promote model 与 promotion gate enforcement，automation 仍是 follow-on
- 结论：该条属于“拆分后部分 materialized”，不是“被静默删除”

## Boundary Of Terms

为避免把本次 reconcile 演化为“全仓大清洗”，本预研固定三类标签边界：

1. `stale`
   - 条件：原文描述已不代表当前事实，但问题方向仍可能有效
   - 动作：补状态注释与 canonical pointer，不重写整篇
2. `superseded`
   - 条件：原文关键判断已被 owner/gate/hook/tests 明确推翻
   - 动作：标注 superseded，并指向最新 canonical truth
3. `deferred`
   - 条件：能力未实现且后续 owner 明确声明延期或拆分
   - 动作：保留原始愿景，补 deferred owner pointer，不得写成“已完成”或“已失效”

判定优先级：

1. 若有可验证实现证据且与原文冲突，标 `superseded`
2. 若无实现证据但有 owner 明确延期边界，标 `deferred`
3. 其余仅标 `stale`，禁止扩大解释

## Why Stale Text Misleads Governance

1. 审计阶段会把旧描述当现状，导致重复验证和错误 escalation
2. manager/worker 在 pre-research 引导中会吸收错误约束，导致 lane 选择和 owner 归属偏移
3. 容易把“文档旧”误报成“hook 没启用”或“gate 未触发”
4. 会制造“预研被打折扣”的泛化叙事，掩盖真实高优先级缺口
   - 真实缺口通常是 launch-time enforcement 与 adequacy materialization，不是提示层缺字

## Minimal Correctness Principle

只做“truth reconcile”，不做“history rewrite”。

1. 必须存在可验证 canonical truth 才允许改旧描述：
   - owner issue / PRD / pre-tests
   - runtime/hook/gate 真源代码
   - 对应 regression test
2. 修改方式以“加状态注释 + 指向 canonical truth”为主，避免重写整篇
3. 对明确 deferred 的内容必须保留并标注 deferred owner，而不是删除
4. 不改变 `pre-tests.md` 的命名体系，不引入平行 `tests.md`

## Landing Zones

1. `docs/B1-docs/raw-<id>/brainstorms.md`
   - 优先在被推翻段落旁追加 `Status Reconcile` 小节；若原文跨度过长且集中补注更清晰，可在文末集中追加并显式指回 stale statement
2. `docs/B2-docs/.../issues/*.md` 或 `prd.md`
   - 当 pre-brainstorm 引述 owner 状态错误时，补 canonical pointer
3. `docs/system/workspace/scripts/quality/*` 与测试脚本
   - 仅作为事实引用来源，不在本条 reconcile owner 中改逻辑
4. 仅在必要时新增轻量“reconcile receipt”到对应 pre-brainstorm 目录，避免共享索引大范围漂移

## Non-Goals For First Materialization

1. 不做一次性批量修复所有历史 pre-brainstorms
2. 不创建“自动扫描全仓并自动改文档”的机制
3. 不把 reconcile owner 与 runtime/gate hardening owner 混合实现
4. 不将 `pre-tests.md` 拆分成多个并行命名产物

## Follow-on Owner Candidates

1. `stale-prebrainstorm-truth-reconcile-governance`
   - 负责建立 reconcile 规则、优先队列和最小变更模板
2. `launch-time-verification-contract-hard-gate-governance`
   - 处理真实高优先级执行缺口，避免把 stale 文档问题替代成主修复目标
3. `pretests-adequacy-item-schema-materialization-governance`
   - 承接仍未完整 materialize 的 adequacy contract
4. `pretests-cleanup-retirement-enforcement-governance`
   - 承接 completion/merge 之后的 retirement gate 空档

## Status Reconcile

- `C-20260411T141700Z-B` is absorbed into `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md` as the canonical verification-contract chain for the same launch-time adequacy concern.
- Keep this brainstorm narrow on stale-truth reconcile; do not reopen a separate launch-time execution owner from this lane.

## Verification Plan

1. 为每个候选 stale 条目建立三点证据：
   - stale statement
   - canonical truth pointer
   - reconcile action
2. 对每个 reconcile 变更执行文本回归检查：
   - 不移除 deferred 语义
   - 不引入新能力承诺
   - 不改变 owner 边界
3. 人工 spot-check：
   - 至少覆盖 1 条“已实现但文档旧”
   - 至少覆盖 1 条“明确 deferred”
   - 至少覆盖 1 条“已吸收关闭”

## Materialization Readiness

ready_for_materialization: `yes`

理由：

1. 问题边界已固定为 truth reconcile，不混入 runtime/gate 行为改动
2. `stale / superseded / deferred` 判定规则已明确，且有优先级
3. 非目标和 landing zones 已限制在最小可执行范围
4. 已给出独立 follow-on owner，避免把高优先级执行缺口塞入同一 owner

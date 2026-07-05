---
b1_id: B1-20260629T025659Z
phase_state: completed
source_raw: raw-20260629T025659Z
source_url: https://github.com/chatterzhao/freely/issues/3616
produced_candidate: C-20260629T025659Z-A
created_at: 2026-06-29
---

# B1_IBM: 统一 fix skill 与 feature skill 的治理顺序

## Discovery
- 提出时间: 2026-06-29，issue 创建不到 1 天，时效性高
- 未被其他 candidate/issue 覆盖，是独立的新问题
- 项目当前处于活跃开发阶段，流程改进直接提升后续所有开发质量
- 价值确认: ✅ 值得投入。统一 fix/feature 流程是架构级改进，影响所有后续工位

## Input
- 来源: raw-20260629T025659Z (GitHub #3616, Gitee IJXH20)
- 当前 fix skill 流程: `wt-create → dev → test → B1 → B2 → pr`
- 当前 feature skill 流程: `wt-create → B1 → B2 → dev → test → pr`
- three-loop 真源定义的 Fix 变体路径（§变体路径）: 治理后置

## Problem

fix 采用"Fix first, govern later"（先写代码，后补治理文档）导致：

1. **pre-tests 形同虚设**：代码写完了、测试跑过了，再补 pre-tests 的 test_command。测试计划变成了事后补作业，失去了 TDD 的 RED-GREEN 循环价值。

2. **TDD 无法落地**：dev-loop skill 的情景 D 要求"先跑 RED 再跑 GREEN"——实现前先确实验证测试能失败，再实现到通过。这要求 pre-tests 在写代码之前就存在。fix 的 dev→test→B1→B2 顺序中，dev 阶段根本没有 pre-tests，TDD 无从谈起。

3. **B1 brainstorms 无意义**：修复已完成并验证通过，再补 brainstorm 分析根因、评估替代方案，只是走形式。决策应该在修之前做。

4. **code-review 缺少决策记录**：B2 的 Implementation Decision Note 记录"为什么选这个方案，考虑过哪些替代"，这些决策应该在实现前完成，而非事后补。

5. **test-pre-merge cherry-pick 机制复杂**：fix 场景 B 在 test 工位写代码 → cherry-pick 到 fix 工位 → 再补治理。如果 B1/B2 先做，fix 工位直接开发，test-pre-merge 回归纯验证角色，不需要 cherry-pick 跳舞。

6. **fix 和 feature 的不一致导致 skill 引导混乱**：用户和 AI 需要记住两套不同的流程，增加认知负担和出错概率。

核心矛盾：**文档治理不是开发的敌人，而是质量保证的盟友**。即使是简单 fix，先想清楚再动手，比动手后再补文档更高效、更可靠。

## Brainstorm

### Option A: 保持现状（fix 治理后置）
- 优点：快速修复可立刻写代码，不用等 B1/B2
- 缺点：pre-tests 失去意义，TDD 无法落地，brainstorm 走过场
- 适用场景：一行修 bug
- 评估：即使是简单 fix，先分析根因再写测试再修代码，质量远高于"先修了再说"

### Option B: 统一为 B1 → B2 → dev → test（与 feature 一致）
- 优点：
  - pre-tests 在 dev 之前就存在，TDD 的 RED-GREEN 循环可以真正执行
  - B1 根因分析指导修复方向，不修表面症状
  - B2 Implementation Decision Note 留下可追溯的决策记录
  - test-pre-merge cherry-pick 机制可以去掉，回归纯验证角色
  - fix 和 feature 流程一致，降低认知负担
- 缺点：简单 fix 也需要写 B1/B2 文档
- 应对：fix 的 B1/B2 比 feature 轻量——不需要全面发散，只需根因分析+修复方案评估；不需要完整 prd，只需 pre-tests

### Option C: 根据 fix 复杂度分级
- 简单 fix（<5 行）→ 跳过 B1/B2，直接 dev
- 中等 fix → B2 only（写 pre-tests，跳过 B1）
- 复杂 fix → B1 + B2 完整流程
- 缺点：引入主观判断（"什么是简单 fix"），门禁无法区分，会变成绕过借口

## Decision: Option B — 统一为 B1 → B2 → dev → test，与 feature 完全一致

理由：
1. 治理文档在开发之前，是质量保证，不是额外负担
2. fix 和 feature 的 B1/B2 要求完全相同——相同的结构、相同的深度、相同的门禁
3. 去掉 test-pre-merge cherry-pick 机制，简化实现
4. 两个 skill 流程一致，降低认知负担

fix 和 feature 的唯一合理差异：
| 维度 | fix | feature |
|------|-----|---------|
| 分支前缀 | `fix/*` / `hotfix/*` | `feature/*` |
| hotfix 路径 | 有（从 main 创建，合并到 main + develop） | 无 |

除此之外，B1/B2/dev/test 的流程、深度、门禁完全一致。不存在"fix 的 B1 可以简单写"——根因分析不到位，修复方案评估不充分，和 feature 的预研不充分一样，都是质量问题。

去掉的机制：
- test-pre-merge 写代码 → cherry-pick 到 fix 工位
- "Fix first, govern later" 哲学
- "fix 的 B1/B2 是轻量版"的错误观念

波及文件：
1. `~/.claude/skills/freely-fix-execution/SKILL.md` — 重写流程顺序
2. `~/.claude/skills/freely-test-execution/SKILL.md` — fix 流程序列
3. `~/.claude/skills/freely-feature-execution/SKILL.md` — 分工表
4. `docs/system/workspace/three-loop-capability-lifecycle.md` — Fix 变体路径
5. `AGENTS.md` — 流程序列 + Bug修复章节
6. 项目级 skill 副本（6 个文件）

## Candidate
- candidate_id: C-20260629T025659Z-A
- status: promoted
- milestone: M-20260629T025659Z-A

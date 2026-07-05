# Brainstorms - 20260327-1003--prebrainstorm-materialization-audit

## Context
- Source: 2026-03-27 对 `docs/B1-docs/raw-*` 与 `docs/milestones.md` 的全量交叉审计
- Goal: 只记录“不正常”的 pre-brainstorm -> candidate -> milestone materialization 漂移；正常项不重复登记
- Scope checked: 114 个 `docs/B1-docs/raw-*` 目录
- Audit rule:
  - 已 `promoted` / `materialized` 的 candidate，必须在 `docs/milestones.md` 中可见其 resulting issue 或明确 candidate handoff
  - 已绑定 milestone 的 `needs_research` / `proposed` / `candidate`，必须继续留在对应 milestone 的 `candidate_issues`
  - pre-brainstorm 文档自身的 `status`、`promoted_issue_path`、`milestone` 不能互相打架
  - 旧格式候选如果仍是 active，也不能继续停留在 `pending://milestone-binding`
  - 旧格式 `done` 条目若没有正式 milestone / issue 归档，也视为未完成的治理债，而不是“正常完成”

## Findings

### A. 已绑定 milestone，但 candidate 没有继续留在 `candidate_issues`

1. `docs/B1-docs/raw-20260320-0052/candidates.md`
- candidate: `C-20260320T005200Z-A`
- current state: `status=needs_research`，`milestone=docs/milestones.md#m-20260306-workspace-routing-foundation`
- anomaly: milestone 已绑定，但 `docs/milestones.md` 中没有这条 candidate 的可见队列项
- impact: 研究项会从 active scan 中静默消失，违反 `LAWS 2A/2C` 的 candidate persistence 要求

2. `docs/B1-docs/raw-20260320-0120/candidates.md`
- candidate: `C-20260320T012000Z-A`
- current state: `status=needs_research`，`milestone=docs/milestones.md#m-20260306-workspace-routing-foundation`
- anomaly: 已绑定 milestone，但未出现在 `candidate_issues`

3. `docs/B1-docs/raw-20260320-1745/candidates.md`
- candidate: `C-20260320T174500Z-A`
- current state: `status=candidate`，`milestone=docs/milestones.md#m-20260306-workspace-routing-foundation`
- anomaly: 已明确属于 `workspace-routing-foundation`，但 milestone 队列缺席

4. `docs/B1-docs/raw-20260325-0333/candidates.md`
- candidate: `C-20260325T033300Z-A`
- current state: `status=proposed`，`milestone=docs/milestones.md#M-20260306-workspace-routing-foundation`
- anomaly: umbrella candidate 仍在继续研究，但 milestone 没有保留它的 candidate 可见性
- note: 同目录下的 `C-20260325T033300Z-B` 已单独 materialize；这更要求 A 条继续保留为后续切口 owner

### B. candidate 已提升 / 已 materialize，但 milestone 没有收入口径

1. `docs/B1-docs/raw-20260324-0415/candidates.md`
- candidate: `C-20260324T041500Z-A`
- current state: `status=promoted`
- promoted issue: `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
- expected: 在 `M-20260306-workspace-routing-foundation` 的 `candidate_issues` 或 `committed_issues` 中可见
- anomaly: `docs/milestones.md` 中不存在该 issue，也不存在对应 `source_candidates`

2. `docs/B1-docs/raw-20260325-0333/candidates.md`
- candidate: `C-20260325T033300Z-B`
- current state: `status=materialized`
- promoted issue: `docs/B2-docs/ibm/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md`
- expected: 在 `M-20260306-workspace-routing-foundation` 中至少以 promoted candidate 或 committed/completed issue 可见
- anomaly: issue 已存在，但 milestone 中没有该 issue，也没有用 `source_candidates` 指回本 pre-brainstorm

3. `docs/B1-docs/raw-20260326-1810/candidates.md`
- candidate: `C-20260326T181000Z-A`
- current state: `status=promoted`
- promoted issue: `docs/B2-docs/config/packaging/issues/freely-layered-architecture-and-tooling-topology.md`
- expected: `docs/milestones.md` 至少存在 `M-20260326-freely-product-architecture`，并收录该 issue
- anomaly: `docs/milestones.md` 中连 milestone section 都不存在，导致 candidate 与 issue 都没有正式编排入口

### C. pre-brainstorm 自身状态漂移，已经指向现有 issue，但字段仍不一致

1. `docs/B1-docs/raw-20260318-2245/candidates.md`
- candidate: `C-20260318-A`
- current state: `promoted_issue_path` 已指向 `checkpoint-commit-and-multi-worktree-supervision-governance`
- anomaly: `milestone` 仍是 `pending://issue-materialization`
- interpretation: 这条线已经被吸收到既有 issue，但 pre-brainstorm 文档没有完成 normalization

2. `docs/B1-docs/raw-20260318-2358/candidates.md`
- candidates: `C-20260318T235800Z-A`, `C-20260318T235800Z-B`
- current state: `status=proposed`，但 `promoted_issue_path` 都已指向 `checkpoint-commit-and-multi-worktree-supervision-governance`
- anomaly: candidate 状态仍停留在 `proposed`，与已存在的 issue 映射冲突；同时 milestone 没有把这份 pre-brainstorm 作为 supporting provenance 挂住
- interpretation: 这里需要决定它们是“absorbed supporting evidence”，还是要重新拆成独立 follow-on candidate

3. `docs/B1-docs/raw-20260318-1630/candidates.md`
- candidate: `C-20260318-A`
- current state: `promoted_issue_path=pending://issue-materialization`，`milestone=pending://milestone-binding`
- anomaly: `docs/milestones.md` 已把这个 pre-brainstorm 作为 `I-20260318T163000Z` 的 `source_candidates`，但 pre-brainstorm 仍像未 materialize
- interpretation: issue 已存在，pre-brainstorm 文档需要补 normalization，避免同一条线同时表现为“已完成”与“未绑定”

### D. legacy active candidates 仍停留在 `pending://milestone-binding`

这类条目不是“正常旧档案”。它们仍是 active candidate，却没有进入任何 milestone 可见队列，违反当前 `candidate persistence` 规则。

1. `docs/B1-docs/raw-20260303-0000/candidates.md`
- candidates: `C-20260303-001`, `C-20260303-002`
- current state: `needs_research`，但 `milestone=pending://milestone-binding`

2. `docs/B1-docs/raw-20260304-0000/candidates.md`
- candidate: `C-20260304-202`
- current state: `proposed`，但 `milestone=pending://milestone-binding`

3. `docs/B1-docs/raw-20260304-0000/candidates.md`
- candidate: `C-20260304-501`
- current state: `needs_research`，但 `milestone=pending://milestone-binding`

4. `docs/B1-docs/raw-20260304-0000/candidates.md`
- candidates: `C-20260304-605`, `C-20260304-607`
- current state: active candidate 仍未绑定 milestone

5. `docs/B1-docs/raw-20260305-0000/candidates.md`
- candidate: `C-20260305-803`
- current state: `needs_research`，但没有正式 milestone queue

6. `docs/B1-docs/raw-20260305-0000/candidates.md`
- candidate: `C-20260305-703`
- current state: `needs_research`，但没有正式 milestone queue

7. `docs/B1-docs/raw-20260306-0016/candidates.md`
- candidate: `C-20260306-002`
- current state: `needs_research`，但没有正式 milestone queue

8. `docs/B1-docs/raw-20260309-1943/candidates.md`
- candidate: `C-20260309T194300Z`
- current state: `proposed`，但没有正式 milestone queue

9. `docs/B1-docs/raw-20260309-2003/candidates.md`
- candidates: `C-20260309T200300Z-A`, `C-20260309T200300Z-B`, `C-20260309T200300Z-C`
- current state: 三条都还是 `proposed`，但没有正式 milestone queue

10. `docs/B1-docs/raw-20260309-2345/candidates.md`
- candidates: `C-20260309T234500Z-A`, `C-20260309T234500Z-B`
- current state: `proposed`，但没有正式 milestone queue

11. `docs/B1-docs/raw-20260310-0056/candidates.md`
- candidates: `C-20260310T005600Z-A`, `C-20260310T005600Z-B`
- current state: active candidate 仍未绑定 milestone

12. `docs/B1-docs/raw-20260320-0512/candidates.md`
- candidate: `C-20260327-parked-worktree-retirement`
- current state: `needs_research`，但仍是 `pending://milestone-binding`

13. `docs/B1-docs/raw-20260321-1835/candidates.md`
- candidate: `C-20260321T183500Z-A`
- current state: `proposed`，但仍是 `pending://milestone-binding`

### E. legacy `done` 条目没有正规 milestone / issue 归档

1. `docs/B1-docs/raw-20260318-1818/candidates.md`
- candidates: `C-20260318-A` 到 `C-20260318-G`
- current state: 全部 `status=done`
- anomaly: 仍停留在 pre-brainstorm 自说自话的 `done`，既不符合当前 `phase_state` 词典，也没有 milestone / owner issue 的正式落点
- interpretation: 需要统一判定这些条目分别应落为 `completed issue evidence`、`absorbed supporting evidence`，还是直接 `dropped`；在完成 normalization 前不能把这一组视为“已经正常结束”

## Refined Analysis

第二轮不是只看 `milestones.md`，而是继续追踪 `milestone -> issue/IBM -> progress/dev -> supporting pre-brainstorm / capability truth`。结论是：上一轮里的“异常”并不全是同一种问题。

### 1. 真正只缺 milestone 编排，不缺 IBM / issue / dev 真源

这些条目已经有正式 issue，且 issue 文档、IBM 产物、verification 乃至 progress 已存在；问题集中在 `docs/milestones.md` 没把它们挂出来。

1. `C-20260324T041500Z-A`
- owner chain 已存在：`I-20260324T041500Z -> issue/prd/pre-tests/tasks -> progress -> verification`
- refined verdict: `milestone-only gap`

2. `C-20260325T033300Z-B`
- owner chain 已存在：`I-20260325T033300Z-B -> issue/prd/pre-tests/tasks -> progress`
- 当前 issue 仍是 `in_verification`
- refined verdict: `milestone-only gap`

3. `C-20260326T181000Z-A`
- owner chain 已存在：`I-20260326T181000Z -> issue/prd/pre-tests/tasks -> verification`
- 缺的是 `docs/milestones.md` 中的 `M-20260326-freely-product-architecture` section
- refined verdict: `missing milestone section`, 不是缺 IBM/dev

### 2. 已被现有 issue / capability 真源吸收，主要是 pre-brainstorm normalization 漂移

这些条目已经能追溯到现有 owner issue 或能力真源，不应再被当成“没有后续实现”；真正缺的是 pre-brainstorm 字段回写与 provenance 归一。

1. `docs/B1-docs/raw-20260318-2245/candidates.md`
- 现状：`promoted_issue_path` 已指向 `checkpoint-commit-and-multi-worktree-supervision-governance`
- refined verdict: `normalization-only drift`

2. `docs/B1-docs/raw-20260318-2358/candidates.md`
- 两条 candidate 都已指向 `checkpoint-commit-and-multi-worktree-supervision-governance`
- 但 status 仍是 `proposed`
- refined verdict: `absorbed-by-existing-issue but not normalized`

3. `docs/B1-docs/raw-20260318-1630/candidates.md`
- milestone、issue、progress 都存在：`I-20260318T163000Z` 已 completed，且 issue 明确引用该 pre-brainstorm
- refined verdict: `owner exists; pre-brainstorm fields stale`

4. `docs/B1-docs/raw-20260310-0056/candidates.md`
- `C-20260310T005600Z-A` 已在 `docs/milestones.md` 的 candidate queue 中可见
- refined verdict: `A 条不是缺 milestone，而是 pre-brainstorm 仍未把 milestone 字段正常化`
- note: `C-20260310T005600Z-B` 仍未单独出现在 milestone queue，因此 B 条仍属 active candidate visibility gap

5. `docs/B1-docs/raw-20260318-1818/candidates.md`
- 这组并非“完全没有实现”：repo 已存在 `skill:ai-cli-availability-manager`，`I-20260318T163000Z` 也把 availability watchdog / bootstrap 吸收为 canonical owner 的一部分
- 但 pre-brainstorm 内部仍保留 pre-v2 的多条 `done` 子项，且没有逐条声明各自最终去向
- refined verdict: `substance largely absorbed, normalization debt remains`

### 3. 已有部分后续实现或其他形态吸收，但还没有形成规范 owner 链

这些条目不能简单判成“没做”，因为仓库里已经能看到 runtime / skill / issue / test 层面的局部吸收；但也不能判成“已正常完成”，因为它们没有形成清晰的 milestone-owned canonical chain。

1. `C-20260320T005200Z-A`
- 已有相关 capability truth：`skill:human-interruption-direct-answer`、`test-freely-interruption-direct-answer`
- 但未找到把该 candidate 正式 materialize/absorbed 的 milestone-owned issue 记录
- refined verdict: `partially realized outside milestone chain`

2. `C-20260320T012000Z-A`
- `runtime/interruption-manager-handler`、`manager-agent.md`、`auto-loop-orchestrator/SKILL.md` 已具备“manager decides direct answer / delegation”的语义
- `I-20260321T192500Z` 解决了 chat reentry / cleanup misrouting 的一部分，但没有把 `C-20260320T012000Z-A` 显式作为 source 或 absorbed candidate 归档
- refined verdict: `partially absorbed by later interruption governance, but source chain missing`

3. `C-20260320T174500Z-A`
- 仓库里已有与该候选同方向的 canonical wording：
  - `skills/README.md` 已写 cleanup 可显式跳过 unrelated dirty / busy worktree
  - `branch-management/references/cleanup-lifecycle.md` 已写 unrelated dirty 不应作为全局阻断
- 但这条 candidate 仍未绑定到正式 owner issue，也没有在 milestone queue 中可见
- refined verdict: `policy partially absorbed, canonical owner still missing`

4. `C-20260321T183500Z-A`
- “lifecycle closure” 相关 wording 已在 `active-lifecycle-boundary...` review、`worktree-maintenance-governance` reference、以及若干后续 issue 中出现
- 但当前 candidate 本身仍未进入 milestone queue，也未 materialize 成独立 owner issue
- refined verdict: `concept diffused into later governance, but not canonically materialized`

5. `C-20260327-parked-worktree-retirement`
- 它不是完全孤立：父 issue `I-20260320T051200Z milestone-planning-and-state-maintenance` 已 completed，且该 candidate 明显是其 follow-on 研究项
- 但这条 follow-on 仍停留在父 pre-brainstorm 文件里，未进入任何 milestone candidate queue
- refined verdict: `follow-on candidate missing its own queue position`

### 4. 仍然是未经吸收的 legacy active candidate 治理债

以下条目第二轮没有找到 milestone、issue、progress 或 capability truth 的明确 owner 入口，仍应保留为真正的 legacy active debt：

- `C-20260303-001`, `C-20260303-002`
- `C-20260304-202`
- `C-20260304-501`
- `C-20260304-605`, `C-20260304-607`
- `C-20260305-803`
- `C-20260305-703`
- `C-20260306-002`
- `C-20260309T194300Z`
- `C-20260309T200300Z-A`, `C-20260309T200300Z-B`, `C-20260309T200300Z-C`
- `C-20260309T234500Z-A`, `C-20260309T234500Z-B`
- `C-20260310T005600Z-B`

这些条目与“已有实现但没记 milestone”不同；它们当前更像是 research debt / stale active queue debt，需要先决定：
- 继续保留到某个 milestone `candidate_issues`
- 被现有 issue 吸收并写清 owner
- 或直接 `dropped`

## Resolution Direction

### Step 1. 先修 milestone 可见性，不先扩写新候选
- 只针对 refined analysis 第 1 类处理：
  - 把 `I-20260324T041500Z`、`I-20260325T033300Z-B` 补回 `M-20260306-workspace-routing-foundation`
  - 对 `20260326-1810` 先补建 `M-20260326-freely-product-architecture` section，再挂 `I-20260326T181000Z`
- 不要把“已有其他形态吸收”的条目和“完全没 owner”的条目混成同一种修法

### Step 2. 再修 pre-brainstorm normalization
- 优先处理 refined analysis 第 2 类：
  - `20260318-2245`
  - `20260318-2358`
  - `20260318-1630`
  - `20260310-0056-A`
  - `20260318-1818`
- 修完后要求 `status`、`promoted_issue_path`、`milestone` 与实际 owner truth 一致

### Step 3. 清理 legacy pending / done 治理债
- 对 refined analysis 第 3 / 第 4 类做一次 `owner-vs-partial-absorption` sweep
- 每条只允许三种去向：
  - 绑定到现有 milestone `candidate_issues`
  - 明确被现有 issue 吸收并改成 `absorbed supporting evidence`
  - 明确 `dropped`，并写清为什么不再进入 active queue
- 对已经有局部实现但未形成 canonical chain 的条目，禁止直接因为“代码/skill 已存在”就跳过 owner 归档

### Step 4. 对 umbrella candidate 单独保留 owner
- `C-20260325T033300Z-A` 不能因为 `B` 已 materialize 就消失
- 需要在 milestone 中继续保留 umbrella candidate，直到 testing ladder / real-environment harness contract 被拆出下一条 issue

### Step 5. 把“支持性来源”与“正式 owner”分开写清
- 对 `20260318-2245`、`20260318-2358`、`20260318-1630` 这类已被既有 issue 吸收的 pre-brainstorm，需要明确：
  - 是否只是 supporting evidence
  - 对应 owner issue 是谁
  - 为什么不再单独 materialize

## Exit Condition For Follow-up Research
- 每个异常条目都满足以下最小条件后，才算这轮预研收口：
  - pre-brainstorm 文档字段自洽
  - `docs/milestones.md` 中可见该条线的 canonical queue position
  - 若 issue 已存在，milestone 与 pre-brainstorm 都能追溯到同一个 owner issue
  - 若仍在研究，candidate 不会从 active milestone scan 中消失

## Closing Recommendation

这轮预研不应继续扩成“重新审所有 pre-brainstorms”。更合适的收口方式，是把后续动作压缩成三个独立治理 lane，并以此结束本次 audit。

### Lane A. milestone reconciliation
- 范围只含 refined analysis 第 1 类：
  - `I-20260324T041500Z`
  - `I-20260325T033300Z-B`
  - `I-20260326T181000Z`
- 目标：修复 `docs/milestones.md` 的正式编排缺口
- 完成标志：issue 已在对应 milestone section 中可见，且 provenance 不再断裂

### Lane B. pre-brainstorm normalization
- 范围只含 refined analysis 第 2 类：
  - `20260318-2245`
  - `20260318-2358`
  - `20260318-1630`
  - `20260310-0056-A`
  - `20260318-1818`
- 目标：把 pre-brainstorm 字段与现有 owner truth 对齐，不新开 issue，不重做已有实现
- 完成标志：`status`、`milestone`、`promoted_issue_path` 与 owner truth 单义一致

### Lane C. absorption-or-drop governance sweep
- 范围含 refined analysis 第 3 类与第 4 类
- 目标：逐条判断是：
  - 进入 milestone `candidate_issues`
  - 被现有 issue 明确吸收
  - 还是直接 `dropped`
- 完成标志：不存在“仓库里好像做了点什么，但 owner 链不存在”的悬空 candidate

## Audit Closure
- 本文档到此为止不再继续扩写新异常类型
- 后续只接受三类增量：
  - 某条异常已被哪个 lane 处理完成
  - 某条异常经核对后应从本审计移出
  - 某条异常被确认需要新开的 follow-up pre-brainstorm
- 若没有新的分类变化，这份 audit 应视为已收口，后续改动转入对应 lane 的执行文档，不再继续堆在本文件

## Execution Update - 2026-03-27

本轮已直接收口的条目：

- `Lane B / normalization`
  - `20260318-1818` 已从 legacy `done + pending://...` 改写为显式 `absorbed supporting evidence` / `dropped`
  - `C-20260320T005200Z-A` 已归到 `I-20260321T192500Z`
  - `C-20260320T012000Z-A` 已归到 `I-20260321T192500Z`
  - `C-20260321T183500Z-A` 已归到 `I-20260324T040500Z`

- `Lane C / absorption-or-drop`
  - `C-20260309T194300Z` 已判定为 `superseded`
  - `C-20260309T234500Z-A` 已判定为 `absorbed supporting evidence`
  - `C-20260309T234500Z-B` 已判定为 `superseded`
  - `C-20260310T005600Z-B` 已补 milestone 绑定并恢复 candidate queue 可见性
  - `C-20260320T174500Z-A` 已补回 milestone candidate queue 可见性，继续保留 `candidate`
  - `C-20260327-parked-worktree-retirement` 已补 milestone 绑定与 candidate queue 可见性，继续保留 `needs_research`

当前仍保留 follow-up judgement 的条目：

- `C-20260320T174500Z-A`
- `C-20260303-001`, `C-20260303-002`
- `C-20260304-202`
- `C-20260304-501`
- `C-20260304-605`, `C-20260304-607`
- `C-20260305-803`
- `C-20260305-703`
- `C-20260306-002`
- `C-20260309T200300Z-A`, `C-20260309T200300Z-B`, `C-20260309T200300Z-C`

这些条目当前仍缺足够强的 canonical owner 或 drop judgement；后续若继续处理，应优先做“是否还有独立 owner 价值”而不是先补形式化 milestone。

## Execution Update - 2026-03-27 legacy owner sweep

第二轮 legacy owner sweep 的进一步结论：

- `C-20260304-501` 已改判为 `absorbed supporting evidence`
  - canonical owner: `I-20260312T001100Z backend-service-contract-and-adapter-taxonomy`
  - reason: 后续架构真源已把 OpenClaw 冻结为 optional adapter/profile，不再需要保留这条旧候选单独承接

- `C-20260304-607` 已改判为 `absorbed supporting evidence`
  - canonical owner: `I-20260326T181500Z ibm-pretests-executable-acceptance-quality-governance`
  - reason: executable acceptance / checklist / pre-tests gate 已进入当前 IBM 真源

- `C-20260305-803`、`C-20260306-002`、`C-20260309T200300Z-A`、`C-20260309T200300Z-B`
  - 已改判为 `superseded`
  - reason: 当前 canonical 目录模型、hooks 架构、workspace skill 边界与治理入口已经替代旧候选假设

- `C-20260303-001`、`C-20260303-002`、`C-20260304-202`、`C-20260304-605`、`C-20260305-703`、`C-20260309T200300Z-C`
  - 当前仍保留 active research 价值
  - 本轮先补 milestone queue 可见性，不伪造 owner 吸收

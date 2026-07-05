# 预研：worktree fleet governance closure

## Context

- 日期：2026-03-21
- 触发：当前仓库同时存在 20+ 个 feature worktree，且已经出现派生链、merge-prep 工位、research-only 工位、已完成但未清理工位并存的情况。
- 已有能力：
  - `skill:worktree-maintenance-governance` 已覆盖 `audit / merge_prep / retirement_handoff`
  - `skill:multi-worktree-supervision` 已覆盖运行态 dirty / checkpoint / fleet 监督
  - `skill:branch-management` 已覆盖基本 create / promote / cleanup 生命周期
- 新暴露的问题：
  - 当前技能还缺“全仓 fleet 审计 + 生命周期闭环 + 逐级向上合并 + develop 收口”这一层
  - `docs/B1-docs/INDEX.md` 在 `develop` 上仍带有冲突标记，说明已有治理产物没有被完整收口
  - 多条 worktree 已经不是单树判断，而是需要核对：
    - pre-brainstorm candidate 是否准确、是否 materialize
    - milestone / issue 生命周期是否走完
    - 真实实现是否存在、测试是否通过
    - 分支是否需要先 merge 到父 feature，再由 merge-prep 汇入 `develop`
    - 在满足 `verified-retirable` 之前是否可以 cleanup

## Problem

当前 `worktree-maintenance-governance` 更像“单个任务或一组相关任务的维护技能”，但还不是“项目级 fleet closure 技能”。

缺少的判断面包括：

1. 全仓 worktree inventory 审计
- 不是只审一棵树，而是核对所有活跃 worktree 的：
  - git ancestry
  - dirty / clean
  - canonical brainstorm / candidate / milestone / issue / review / tests
  - 是否已进入 `develop`
  - 是否应该继续保留

2. candidate 与 issue 生命周期闭环核验
- 需要检查：
  - pre-brainstorm 是否真的产出了 candidate
  - candidate 是否准确、是否进入 `docs/milestones.md`
  - promoted candidate 是否真的 materialize 成 issue
  - issue 是否经历 `in_ibm / done_ibm / in_dev / in_verification / completed`
  - 已 completed 的 issue 是否真的有实现与测试证据，而不是只停在文档

3. 逐级向上合并治理
- 当分支不是直接从 `develop` 拉出时，不能跳过父分支
- 需要稳定执行：
  - `child -> parent -> merge-prep-from-develop -> develop`
- 同时要区分：
  - child 未完成
  - parent 未完成
  - merge-prep 暴露了 develop 集成问题

4. verified-retirable 与 cleanup 闭环
- 当前规则要求 cleanup 只能发生在 `verified-retirable` 之后
- 但还缺一条“项目级审计完成后如何批量判断哪些 worktree 可以 retire”的执行框架

## Why Existing Skills Are Not Enough

### `worktree-maintenance-governance`

它能判断单树真实状态，也能做一组相关树的 merge-prep，但没有要求：

- 扫描所有活跃 worktree
- 对每棵树核对 candidate / milestone / issue 生命周期
- 给出仓库级 closure plan
- 一路向上 merge 到 `develop`
- 在 closure 完成后执行 cleanup checklist

### `branch-management`

它提供命令和基本 lifecycle，但不负责：

- 判断 candidate 是否准确
- issue 是否真的 completed
- 哪条链该先 merge
- 哪条 research tree 该 retire

### `multi-worktree-supervision`

它偏运行态健康与 checkpoint 管理，不负责文档真相、issue 生命周期和 develop 收口。

## Proposed Direction

不要新增一个完全平行的新技能。

更合理的是扩展：

- `skill:worktree-maintenance-governance`

新增一个项目级模式，例如：

- `fleet_closure`

这个模式负责：

1. 枚举所有 active worktree
2. 对每棵树做最小生命周期核对
3. 把每棵树分成：
  - `continue-dev`
  - `merge-up`
  - `merge-prep-to-develop`
  - `research-writeback-then-retire`
  - `retire-now`
  - `blocked`
4. 对存在父子依赖的链路执行逐级向上 merge 计划
5. 对候选 issue / milestone / completion evidence 做一致性核查
6. 在达成 `verified-retirable` 后再 cleanup

## Required Checks For Fleet Closure

每棵 worktree 至少核对：

1. Git state
- branch
- execution base
- merge-base with parent / develop
- ahead / behind
- clean / dirty

2. Canonical docs
- source pre-brainstorm
- `candidates.md`
- `docs/milestones.md`
- issue / review / tasks / pre-tests / progress / recovery（如适用）

3. Lifecycle truth
- candidate 是否仍停在 `candidate_issues`
- promoted item 是否已 materialize
- issue 的 `phase_state` 是否与 evidence 一致
- `completed` 是否真的已实现、验证并可追溯

4. Merge / retire decision
- 是否能直接 merge 到父分支或 `develop`
- 是否必须先 merge-prep
- 是否只该 writeback then retire
- 是否还需继续开发

## Acceptance

- 能对全仓所有活跃 worktree 给出一份明确 closure inventory
- 能发现 candidate / issue / milestone 生命周期不一致
- 能发现“文档说完成但真实没有完成”的情况
- 能对非 `develop` 派生链执行 `child -> parent -> merge-prep-from-develop -> develop`
- 能在完成后给出 cleanup 清单，并只对 `verified-retirable` 的树执行 retire
- 相关规则被沉淀到 skill，而不是继续依赖人工经验

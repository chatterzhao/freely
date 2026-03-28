# 预研：lifecycle complete before merge governance

## Context

- 日期：2026-03-21
- 触发：
  - 本轮在推进当前 active worktree 生命周期时，暴露出一个治理边界问题：
    - worktree 是否可能在 issue / milestone 仍处于活跃生命周期时被提前合并？
  - 用户明确指出：
    - 除了纯研究结果最终收口为 `needs_research` / `dropped` 这类研究结论外，正常实现型 worktree 不应在生命周期未走完前就向上合并。

## Problem

当前仓库已经有 worktree 治理、stacked merge-chain、fleet closure、remote branch retirement 等能力。

但还缺一条更硬的 merge gate 语义：

- 什么叫“生命周期走完”？
- 哪些 issue / milestone / worktree 状态允许 promote / merge？
- 哪些情况即使实现和 review 基本完成，也仍不能 merge？

如果这条边界不稳定，会出现两类错误：

1. 过早向上合并
- 当前 issue 还在 `in_ibm / in_dev / in_verification`
- 当前 worktree 还未完成状态回写与 closure
- 但因为“内容看起来差不多了”，被提前 promote

2. 错误冻结研究线
- 纯研究线本应以 `needs_research` / `dropped` 收口
- 却被套用实现型 worktree 的 merge 要求，导致无法正确结束

3. 集成测试看似“能跑”，但主管真实 gate 还没发挥作用
- 本轮在 `develop` 工位真实执行了：
  - `freely start`
  - `freely chat "<项目级主管任务>"`
- 结果表明：
  - 主管进程确实被拉起
  - chat 也被 intake 成功
  - 但新任务没有先触发新的 patrol / restart-point routing
  - 而是被错误吸收到旧的 `cleanup://merged-worktree-followthrough` continuity
- 这说明不能把“能启动 + 能 intake”误当成“merge gate / lifecycle gate 已正确生效”

4. hook 名义存在，但真实 merge 仍可能漏拦
- 本轮又复现到一条更具体的 develop merge 漏口：
  - `pre-merge-commit` hook 已启用
  - `governance-merge-gate --staged` 单独运行会失败
  - 但真实 `git merge --no-ff <feature>` 仍能进入 `develop`
- 追到 hook 现场后确认：
  - `pre-merge-commit` 触发时，`git diff --cached` 已经能看到 merge 结果
  - 但 `MERGE_HEAD` 在该时点为空
  - hook 因为把 `MERGE_HEAD` 当成前置守卫而直接 `exit 0`
- 这说明 merge gate 不仅要“有规则”，还要覆盖真实 hook 时序；否则 develop-bound merge 仍会把 runtime/test 真源绕过 candidate-driven lifecycle evidence

5. `absorbed` 候选被用成了过宽的 develop merge 通行证
- 本轮修完 hook 后，又暴露出第二层门禁缺口：
  - 只要 merge diff 里出现一个 `status: absorbed` 的候选
  - 且它写了 `promoted_issue_path`
  - gate 就会把它当成 develop-bound merge 的充分治理证据
- 但这还不够：
  - merge 可能根本没有基于任何具体 issue
  - 即使 `promoted_issue_path` 存在，也可能只是“某个 owner 在仓库里存在”，而不是“本次 merge 真正基于该 owner issue”
  - 这样会把 `candidate -> owner exists` 错当成 `candidate -> milestone -> issue` 已经对本次 merge 生效
- 因此 develop merge 的判断顺序应收紧为：
  - 先问：本次 merge 是否基于一个具体 issue（issue / progress / review owner 必须进入 diff）
  - 再问：该 issue 的 `C/M/I` 链是否打通
  - 最后才按允许状态判断能否放行

## Proposed Clarification

### 1. merge gate 应以 lifecycle closure 为准

对实现型 worktree：

- 只有当当前 issue 生命周期走到：
  - doc-loop / dev-loop 已完成
  - verification 已完成
  - canonical issue / milestone / candidate / review 已同步
  - worktree 已达到 closure-ready
- 才能进入 merge / promote

### 2. 研究线的 closure 例外要单独定义

对纯研究线：

- 若结论是：
  - `needs_research`
  - `dropped`
  - `superseded`
- 可以作为研究生命周期完成而收口
- 不应强制要求它像实现型 issue 一样进入 dev-loop 后再 merge

### 3. worktree merge 是 auto-loop 的主管 gate，不是 worker 自行判断

- worker 负责执行当前 restart point
- manager 负责判断：
  - lifecycle 是否已闭环
  - 当前 worktree 是实现型 closure，还是研究型 closure
  - 是否满足 merge / cleanup / remote retirement 条件

### 4. 这层 gate 需要事件触发和巡检都能命中

- 不应只在人工准备 merge 时检查一次
- 也不应只在文档真源里“写了应该如此”就视为完成
- 至少要能通过真实集成测试证明：
  - 新的主管级 signal 不会被旧 continuity 错误吸收
  - 主管能先判断 lifecycle closure，再决定 merge / cleanup / delegate

## Likely Landing

更可能应扩到：

1. `three-loop-capability-lifecycle.md`
- 明确“合并不是 dev 完成即触发，而是 lifecycle closure gate”

2. `worktree-maintenance-governance`
- 明确 merge / retire 的最小条件
- 区分实现型 closure 与研究型 closure

3. `milestone-planning-state-maintenance`
- 明确 milestone phase 与 merge readiness 的关系

## Expected Result

本条预研应最终收敛成：

1. 明确实现型 worktree 必须 lifecycle complete 才能 merge
2. 明确研究型 worktree 的收口例外
3. 明确这层 gate 由主管判断，而不是 worker 凭感觉推进
4. 对 develop-bound implementation merge 冻结更硬的 owner rule：
   - merge diff 必须绑定到一个具体 issue（issue / progress / review owner）
   - touched candidate 必须与同次 merge 中的 owner issue 处于同一条 `C/M/I` 线
   - `absorbed` 不再能靠“仓库里存在某个 owner issue”单独放行

## Materialization Decision

- `C-20260321-1835-A` 不再继续作为 absorbed supporting evidence 留在 pre-brainstorm 层。
- 该候选现已 materialize 为：
  - `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- 原因：
  - 这次 develop merge 漏口已经不是 wording 讨论，而是 active gate 真源缺口
  - 若没有独立 issue owner，这次修复本身就会再次违反它要收紧的 merge rule

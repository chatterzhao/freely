# 预研头脑风暴：active-milestone-placement-and-consumption-gate

## 背景

这一轮在回看 merge gate、candidate 持续可见性与 `C/M/I` traceability 时，已经确认三件事：

1. `LAWS` 已经要求 active candidate 不得悬空，`needs_research / proposed / blocked` 必须留在 `docs/milestones.md` 的 `candidate_issues`
2. 现有 merge gate 也已经开始检查 candidate 是否进入 milestone，以及 `C-* -> M-* -> I-*` 是否保留 shared issue-id key
3. 但当前 gate 仍把“出现在某个 milestone 队列里”近似成“已经可消费”，没有继续检查这条 candidate 是否被放进了正确且仍活跃的 milestone

这会留下一个新的治理缺口：

- candidate 可能仍是 `milestone: unassigned`
- candidate 可能被挂进错误的历史 milestone
- candidate 也可能被挂进已经收口、不会再消费的 milestone

从格式上看它“进了 milestone”，但从排期上看它仍然在悬空。

## 现场事实

### 1. 现有规则已经覆盖“要进 milestone”，但没覆盖“放对 milestone”

`docs/LAWS.md` 已明确：

- unresolved candidate 必须保留在 milestone 的 `candidate_issues`
- promoted candidate 必须先接入 `M-*`，再 materialize 成 `I-*`
- `I-*` 必须保留 shared issue-id key

`docs/system/workspace/scripts/quality/governance-merge-gate` 也已经检查：

- `needs_research / proposed / blocked` 是否在某个 `candidate_issues`
- `promoted` candidate 是否有真实 owner issue
- issue `phase_state` 是否与 milestone queue 一致

所以问题不是“完全没有治理”，而是治理只走到“可见性”和“链路存在”，还没走到“可消费性”。

### 2. 现有 gate 没有校验 milestone placement correctness

当前 merge gate 没有稳定冻结这些判断：

- candidate 文件里的 `milestone:` 是否与 `docs/milestones.md` 中实际承接它的 `M-*` 一致
- unresolved candidate 所在 milestone 是否 `status: active`
- 已完成 milestone 是否还能继续接纳新的 active candidate
- candidate 是否被放进了当前应消费它的 milestone，而不是某个历史或错误 lane

因此只要把 candidate 塞进“某个 milestone 队列”，当前 gate 就可能放行。

### 2.5 `needs_research` 还缺少谨慎的后移与丢弃规则

当前 unresolved candidate 的 canonical 规则主要强调：

- 不得静默消失
- 必须保持可见

但还没有同样明确地写清：

- 如果当前 milestone 已确认本轮不会消费，何时应该后移到后续 active milestone
- 后移时怎样避免把 candidate 挂到一个长期不会消费的远期 milestone
- 何时应直接标记为 `dropped`，而不是继续伪装成“以后可能做”

如果没有这层规则，candidate 即使可见，也可能长期停留在一个事实上不会再消费它的队列中。

### 3. 当前真实例子说明“只要求可见”不够

`C-20260331-1840-A` 这类研究并不是远期设想，而是当前里程碑就应继续消费的能力缺口。

如果它继续保持：

- candidate 文档里 `milestone: unassigned`
- milestone 里没有 candidate queue entry

那么它既不算 dropped，也不算已吸收，只是在 active scan 之外漂浮。

这正是“形式上有预研，排期上没人负责”的状态。

## 问题定义

Freely 需要冻结一条更强的 milestone placement contract：

1. active candidate 不仅要进入 milestone，还要进入正确的 milestone
2. unresolved candidate 必须进入 `status: active` 的 milestone，而不是历史完成里程碑
3. candidate 文档中的 `milestone:`、milestone queue entry、后续 issue 的 milestone identity 必须一致
4. “已进入 milestone” 必须真正代表“会在当前 milestone 节奏中被消费”，而不是只满足一个静态字段
5. `needs_research` 的后移与 dropped 判断必须成为显式治理动作，而不是长期模糊挂起

## 目标

1. 把“candidate placement correctness”从隐含习惯提升为明确治理合同
2. 明确 active candidate 不能保持 `milestone: unassigned`
3. 明确 unresolved candidate 必须进入 active milestone 的 `candidate_issues`
4. 明确 `needs_research` 在“继续留当前 milestone / 谨慎后移 / 直接 dropped”之间的决策规则
5. 明确 merge gate / governance-check 需要同时检查可见性与 placement correctness
6. 明确 completed milestone 默认不能继续承接新的 unresolved candidate

## 非目标

1. 本轮不直接实现完整的 milestone 排期引擎
2. 本轮不要求所有 milestone 都引入更细的 `M1.1 / M2.1` 子编号
3. 本轮不重写全部历史 pre-brainstorm，只先冻结最小 gate contract

## 关键边界

### 1. “在 milestone 中”不等于“会被消费”

只验证 candidate 出现在某个 milestone 队列中，只能证明它可见，不能证明它：

- 属于当前 lane
- 属于正确 lane
- 仍处在 active milestone 中

治理合同必须把这三件事补齐。

### 2. `needs_research` 不是悬空许可，而是当前里程碑中的待消费状态

`needs_research` 只能表示：

- 本轮还没 materialize 成 owner issue
- 但它已经被某个 milestone 显式接纳，并写清 `next_action` 与 `revisit_trigger`

它不应再意味着：

- 先放在 pre-brainstorm 里，之后再说

### 2.5 `needs_research` 的后移必须是“最近可消费迁移”，不是“延后消失”

当当前 milestone 已明确本轮不会消费某条 `needs_research` candidate 时，允许后移，但必须同时满足：

- 目标 milestone 仍是 active
- 目标 milestone 是已知最早会消费它的里程碑，而不是模糊远期占位
- `next_action` 写明为什么当前 milestone 不再消费，以及后移后的消费条件

如果无法给出这三个判断，默认不应后移；应继续留在当前 milestone，或直接判断为 `dropped`。

### 2.6 `dropped` 是合法收口，不是失败

如果 candidate 已确认：

- 不再符合当前产品方向
- 被现有 owner 完整吸收且不再需要单独消费
- 或者继续保留只会制造噪音

更稳的做法是显式标记为 `dropped`，而不是继续挂在 `needs_research` 队列里制造“永远以后再看”。

### 3. milestone placement 必须能沿 `C/M/I` 一路追踪

更稳的 contract 应该是：

- `C-{shared-key}` 在 candidate 文档中声明 `milestone: M-*`
- `docs/milestones.md` 中的同一 `M-*` 真正承接这条 candidate
- 进入 owner issue 后，`I-{shared-key}` 继续保留 shared key，且仍属于同一 milestone family

如果 candidate、milestone、issue 三处的 placement truth 不一致，就不是“文档不同步”，而是治理真相不一致。

## 预期收口

本条预研应最终收敛成：

1. candidate placement correctness 的正式 merge gate 规则
2. active milestone / completed milestone 对 unresolved candidate 的承接边界
3. candidate `milestone:` 字段与 milestone queue 实际位置的一致性检查
4. 对 `milestone: unassigned` active candidate 的明确禁止
5. `needs_research` 的后移规则与 `dropped` 判定边界

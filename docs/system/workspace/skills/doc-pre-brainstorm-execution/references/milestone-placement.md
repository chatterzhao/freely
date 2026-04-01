# Milestone Placement

## Core rule

active candidate 不能只“存在于 pre-brainstorm”，必须同时满足：

- 绑定一个明确的 `M-*`
- 出现在该 milestone 的 `candidate_issues`
- 带有可执行的 `next_action`
- 带有明确的 `revisit_trigger`

对 active candidate，以下放置默认无效：

- `milestone: unassigned`
- `pending://milestone-binding`
- 已 `completed` 的 milestone
- 与 candidate 文档声明不一致的 milestone

## How to choose the milestone

优先顺序不是“随便找一个能挂进去的 milestone”，而是“最早会真正消费它的 active milestone”。

按下面顺序判断：

1. 如果这条 candidate 明显属于当前正在推进的能力族，或是当前现场事故直接暴露出的同一 contract gap，优先放入当前 active milestone。
2. 如果它依赖另一个 active milestone 先完成，放入最早会消费它的后续 active milestone，并在 `next_action` 中写清依赖。
3. 如果它只是仍需研究，但判断它应在近期里程碑继续被扫描和消费，仍然要放入某个 active milestone，而不是留成 `unassigned`。
4. 只有在显式 `dropped`、`absorbed`、`completed` 后，才允许离开 active candidate queue。

## Rehome or drop

如果当前 milestone 已明确这条 `needs_research` candidate 本轮不会消费，不要让它继续模糊挂着。必须在三种动作中选一个：

1. 继续留在当前 milestone
- 适用于：它仍属于当前能力族，只是本轮排序暂时靠后
- 要求：`next_action` 和 `revisit_trigger` 仍能指向近期消费

2. 谨慎后移到后续 active milestone
- 适用于：当前 milestone 已明确不再消费，但后续某个 active milestone 已经足够接近、且能说明为什么会由它消费
- 要求：
  - 目标 milestone 仍是 active
  - 它是已知最早会消费这条 candidate 的 milestone
  - `next_action` 写明后移原因、依赖和重新消费条件

3. 直接标记 `dropped`
- 适用于：继续保留只会制造噪音，或 candidate 已不再值得单独消费
- 要求：写清 dropped reason，不再伪装成未来可能继续推进

禁止做法：

- 因为当前 milestone 暂时排不上，就把 candidate 随手移到一个长期不会消费的远期 milestone
- 不愿判断是否 dropped，就让 candidate 永久保持 `needs_research`

## `needs_research` placement

`needs_research` 不表示“以后再说”，而表示：

- 还不能进入 IBM
- 但已经进入某个 active milestone 的待消费队列

放置时要同时回答：

- 谁会在后续轮次继续研究它
- 近期在哪个 milestone 节奏里重新扫描它
- 触发重新消费的条件是什么

如果这三个问题答不出来，就说明 candidate 还没真正放置完成。

## Patrol expectations

主管扫描 milestone 时，应优先质疑以下 unresolved candidate：

- 当前 active milestone 中长期没有 worker 接手
- `next_action` 过于空泛，无法形成下一跳
- `revisit_trigger` 无法判断何时重启
- 已经明显属于别的 active milestone，但还停在旧 milestone
- 当前 capability / incident 已经证明它应在近期消费，却仍留在 `unassigned` 或历史 milestone
- 当前 milestone 已明确不会消费它，但也没有后移或 dropped 判断

## Writeback rule

candidate 文档与 milestone writeback 必须原子同步：

- `candidates.md.milestone`
- `docs/milestones.md` 对应 `candidate_issues` entry
- `next_action`
- `revisit_trigger`

不能只改其中一个就算“已经放进 milestone”。

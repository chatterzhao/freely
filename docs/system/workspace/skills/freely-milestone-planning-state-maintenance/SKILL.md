---
name: freely-milestone-planning-state-maintenance
description: >- 扫描 `docs/milestones.md` 与关联 candidate、issue、progress evidence，
  做 sequencing、状态维护和写回一致性收口。

  Use when: 主管发现 milestone 排序冲突、队列失衡或 standing-source drift。
  触发词："milestone"、"排序"、"队列"、"sequencing"、"状态维护"。
---

# skill:freely-milestone-planning-state-maintenance

## 目标

这不是业务实现 worker。

它负责：

- 规划 active candidate / committed issue 的顺序
- 确保 unresolved candidate 被放在会真正消费它的 active milestone，而不是 `unassigned`、错误 milestone 或已完成 milestone
- 当当前 milestone 已确认不消费某条 `needs_research` candidate 时，负责判断它应继续留当前 milestone、后移到更合适的 active milestone，还是直接 dropped
- 识别 milestone 与关联产物的状态漂移
- 回写 milestone 与相关摘要，让治理事务收口
- 当 `freely-doc-B2_IBM-execution` skill materialization 已产出一个或多个 `I-{issue-id}*` 时，把正式编排从 `M-{issue-id}` 候选位切到这些 `I-*`

## 输入

- `docs/milestones.md`
- 关联 `candidates.md`
- issue / progress / recovery / cleanup evidence
- 当前 fleet / verification / merge / cleanup 状态

## 输出

- 更新后的 `docs/milestones.md`
- 必要的关联 writeback 摘要
- sequencing 建议
- drift / blocker 说明

## 适用场景

- 多个 candidate 同时可推进，需要排序
- active candidate 已可见，但 placement 不正确，导致长期不被消费
- unresolved candidate 已在当前 milestone 停留过久，需要判断是继续保留、后移，还是 dropped
- committed issue 的依赖顺序不再清楚
- candidate / issue / progress / recovery / cleanup 之间出现漂移
- verification / cleanup 完成后，需要回写 completed queue
- IBM 已从某个 milestone candidate 物化出正式 issue，但 milestone 还没切换到 `I-*` 编排
- standing-source scan 发现排期或状态维护问题

## 不负责

- 不直接写业务代码
- 不直接扩写 IBM / dev 正文
- 不替代 manager 做项目级最终优先级裁决

## 事务视角

把下面这条链视为同一治理事务：

- `brainstorms.md`
- `candidates.md`
- `docs/milestones.md`
- issue / progress / recovery
- completed / cleanup evidence

其中同一条治理线默认共享同一个 `{issue-id}`：

- `C-{issue-id}`：pre-brainstorm candidate 身份
- `M-{issue-id}`：milestone candidate 身份
- `I-{issue-id}*`：`freely-doc-B2_IBM-execution` skill materialization 后的正式 issue 身份

事务完成条件是：

- 当前阶段相关 canonical artifacts 已同步，而不是只改了其中一个文件

## 完成标志

- milestone 队列顺序清楚
- unresolved candidate 的消费 milestone 与重启条件清楚，没有 `unassigned` 或明显不可消费的挂起状态
- 对当前 milestone 已不再消费的 `needs_research` candidate，已显式做出留置、后移或 dropped 决策
- 状态漂移已回写或显式留痕
- 已 materialize 的 `I-{issue-id}*` 已被放入正确的 milestone 阶段，并且顺序清楚
- 下一轮 manager 可以基于 milestone 继续委派

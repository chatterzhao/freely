---
name: milestone-planning-state-maintenance
description: 扫描 `docs/milestones.md` 与关联 candidate / issue / progress / recovery / cleanup evidence，做 sequencing、状态维护和写回一致性收口。当主管发现 standing-source drift、排序冲突或队列失衡时使用。
---

# skill:milestone-planning-state-maintenance

## 目标

这不是业务实现 worker。

它负责：

- 规划 active candidate / committed issue 的顺序
- 识别 milestone 与关联产物的状态漂移
- 回写 milestone 与相关摘要，让治理事务收口

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
- committed issue 的依赖顺序不再清楚
- candidate / issue / progress / recovery / cleanup 之间出现漂移
- verification / cleanup 完成后，需要回写 completed queue
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

事务完成条件是：

- 当前阶段相关 canonical artifacts 已同步，而不是只改了其中一个文件

## 完成标志

- milestone 队列顺序清楚
- 状态漂移已回写或显式留痕
- 下一轮 manager 可以基于 milestone 继续委派

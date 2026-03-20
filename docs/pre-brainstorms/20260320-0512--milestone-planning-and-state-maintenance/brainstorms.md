# 预研头脑风暴：milestone 排期与状态维护 worker

## 背景

- Freely 已经把 `docs/milestones.md` 定义成项目级编排入口。
- 但当前真源还没有一个明确能力，专门负责：
  - milestone sequencing
  - candidate / committed / completed 队列维护
  - candidate / issue / progress / recovery / cleanup 之间的状态一致性
- 结果是：
  - milestone 像编排中心，但没有专门 worker 持续维护
  - 主管虽然知道 milestone 是 standing source，却没有一条明确的委派路径
  - `pre-brainstorm -> candidate -> milestone -> issue -> progress/recovery` 更像“靠规范遵守的文档事务”，而不是有专人 reconcile 的事务

## 主问题

需要明确三件事：

1. 里程碑排期应何时研究。
2. 主管何时应委派专门 worker 做排期和状态维护。
3. `pre-brainstorm / candidate / milestone / issue / progress / recovery` 是否应被视为同一治理事务的一部分。

## 核心判断

### 1. 这确实应被看作一个治理事务

不是数据库事务，而是治理事务：

- 当新问题从 pre-brainstorm 进入 candidate
- candidate 被接纳进入 milestone
- candidate promotion 成 issue
- issue 进入 dev / verification / completed

这些迁移只有在相关 canonical artifacts 都同步后，才算事务完成。

也就是说：

- 不是只改一个文档就算完成
- 而是要让相关产物一起收敛

### 2. 现在的约束主要来自 skill / law / quality gate

现状已经有一半：

- `doc-pre-brainstorm-execution` 要求 candidate 与 milestone 原子同步
- `LAWS 2C` 规定跨环写回
- `milestones.md` 是 standing source 编排入口

但还缺：

- 专门的 `milestone planning / state maintenance` worker
- 主管定期委派它做 reconcile

### 3. milestone 排期属于 standing-source scan 后的独立工作

它不该等“实现开始前最后一刻”才想起来。

更合适的是：

- 主管在 standing-source scan 中看到 candidate pool / committed queue / progress drift
- 判断这是一个 planning/state-maintenance 问题
- 再委派专门 worker

## 主管何时委派

以下场景应优先委派：

- 有多个 candidate 同时可推进，需要排序
- 依赖关系、owner 边界或执行 base 已影响下一跳
- candidate / milestone / issue / progress / recovery 出现状态漂移
- 已完成/已验证 issue 尚未写回 milestone completed queue
- merge / cleanup / verification 结果未回写 milestone
- active candidate 太多，`next_action` 已不足以表达 sequencing

## worker 职责

这个 worker 不做业务实现。

它负责：

- 扫描 `docs/milestones.md`
- 读取关联 `candidates.md` / issue / progress / recovery / cleanup evidence
- 识别队列排序、依赖、漂移和缺失写回
- 回写 milestone 与必要的关联文档摘要
- 输出下一轮推荐排班

## 不负责

- 不直接写业务代码
- 不直接补 IBM / dev 产物正文
- 不替代 manager 做顶层优先级裁决

## 事务视角

我更倾向于把下面这条链看作同一治理事务：

```text
pre-brainstorm
-> candidates.md
-> milestones.md.candidate_issues
-> issue_path / committed_issues
-> progress / recovery / verification
-> completed_issues / cleanup evidence
```

事务完成条件不是“某一步做了”，而是：

- 当前阶段相关 canonical artifacts 都同步了

## 何时研究里程碑排期

应在以下时机研究，而不是拖到实现临门一脚：

- candidate pool 形成时
- candidate 准备 promotion 时
- committed issue 队列出现竞争或依赖时
- verification / cleanup 完成后需要重排 active batch 时
- standing-source scan 发现 drift 时

## 完成标志

- 主管有明确的 milestone planning / state maintenance 委派路径
- 真源里明确这是一种 standing-source maintenance worker
- 事务性约束从“隐含”变成可读的治理规则

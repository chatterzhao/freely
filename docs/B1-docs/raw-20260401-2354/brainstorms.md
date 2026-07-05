# Brainstorm: implementation-decision-notes-in-review-artifacts

- brainstorm_id: `20260401-2354--implementation-decision-notes-in-review-artifacts`
- created_at: `2026-04-01`
- status: `active`
- related_signals:
  - Freely 已经把 pre-brainstorm candidate、IBM `prd.md`、`pre-tests.md` 与 verification evidence 做成 traceable lifecycle，但 dev-loop 中“这次为什么这样实现、放弃了什么、还有哪些残余风险”仍主要散落在 reviewer prose 里
  - 当前 `governance-merge-gate` 已能把 develop-bound 变更关联到 candidate / issue / progress / review artifacts，但还不会拒绝“实现改了、review 也在、却没有 implementation decision note”的情况
  - 用户明确要求这类 thoughtfulness 不应随机落点，也不应只靠模型自觉；需要固定主落点和最小 gate

## Problem

Freely 已经有两层 thoughtfulness 真源：

1. candidate / pre-brainstorm
- 解释为什么值得做
- 解释进入 IBM 前还缺什么
- 记录开放问题与 acceptance review

2. IBM / PRD
- 解释 issue scope、non-goals、non-negotiables、acceptance 与 implementation slices

但在 dev-loop 里，真正决定“这次实现为什么选 A 而不是 B”的那一跳，还没有一个统一、低摩擦、issue-bound 的 canonical landing surface。

结果是：

- 具体实现决策可能只存在于会话记忆或零散 prose
- reviewer / future worker 能看到“改了什么”，却不一定能快速恢复“为什么这么改”
- gate 已能约束 candidate、issue、pre-tests，却还不能发现“实现有 review artifact 但没有真正记录决策”的偏航

## Tension

1. 不能新造一个平行 truth system
- 不能再建独立 `decision-summaries/` 目录
- 不能让同一批实现同时在 issue、progress、review 三处各写一份

2. 不能要求每个小改动都写长文
- 纯机械改名、纯 typo、纯 queue/milestone 调整不值得强制
- 但 develop-bound implementation-bearing 变更必须留下最小 decision note

3. 不能把 candidate / PRD 重复一遍
- dev-loop decision note 应承接上游，而不是重写 pre-brainstorm / IBM
- 它需要回答的是“在当前 owner 边界下，这次实现为什么这么落”

4. gate 需要可执行代理条件
- 不能尝试自动判断“模型是否足够 thoughtful”
- 应检查：是否有 implementation-bearing diff、是否绑定 owner issue、是否在该 issue 的 review artifact 中写了固定结构

## Decision

本轮冻结如下最小 contract：

1. canonical landing surface
- implementation decision note 的主落点固定为 issue-bound `code-reviews/` / verification artifact
- 其他产物只允许引用，不允许再复制一份并声称自己是主真源

2. 最小字段
- `decision`
- `why_this`
- `alternatives_considered`
- `boundary_non_goals`
- `residual_risk`

3. 何时强制
- develop-bound merge 若 materialize capability / implementation truth，而不是只改 pre-brainstorm / milestone / IBM / progress / laws prose，就必须有 implementation decision note

4. gate strategy
- `governance-merge-gate` 不判断 prose 质量
- 只判断：
  - 当前 diff 是否包含 implementation-bearing path
  - 当前 diff 是否绑定到 real owner issue
  - owner issue 的 `verification_artifact_dir` 下是否有 staged review artifact
  - review artifact 中是否有完整 decision note 最小字段

## Why Review Artifact

选择 review/verification artifact，而不是 `progress`、`prd.md` 或新目录，原因是：

1. 语义最贴合
- 这是对“本批实现决策”的 close reading，不是对 candidate / PRD 的重述

2. 与 issue 绑定天然存在
- issue 已有 `verification_artifact_dir`
- merge gate 已能把 review artifact 反查到 owner issue

3. 可以与 residual risk 同层
- 当前 verification 文档本来就在写 `Scope Verdict`、`Commands`、`Residual risk`、`Notes`
- implementation decision note 放在这里最自然

4. 不产生平行真相系统
- pre-brainstorm / IBM / dev-loop / verification 各自有主产物
- 本轮只补 dev-loop 缺口，不再引入新 artifact family

## Promotion Readiness

这条研究已经不只是原则讨论，边界已经稳定：

- 主落点已确定为 issue-bound review artifact
- 最小字段已冻结
- gate 可利用现有 `verification_artifact_dir` 与 `governance-merge-gate` 关联 owner issue
- 不需要改宪法；属于法律、skill、gate 与测试层

因此适合直接 materialize 成一个 focused governance issue，而不是继续停留在 umbrella 思辨。

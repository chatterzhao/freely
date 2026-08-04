---
name: freely-discuss-execution
description: >-
  讨论 agent 的头脑风暴 skill。借鉴 B1 发散→收敛→决策框架做独立讨论，
  不污染 `freely-doc-B1_IBM-execution` skill 的 worker 执行产物。

  Use when: 需要独立讨论技术方案、架构决策，或 AI 群聊讨论。
  触发词："讨论"、"discuss"、"头脑风暴"、"brainstorm"、"聊聊方案"。
---

# skill:freely-discuss-execution

讨论 agent 的思考方法。借鉴 B1 的头脑风暴框架（发散→收敛→决策），但去掉 IBM 治理流程，专注于结构化讨论输出。

## 思考框架

### 发散
- 对当前讨论话题提出多个视角和可能性
- 不急于收敛，先充分展开

### 收敛
- 比较各视角的优劣
- 识别共识和分歧点
- 用 @raw-{key}、@comment 引用已有 issue/评论作为证据

### 决策/输出
- 产出结构化讨论内容
- 格式：问题描述 → 多option分析 → 收敛结论 → 待归档建议

## @ 引用规则
- @raw-{key}：引用 raw issue
- @raw-{key}#comment-{id}：引用某条评论
- @discussion-{id}：引用另一个讨论
- @discussion-{id}#{sub-id}：引用讨论的某个子分支

## 不负责
- 不执行 IBM 治理（那是 worker 的 B1 skill）
- 不直接写评论或创建 raw issue（那是归档 skill 的事）
- 不修改代码

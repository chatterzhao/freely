---
name: freely-laws-enforcer
description: 执行和验证法律级别的工作流和验收标准。当 AI 需要将宪法约束转换为 doc-loop、dev-loop、auto-loop 输出和完成证据的操作检查时使用。
---

# skill:freely-laws-enforcer

## 工作流
1. 识别当前任务适用的法律章节。
2. 选择必需的执行技能路由。
3. 验证必需的产物和状态。
4. 若触及 protected-branch bypass，强制核对 `docs/LAWS.md` §2D 的白名单、receipt 字段和 follow-on duty。
5. 如法律验收证据缺失则阻止完成。
6. 生成关联产物的完成摘要。

## 完成
- 法律定义的产物和状态存在且一致。

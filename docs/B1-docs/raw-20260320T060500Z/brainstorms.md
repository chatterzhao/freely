# 预研头脑风暴：Agent 状态时光机与共享连续性控制面

## 来源
- 外部文章：`把 Agent 的状态放进数据库`，微信公众平台，2026-03-20
- 原文链接：`https://mp.weixin.qq.com/s/t5nNOS39jtzLsGJr-kcXvw`

## 背景
- 文章提出一个强假设：当 Agent 从单人单机走向多 Agent、多设备、多人协作与 To B 场景时，本地目录不再足够，状态需要进入一个可共享、可审计、可恢复、可分支的统一状态层。
- 文中用 PGFS/JuiceFS + PostgreSQL 作为实现例子，但真正有价值的不是具体技术，而是两个能力：
  - `time machine`：代码、配置、记忆、任务状态一起回到任意时间点
  - `shared brain`：多个 Agent / 多人 / 多机共享同一套 canonical state
- Freely 当前已经在做 worktree、checkpoint、continuity、recovery、handoff，但这些能力还没有统一成“状态级 snapshot / fork / rollback / shared continuity”问题。

## 文章里真正值得 Freely 吸收的点

### 1. 恢复对象不应只盯 Git 和代码
- 文章点得很准：很多关键状态不在 Git 里。
- 对 Freely 来说，这包括：
  - session continuity artifact
  - handoff / resolution artifact
  - runtime 状态与 supervisor 视图
  - manager/worker 的跨循环写回证据
- 如果这些状态出了问题，仅靠 Git commit / worktree 并不能把系统完整带回可继续运行的点。

### 2. “从某时刻 fork 一套实验环境” 是真实需求
- 文章把这一点描述成“基于某时间点瞬间克隆与分支”。
- Freely 已经有 worktree / feature branch / `test-pre-merge-*` 临时测试批次，但主要解决的是代码隔离。
- 未来如果要让多个 worker 或多个设备共享更强的连续性，可能还需要“状态级 fork”，而不只是代码级 fork。

### 3. 多 Agent 共享的不应只是目录，而是 canonical coordination state
- 文中举的是任务状态、共享记忆、共享工作目录。
- 对 Freely，更可取的表述是：
  - 共享 canonical issue / continuity / handoff / runtime snapshot
  - 保留 worker 私有上下文
- 这比“共享同一个文件目录”更贴近 Freely 的 owner/worktree 模型。

## 不应直接照搬的点

### 1. PGFS 不应成为 Freely 当前默认底座
- Freely 当前主线是三层循环、治理边界、自治监督与恢复。
- 若现在把 PGFS 变成默认依赖，会把问题从“治理与能力边界”提前扭成“基础设施选型”。

### 2. 共享同一工作目录会与现有 branch/worktree ownership 打架
- Freely 依赖 dedicated worktree 保障 owner 边界。
- 粗粒度共享目录可能削弱 worktree discipline，而不是增强它。

### 3. 不能把“数据库化”误当成“问题已解决”
- 文章的核心启发是统一状态面，不是“只要进数据库就自然治理正确”。
- Freely 仍需要先定义：
  - 什么状态应该被 snapshot
  - 谁拥有 snapshot / rollback / fork 的触发权
  - 这些能力属于 runtime、manager、还是独立 control plane

## 对 Freely 的预研问题

### 1. Freely 当前有哪些关键状态在 Git/worktree 治理外
- 需要列清：
  - session / handoff / recovery 证据
  - runtime / monitor / supervisor 状态
  - 多 worker 共享的协调状态

### 2. 哪些状态需要 snapshot / fork / rollback
- 不是所有状态都需要 PITR 级能力。
- 需要区分：
  - `must-recover-together`
  - `can-recompute`
  - `worker-private`
  - `shared-canonical`

### 3. 最小实现是否应从本地 snapshot index 开始
- 一个更现实的顺序可能是：
  - 先做本地 continuity snapshot index / fork metadata
  - 再决定是否需要数据库 backing
  - 最后再评估 PGFS / Postgres / object store / hybrid

## 初步判断
- 这条研究值得进入 Freely 的正式 candidate。
- 但 capability 应定义为：
  - `state snapshot + fork + rollback + shared continuity`
- 而不是：
  - `接入 PGFS`

## 非目标
- 本轮不做 PGFS 集成
- 本轮不把 PostgreSQL 定成 Freely 的默认运行时依赖
- 本轮不替换现有 branch/worktree 模型

# Freely 项目设计分析报告

## 一、项目概览

Freely 是一个 Jarvis 式的自主循环运行器，采用 IBM（Input-Brainstorm-Map）架构和三个 Loop 方法论（A:auto-loop、D:doc-loop、D:dev-loop）。

**核心组件**：
- ACP Bridge：与外部 AI CLI（claude-agent-acp）的持久会话管理
- A2A Server/Client：Agent 间通信协议（新增）
- Handoff 机制：Manager-Worker 状态传递与委托
- Runtime Daemon：自主循环运行的核心编排器

---

## 二、设计评估矩阵

| 维度 | 评级 | 说明 |
|------|------|------|
| ACP Session 管理 | ⭐⭐⭐⭐ 优秀 | 三级缓存命中策略，显著降低 token 成本 |
| 三个 Loop 方法论 | ⭐⭐⭐⭐ 优秀 | 问题处理分层清晰 |
| A2A 协议实现 | ⭐⭐⭐ 良好（新增） | 功能完整，但与现有系统集成不足 |
| Handoff 机制 | ⭐⭐ 中等 | 状态机复杂，exit_kind 过多 |
| Manager-Worker 通信 | ⭐⭐ 不足 | 缺乏标准化协议，依赖文件系统 |
| ACP-A2A 边界 | ⭐⭐ 不清晰 | 职责重叠，缺乏统一抽象 |

---

## 三、详细分析

### 3.1 优秀设计（应保留）

#### 3.1.1 ACP Session 三级缓存架构

```
第 1 级：同 session resume（几乎免费）
第 2 级：新 session 同 system prompt（便宜）
第 3 级：新 session 不同 prompt（全价）
```

**优势**：
- 解决了 direct 模式每次重发 system prompt 的高成本问题
- Manager 和 Worker 各自独立的 session 模型，互不干扰
- ACP Bridge 作为持久化 relay，支持跨 AI 循环复用

#### 3.1.2 三个 Loop 方法论

```
A:auto-loop（外循环）
├── 发现与路由 Issue
├── 进入 D:doc-loop 或 D:dev-loop
├── completion/verification/cleanup judgment
└── 吸收结果并进入下一轮
```

**优势**：
- 问题来源多样（scan、chat、github issue）
- B1→B2→Dev 的两阶段设计，确保问题收敛
- 里程碑作为规划层追踪已纳入任务

#### 3.1.3 Handoff 状态持久化

Handoff 作为 Manager-Worker 之间的状态持久层是合理的：
- 记录 `exit_kind`、`reason`、`next_action` 等状态
- 支持 worker 完成后 manager 接管
- 通过 SQLite 数据库持久化，支持恢复

---

### 3.2 问题设计（需重构）

#### 3.2.1 Handoff 状态机过于复杂

**问题**：
```python
EXIT_KIND_ALIASES = {
    'completed': 'worker_done',
    'success': 'worker_done',
    'partial': 'worker_done',
    # ... 30+ 个别名
    'blocked': 'worker_blocked',
    'stuck': 'worker_blocked',
    # ...
}
```

**分析**：
- 30+ 个 exit_kind 别名说明 AI 输出格式不统一
- `worker_done`、`worker_blocked`、`worker_handoff_needed` 三个状态在实际使用中经常混淆
- 大量 fallback 逻辑（如 `completion_summary` 作为 `reason` 的 fallback）表明设计不清晰

**建议**：
- 简化为 3-4 个核心状态：`working`、`completed`、`blocked`、`needs_handoff`
- AI 输出标准化，减少别名依赖
- 使用 A2A Task State 替代 exit_kind

#### 3.2.2 Manager-Worker 通信协议不标准

**当前设计**：
```
Manager → Worker：通过文件系统传递 prompt 文件
Worker → Manager：通过 handoff JSON 写入数据库
```

**问题**：
- 缺乏双向实时通信能力
- Worker 状态更新需要主动轮询或写入数据库
- 不支持 streaming、progress 更新等现代 agent 能力

**建议**：
- 采用 A2A 协议作为标准通信协议
- A2A Client 放在 Manager 端
- A2A Server 放在 Worker 端
- Handoff 降级为状态持久化层

#### 3.2.3 ACP 与 A2A 边界不清晰

**当前实现**：
- ACP Bridge：管理 AI CLI 的会话生命周期
- A2A Server/Client：Agent 间通信（新增，但未与 ACP 集成）

**问题**：
- ACP 关注的是"如何与 AI 通信"
- A2A 关注的是"agent 之间如何通信"
- 两者都涉及通信，但抽象层次不同，容易混淆

**建议**：
```
层1: ACP Bridge（AI CLI 会话管理）
     └─ 管理 claude-agent-acp 的生命周期
     └─ 提供 session/new、session/prompt 等接口

层2: A2A Protocol（Agent 间通信）
     └─ Manager ↔ Worker 的任务委托
     └─ 基于 ACP Bridge 构建

层3: Handoff（状态持久化）
     └─ A2A 的 fallback
     └─ 恢复时的状态来源
```

#### 3.2.4 A2A 实现与现有系统脱节

**问题**：
- A2A Server 已经实现，但：
  - 尚未与 Freely Runtime 集成
  - 尚未与 ACP Bridge 集成
  - 尚未有 worker 使用 A2A 协议
- 新增的 A2A 只是"技术演示"，不是生产实现

**建议**：
- 制定明确的迁移计划
- 从小处开始：在现有 handoff 基础上增加 A2A transport
- 保留 fallback 机制，确保向后兼容

---

### 3.3 架构问题汇总

#### 3.3.1 协议层叠问题

```
当前：
ACP Bridge ←→ claude-agent-acp
     ↓
文件系统/数据库
     ↓
Handoff ←→ Worker

建议：
ACP Bridge ←→ claude-agent-acp
     ↓
A2A Protocol ←→ Worker Agent
     ↓
Handoff（持久化）
```

#### 3.3.2 状态同步问题

**问题**：Manager 需要主动查询 Worker 状态
- 当前：轮询 handoff 表
- 问题：延迟高，资源浪费

**建议**：使用 A2A Server-Sent Events (SSE) 流推送

---

## 四、建议的 Issue

### Issue 1: A2A 协议与 Freely Runtime 集成

**描述**：
将 A2A 协议正式集成到 Freely Runtime，作为 Manager-Worker 通信的标准协议。

**验收标准**：
- Worker 启动时自动启动 A2A Server
- Manager 通过 A2A Client 委派任务
- A2A Task State 替代 exit_kind
- Handoff 作为 fallback 机制保留

### Issue 2: Handoff 状态机简化

**描述**：
简化 Handoff 的 exit_kind，从 30+ 别名简化为 3-4 个核心状态。

**验收标准**：
- AI 输出标准化，无需别名映射
- 核心状态：`working`、`completed`、`blocked`、`needs_handoff`
- 移除 fallback 逻辑

### Issue 3: 协议边界治理文档

**描述**：
编写文档明确 ACP、A2A、Handoff 的职责边界。

**验收标准**：
- 文档说明各层职责
- 明确数据流和调用关系
- 更新架构图

---

## 五、优先级建议

| Issue | 优先级 | 复杂度 | 价值 |
|-------|--------|--------|------|
| Issue 3: 协议边界文档 | P0 | 低 | 高（避免后续混乱） |
| Issue 2: Handoff 简化 | P1 | 中 | 高（降低维护成本） |
| Issue 1: A2A 集成 | P2 | 高 | 中（长期价值） |

---

## 六、结论

### 保留
- ACP Session 三级缓存架构
- 三个 Loop 方法论
- Handoff 状态持久化机制

### 优化
- 简化 Handoff exit_kind
- 明确 ACP-A2A-Handoff 边界
- 标准化 AI 输出格式

### 重构
- 将 A2A 作为 Manager-Worker 标准通信协议
- A2A Server 集成到 Worker Runtime
- A2A Client 集成到 Manager Runtime
- Handoff 降级为状态持久化层

---

*生成时间：2026-06-12*
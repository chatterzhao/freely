# Freely 项目设计分析总结报告

**生成时间**：2026-06-12  
**分析范围**：ACP 技术、A2A 协议、Agent 通信架构、Manager-Worker 协作

---

## 一、项目当前状态

### Worktree 概览
| Worktree | 分支 | 状态 |
|----------|------|------|
| 主目录 | develop | 受保护 |
| feature-raw-20260612T000223Z23Z-a2a-replace-handoff | feature/* | 活跃开发中 |
| test-pre-merge-20260612T000223Z-a2a-replace-handoff | test-pre-merge-* | 验证中 |

### 活跃 Milestone
- **M-20260524T053214Z-A**：`ACP session 生命周期接入 tool_switch_events` (in_dev)

---

## 二、设计评估总结

### 2.1 优秀设计（保留）

#### ✅ ACP Session 三级缓存架构
**评级**：⭐⭐⭐⭐⭐

```
第 1 级：同 session resume（几乎免费）
第 2 级：新 session 同 system prompt（便宜）
第 3 级：新 session 不同 prompt（全价）
```

**优势**：
- 解决 direct 模式每次重发 system prompt 的高成本问题
- Manager 和 Worker 各自独立的 session 模型
- ACP Bridge 作为持久化 relay，支持跨 AI 循环复用

**代码示例**：`acp-bridge.py` 中的 `session_new`、`session_resume`、`session_prompt` 方法

#### ✅ 三个 Loop 方法论
**评级**：⭐⭐⭐⭐⭐

```
A:auto-loop（外循环）
├── 发现与路由 Issue
├── 进入 D:doc-loop 或 D:dev-loop
└── completion/verification/cleanup judgment
```

**优势**：
- 问题来源多样化（scan、chat、github issue）
- B1→B2→Dev 两阶段设计确保问题收敛
- 里程碑作为规划层追踪已纳入任务

#### ✅ 宪法驱动的治理
**评级**：⭐⭐⭐⭐⭐

**优势**：
- 明确的分支策略（main/develop/feature/test-pre-merge-*）
- Worktree 隔离保证并行开发安全
- 硬性约束不可绕过

---

### 2.2 问题设计（需重构）

#### ⚠️ Handoff 状态机过于复杂
**评级**：⭐⭐

**问题**：
```python
EXIT_KIND_ALIASES = {
    'completed': 'worker_done',
    'success': 'worker_done',
    'partial': 'worker_done',
    'clean_success': 'worker_done',
    'completed_with_findings': 'worker_done',
    # ... 30+ 个别名
    'blocked': 'worker_blocked',
    'stuck': 'worker_blocked',
    'cannot_proceed': 'worker_blocked',
    # ...
}
```

**分析**：
- 30+ 个 exit_kind 别名说明 AI 输出格式不统一
- 大量 fallback 逻辑（`completion_summary` 作为 `reason` 的 fallback）表明设计不清晰
- 状态机过于复杂导致维护成本高

**根因**：试图让 AI 自由输出，然后通过别名映射规范化

**建议**：
- 简化为 3-4 个核心状态：`working`、`completed`、`blocked`、`needs_handoff`
- 标准化 AI 输出格式，减少别名依赖
- 使用 A2A Task State 替代 exit_kind

#### ⚠️ Manager-Worker 通信协议不标准
**评级**：⭐⭐

**当前设计**：
```
Manager → Worker：通过文件系统传递 prompt 文件
Worker → Manager：通过 handoff JSON 写入数据库
```

**问题**：
- 缺乏双向实时通信能力
- Worker 状态更新需要主动轮询
- 不支持 streaming、progress 更新

**建议**：
- 采用 A2A 协议作为标准通信协议
- 使用 SSE 流推送实时状态

#### ⚠️ A2A 实现与现有系统脱节
**评级**：⭐⭐⭐

**问题**：
- A2A Server 已经实现（功能完整）
- 但尚未与 Freely Runtime 集成
- 只是"技术演示"，不是生产实现

**建议**：
- 制定明确的迁移计划
- 保留 fallback 机制，确保向后兼容

#### ⚠️ ACP-A2A-Handoff 边界不清晰
**评级**：⭐⭐

**问题**：
```
当前：
ACP Bridge ←→ claude-agent-acp（AI CLI 会话管理）
     ↓
文件系统/数据库（状态传递）
     ↓
Handoff ←→ Worker

问题：
- ACP 关注"如何与 AI 通信"
- A2A 关注"agent 之间如何通信"
- 两者职责重叠，容易混淆
```

**建议**：
```
层1: ACP Bridge（AI CLI 会话管理）
层2: A2A Protocol（Agent 间通信）← 基于 ACP 构建
层3: Handoff（状态持久化）← A2A 的 fallback
```

---

## 三、核心问题分析

### 3.1 为什么 scan 列表没做完就停了？

**可能原因**：
1. **循环终止条件问题**：
   - Manager 发现所有任务都已处理或有活跃 worker
   - 但可能遗漏了新问题

2. **状态判断问题**：
   - scan 结果与 handoff 状态不同步
   - Manager 误判任务已完成

3. **资源限制**：
   - token 限制导致循环提前终止
   - context window 满了

**建议修复**：
- 检查 scan → handoff 状态转换逻辑
- 添加更详细的日志记录
- 验证循环终止条件

### 3.2 Manager-Worker 协作不好的根本原因

**核心问题**：缺乏标准化的双向通信协议

**当前**：通过文件系统传递 prompt，通过数据库传递结果
**问题**：
- 无法实时感知对方状态
- 需要主动轮询
- 没有流式更新

**解决方案**：A2A Protocol + SSE

---

## 四、建议的改进计划

### P0（立即行动）：协议边界治理文档

**目标**：明确 ACP、A2A、Handoff 职责边界

**验收标准**：
- [ ] 文档说明各层职责
- [ ] 明确数据流和调用关系
- [ ] 更新架构图

### P1（短期）：Handoff 状态机简化

**目标**：简化 exit_kind，从 30+ 别名简化为 3-4 个核心状态

**验收标准**：
- [ ] AI 输出标准化，无需别名映射
- [ ] 核心状态：`working`、`completed`、`blocked`、`needs_handoff`
- [ ] 移除 fallback 逻辑

### P2（中期）：A2A 协议正式集成

**目标**：将 A2A 作为 Manager-Worker 标准通信协议

**验收标准**：
- [ ] Worker 启动时自动启动 A2A Server
- [ ] Manager 通过 A2A Client 委派任务
- [ ] A2A Task State 替代 exit_kind
- [ ] Handoff 作为 fallback 机制保留

---

## 五、架构建议

### 推荐的 Agent 通信架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Manager Agent                           │
├─────────────────────────────────────────────────────────────┤
│  A2A Client                                                │
│  ├── discover_agent() → 发现 Worker 能力                   │
│  ├── create_task() → 创建 A2A Task                        │
│  ├── update_task() → 更新任务状态                          │
│  └── wait_for_completion() → 等待任务完成                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ A2A Protocol (Unix Socket)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Worker Agent                           │
├─────────────────────────────────────────────────────────────┤
│  A2A Server                                                │
│  ├── GET /agentCard → 声明能力                            │
│  ├── POST /tasks → 创建任务                               │
│  ├── PATCH /tasks/{id} → 更新状态                         │
│  └── SSE /tasks/{id}/stream → 流式状态推送               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ ACP Protocol
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     ACP Bridge                             │
├─────────────────────────────────────────────────────────────┤
│  session/new → 创建 AI CLI 会话                           │
│  session/prompt → 发送 prompt 获取响应                     │
│  session/resume → 恢复已有会话                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    claude-agent-acp
```

### A2A 与 Handoff 集成策略

**Phase 1：共存**
- 保持 Handoff 作为主要状态持久化
- A2A 作为可选通信层

**Phase 2：迁移**
- A2A Task 逐步替代 Handoff 表
- 保留 Handoff 作为 fallback

**Phase 3：简化**
- 删除 Handoff 状态机复杂度
- A2A 成为唯一协议

---

## 六、结论

### 保留
- ✅ ACP Session 三级缓存架构
- ✅ 三个 Loop 方法论
- ✅ 宪法驱动的治理
- ✅ Handoff 状态持久化机制

### 优化
- 🔧 Handoff exit_kind 简化
- 🔧 明确 ACP-A2A-Handoff 边界
- 🔧 标准化 AI 输出格式

### 重构
- 🔨 A2A 作为 Manager-Worker 标准通信协议
- 🔨 A2A Server 集成到 Worker Runtime
- 🔨 A2A Client 集成到 Manager Runtime
- 🔨 Handoff 降级为状态持久化层

---

*本报告基于对 Freely 项目代码和文档的全面分析生成*
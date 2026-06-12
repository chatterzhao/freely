---
name: a2a-replace-handoff
raw_key: raw-20260612T000223Z
created: 2026-06-12T00:10:00Z
status: proposed
---

# A2A 协议替换 Freely Handoff 架构重构 - Brainstorm

## 1. Discovery (发现)

### 问题来源
- Freely 自举开发中暴露：大量 `launch_failed, launchable check failed`
- scan 列表做完就停止的根因之一
- Manager 盲目委派 → Worker launchable check 失败

### 根因分析
```
grep "launch_failed" .freely/freely.db:
大量 launch_failed, launchable check failed

Manager 不知道 Worker 需要什么能力
→ 盲目委派
→ launchable check 失败
→ Worker 未启动
→ scan 列表停摆
```

### 现有机制问题

#### Handoff 机制缺陷
| 能力 | A2A | Freely Handoff |
|------|-----|----------------|
| Agent 能力发现 | ✅ Agent Card 标准 | ❌ 无 |
| 完整状态机 | ✅ 8 种状态 | ❌ 3 种状态 |
| 实时推送 | ✅ SSE/Streaming | ❌ 无 |
| 能力协商 | ✅ Capability negotiation | ❌ 无 |
| 开放互操作 | ✅ Linux 基金会标准 | ❌ 私有 |

## 2. Research (研究)

### A2A 协议概述
- Linux 基金会 AI Agents 工作组发布
- 定义 Agent 间通信标准
- 核心概念：
  - **Agent Card**: 描述 Agent 能力、技能、端点
  - **Task**: 任务状态机（submitted, working, completed, failed...）
  - **Message**: 任务消息（text, data, artifact）
  - **Streaming**: SSE/WebSocket 实时推送

### A2A vs MCP 对比
| 特性 | A2A | MCP |
|------|-----|-----|
| 用途 | Agent 间通信 | Agent 与工具交互 |
| 模式 | 双向对话 | 工具调用 |
| 状态管理 | 有 | 无 |
| 生态 | 开放标准 | Anthropic 主导 |

### Freely 适配性分析

#### 优势
1. **标准化能力声明**: Agent Card 解决 launchable check 失败问题
2. **状态机完善**: 8 种状态覆盖 Manager-Worker 完整生命周期
3. **实时通信**: SSE 替换轮询，Manager 实时感知 Worker 状态
4. **生态互操作**: 可与外部 Agent 系统互通

#### 挑战
1. **Freely 特有概念映射**:
   - worktree 隔离 → 需要自定义 agentProvider
   - exit_kind → 需要扩展 Task 状态
   - handoff_json → 需要自定义 artifact 类型
2. **同实例紧密协作**: A2A 设计为跨服务，Freely 是同一进程内的紧密耦合
3. **向后兼容**: 需要保留现有 DB schema 和 API

### 替代方案评估

#### 方案 A: A2A 彻底替换
- 完全采用 A2A 协议
- 自定义 Freely Agent Card 扩展
- 映射 exit_kind 到 A2A Task 状态
- SSE 替换轮询
- **优点**: 标准化、生态互操作
- **缺点**: 改动大、需要处理同实例紧耦合问题

#### 方案 B: Handoff + Agent Card 混合
- 保留 Handoff 核心逻辑
- 增加 Agent Card 能力声明
- 保留轮询（可渐进改为 SSE）
- **优点**: 改动小、风险低
- **缺点**: 仍是私有协议、不完整

#### 方案 C: 保持现状
- 不做架构重构
- 修复 launchable check 问题
- 增强 Handoff 状态机
- **优点**: 无架构风险
- **缺点**: 持续维护私有协议、无法与外部生态互通

## 3. Decision (决策)

### 推荐方案: 方案 A - A2A 彻底替换

**理由**:
1. 根因明确：Handoff 机制缺陷导致 launchable check 失败
2. A2A 是开放标准，长期价值大于短期改动成本
3. Freely 已有良好的模块化基础，可以平滑迁移
4. 解决后可以直接解决 scan 列表停摆问题

### 实现路径

#### Phase 1: 协议设计
- 设计 Freely Agent Card 扩展（worktree、skill、exit_kind）
- 映射 exit_kind → A2A Task 状态
- 定义 Freely 特有的 artifact 类型

#### Phase 2: 原型实现
- 实现 A2A Server (Worker 端)
- 实现 A2A Client (Manager 端)
- 保留 Handoff 作为 fallback

#### Phase 3: 状态迁移
- 将 handoff table 迁移到 A2A Task
- 迁移完成后删除旧 handoff 逻辑

#### Phase 4: 增强功能
- SSE 实时推送
- 能力协商
- 外部 Agent 互操作

### 关键里程碑
- M1: Agent Card 设计完成
- M2: 原型通过 basic handoff 测试
- M3: 完整状态机迁移
- M4: SSE 推送上线

### 风险与缓解
| 风险 | 缓解措施 |
|------|----------|
| 同实例紧耦合 | 使用 Unix Domain Socket |
| 状态映射丢失 | 保留完整映射表 |
| 性能下降 | 基准测试监控 |
| 外部 Agent 不兼容 | 提供 adapter 层 |

### 下一步
进入 `freely-doc-B2_IBM-execution`，产出 I-* issue，包含：
- PRD: A2A 协议详细设计
- pre-tests: 迁移测试用例
- tasks: 实施计划
- code-review: 架构评审

### 结论
A2A 替换 Handoff 是正确的架构方向。短期内需要较多改动，但长期价值明确。建议进入 B2_IBM 阶段产出详细设计。

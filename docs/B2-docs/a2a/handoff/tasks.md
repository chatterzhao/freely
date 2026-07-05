# Tasks: A2A 协议替换 Freely Handoff 架构重构

## Task 分解

### Phase 1: 协议设计

#### T1.1: Freely Agent Card 扩展设计
- **负责人**: AI
- **描述**: 设计 Freely Agent Card JSON Schema，包含 worktree 隔离、skill、exit_kind 扩展
- **输入**: A2A Agent Card 规范
- **输出**: `docs/system/workspace/a2a/freely-agent-card-schema.md`
- **验收**: Schema 能覆盖 Freely 特有能力

#### T1.2: exit_kind → A2A Task 状态映射表
- **负责人**: AI
- **描述**: 定义 exit_kind 到 A2A Task 状态的完整映射
- **输入**: 当前 handoff exit_kind 定义
- **输出**: `docs/system/workspace/a2a/exit-kind-mapping.md`
- **验收**: 映射表完整且可逆

#### T1.3: Freely 特有 artifact 类型定义
- **负责人**: AI
- **描述**: 定义 handoff_json、completion_summary、evidence_paths 的 artifact 类型
- **输入**: 当前 handoff JSON Schema
- **输出**: `docs/system/workspace/a2a/freely-artifact-types.md`
- **验收**: artifact 类型能表示所有 handoff 场景

#### T1.4: 架构评审
- **负责人**: AI + 人类审查
- **描述**: 评审 Phase 1 设计文档
- **输入**: T1.1-T1.3 输出
- **输出**: 评审报告
- **验收**: 评审通过

### Phase 2: 原型实现

#### T2.1: A2A Server (Worker 端) 实现
- **负责人**: AI
- **描述**: 实现 A2A Server，包含 Agent Card endpoint、Task CRUD、SSE streaming
- **输入**: Phase 1 设计
- **输出**: `docs/system/workspace/scripts/runtime/a2a_server.py`
- **验收**: 
  - Agent Card endpoint 可访问
  - Task CRUD 操作正常
  - SSE streaming 正常工作

#### T2.2: A2A Client (Manager 端) 实现
- **负责人**: AI
- **描述**: 实现 A2A Client，包含能力发现、Task 创建和状态监控
- **输入**: Phase 1 设计
- **输出**: `docs/system/workspace/scripts/runtime/a2a_client.py`
- **验收**: 
  - 能发现 Worker Agent Card
  - 能创建和监控 Task

#### T2.3: Handoff Fallback 实现
- **负责人**: AI
- **描述**: 保留现有 Handoff 作为 fallback
- **输入**: 当前 handoff 实现
- **输出**: 修改后的 handoff.py
- **验收**: A2A 不可用时自动 fallback

#### T2.4: Basic Handoff 测试
- **负责人**: AI
- **描述**: 验证 basic handoff 场景
- **输入**: pre-tests.md
- **输出**: 测试日志
- **验收**: T1-T4 测试通过

### Phase 3: 状态迁移

#### T3.1: handoff table 迁移脚本
- **负责人**: AI
- **描述**: 编写脚本将 handoff table 迁移到 A2A Task
- **输入**: 当前 handoff.db
- **输出**: `bin/a2a-migrate-handoff.py`
- **验收**: 迁移脚本正确处理所有记录

#### T3.2: 迁移验证
- **负责人**: AI
- **描述**: 验证迁移后数据完整性
- **输入**: 迁移后的 A2A Task
- **输出**: 验证报告
- **验收**: 无数据丢失

#### T3.3: 旧 handoff 逻辑删除
- **负责人**: AI
- **描述**: 删除旧的 handoff 逻辑（确认迁移成功后）
- **输入**: Phase 3.2 验证结果
- **输出**: 修改后的 handoff.py
- **验收**: 旧代码删除且无回归

#### T3.4: 性能基准测试
- **负责人**: AI
- **描述**: 基准测试 A2A vs Handoff 性能
- **输入**: 性能测试脚本
- **输出**: 基准测试报告
- **验收**: 性能不下降

### Phase 4: 增强功能

#### T4.1: SSE 实时推送完善
- **负责人**: AI
- **描述**: 完善 SSE 推送，覆盖所有状态变化
- **输入**: T2.1 输出
- **输出**: 修改后的 a2a_server.py
- **验收**: T3 测试通过

#### T4.2: 能力协商自动化
- **负责人**: AI
- **描述**: 实现能力协商自动化
- **输入**: A2A 能力协商规范
- **输出**: 修改后的 a2a_client.py
- **验收**: 能自动协商能力

#### T4.3: 外部 Agent 互操作
- **负责人**: AI
- **描述**: 实现与外部 A2A Agent 的互操作
- **输入**: 外部 A2A Agent 测试
- **输出**: adapter 层代码
- **验收**: T5 测试通过

## 依赖关系

```
T1.1 ─┬─ T1.4
T1.2 ─┘    │
          ↓
T2.1 ─┬─ T2.4
T2.2 ─┘
T2.3 ────────↓
               │
T3.1 ─┬─ T3.2 ─┬─ T3.3 ─┬─ T3.4
T4.1 ─┴────────┴────────┴─ T4.2 ─→ T4.3
```

## 时间估算

| Phase | 任务数 | 估算工时 |
|-------|--------|----------|
| Phase 1 | 4 | 4h |
| Phase 2 | 4 | 8h |
| Phase 3 | 4 | 6h |
| Phase 4 | 3 | 6h |
| **总计** | **15** | **24h** |

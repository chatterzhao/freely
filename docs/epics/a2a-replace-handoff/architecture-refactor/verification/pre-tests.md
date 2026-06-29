# Pre-Tests: A2A 协议替换 Freely Handoff 架构重构

## Acceptance Items v2

### 核心功能测试

#### T1: Agent Card 发现
- **描述**: Manager 能通过 Agent Card 发现 Worker 能力
- **预期结果**: GET /.well-known/agent.json 返回 Freely Agent Card
- **验证方式**: 
  ```bash
  curl http://localhost:7890/.well-known/agent.json
  # 应返回包含 freely 扩展的 Agent Card
  ```

#### T2: exit_kind 状态映射
- **描述**: exit_kind 正确映射到 A2A Task 状态
- **预期结果**: 
  | exit_kind | Task state |
  |-----------|------------|
  | worker_working | working |
  | worker_done | completed |
  | worker_blocked | input-required |
- **验证方式**: 发送 handoff_json，检查 Task 状态

#### T3: SSE 实时推送
- **描述**: Manager 能通过 SSE 接收 Worker 状态实时推送
- **预期结果**: Worker 状态变化时，SSE 流立即推送
- **验证方式**: 
  ```bash
  curl -N http://localhost:7890/tasks/{id}/stream
  # Worker 状态变化时，应收到推送
  ```

#### T4: Handoff 兼容
- **描述**: 现有 handoff 场景全部兼容
- **预期结果**: 旧 handoff JSON 能正确转换为 A2A Task
- **验证方式**: 发送旧格式 handoff_json，验证转换正确

#### T5: 外部 Agent 互操作
- **描述**: 与外部 A2A Agent 能互通
- **预期结果**: 能接收外部 Agent 的 Task，并返回结果
- **验证方式**: 使用外部 A2A Client 测试

### 性能测试

#### T6: 延迟基准
- **描述**: A2A 通信延迟不超过 Handoff
- **预期结果**: Task 创建到状态更新的延迟 < 100ms
- **验证方式**: 基准测试脚本

#### T7: 并发能力
- **描述**: 支持多个并发 Task
- **预期结果**: 10 个并发 Task 正常处理
- **验证方式**: 并发测试脚本

### 边界测试

#### T8: 异常处理
- **描述**: 异常情况下正确处理
- **预期结果**: 
  - 网络断开时重试
  - 超时时返回错误
  - 无效 JSON 时报错
- **验证方式**: 异常场景测试

#### T9: Fallback 机制
- **描述**: A2A 不可用时 fallback 到 Handoff
- **预期结果**: A2A 服务不可用时，自动切换到旧 Handoff
- **验证方式**: 模拟 A2A 服务不可用

## 测试执行

### 环境准备
```bash
# 启动 A2A Server (Worker 端)
freely start --mode worker

# 启动 Manager
freely start --mode manager
```

### 执行测试
```bash
# 运行所有 pre-tests
./bin/freely test --suite a2a-migration

# 运行单个测试
./bin/freely test --test T1-agent-card-discovery
```

### 验证通过标准
- 所有 T1-T9 测试通过
- 性能测试结果符合预期
- 无回归问题

## 测试产物

- 测试日志：`.freely/test-results/a2a-migration-{timestamp}.log`
- 覆盖率报告：`.freely/test-results/coverage-a2a-{timestamp}.html`
- 性能报告：`.freely/test-results/benchmark-a2a-{timestamp}.json`

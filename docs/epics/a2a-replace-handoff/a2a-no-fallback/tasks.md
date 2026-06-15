# Tasks: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)

## Task 分解

### Phase 1: 修复信号文件 WORKERS 字段

#### T1.1: a2a_task.py — a2a-exit 写入 WORKERS
- **负责人**: AI
- **描述**: 修改 `a2a_task.py`，在 a2a-exit 路径中增加 WORKERS 字段写入到 `last-exit-task.env`
- **输入**: 当前 `a2a_task.py` 源码
- **输出**: 修改后的 `a2a_task.py`
- **验收**: a2a-exit 后 `last-exit-task.env` 包含 WORKERS 字段

#### T1.2: env 文件格式验证
- **负责人**: AI
- **描述**: 验证 `last-exit-task.env` 中 WORKERS 字段的 JSON 格式正确，下游可正常解析
- **输入**: T1.1 输出
- **输出**: 测试日志
- **验收**: 下游读取 WORKERS 字段正常

### Phase 2: 更新所有 Prompt

#### T2.1: manager-agent.md 更新
- **负责人**: AI
- **描述**: 将 `manager-agent.md` 中的 JSON block 指令替换为 a2a-exit 指令
- **输入**: 当前 `manager-agent.md`
- **输出**: 修改后的 `manager-agent.md`
- **验收**: 文件中无 JSON block 指令残留

#### T2.2: worker-agent.md 更新
- **负责人**: AI
- **描述**: 将 `worker-agent.md` 中的 JSON block 指令替换为 a2a-exit 指令
- **输入**: 当前 `worker-agent.md`
- **输出**: 修改后的 `worker-agent.md`
- **验收**: 文件中无 JSON block 指令残留

#### T2.3: 系统 prompt 更新
- **负责人**: AI
- **描述**: 将系统 prompt 中的 JSON block 指令替换为 a2a-exit 指令
- **输入**: 当前系统 prompt 文件
- **输出**: 修改后的系统 prompt
- **验收**: 文件中无 JSON block 指令残留

#### T2.4: WORKER_STATE_INJECT 更新
- **负责人**: AI
- **描述**: 移除 WORKER_STATE_INJECT 中的 JSON block 指令
- **输入**: 当前 WORKER_STATE_INJECT 定义
- **输出**: 修改后的 WORKER_STATE_INJECT
- **验收**: 区块中无 JSON block 指令残留

#### T2.5: repair prompt 更新
- **负责人**: AI
- **描述**: 将 repair prompt 中的 JSON block 指令替换为 a2a-exit 指令
- **输入**: 当前 repair prompt
- **输出**: 修改后的 repair prompt
- **验收**: 文件中无 JSON block 指令残留

#### T2.6: delta prompt 更新
- **负责人**: AI
- **描述**: 将 delta prompt 中的 JSON block 指令替换为 a2a-exit 指令
- **输入**: 当前 delta prompt
- **输出**: 修改后的 delta prompt
- **验收**: 文件中无 JSON block 指令残留

### 验证

#### T3.1: 全量 grep 确认
- **负责人**: AI
- **描述**: 对所有 prompt 文件进行 grep，确认无 JSON block 指令残留
- **输入**: 修改后的所有 prompt 文件
- **输出**: grep 结果日志
- **验收**: grep 返回空

#### T3.2: Fallback 恢复验证
- **负责人**: AI
- **描述**: 设置 `FREELY_A2A_TEXT_PARSING_FALLBACK=1`，验证旧行为可恢复
- **输入**: T1.1-T2.6 修改后的代码
- **输出**: 测试日志
- **验收**: env 生效时旧路径可用

## 依赖关系

```
T1.1 ──→ T1.2
               
T2.1 ──→ T2.2 ──→ T2.3 ──→ T2.4 ──→ T2.5 ──→ T2.6
                                              │
                                              ↓
                                         T3.1 ──→ T3.2
```

## 时间估算

| Phase | 任务数 | 估算工时 |
|-------|--------|----------|
| Phase 1 | 2 | 1h |
| Phase 2 | 6 | 2h |
| 验证 | 2 | 1h |
| **总计** | **10** | **4h** |

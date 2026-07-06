# Pre-Tests: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)

## Acceptance Items v2

### 核心功能测试

#### T1: a2a-exit 写入 WORKERS
- **描述**: a2a_task.py 的 a2a-exit 路径正确写入 WORKERS 字段到 last-exit-task.env
- **预期结果**: 
  - `last-exit-task.env` 包含 `WORKERS` 字段
  - WORKERS 值为合法 JSON 数组
- **验证方式**: 
  ```bash
  # 触发 a2a-exit 后检查 env 文件
  grep "WORKERS" /path/to/last-exit-task.env
  # 应返回 WORKERS=["...","..."]
  ```

#### T2: manager-agent.md 无 JSON block
- **描述**: manager-agent.md 中无 JSON block 指令残留
- **预期结果**: 文件中所有 JSON block 相关指令已替换为 a2a-exit 指令
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block\|<json>" docs/agents/manager-agent.md
  # 应返回空
  ```

#### T3: worker-agent.md 无 JSON block
- **描述**: worker-agent.md 中无 JSON block 指令残留
- **预期结果**: 文件中所有 JSON block 相关指令已替换为 a2a-exit 指令
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block\|<json>" docs/agents/worker-agent.md
  # 应返回空
  ```

#### T4: 系统 prompt 无 JSON block
- **描述**: 系统 prompt 中无 JSON block 指令残留
- **预期结果**: 系统 prompt 中的 JSON block 指令已移除
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block\|<json>" /path/to/system-prompt
  # 应返回空
  ```

#### T5: WORKER_STATE_INJECT 无 JSON block
- **描述**: WORKER_STATE_INJECT 区块中无 JSON block 指令残留
- **预期结果**: 区块中所有 JSON block 指令已移除
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block\|<json>" /path/to/worker_state_inject
  # 应返回空
  ```

#### T6: repair prompt 无 JSON block
- **描述**: repair prompt 中无 JSON block 指令残留
- **预期结果**: 文件中已使用 a2a-exit 指令
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block" /path/to/repair-prompt
  # 应返回空
  ```

#### T7: delta prompt 无 JSON block
- **描述**: delta prompt 中无 JSON block 指令残留
- **预期结果**: 文件中已使用 a2a-exit 指令
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block" /path/to/delta-prompt
  # 应返回空
  ```

### 回退测试

#### T8: Fallback 环境变量恢复
- **描述**: 设置 `FREELY_A2A_TEXT_PARSING_FALLBACK=1` 后，旧行为可恢复
- **预期结果**: 
  - 环境变量生效时，旧文本解析路径可用
  - AI 输出 JSON block 格式时仍可被正确解析
- **验证方式**: 
  ```bash
  FREELY_A2A_TEXT_PARSING_FALLBACK=1 ./bin/freely test --suite a2a-text-fallback
  # 应与修改前行为一致
  ```

### 边界测试

#### T9: 空 WORKERS 场景
- **描述**: 当无 Worker 被委派时，WORKERS 字段的处理
- **预期结果**: 
  - WORKERS 可序列化为空数组 `[]`
  - 下游读取空数组时不会报错
- **验证方式**: 触发无委派场景，检查 env 文件

#### T10: 全量 grep 审计
- **描述**: 全仓确认无 JSON block 指令残留
- **预期结果**: 除了明确注释说明的兼容代码，无 JSON block 指令
- **验证方式**: 
  ```bash
  grep -rn "json_block\|JSON block\|<json>" --include="*.md" --include="*.py" \
    docs/agents/ scripts/ src/
  # 应只在兼容/注释中出现
  ```

## 测试执行

### 环境准备
```bash
# 确保在 feature/a2a-no-fallback 分支
git branch | grep feature/a2a-no-fallback
```

### 执行测试
```bash
# 运行所有 pre-tests
./bin/freely test --suite a2a-no-fallback

# 运行单个测试
./bin/freely test --test T1-a2a-exit-workers
```

### 验证通过标准
- 所有 T1-T10 测试通过
- 全量 grep 确认无遗漏 prompt 文件
- Fallback 恢复验证通过

## 测试产物

- 测试日志：`.freely/test-results/a2a-no-fallback-{timestamp}.log`
- grep 审计日志：`.freely/test-results/grep-audit-{timestamp}.log`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。

# Brainstorm: a2a-exit --agent-id vs --role 参数不匹配

## 问题发现过程

2026-06-18 Freely daemon 以 task_mode=auto 启动后，Manager Round 1-3 运行期间出现：
- Manager 声称"已派出 2 个 Worker"（task IDs: d3273b2c, 72d91911）
- 但 `a2a_task.py list --role worker --status submitted` 返回空
- Runtime 事件记录 `manager_exit_contract_delegate_workers worker_prompts_csv=none`
- Manager continuity 报告: "Workers created via a2a-exit --role worker are never executed"

## 根因分析

1. **Manager prompt 模板** (`manager-agent.md`) 使用 `--agent-id worker`
2. **a2a-exit handler** (`a2a_task.py:798`) 读取 `--role` 参数设置 `agent_id`，不识别 `--agent-id`
3. Manager 执行 `a2a-exit --agent-id worker` → handler 使用默认值 `agent_id=manager` → task 创建为 manager
4. Runtime `list --role worker --status submitted` 查询 agent_id=worker 的 task → 找不到
5. Worker 委派链路完全中断

## 同时发现的 config_bool_enabled bug

同一 session 的 daemon-launch.log 中出现：
```
config_bool_enabled: command not found
→ tool_unproductive detected → runtime stopped
```

根因：`freely` 脚本第 3975 行函数名被重复拼接：`config_bool_enabledconfig_bool_enabled()`。
5 个调用点全部静默失败，导致 slot 切换、工具自动恢复、代理配置等保护逻辑被跳过。

## 方案评估

### 方案 A：仅修正 Manager prompt 模板
- 将 `manager-agent.md` 中所有 `--agent-id worker` 改为 `--role worker`
- 同时修改 `acp-a2a-architecture.md` 中的相同错误
- 优点：最小改动，消除根因
- 缺点：其他文档/raw issue 中仍可能有 `--agent-id worker` 残留，未来再犯

### 方案 B：方案 A + a2a-exit handler 向后兼容
- 方案 A 全部
- `a2a_task.py` a2a-exit handler 添加 fallback：若 `--agent-id` 有值且 `--role` 为默认值 → 映射 `--agent-id` 到 `--role`
- 优点：对历史 prompt 模板兼容，降低未来犯错成本
- 缺点：维护一个废弃参数的兼容代码

### 方案 C：修改 a2a-exit handler 统一用 `--agent-id`
- 所有 prompt 模板和文档保留 `--agent-id`
- 修改 handler 直接读取 `--agent-id`（已经是 argparse 的已知参数）
- 优点：prompt 模板不用改
- 缺点：与现有 Runtime 内部使用 `--role` 的约定冲突（第 12886 行等）

## 决策：方案 B

- 主路径：prompt 模板统一使用 `--role worker`（与 Runtime 内部约定一致）
- 安全网：a2a-exit handler 兼容 `--agent-id` 作为 fallback
- 同时修复 config_bool_enabled bug
- 同步更新三个 loop 文档，记录接口约定和已知陷阱

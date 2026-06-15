# PRD: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)

## Goal

消除双路径（a2a-exit + 文本 JSON 解析 fallback），使全线走 a2a-exit 标准路径。本次 Phase 1+2 覆盖信号文件修复和 Prompt 统一。

## Background

### 当前问题

父 Epic `a2a-replace-handoff` 已完成 A2A 协议替换 Handoff 的核心实现。但代码中仍存在双路径：

```
a2a-exit (标准路径)      ────→   A2A Task State Machine
                               ↗
文本JSON解析 (fallback)  ────→   旧 handoff exit_kind 映射
```

### 双路径的危害

| 危害 | 说明 |
|------|------|
| 维护成本双倍 | 两套解析逻辑、两套持久化、两套 prompt 指令 |
| 行为不确定性 | 哪个路径实际生效取决于运行时上下文 |
| 测试覆盖分散 | 需要同时测试两个路径 |
| 迁移阻塞 | fallback 存在让 AI 倾向输出旧格式 |

## Scope

### In Scope (Phase 1+2)

#### Phase 1: 信号文件 WORKERS 字段
- 修复 `a2a_task.py` 的 a2a-exit 路径
- 确保 WORKERS 字段正确写入 `last-exit-task.env`
- 验证 env 文件格式符合下游预期

#### Phase 2: Prompt 统一
- 更新 `manager-agent.md`：改为 a2a-exit 指令
- 更新 `worker-agent.md`：同上
- 更新系统 prompt：移除 JSON block 指令
- 更新 `WORKER_STATE_INJECT`：移除 JSON block 指令
- 更新 repair prompt：改为 a2a-exit
- 更新 delta prompt：改为 a2a-exit

### Out of Scope (Phase 3-6，后续完成)

- 删除 `parse_a2a_task_json_reply` 的 tail+regex 路径
- 删除 `last-workers-csv.txt`/`last-exit-kind.txt` 持久化
- 废弃 `a2a_task_parser.py`
- Worker handoff 改用 DB 查询

## Design

### Phase 1: 信号文件修复

```python
# a2a_task.py — a2a-exit 写入 WORKERS 字段
# 修改前：缺少 WORKERS 写入
def write_a2a_exit(...):
    write_env("last-exit-task.env", {
        "A2A_TASK_STATE": state,
        "EXIT_KIND": exit_kind,
        # WORKERS 字段缺失
    })

# 修改后：增加 WORKERS 字段写入
def write_a2a_exit(...):
    write_env("last-exit-task.env", {
        "A2A_TASK_STATE": state,
        "EXIT_KIND": exit_kind,
        "WORKERS": json.dumps(workers_list),  # 新增
    })
```

### Phase 2: Prompt 指令替换

所有 prompt 文件中的 JSON block 指令替换标准：

```
旧指令（移除）:
  <json_block>
  "exit_kind": "...",
  "completion_summary": "..."
  </json_block>

新指令（使用 a2a-exit）:
  使用 a2a-exit 命令输出 A2A Task 标准格式
```

## Dev-Loop Handoff

B2_IBM 完成后，进入 `skill:freely-dev-loop-execution`：

1. 实现 Phase 1 信号文件修复
2. 实现 Phase 2 Prompt 替换
3. pre-tests 验证
4. 提交 code-review
5. 通过后合并到 develop

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| Prompt 变更影响 AI 输出 | FREELY_A2A_TEXT_PARSING_FALLBACK=1 可恢复 |
| 遗漏某些 prompt 文件 | 使用 grep 确认完整分布后再修改 |
| WORKERS 格式变更下游不兼容 | 保持与下游期望一致的 JSON 格式 |

# PRD: Manager prompt 模板补 --role worker + a2a_task.py --role 改为 required

- issue_id: I-20260719T071858Z-A
- epic: a2a
- story: task-role-required

## Goal

Manager AI 委派 Worker task 时 a2a-exit 命令正确携带 `--role worker`，确保 task 以正确的 agent_id 创建在 A2A DB 中，Runtime 能够发现并启动 Worker ACP session。

## 实现方案

### 修改 1: Manager prompt 模板（freely L15528-15539）

改前:
```bash
python3 docs/system/workspace/scripts/runtime/a2a_task.py a2a-exit \
  --state submitted|completed|failed \
  --summary "本轮做了什么" \
  --workers "worker-prompt.csv路径（委派时填写）" \
  --next "下一步建议"

示例 — 委派 Worker:
  a2a-exit --state submitted --summary "created 3 workers" --workers "..."

示例 — 分析完成无事可做:
  a2a-exit --state failed --summary "no actionable items, scan stale"
```

改后:
```bash
python3 docs/system/workspace/scripts/runtime/a2a_task.py a2a-exit \
  --state submitted|completed|failed \
  --role worker|manager \
  --summary "本轮做了什么" \
  --workers "worker-prompt.csv路径（委派时填写）" \
  --next "下一步建议"

示例 — 委派 Worker:
  a2a-exit --state submitted --role worker --summary "created 3 workers" --workers "..."

示例 — Manager 自身状态:
  a2a-exit --state submitted --role manager --summary "analysis in progress, delegating next round"

示例 — 分析完成无事可做:
  a2a-exit --state failed --role manager --summary "no actionable items, scan stale"
```

### 修改 2: a2a_task.py L830

改前:
```python
p_exit.add_argument("--role", default="manager", help="Role: manager|worker")
```

改后:
```python
p_exit.add_argument("--role", required=True, help="Role: manager|worker")
```

### 全仓调用点验证

修改前需确认所有现有 `a2a-exit` 调用已传 `--role`：
- freely 中的 prompt 模板（本次修复目标）
- three-loop-capability-lifecycle.md L156-157（文档示例，已有 --role worker）
- manager-agent.md L83（agent 文档，已有 --role worker）
- Worker 退出时的 a2a-exit

## Dev-Loop Handoff

- 修改文件:
  - `docs/system/workspace/scripts/runtime/freely` L15528-15544
  - `docs/system/workspace/scripts/runtime/a2a_task.py` L830
- 改动: 2 文件，~10 行

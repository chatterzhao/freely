---
local_id: raw-20260621T043842Z42Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T043842Z-A
platform_ids:
  github:
    issue_id: '3201'
    url: https://github.com/chatterzhao/freely/issues/3201
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T04:38:59Z'
updated_at: '2026-06-21T04:38:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

Worker fork session 调用 `a2a-exit` 时，`a2a_task.py` 通过 `os.getcwd()` 获取项目路径来计算 A2A socket 路径。但 worker 的 CWD 是 worktree 目录，与 manager 项目路径不同，导致 socket 路径不匹配，worker 无法连接 A2A server。

## 根因链

1. **A2A socket 路径计算** (`a2a_server.py` L53-54, `a2a_task.py` L22-24):
   ```python
   f"/tmp/freely-a2a-{sha256(abspath(project))[:16]}.sock"
   ```
   完全由 project 路径决定。

2. **Worker fork 启动** (`freely` L12496-12508): `cd "$target_project"`（worktree 目录）
   → fork session CWD 变成 worktree 路径

3. **a2a_task.py 解析 project** (`a2a_task.py` L31-32):
   ```python
   def _resolve_project() -> str:
       return PROJECT or os.getcwd()  # ← worktree 路径
   ```

4. **Socket path 不匹配**: Manager 的 socket 在 `/tmp/freely-a2a-{hash(manager)}.sock`，Worker 计算的是 `/tmp/freely-a2a-{hash(worktree)}.sock` → 不存在。

5. **错误静默** (`a2a_task.py` L853-855): 打印 JSON error 但 exit code 0

## 关键发现

`SESSION_PARENT_PROJECT="$manager_project"` **已写入** worker 的 session state file（`freely` L12454），但 **未导出** 到 worker 子进程的环境变量中（L12498 只导出了 `FREELY_ROLE_HINT` 和 `SESSION_PARENT_ID`）。

## Fork 是正确的选择

Fork 的架构意图（`session-lifecycle-protocol.md` L72-78）:
- Worker 继承 manager 上下文（cache hit，节省 40-120x 成本）
- Worker 写入自己的 JSONL（不污染 manager session）
- A2A socket 隔离是**意外副作用**，非设计目标

**Fork 是正确的 launch kind**，无需改变。只需修复 socket 路径传递。

## 修复方案

最优雅的方案（最小改动、最一致）:

1. `freely` L12498: 在 worker 子进程环境中增加:
   ```bash
   export SESSION_PARENT_PROJECT="$manager_project"
   ```

2. `a2a_task.py` L31-32: `_resolve_project()` 检查环境变量:
   ```python
   def _resolve_project() -> str:
       return PROJECT or os.environ.get("SESSION_PARENT_PROJECT") or os.getcwd()
   ```

与已有的 `SESSION_PARENT_ID` 模式一致，改动仅 3 行代码。

---
local_id: raw-20260622T123204Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3364'
    url: https://github.com/chatterzhao/freely/issues/3364
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T12:32:21Z'
updated_at: '2026-06-22T12:32:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

当前代码中多处直接使用 `gh issue close`、`gh issue create` 等裸命令，绕过了 platform-adapter 的统一封装。platform-adapter 是所有平台操作（GitHub/Gitee）的唯一入口。

具体违规点：
1. `wt-close --platform-only` 内部用 `gh issue close` 关平台 issue——应改用 platform-adapter
2. `issue-sync` 内部多处 `gh issue close/comment`
3. 其他脚本中散落的 `gh` 调用

## 修复

### 1. platform-adapter 加 `close` CLI 子命令
```python
# platform-adapter.py __main__ 加:
elif sys.argv[1] == "close":
    platform, num = sys.argv[2], sys.argv[3]
    result = close_issue("", num)  # local_id 可为空，只关平台
    print(json.dumps(result))
```

### 2. wt-close --platform-only 改用 platform-adapter
```bash
# 旧: gh issue close "$_po_raw_gh" --repo ...
# 新:
python3 "$PROJECT_ROOT/docs/system/workspace/scripts/sync/platform-adapter.py" \
  close github "$_po_raw_gh"
```

### 3. 审计所有 gh 调用
找出所有直接 `gh issue` / `gh pr` 调用，逐一改为 platform-adapter 或封装命令。

## 涉及文件
- `docs/system/workspace/scripts/sync/platform-adapter.py` — 加 close CLI
- `docs/system/workspace/scripts/worktree/wt-close` — 替换 gh issue close
- `bin/issue-sync` — 审计 gh 调用
- 其他有裸 gh 调用的脚本

## 原则
- 平台 API 调用只存在于 platform-adapter 内部
- 所有其他代码通过 platform-adapter CLI 或 issue-sync 间接操作平台
- Agent 永远不直接调 gh

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
local_id: raw-20260626T130431Z31Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3551'
    url: https://github.com/chatterzhao/freely/issues/3551
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T13:04:51Z'
updated_at: '2026-06-26T13:32:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T130431Z-A
source_candidate: docs/B1-docs/raw-20260626T130431Z31Z/candidates.md#C-20260626T130431Z-A
---

## 问题

Phase 6b（test-pre-merge 清理）硬编码 `git worktree remove --force` 和 `git branch -D`，无论 wt-close 是否传了 `--force`。且所有错误用 `2>/dev/null || true` 静默吞掉。

## 设计

`--force` 必须与 `--reason` 配套使用（已有 gate）。`--reason` 的内容就是用户的确认：意思是"严重警告，继续将彻底丢失，丢弃所有修改"。

### 无 --force 时
安全删除，失败必须报错阻塞，不能用 `--force` / `-D`。

```bash
if [[ "$FORCE" != true ]]; then
    # 安全删除：worktree 不用 --force，branch 用 -d
    if [[ -d "$_tp_wt" ]]; then
        git worktree remove "$_tp_wt" || { echo "wt-close: 删除 test 工位失败" >&2; exit 1; }
    fi
    if git show-ref --verify --quiet "refs/heads/$_tp_branch"; then
        git branch -d "$_tp_branch" || { echo "wt-close: 删除 test 分支失败" >&2; exit 1; }
    fi
    echo "wt-close: test-pre-merge cleaned ✓"
fi
```

### 有 --force 时
`--reason` 已确认用户意图。执行后打印严重警告日志：**"严重警告，已经用 --force 参数彻底丢弃了所有修改"**。

```bash
if [[ "$FORCE" == true ]]; then
    echo "wt-close: 严重警告 —— 已经用 --force 参数彻底丢弃了所有修改"
    [[ -d "$_tp_wt" ]] && git worktree remove --force "$_tp_wt" || true
    git branch -D "$_tp_branch" 2>/dev/null || echo "wt-close: warning - test branch deletion failed" >&2
fi
```

## 涉及文件

- `docs/system/workspace/scripts/worktree/wt-close`: Phase 6b 逻辑重写

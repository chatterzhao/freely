---
b1_id: B1-20260708T183102Z
phase_state: completed
source_raw: raw-20260708T183102Z
created_at: 2026-07-08
---

# B1_IBM: pr-merge-guarded path + wt-close issue-sync + worktree resolution

## Input

raw issue: raw-20260708T183102Z。5 个问题分布在 pr-merge-guarded 和 wt-close 两个文件中。

## Problem

### Bug 1: _sync_issues_changed_in_merge 读文件路径错

**位置**: pr-merge-guarded 第 459 行

```bash
local issues_dir="$PWD/docs/B1-docs"    # develop！
local issue_file="$issues_dir/$local_id/issue.md"
[[ -f "$issue_file" ]] || continue      # merge 前 develop 上没文件 → 跳过
```

**根因**: `$PWD` 是 develop（pr-merge-guarded 在 develop 执行）。merge 前 issue.md 只在 fix worktree 上存在（B1 阶段在 worktree 创建），develop 上还没有。`[[ -f ]]` 失败 → `continue` 跳过 → 所有后续 issue-sync 操作都不执行。

**影响**: issue-sync close 静默失败。platform issue 虽然关了（issue-sync 内部通过 API 关），但 `platform_state: closed` 没写入本地 issue.md。wt-close 再写一次 → diff → 阻塞。

**关键**: 第 480 行 `--project "$_wt_path"` 是**写**路径，已经指向 worktree——正确的。但第 459-470 行是**读**路径，错误地指向了 develop。读写路径不一致。

### Bug 2: worktree 解析脆弱

**位置**: pr-merge-guarded 第 456 行

```bash
_wt_path=$(git worktree list --porcelain | \
  awk -v br="$_src_branch" \
  '$1=="worktree"{wt=$2} $1=="branch" && index($2,br){print wt}' | head -1)
```

**问题**:
1. `index($2, br)` 是子串匹配，不是精确匹配
2. `head -1` 取第一个——`git worktree list --porcelain` 的输出顺序不可靠
3. 没有用 raw_key 定位

**对比**（正确做法）: `worktree-common.sh` 的 `freely_wt_assert_dev_test_consistent` 用 raw_key 精确匹配分支名 `*fix/raw-*$_raw_key*`。

### Bug 3: wt-close 冗余 issue-sync close

**位置**: wt-close 第 733 行

正常流程下 `pr-merge-guarded` 的 `_sync_issues_changed_in_merge` 已完成：
- 关平台 issue
- 写 `platform_state: closed` 到 worktree
- commit + push

wt-close 再跑一次 `issue-sync close`：
- 平台 issue 已关 → API 调用是 no-op
- worktree issue.md 已有 `platform_state: closed` → 无 diff（修好 Bug 1 后）
- 如果 pr-merge 没正确执行（Bug 1），这次写入会产生 diff → 阻塞

**结论**: 修好 Bug 1 后，wt-close 的正常路径 issue-sync close 完全冗余。

### Bug 4: wt-close 遇 diff 引导 force 丢弃

**位置**: wt-close 第 972-1001 行

当前行为：检测到未提交文件 → 两条路：① force 丢弃 ② stash + 正规化。但两条路平级显示，用户容易选 force（看起来更简单）。

**问题**: 当 diff 是 issue-sync 写入的 `+platform_state: closed` 时，这些修改是有价值的状态记录。应该：
1. 识别 diff 是否来自 issue-sync（只有 `platform_state: closed` 变更）
2. 如果是 → 明确指出这是流程问题，引导 stash → wt-close → 正规化
3. 不提供 force 丢弃选项（或至少降级提示）

### Bug 5: wt-close updated_at 时间戳

**位置**: wt-close 第 752 行

```bash
_fm_set_str "$_wt_i_file" "updated_at" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
```

跟 PR #3817 修复的 issue-sync close 同款 bug。每次写入 `updated_at` 都不同 → 即使其他字段无变化也产生 git diff。

### Bug 6（新发现）: 吸收的 I-* issue 写入路径

**位置**: wt-close 第 743-751 行

```bash
_wt_i_file="$PROJECT_ROOT/docs/B1-docs/$_wt_i_absorbed_i/issue.md"
...
_fm_set_str "$_wt_i_file" "platform_state" "closed"
```

`$PROJECT_ROOT` 是 primary worktree（develop 保护分支）。直接写 develop 上的文件 → 修改保护分支。

**修复**: 应该写 worktree 的副本（`$wt_path/docs/B1-docs/...`），或者通过 pr-merge-guarded 的 sync 机制处理。

## Decision

一个 raw issue，改 2 个文件，6 处：

### pr-merge-guarded

| # | 改什么 | 怎么改 |
|---|--------|--------|
| 1 | 第 459 行读路径 | `$PWD/docs/B1-docs` → `$_wt_path/docs/B1-docs`；fallback `$PWD/docs/B1-docs` |
| 2 | 第 456 行 worktree 解析 | awk 分支名匹配 → 同 `worktree-common.sh` 的 raw_key 精确匹配 |

### wt-close

| # | 改什么 | 怎么改 |
|---|--------|--------|
| 3 | 第 733 行冗余 close | 读 worktree issue.md 的 `platform_state`；已 closed → 跳过 |
| 4 | 第 733 行缺失时处理 | 不写文件，提示 stash → wt-close → 新工位正规化 |
| 5 | 第 752 行 updated_at | 删除 |
| 6 | 第 743 行吸收 I-* 路径 | `$PROJECT_ROOT` → `$wt_path`（或其他可写路径） |

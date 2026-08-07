# Cleanup Verification — .codex/config.toml untrack

- raw_key: raw-20260807T105604Z
- issue: I-20260807T105604Z-A
- lane: premerge-integration (test-pre-merge-20260807T105604Z-codex-config-untrack)
- date: 2026-08-07

## RED（修复前，develop）

`.codex/` 已在 `.gitignore:78`，但 `.codex/config.toml` 仍被跟踪；本地个人字段修改使其成为 tracked modification：

```
$ git -C /Users/zhaoyu/Downloads/code/my-freely/freely status --short
 M .codex/config.toml
$ git -C /Users/zhaoyu/Downloads/code/my-freely/freely ls-files .codex
.codex/config.toml
```

这导致 develop working tree dirty（`project_dirty_entries > 0`），daemon start / guarded merge 被 clean-tree 检查拒绝。

## 修复

`git rm --cached .codex/config.toml`（解除跟踪，本地文件保留），提交 `3bd296858`。

## GREEN（修复后，test-pre-merge 工位）

在 test-pre-merge-20260807T105604Z-codex-config-untrack 放置本地 `.codex/config.toml`（个人字段内容）后：

```
$ git ls-files .codex
（空）
$ git check-ignore -v .codex/config.toml
.gitignore:78:.codex/	.codex/config.toml
$ git status --porcelain
（空）
$ git status --porcelain | wc -l
0
$ git status --ignored --short | rg '\.codex'
!! .codex/
```

结论：`.codex/config.toml` 不再被跟踪，本地修改不会污染工作树；cleanup 目标达成。

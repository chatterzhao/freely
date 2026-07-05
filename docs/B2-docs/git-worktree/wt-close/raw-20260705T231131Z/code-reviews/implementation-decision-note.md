- issue_id: I-20260705T231131Z-A
# Implementation Decision Note: 全项目旧路径引用清理

## Implementation Summary

修复 33 个文件中的旧路径引用，使所有执行脚本正确读写新目录结构。

## Key Decisions

1. **B1-docs raw-*: sed 替换** — `docs/issues/raw-{key}` → `docs/B1-docs/raw-{key}` 是纯目录改名，sed 安全
2. **B2-docs I-*: find 搜索** — I-* 文件从 `docs/issues/I-{key}/issue.md`（目录+文件）改为 `docs/B2-docs/.../I-{key}.md`（扁平文件），使用 `find -path "*/raw-{key}*/issues/I-{key}*.md"` 通过 raw_key 反向查找
3. **governance-closeout-gate: 双路径分派** — `_issue_file()` 根据 issue_id 前缀（raw-/I-）分派到 B1-docs 或 B2-docs
4. **epics-map.svg 文件名不变** — sed 误将 `docs/epics-map.svg` 改为 `docs/B2-docs-map.svg`，已修正。SVG 文件名从未改名

## Verification

- 所有修改文件 `bash -n` 通过
- `grep 'docs/issues\|docs/epics'` 核心脚本归零
- 端到端路径验证：B1-docs 633 个 raw issue、B2-docs 94 个 I-* 文件全部可达
- wt-create --source platform 功能正常

## Owner Issue
- I-20260705T231131Z-A: docs/B2-docs/git-worktree/wt-close/raw-20260705T231131Z/issues/I-20260705T231131Z-A.md
- C-20260705T231131Z-A: docs/B1-docs/raw-20260705T231131Z/candidates.md

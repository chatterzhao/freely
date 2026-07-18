# PRD: commands.md wt-close --force 文案同步
- issue_id: I-20260717T235950Z-A

## Goal
commands.md §wt-close 选项表 --force 行与 usage() 真源语义一致（autonomous gate 语义）。

## 实现方案
L193 旧文案 → "永久丢弃（不可恢复）。绕过自治门禁的拒绝判定(unfinished/foreign block)；正常自治关闭不需要此标志——gate 自动判定放行。有未合并提交时需同时 `--discard-unmerged`"。

## Dev-Loop Handoff
RED: grep "自治门禁" commands.md §--force 行 → 无匹配。GREEN: 匹配且与 --help 判据一致（同 at005 关键词）。

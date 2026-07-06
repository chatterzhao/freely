# Tasks: 全项目旧路径引用清理

## Task 1: 批量 sed — docs/epics → docs/B2-docs
- 文件: check-epics-map, freely-review, freely-watchdog, pr-review-guarded, pr-merge-guarded, pr-create-guarded, checkpoint-guard, governance-merge-gate, freely CLI
- 方法: `sed -i '' 's|docs/epics|docs/B2-docs|g'`
- 验收: grep 确认 docs/epics 归零 (排除 epics-map.svg)

## Task 2: 批量 sed — docs/issues → docs/B1-docs (纯 raw-* 文件)
- 文件: raw-issue-pull, issue-sync-bootstrap, issue-migrate-intake, wt-create, .gitignore, freely-review, pr-merge-guarded, pr-create-guarded, wt-close
- 方法: `sed -i '' 's|docs/issues|docs/B1-docs|g'`
- 注意: wt-close L688/L738 后续手动修复（I-* 引用）

## Task 3: 手动修复 — I-* 引用改用 B2-docs find
- bin/issue-sync L661: I-* 文件查找
- bin/pr-review-guarded L604: I-* find
- bin/issue-index: ISSUES_DIR + B2-docs 扫描
- governance-closeout-gate L19: raw/I-* 双路径分派
- interruption-manager-handler L100: raw/I-* 分支处理
- wt-close L688/L738: absorbed I-* 查找

## Task 4: 扩展清理
- docs/progress/ → docs/B2-docs/
- .freely/intake/ → docs/B1-docs/
- milestones.md 历史标题

## Task 5: Bug 修复
- epics-map.svg 文件名误改还原
- pr-review-guarded code-reviews fallback 路径修正

## Task 6: 验证
- bash -n 语法检查全部通过
- 端到端路径可达性验证
- git diff 审查

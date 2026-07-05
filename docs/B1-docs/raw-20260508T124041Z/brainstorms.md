# Brainstorm: wt-create pull 必须等 fix/feature 工位创建后执行
- 来源: raw-20260508T124041Z (#258)
- 日期: 2026-05-08
## Discovery
wt-create 在 `_require_issue_exists` 中调 `_pull_raw_issue`，此时工位未创建。`raw-issue-pull` 要求分支名含 raw-key，在 develop 上被拦截。
## Research  
`raw-issue-pull` 第 43-48 行拒绝 develop/main。设计意图是所有 pull 在工位内执行。
## Decision
pull 移到 fix/feature 工位创建后，cd 入工位执行。

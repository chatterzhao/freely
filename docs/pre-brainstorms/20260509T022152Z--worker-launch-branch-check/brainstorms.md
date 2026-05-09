# Brainstorm: Worker Launch 验证 fix/feature 分支
- 来源: raw-20260509T022152Z (#264)
- 日期: 2026-05-09
## Discovery
Worker 被 launch 到 develop/test-pre-merge，无法 commit，快速退出触发 storm。
## Decision
在 worker_prompt_launchable_for_manager_project 中校验 target branch 必须是 fix/* 或 feature/*。
## 修复
一行检查: `case "$target_branch" in fix/*|feature/*) ;; *) return 1 ;; esac`

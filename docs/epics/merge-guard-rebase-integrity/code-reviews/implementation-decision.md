# Implementation Decision Note: Merge Guard + Rebase Integrity

- issue_id: I-20260617T055840Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: 采用 GitHub branch protection (required status check) + git post-rewrite/pre-rebase hooks + pr-merge-guarded gate 三层防护
- why_this: Branch protection 是 GitHub 原生能力，git hooks 是行业标准（Apache Mesos 等项目证实），pr-merge-guarded gate 是最后防线。总改动 ~250 行，零新依赖。
- alternatives_considered: (A) safe-rebase wrapper script — 否决：需主动使用、冲突时绕过；(B) affected-files gate — 否决：issue 规范与实现存在漂移、误报率高；(C) 保留 --admin flag — 否决：不解决根本问题
- boundary_non_goals: 不覆盖 git commit --amend（太 noisy）、不覆盖手动 git merge（已有 pre-merge-commit hook）、不覆盖 force push（已有 pre-push hook）、不强制 branch protection（可选一次性配置）
- residual_risk: (1) Hook 禁用：git -c core.hooksPath=/dev/null 可跳过，pr-merge-guarded gate 为二次防线；(2) 快照 7 天过期：长时间挂起的 rebase 可能丢失快照；(3) GitHub API 失败：_set_governance_check_pass 静默 fallback，未配置 branch protection 时不影响功能

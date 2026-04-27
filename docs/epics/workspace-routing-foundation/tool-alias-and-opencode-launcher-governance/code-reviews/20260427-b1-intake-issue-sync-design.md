# B1 intake→issue sync design - premerge verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Unify chat/intake into issue-centric model. Every chat creates raw issue or comment. Platform isolation: AI never reads/writes platform directly. Sync via scan/push scripts.`
- why_this: `Two separate input paths (.freely/intake/ and task-source-scan) required different storage and processing. Unified model eliminates inbox, traces every chat to an issue, enables multi-platform sync.`
- alternatives_considered: `1) Keep intake and issue separate: rejected because dual paths create inconsistency. 2) Only fix chat routing: rejected because storage fragmentation remains. 3) Full refactoring with docs/issues/: chosen because it solves both routing and storage.`
- boundary_non_goals: `No freely chat runtime refactoring (deferred to B2). No platform adapter implementation (skeleton only). No comment sync (phase 2).`
- residual_risk: `gitee-issue.py had wrong API path (fixed). 161 milestone issues synced to both GitHub and Gitee. docs/issues/ entries committed with dual platform_ids.`

## Verification
- 161/161 issues synced to GitHub (chatterzhao/freely #2-#162) and Gitee (zhaoquan/freely)
- gitee-issue.py API path fix: /repos/{owner}/issues with repo in body
- platform-adapter.py: unified interface for GitHub+Gitee
- docs/issues/ storage: frontmatter + platform_ids per-platform
- 26 brainstorms + 7 decisions + 30 tasks documented

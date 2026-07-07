---
b1_id: B1-20260707T064609Z
phase_state: completed
source_raw: raw-20260707T064609Z
produced_candidate: C-20260707T064609Z-A
---
# B1: commands.md 与源码对齐
## Discovery: 10 个命令的文档差距
| 命令 | 遗漏 |
|------|------|
| feedback | edit 子命令、--severity |
| wt-create | --base、--skill、legacy |
| pr-create-guarded | --title、--body、--base |
| pr-review-guarded | --reviewer、--slot、--verdict、--reason |
| pr-merge-guarded | complete、--dry-run |
| wt-close | --force、--discard-unmerged、--platform-only、--skip-platform、--dry-run、--reason |
| develop-push | status、defer、clear |
| issue-sync | 整条命令 |
| deploy-skills | 整条命令 |
## Decision: 以源码 help/usage 为准，逐条对齐
## Candidate: C-20260707T064609Z-A, promoted

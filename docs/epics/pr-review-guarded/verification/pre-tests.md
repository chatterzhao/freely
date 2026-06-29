# Pre-Tests: pr-review-guarded

## Acceptance Items

### AI-1: pr-review-guarded 命令可用
- **Given**: feature worktree with PR created
- **When**: freely pr-review-guarded <branch>
- **Then**: 6 review dimensions checked, review document written, verdict output
- **adequacy**: verified

### AI-2: pr-merge-guarded 检查 verdict
- **Given**: review document with verdict=pass
- **When**: freely pr-merge-guarded develop <branch>
- **Then**: merge proceeds
- **adequacy**: verified

### AI-3: pr-merge-guarded 阻塞 fail verdict
- **Given**: review document with verdict=fail
- **When**: freely pr-merge-guarded develop <branch>
- **Then**: blocked with "PR review not passed"
- **adequacy**: verified

### AI-4: 流程链路一致性
- **Given**: 所有 18 个文件更新
- **When**: grep "pr-create → pr-review → pr-merge" across project
- **Then**: no stale "pr-create → pr-merge" references remain
- **adequacy**: verified

### AI-5: deploy-skills 后新流程生效
- **Given**: skill 文件更新
- **When**: freely deploy-skills
- **Then**: AI 看到新流程 pr-create → pr-review → pr-merge
- **adequacy**: verified

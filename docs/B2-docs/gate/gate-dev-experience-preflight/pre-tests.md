# Pre-tests — gate dev experience

- issue_id: `I-20260429-2000-A`
- issue_path: `docs/epics/workspace-routing-foundation/gate-dev-experience-preflight/issues/I-20260429-2000-A.md`

## 验收项

1. `./bin/governance-merge-gate --range develop..feature/gate-dev-experience-improvements-20260429` 返回正确结果
2. `freely pr-merge-guarded test-pre-merge-xxx feature/gate-dev-experience-improvements-20260429` 先跑预检
3. `git commit` milestones.md 不触发 sk- 误报

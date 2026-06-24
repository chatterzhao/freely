---
issue_id: raw-20260624T141559Z
phase_state: done_b2_ibm
---

- issue_id: raw-20260624T141559Z
- issue_path: docs/issues/raw-20260624T141559Z/issue.md

## Implementation Decision Note

- decision: `cmd_feedback` 改为 `issue-sync create` 的薄封装，去掉 `--repo` 参数，repo 由 `issue-sync` 从 git remote 自动检测
- why_this: `issue-sync` 是项目中唯一的平台接触面，所有其他命令（wt-close、pr-create 等）都通过它操作多平台。`cmd_feedback` 是唯一的例外——硬编码 `gh issue create`。对齐架构后，加新平台只需在 `issue-sync` adapter 层新增，feedback 零改动
- alternatives_considered:
  - Option A: 在 cmd_feedback 内加 GitHub/Gitee 分支 — 重复实现，违反 DRY，加平台改两处
  - Option B: 改为 issue-sync 薄封装 — 采用，架构对齐
  - Option C: 移除 cmd_feedback — 不必要，保留作为便捷入口
- boundary_non_goals:
  - 不改 issue-sync API
  - 不添加新平台 adapter
  - 不改 wt-create/wt-close/pr-create 等其他命令
- residual_risk: 低。issue-sync 不可用时 feedback 返回错误，本地 issue.md 已保存可手动处理

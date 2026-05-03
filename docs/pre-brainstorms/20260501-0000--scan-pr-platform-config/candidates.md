
### C-20260501-0000-A

- title: `PR scan surface + FREELY_REPO_PLATFORMS config`
- status: `promoted`
- scope: 为 task-source-scan 增加 open_pull_requests 扫描面，并引入 FREELY_REPO_PLATFORMS 配置控制启用平台
- priority: `P0`
- type: `feature`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `discovery`
- phase_state: `done_pre_brainstorm`
- promoted_to: `I-20260501-0000-A`
- promoted_issue_path: `docs/issues/I-20260501-0000-A/issue.md`
- session_refs:
  - {tool: ccds, session_id: "20260501-scan-pr-platform", jsonl_path: "unavailable://manual", role: "author"}
- acceptance_criteria:
  - task-source-scan 在配置 FREELY_REPO_PLATFORMS 后输出 open_pull_requests 扫描面
  - 空配置时无 PR surface（向后兼容）
  - 多平台支持（github + gitee）
- promotion_gate: `governance-merge-gate`
- open_questions:
  - 是否需要在 PR scan 中支持更多平台（gitlab, bitbucket）
- acceptance_reviews:
  - reviewer: `human`
  - status: `pending`
- next_action: `Hotfix merge to develop.`

# Candidates

## C-20260616T111514Z-A: legacy issue

- candidate_format_version: v2
- title: write_config bash heredoc 替换为 Python freely_config.py init-toml，补齐 10 个 posture 字段
- status: promoted
- decision_reason: 单文件改动，消除双序列化路径，补齐缺失字段
- next_action: pr-merge-guarded → wt-close
- acceptance_criteria:
  - write_config() 调用 Python init-toml，不再使用 cat heredoc
  - 所有 10 个 posture/consent 字段已包含
- promotion_gate: governance-gate 通过
- promoted_issue_path: docs/issues/I-20260616T111514Z-A/issue.md
- milestone: M-20260616T111514Z-A

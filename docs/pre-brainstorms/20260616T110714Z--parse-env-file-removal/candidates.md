# Candidates: parse_env_file removal

## C-20260616T110714Z-parse-env-removal

- raw_issue: raw-20260616T110714Z
- status: `promoted`
- promoted_issue_id: I-20260616T110714Z-parse-env-removal
- promoted_issue_path: docs/issues/I-20260616T110714Z-parse-env-removal/issue.md
- decision_reason: parse_env_file 被有意删除（而非恢复）。彻底 TOML-only 方案不需要 config.env 迁移代码。自带完整 IBM 链。
- acceptance_criteria:
  - parse_env_file 不恢复（删除调用方和 --from-env flag）
  - 所有 config.env 迁移/回退代码移除
  - freely init 只释放 config.toml.example
  - load_config: config.toml 缺失→阻塞提示

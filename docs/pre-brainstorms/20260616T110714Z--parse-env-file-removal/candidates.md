# Candidates: parse_env_file removal

## C-20260616T110714Z-parse-env-removal

- raw_issue: raw-20260616T110714Z
- status: `absorbed`
- absorbed_by: I-20260616T044030Z-A (config.toml clean break — 彻底 TOML-only)
- absorb_reason: parse_env_file 删除是 config-toml-complete clean-break 的子任务。不恢复该函数，而是彻底移除所有 config.env 迁移代码。
- acceptance_criteria:
  - parse_env_file 不恢复（删除调用方和 --from-env flag）
  - 所有 config.env 迁移/回退代码移除
  - freely init 只释放 config.toml.example
  - load_config: config.toml 缺失→阻塞提示

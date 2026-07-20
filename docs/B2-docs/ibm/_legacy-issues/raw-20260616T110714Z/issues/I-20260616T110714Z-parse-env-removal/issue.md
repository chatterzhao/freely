---
local_id: I-20260616T110714Z-parse-env-removal
kind: linked
phase_state: completed
promoted_from: raw-20260616T110714Z
source_candidate: docs/B1-docs/raw-20260616T110714Z/candidates.md
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260616T110714Z/issues/I-20260616T110714Z-parse-env-removal/issue.md
verification_artifact_dir: docs/B2-docs/config-toml-complete/code-reviews
primary_platform: github
platform_ids:
  github:
    issue_id: '2869'
    url: https://github.com/chatterzhao/freely/issues/2869
    synced_at: '2026-06-17T00:25:04Z'
updated_at: '2026-06-17T16:38:34Z'
created_at: '2026-06-17T00:25:04Z'
platform_state: closed
---

# Issue: config.toml clean break — parse_env_file removal + quality fixes

## Summary
parse_env_file 缺失是 config.toml clean break 的实现子任务。不恢复该函数，而是彻底删除所有 config.env 迁移代码，同时修复 freely_config.py 中的多个质量缺陷。

## Changes
- freely_config.py: 删除 parse_env_file/--from-env，修复 dict_to_toml/_shell_quote/cmd_print
- freely: load_config 阻塞提示，init 只释放 example
- network-proxy-resolver.sh: TOML-only
- config.toml.example: 56字段中文注释
- docs: config.env→config.toml

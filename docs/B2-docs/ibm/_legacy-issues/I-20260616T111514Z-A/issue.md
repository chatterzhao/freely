---
local_id: I-20260616T111514Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260616T111514Z
source_candidate: docs/pre-brainstorms/20260616T111514Z--config-write-python/candidates.md
canonical_issue_path: ''
created_at: 2026-06-17 00:00:00+00:00
updated_at: 2026-06-17 00:00:00+00:00
author: zhaoquan
channel: freely-fix-execution
pre_tests_path: ''
verification_artifact_dir: docs/pre-brainstorms/20260616T111514Z--config-write-python/code-reviews
platform_state: closed
---

# I-20260616T111514Z-A: write_config heredoc → Python

## 实现
替换 write_config() 中的 cat <<EOF heredoc 为 python3 freely_config.py init-toml --value ... 调用。

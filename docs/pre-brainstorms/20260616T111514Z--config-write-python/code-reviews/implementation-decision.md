# Implementation Decision Note: write_config heredoc → Python

- issue_id: I-20260616T111514Z-A
- decision: 替换 bash heredoc 为 Python init-toml
- why_this: 消除双序列化路径，统一通过 _toml_quote 转义
- alternatives: 保留 heredoc 但补齐字段 → 拒绝（仍有转义风险）

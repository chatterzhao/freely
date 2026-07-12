# Tasks: config.toml skip_ibm 配置
- issue_id: I-20260712T105347Z-A
- [x] templates/config.toml.example: [skip_ibm_gate] section
- [x] governance-merge-gate: _load_skip_ibm_allowed_paths()
- [x] governance-merge-gate: templates/ governance-only path
- [x] Syntax verification
- [x] PR → merge

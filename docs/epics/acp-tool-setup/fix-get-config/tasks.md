# Tasks: fix get_config/set_config regression
- issue_id: I-20260630T135725Z-A
## Task 1: Fix _init_acp_tool_setup
- Replace get_config → grep config.toml
- Replace set_config → upsert_config_key
## Task 2: Fix _ensure_acp_bridge_running
- Replace get_config → ${!_config_key:-}

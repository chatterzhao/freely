---
candidate_id: C-20260715T082216Z-A
status: promoted
source_raw: raw-20260715T082216Z
milestone: M-20260715T082216Z-A
---

## C-20260715T082216Z-A: registry-driven slot env injection in bridge startup

- candidate_format_version: v2
- title: add _load_slot_env_vars to tool-launchers.sh, use in _bridge_ensure_running
- status: promoted
- decision_reason: tool-launchers.sh 已有 _tool_registry_get，新增 _load_slot_env_vars 通过 registry 直接读 slot config 注入凭证 env vars，支持所有注册 tool（JSON/TOML）
- next_action: B2→dev 实现
- acceptance_criteria:
  - _bridge_ensure_running 启动 bridge 时传入 slot 凭证
  - Claude 类型: settings.json → env section → ANTHROPIC_* vars
  - OpenCode 类型: settings.json → env section
  - Cline 类型: data/settings/providers.json → credential fields
  - Codex 类型: 通过 CODEX_HOME env var（现有 bridge_config_env 机制）
  - daemon 启动后 AI cycle 不再 tool_unproductive
- promotion_gate: bash -n + 所有 tool slot 的 env 加载测试 + daemon 启动验证
- promoted_issue_id: I-20260715T082216Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260715T082216Z/issues/I-20260715T082216Z-A.md
- milestone: M-20260715T082216Z-A

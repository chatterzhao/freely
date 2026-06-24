---
local_id: I-20260624T013737Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T013737Z
source_candidate: docs/pre-brainstorms/20260624T013737Z--tool-registry-toml/candidates.md#C-20260624T013737Z-A
canonical_issue_path: docs/issues/I-20260624T013737Z-A/issue.md
milestone: "M-20260624T013737Z-A"
title: "feat: tool-registry.json5 → TOML 配置驱动注册表（Phase 1+2）"
platform_ids:
  github:
    issue_id: '3399'
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-24T01:37:56Z
updated_at: 2026-06-24T06:00:00Z
intake_id: ""
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/epics/tool-registry-toml/verification/pre-tests.md
verification_artifact_dir: docs/epics/tool-registry-toml/code-reviews
---

# I-20260624T013737Z-A: tool-registry TOML 配置驱动注册表（Phase 1+2）

- source_candidate: `docs/pre-brainstorms/20260624T013737Z--tool-registry-toml/candidates.md#C-20260624T013737Z-A`
- pre_tests_path: `docs/epics/tool-registry-toml/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/tool-registry-toml/code-reviews`
- milestone: M-20260624T013737Z-A

## 实现

### Phase 1: TOML 格式迁移 + 文件优先级
1. 创建 `tool-registry.toml` — 系统内置注册表（完整 schema）
2. 更新 `tool-registry-query.py` — 支持 TOML + 双文件合并

### Phase 2: config_schema 字段抽象
3. 添加通用 `_tool_config_field` 函数
4. 重构 `monitor-ai-acp.sh` — 用 config_schema.fields 消除权限字段硬编码
5. 重构 `tool-launchers.sh` `_apply_tool_alias_settings` — 同上
6. 重构 `freely` `_bridge_env_for_registered_tool` — 同上（已是半抽象，补充完整性）

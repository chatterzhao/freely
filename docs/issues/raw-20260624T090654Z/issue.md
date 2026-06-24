---
local_id: raw-20260624T090654Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3419'
    url: https://github.com/chatterzhao/freely/issues/3419
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T09:07:12Z'
updated_at: '2026-06-24T09:07:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标
ai-cli 命令的 case 分支通用化，支持通过 registry 发现的新工具。

## P1（必须）
cmd_login/cmd_switch/cmd_save 中 *) 分支 fallback 到 generic 路径。

## P2（改进）
_login_apikey_alias() config 模板生成从 registry 驱动。

## P3（增强）
_require_acp_binary 从 registry 读取 acp.binary。

## 不重构
codex 的多槽位/auth bundle/provider 特化逻辑。

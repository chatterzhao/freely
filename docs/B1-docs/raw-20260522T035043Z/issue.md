---
local_id: raw-20260522T035043Z43Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2107'
    url: https://github.com/chatterzhao/freely/issues/2107
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-22T03:50:56Z'
updated_at: '2026-06-17T00:22:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

codex apikey 需要：
1. _login_apikey_alias 加 codex case：生成 auth.json + config.toml，alias='cd slot && codex'
2. cmd_login codex apikey 改走 _login_apikey_alias
3. cmd_switch codex apikey slot 时更新 config.env AI_TOOL

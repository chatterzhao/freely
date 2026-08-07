---
local_id: raw-20260522T044515Z15Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2110'
    url: https://github.com/chatterzhao/freely/issues/2110
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-22T04:45:30Z'
updated_at: '2026-06-17T00:22:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 现状
codex_probe_current_slot_now 只支持 codex exec。apikey slot 无法探测。

## 改造
统一 slot_probe(tool, slot_dir): 用各工具免交互模式发 'hi' 探测

| 工具 | 探测命令 |
|------|---------|
| claude | claude -p 'hi' --settings slot/settings.json |
| opencode | OPENCODE_CONFIG=slot/settings.json opencode run 'hi' |
| codex | cd slot && codex exec 'hi' --skip-git-repo-check |

'alias' 方式也可直接调 alias名 -p 'hi'。

## 涉及
- availability-watchdog.sh: codex_probe_current_slot_now → 通用 slot_probe
- probe_all_codex_slots → probe_all_slots
- ai-cli: cmd_switch 后可用 slot_probe 验证

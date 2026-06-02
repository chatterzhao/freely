---
local_id: raw-20260601T041937Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2392'
    url: https://github.com/chatterzhao/freely/issues/2392
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-01T04:19:52Z'
updated_at: '2026-06-01T04:19:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 修复
1. build_prompt delta 模式: cat <<'PROMPT_DELTA' → cat <<PROMPT_DELTA，让 ${LAST_WORKCELL_EXIT_REASON} 正确展开
2. 新增 [BUILD] scan+prompt_time=Xs 到 cycle log，分离 scan 耗时和 AI 响应耗时

## 根因
'PROMPT_DELTA' 单引号阻止了变量展开，AI 收到字面字符串而非实际 exit_reason

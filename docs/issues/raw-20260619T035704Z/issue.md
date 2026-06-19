---
local_id: raw-20260619T035704Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T035704Z-A
source_candidate: C-20260619T035704Z-A
platform_ids:
  github:
    issue_id: '3022'
    url: https://github.com/chatterzhao/freely/issues/3022
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T03:56:44Z'
updated_at: '2026-06-19T04:00:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`governance-merge-gate` 的 `parse_candidate_file` 正则 `^##{1,3}\s+(C-[A-Za-z0-9-]+)` 不匹配单 `#` heading。当 `candidates.md` 用 `# C-xxx` 时返回空列表，gate 报 `"no valid source_candidate"`，但不提示 heading 格式是根因。

PR #3021 的 doc-only SVG 变更因此失败 10+ 次。

## 建议

1. regex 改为 `^#{1,3}` 接受单 # heading
2. 报错信息在发现文件存在但无匹配记录时给诊断提示
3. skill/模板补充 heading 格式要求

Raw issue: `docs/issues/raw-20260619T035604Z/issue.md`


---
schema_version: '1'
local_id: raw-20260807T071225Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260807T071225Z-A'
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4095'
    url: https://github.com/chatterzhao/freely/issues/4095
    synced_at: ''
  gitee:
    issue_id: IK75A4
    url: https://gitee.com/zhaoquan/freely/issues/IK75A4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T07:12:25Z'
updated_at: '2026-08-07T07:12:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

# fix: scan parse_frontmatter 无法解析嵌套 platform_ids 导致 strict raw 误报 invalid

## 现象
7 个 strict raw（schema_version 1）被 scan 误报 2a_invalid_raw_metadata（detail: raw metadata fields are missing, extra, or reordered），但 raw_metadata_contract.validate 直接调用通过。

## 根因
task-lifecycle-scan.py 的 parse_frontmatter（L350-374）用简单行解析：嵌套 YAML（platform_ids 下的 github:/issue_id:/url: 行）被当作顶层字段 → 字段集合与 RAW_METADATA_FIELDS 不符 → validate 报 reordered/extra。flow 单行格式则被解析为字符串（platform_ids must be a mapping）。

## 修复方案
parse_frontmatter 优先 yaml.safe_load（严格 YAML frontmatter，正确处理嵌套），失败时回退行解析 + bullet 补充（兼容 I-* 混合格式）。

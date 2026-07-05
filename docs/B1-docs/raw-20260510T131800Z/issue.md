---
local_id: raw-20260510T131800Z00Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260510T131800Z-A
platform_ids:
  github:
    issue_id: '288'
    url: https://github.com/chatterzhao/freely/issues/288
primary_platform: github
platform_state: closed
updated_at: '2026-06-17T00:21:45Z'
---
## 问题
handoff.py insert 不支持 exit_kind，AI prompt 没告诉 AI 写 exit_kind。
## 修复
insert 加 exit_kind 参数 + CLI + AI prompt 示例。

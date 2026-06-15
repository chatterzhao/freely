---
local_id: raw-20260510T1326Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260510T1326Z-A
platform_ids:
  github:
    issue_id: '289'
    url: https://github.com/chatterzhao/freely/issues/289
primary_platform: github
platform_state: closed
---
## 问题
init 不检查分支名，导致不合规分支进入，AI 后续无法处理。
## 修复
init 时扫描所有分支，不合规直接拒绝，列出支持格式。

---
schema_version: '1'
local_id: raw-20261104T082603Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4184'
    url: https://github.com/chatterzhao/freely/issues/4184
    synced_at: ''
  gitee:
    issue_id: IKSWRF
    url: https://gitee.com/zhaoquan/freely/issues/IKSWRF
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:26:03Z'
updated_at: '2026-11-04T08:26:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# fix: issue-sync close 在非终态时先关平台再报错，产生部分成功

workflow_kind: fix

## 根因
`issue-sync close` 先执行平台关闭，再检查本地 raw 是否处于终态；本地为 `proposed` 时平台已关闭、命令却以非零退出，调用方无法判断真实结果。

## 证据
- 实测 `issue-sync close raw-20261104T074512Z`：输出 `github: closed`、`gitee: closed`，随后 `[raw-lifecycle] platform close requires terminal raw phase` 并 `[ERROR] ... close failed`。
- 平台侧 `gh issue view` 确认为 `CLOSED`，说明关闭已生效。

## 影响
- 部分成功 + 非零退出：调用方重试会得到"已关闭"，或误判为失败并人工干预。
- 与"写通道必须自证已同步"的契约冲突。

## 修复方案
1. 先校验本地 phase，再执行平台写；非终态直接失败且不动平台。
2. 或允许关闭但把退出码改为 3（部分成功）并输出结构化结果。
3. 所有平台写命令统一「校验 → 执行 → 回写 → 退出码」四段。

## 验收标准
- RED：对 `proposed` 的 raw 执行 close，断言平台状态未变且退出非零；当前平台已关闭。
- GREEN：终态 raw 执行 close，平台关闭且 `platform_state=closed` 一致。
- GREEN：部分成功场景退出码 3 并输出每平台 status。

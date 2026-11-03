---
schema_version: '1'
local_id: raw-20260725T072209Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4075'
    url: https://github.com/chatterzhao/freely/issues/4075
    synced_at: ''
  gitee:
    issue_id: IK3YJ0
    url: https://gitee.com/zhaoquan/freely/issues/IK3YJ0
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-25T07:22:09Z'
updated_at: '2026-07-25T07:22:32Z'
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

workflow_kind: feature

## 根因
受控命令和 hook 在门禁失败时会安全地阻断原动作，但失败没有稳定转化为可由 runtime/A2A 消费的结构化回流事件。

## 影响
流程可能把‘原动作已拦截’误解为‘当前治理工作应停止’，导致同一 issue 的 doc/dev 修复、证据补齐或人工决策没有明确下一跳。

## 修复方案
保持 hook 和 guarded 命令的同步阻断；在 runtime 结果采集边界构造结构化失败证据，按失败类别回流至 owner loop、Reviewer、Manager 或 recovery；使用失败指纹和重试上限避免重复派发及无界重试；不得把 gate failure 映射为 stop_ai 或绕过门禁。

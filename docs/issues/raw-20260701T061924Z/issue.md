---
local_id: raw-20260701T061924Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3691'
    url: https://github.com/chatterzhao/freely/issues/3691
    synced_at: ''
  gitee:
    issue_id: IJY1WN
    url: https://gitee.com/zhaoquan/freely/issues/IJY1WN
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T06:19:45Z'
updated_at: '2026-07-01T06:19:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
---

\n\n
## 审计结果

| 门禁 | skill引用 | 分组输出 | 修复引导 | 状态 |
|------|:--:|:--:|:--:|------|
| governance-merge-gate | 9 ✅ | ✅ | ✅ | 刚修好 |
| pretests-gate | 0 ❌ | ❌ | ❌ | 需治 |
| pretests-retirement-gate | 5 ⚠️ | ❌ | ⚠️ | 散乱 |
| check-epics-map | 0 ❌ | ❌ | ❌ | 需治 |

## pretests-gate (最需要治)
当前输出: 1 行 "blocked completion due to pre-tests evidence failures" + 逐条错误
缺失:
- 没有分类汇总（Unit/Integration/E2E section 错误、acceptance item 错误、evidence 错误）
- 没有 skill 引用
- 没有 "需要阅读的 Skill" 汇总

## pretests-retirement-gate
有 5 个 skill 引用但散落，需要分组输出

## check-epics-map
只有 FAILED 提示，需要加修复命令 (`./bin/check-epics-map --update` 或类似)

## 修复
3 个门禁统一为和 governance-merge-gate 一样的格式：
── 需要阅读的 Skill ──
── 分类错误 ──
── 修复引导 ──

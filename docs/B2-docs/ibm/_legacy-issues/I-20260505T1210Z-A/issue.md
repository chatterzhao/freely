---
local_id: I-20260505T1210Z-A
issue_title: 修正 scan 常量对齐 IBM Framework §89 + 迁移现有 issue
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
promoted_from: raw-20260505T1210Z
platform_ids:
  github:
    issue_id: '214'
    url: https://github.com/chatterzhao/freely/issues/214
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/issue-state-refactor/issues/I-20260505T1210Z-A.md
created_at: '2026-05-05T12:10:02Z'
updated_at: '2026-05-17T08:02:19Z'
session_refs: []
platform_state: closed
---

## Scope

1. task-lifecycle-scan.py 第15-19行：修正 TERMINAL_RAW / DONE_STATES / ACTIVE_B2
2. 迁移脚本：为所有已有 raw/I-* 补充 platform_state 字段

## 改动

- TERMINAL_RAW: 去掉 completed → {absorbed, dropped}
- DONE_STATES: 去掉 done, done_ibm → {done_b2_ibm, completed}
- ACTIVE_B2: 去掉 in_ibm → {in_b2_ibm, done_b2_ibm, in_dev, blocked_dev}
- 迁移: 非空 platform_ids → 查 GitHub state → 设 platform_state

## 验证

- scan 不再把 phase_state=closed 的 raw 当 non-terminal
- 现有 179 个 completed 的 I-* 不受影响

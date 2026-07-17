---
local_id: raw-20260717T062449Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T062449Z-A
platform_ids:
  github:
    issue_id: '3962'
    url: https://github.com/chatterzhao/freely/issues/3962
    synced_at: ''
  gitee:
    issue_id: IK1OPY
    url: https://gitee.com/zhaoquan/freely/issues/IK1OPY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T06:25:21Z'
updated_at: '2026-07-17T06:25:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 缺口（trace-contract.md §12 已登记，本案落地修复）
1. A-L041(ai_launch_observed) 实测于 cycle 收尾才发出（2026-07-16 晚于 ai_launch_begin 94s），launch_observed 语义漂移
2. A-L042 OUT to= 打印候选集 A-L020|A-L090|... 而非实际下一跳（违反契约 §4 to=actual next）
3. A-L090/A-L092 OUT to=UNSET——cleanup 链未按 desired_state 声明实际下一跳（running→重拉控制面/A-L240,否则 TERM）

## 修复方向
- L041 前移至 monitor 首次确认 AI 进程存活处
- L042 OUT 由 post-cycle 路由决策层打实际 to
- L090/L092 按 desired_state 条件声明 to
- 同步更新 trace-contract §12（修复项移出 known-gaps）

## 依据
docs/system/workspace/three-loop-trace-contract.md §12（raw-20260717T004752Z lane 登记）

---
schema_version: '1'
local_id: raw-20261103T063348Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4135'
    url: https://github.com/chatterzhao/freely/issues/4135
    synced_at: ''
  gitee:
    issue_id: IKSKUZ
    url: https://gitee.com/zhaoquan/freely/issues/IKSKUZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T06:33:48Z'
updated_at: '2026-11-03T06:33:53Z'
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

workflow_kind: fix

## 现象
在 test-pre-merge 工位执行 `freely daemon start` 失败（例如 `AGENT_AI_TOOL not set`、A2A server 启动超时、supervisor 未起来）后，随后执行 `freely daemon stop` 会把 `.freely/run/test-gate.env` 写成 `TEST_STATUS=completed` 且 `LAST_TESTED_COMMIT=<HEAD>`。pretests-retirement-gate 只比对 test-gate 与 HEAD，因此未真正跑过测试的工位也能通过 PR 门禁。

## 根因
`_update_test_gate` 在 start/stop 两个路径都会写 completed，未区分“本次启动是否成功物化 supervisor / 测试是否真实执行”。失败启动后的 stop 仍走完成路径。

## 修复方向
1. start 失败时不写 testing/completed；stop 只有在本轮存在成功 start（或存在真实测试执行标记）时才写 completed。
2. 或在 test-gate.env 增加 `TEST_SESSION_STARTED=1` 字段，stop 仅在为 1 时写 completed。
3. 补单测：start 失败 → stop 后 TEST_STATUS 不得为 completed。

## 发现场景
2026-11-03 执行 chat-help test 工位验证时复现：首次 daemon start 因缺 agent-table 失败，stop 仍写 completed（后续补配置重跑才得到真实证据）。

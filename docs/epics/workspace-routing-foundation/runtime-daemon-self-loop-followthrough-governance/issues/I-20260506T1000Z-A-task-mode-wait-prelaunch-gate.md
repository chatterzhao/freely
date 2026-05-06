---
local_id: I-20260506T1000Z-A
kind: linked
phase_state: in_verification
source_candidate: docs/pre-brainstorms/20260506T1000Z--task-mode-wait-prelaunch-gate/candidates.md#C-20260506T1000Z-A
platform_ids:
  github: "229"
primary_platform: github
verification_artifact_dir: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews
hash: ""
created_at: 2026-05-06T10:00:00Z
updated_at: 2026-05-06T10:00:00Z
---

# I-20260506T1000Z-A: task_mode=wait supervisor 前置门禁

## Scope

Supervisor 主循环 `select_launch_kind` 前增加 manager 专属 wait 模式检查。wait 时 sleep CHECK_INTERVAL + continue，不 build prompt、不 launch AI。

## Implementation

`docs/system/workspace/scripts/runtime/freely` supervisor 循环 L18202-18212：9 行 bash 前置门禁。

## Verification

- test-pre-merge 启动 daemon (task_mode=wait) → 无 prompt build / AI launch
- task-mode set --task-mode auto → 正常发射

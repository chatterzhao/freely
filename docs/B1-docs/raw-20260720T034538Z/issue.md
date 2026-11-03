---
local_id: raw-20260720T034538Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '4044'
    url: https://github.com/chatterzhao/freely/issues/4044
    synced_at: ''
  gitee:
    issue_id: IK28PZ
    url: https://gitee.com/zhaoquan/freely/issues/IK28PZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T03:46:01Z'
updated_at: '2026-07-20T03:46:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
当 Manager 通过 a2a-exit 委派 B1 预研任务时，Runtime 的 auto-mode 会检测 submitted A2A tasks 并启动 Worker ACP session。但在 worker launch 阶段，verification contract 检查以下必填字段：

- owner_issue
- pre_tests_path
- verification_artifact_dir
- required_test_lanes
- required_acceptance_item_ids
- minimum_evidence_level
- target_environment
- closeout_gate_command
- closeout_target_lane
- closeout_promotion_gate
- closeout_requires_adequacy
- closeout_review_artifact_policy

这些字段全部为空，导致 VERIFICATION_METADATA_PRESENT="false" -> launch verification 失败 -> AI worker 无法启动 -> workcell 标记 LAST_EXIT_REASON="manager_worker_launch_verification_blocked"。

## 影响
- 所有委派的 Worker 在 launch 阶段即被阻塞，无法执行任何任务
- ACP bridge 进程空转，A2A task 卡在 "working" 状态
- B1 预研、merged_develop closeout、platform sync 等所有任务全部停滞
- 当前 4 个 worktree 中有已完成的 B1 修改（phase_state/absorbed_into）和 platform sync 修改，但全部无法提交

## 修复方案
worker_launch verification 需要区分任务类型：
1. B1 预研任务（或阶段无关的任务）：跳过 verification metadata 检查，或设默认值
2. B2/dev/test 任务：需要 owner_issue、pre_tests_path 等，保持现有检查
3. 或者在 a2a-exit 委派时允许传入 --skip-verification 标记

## 证据
workcell-state.env（4 个 worktree 相同模式）:
DESIRED_RUNTIME_STATE="stopped"
LAST_SUPERVISOR_STATE="down"
LAST_AI_STATE="down"
LAST_EXIT_REASON="manager_worker_launch_verification_blocked"

worker-verification-contract.env:
VERIFICATION_METADATA_PRESENT="false"

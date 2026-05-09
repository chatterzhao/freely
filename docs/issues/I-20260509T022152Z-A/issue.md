---
local_id: I-20260509T022152Z-A
kind: linked
status: in_dev
phase_state: in_dev
promoted_from: raw-20260509T022152Z
source_candidate: docs/pre-brainstorms/20260509T022152Z--worker-launch-writable-redirect/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-09T02:22:01Z
updated_at: 2026-05-09T02:22:01Z
intake_id: ""
author: platform
channel: fix-execution
session_refs: []
pre_tests_path: docs/epics/worker-launch-writable-redirect/pre-tests.md
verification_artifact_dir: docs/epics/worker-launch-writable-redirect/code-reviews
---

# I-20260509T022152Z-A: worker launch 验证 target 必须是 fix/feature

- source_candidate: `docs/pre-brainstorms/20260509T022152Z--worker-launch-writable-redirect/candidates.md`
- pre_tests_path: `docs/epics/worker-launch-writable-redirect/pre-tests.md`
- verification_artifact_dir: `docs/epics/worker-launch-writable-redirect/code-reviews`

## 实现

`worker_prompt_launchable_for_manager_project` 增加 branch 前缀检查：
- target branch 为 `develop`/`main`/`test-pre-merge-*` → return 1（拒绝 launch）
- 报错信息含当前 branch 和允许前缀列表
- `fix/*` 和 `feature/*` 正常放行

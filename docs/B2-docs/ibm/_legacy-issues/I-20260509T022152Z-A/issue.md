---
local_id: I-20260509T022152Z-A
kind: linked
phase_state: absorbed
promoted_from: raw-20260509T022152Z52Z
source_candidate: docs/B1-docs/raw-20260509T022152Z52Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '404'
    url: https://github.com/chatterzhao/freely/issues/404
    synced_at: '2026-05-17T04:48:30Z'
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-09 02:22:01+00:00
updated_at: '2026-05-17T04:48:30Z'
intake_id: ''
author: platform
channel: fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/worker-launch-writable-redirect/pre-tests.md
verification_artifact_dir: docs/B2-docs/worker-launch-writable-redirect/code-reviews
platform_state: open
---

# I-20260509T022152Z-A: worker launch 验证 target 必须是 fix/feature

- source_candidate: `docs/B1-docs/raw-20260509T022152Z52Z/candidates.md`
- pre_tests_path: `docs/B2-docs/worker-launch-writable-redirect/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/worker-launch-writable-redirect/code-reviews`

## 实现

`worker_prompt_launchable_for_manager_project` 增加 branch 前缀检查：
- target branch 为 `develop`/`main`/`test-pre-merge-*` → return 1（拒绝 launch）
- 报错信息含当前 branch 和允许前缀列表
- `fix/*` 和 `feature/*` 正常放行

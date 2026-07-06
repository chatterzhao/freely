---
local_id: I-20260324-0415
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260324-0415/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '53'
    url: https://github.com/chatterzhao/freely/issues/53
    synced_at: '2026-04-27T11:17:09Z'
  gitee:
    issue_id: IJFO6L
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6L
    synced_at: '2026-04-27T13:14:55Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md
last_synced_comment_at:
  github: '2026-04-27T11:17:09Z'
hash: ''
created_at: '2026-04-27T11:17:09Z'
updated_at: '2026-04-27T11:17:09Z'
platform_state: closed
---

Freely 已经具备多种观察面：

- `live-status`
- `fleet-status`
- session jsonl
- cycle log
- continuity / prompt / verification artifacts

但还没有统一 contract 去说明：

1. 真实环境测试时应该先看哪些 surface
2. 何种 signal 表示“仍在推进”或“已经空转”
3. 用户、manager、watchdog 应如何共享同一组状态卡片与 deep refs
4. 这套 contract 如何从 Freely self-host 泛化到未来任意应用

canonical: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md

- local_id: raw-20260711T100936Z
- kind: raw
- phase_state: absorbed
- absorbed_into: I-20260711T100936Z-A
- platform_ids:
- github:
- issue_id: '3885'
- url: https://github.com/chatterzhao/freely/issues/3885
- synced_at: ''
- gitee:
- issue_id: IK0D5J
- url: https://gitee.com/zhaoquan/freely/issues/IK0D5J
- synced_at: ''
- primary_platform: github
- canonical_issue_path: ''
- last_synced_comment_at: {}
- hash: ''
- created_at: '2026-07-11T10:09:58Z'
- updated_at: '2026-07-11T10:09:58Z'
- intake_id: ''
- author: platform
- channel: github
- session_refs: []

\n\n## 问题

freely daemon stop 和 AI crash 都通过 SIGTERM 终止 ACP 进程，都产生 rc=143。
monitor-ai-acp.sh 无法区分这两种情况。

## 修复
在 monitor-ai-acp.sh 增加 stop_marker 检查：stop_reason=unknown 时若 stop_marker 文件存在 → stop_requested → exit 0。

## 验收
daemon stop → stopReason=stop_requested (非 unknown/crash)

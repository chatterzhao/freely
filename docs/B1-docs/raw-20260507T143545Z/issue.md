---
local_id: raw-20260507T143545Z45Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-17T00:24:14Z'
platform_ids:
  github:
    issue_id: '248'
    url: https://github.com/chatterzhao/freely/issues/248
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T14:35:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/B2-docs/timestamp-seconds-upgrade/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/timestamp-seconds-upgrade/code-reviews
platform_state: closed
---

- pre_tests_path: docs/B2-docs/timestamp-seconds-upgrade/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/timestamp-seconds-upgrade/code-reviews

## 问题
YYYYMMDDTHHMMZ 格式缺少秒，导致同分钟内 key 碰撞风险。正则 \d{4} 截断 6 位秒导致门禁假阳性。

## 修复
全部 \d{4} → \d{4,6}，_normalize_key_variants 增强为三格式互转含秒。

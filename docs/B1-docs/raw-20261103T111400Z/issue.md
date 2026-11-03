---
schema_version: '1'
local_id: raw-20261103T111400Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T111400Z-A
platform_ids:
  github:
    issue_id: '4140'
    url: https://github.com/chatterzhao/freely/issues/4140
    synced_at: ''
  gitee:
    issue_id: IKSP0M
    url: https://gitee.com/zhaoquan/freely/issues/IKSP0M
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T11:14:00Z'
updated_at: '2026-11-03T12:04:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T04:00:00Z'
closeout_note: ''
---
# chore: 物化 open raw 文档并回填历史 platform_ids


workflow_kind: fix

## 背景
双平台 open issue 已按 raw key 对齐（13=13，见 raw-20261103T091157Z 合并结果），但本地 docs/B1-docs 仍缺 13 个 open issue 的 raw 文档；另有 13 个历史本地 raw 文档缺平台编号。

## 任务（纯治理文档，不含代码）
1. 用 platform-adapter pull 物化 13 个双平台 open raw 文档（带双平台 platform_ids）。
2. 回填 13 个历史本地 raw 文档的 platform_ids（按 [RAW-key] 标题前缀唯一匹配，不猜、不创建历史 issue）。
3. 用 test-platform-open-parity.py --require-local-docs 作为验收（当前 FAIL，物化/回填后应 GREEN）。
4. 不批量补建历史 closed 镜像。

## 验收
- 13 个 open raw key 均有本地 docs/B1-docs/raw-{key}/issue.md，platform_ids.github 与 gitee 均非空且与平台实际编号一致。
- test-platform-open-parity.py --require-local-docs 通过。
- 改动仅限 docs/（B1/B2/milestones），无代码变更。

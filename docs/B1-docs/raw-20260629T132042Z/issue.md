---
local_id: raw-20260629T132042Z42Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T132042Z-A
platform_ids:
  github:
    issue_id: '3624'
    url: https://github.com/chatterzhao/freely/issues/3624
    synced_at: ''
  gitee:
    issue_id: IJXO6I
    url: https://gitee.com/zhaoquan/freely/issues/IJXO6I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T13:21:02Z'
updated_at: '2026-06-29T13:21:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

./bin/ → freely 替换在 216 个文件中执行，但以下 .sh 文件被 gate 判定为代码而撤销：

- .githooks/pre-commit.sh
- docs/system/workspace/hooks/pre-commit.sh
- docs/system/workspace/hooks/pre-merge-commit.sh
- docs/system/workspace/hooks/pre-push.sh
- docs/system/workspace/hooks/reference-transaction.sh
- docs/system/workspace/scripts/start-lead-agent.sh

这些文件的修改被撤销，需单独创建 raw issue 走完整 IBM 治理。

## 改动
以上 6 个 .sh 文件中将 ./bin/freely xxx → freely xxx、./bin/pr-xxx → freely pr-xxx

## 验收
- 6 个文件中的命令引用统一为 freely xxx 格式
- 通过完整 IBM 门禁

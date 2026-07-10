---
local_id: raw-20260710T034650Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T034650Z-A
platform_ids:
  github:
    issue_id: '3861'
    url: https://github.com/chatterzhao/freely/issues/3861
    synced_at: ''
  gitee:
    issue_id: IK043A
    url: https://gitee.com/zhaoquan/freely/issues/IK043A
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T03:47:12Z'
updated_at: '2026-07-10T03:47:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
pre-scan-fix.sh 三项待完成：
1. 注释 14-15 行写 `FREELY_SKIP_IBM_GATE=1`，应为完整格式 `="违规绕过门禁中，理由充分，是：<业务理由>"
2. BATCH_BODY 缺少 `##` 章节标题——feedback 新要求 body 必须含至少一个 ## section
3. 未集成到 daemon cycle——scan 前不会自动执行

## 修复
1. 注释修正为完整格式
2. BATCH_BODY 改为结构化章节（## 问题 / ## 修复 / ## 验收）
3. daemon cycle (line ~17153 scan 前) 调用 pre-scan-fix.sh --project $PROJECT_ROOT

## 验收
- grep FREELY_SKIP_IBM_GATE=1 无残留
- feedback 命令可接受 BATCH_BODY 格式
- daemon cycle 中 scan items 数量显著减少

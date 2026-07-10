---
local_id: raw-20260710T000650Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T000650Z-A
platform_ids:
  github:
    issue_id: '3850'
    url: https://github.com/chatterzhao/freely/issues/3850
    synced_at: ''
  gitee:
    issue_id: IK012G
    url: https://gitee.com/zhaoquan/freely/issues/IK012G
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T00:07:13Z'
updated_at: '2026-07-10T00:07:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
Scan 输出 685 items，其中 636 个是 terminal phase + 无 platform_ids 的本地文档残留。它们无法被 _sync_platform_direct 自动处理，也不该进入 Manager 的 AI cycle。

## 修复

### 1. pre-scan-fix.sh（新增）
Daemon cycle 在 scan 之前执行，自动处理 terminal phase 本地文档：
- 遍历 B1-docs/raw-*/issue.md
- terminal phase + 无 platform_ids → 对齐 frontmatter (platform_state = closed)
- 创建 1 个 batch raw issue (--skip-ibm)
- wt-create → 批量修改 → pr-create --skip-ibm → pr-merge --skip-ibm → wt-close

### 2. scan raw_key fallback
platform_ids 为空时，用 extract_raw_key() 从平台 issue 标题匹配：
- get_platform_open_issues 返回的 title 包含 [RAW-{key}]
- 匹配后自动填充 platform_ids 到 all_platform_states 映射
- _sync_platform_direct 可以正常执行

## 验收
- pre-scan-fix.sh 执行后 636 个本地文档被修复
- scan 输出 items 从 685 降到 ~50 个
- 平台 issue 能通过 raw_key 匹配到本地文档

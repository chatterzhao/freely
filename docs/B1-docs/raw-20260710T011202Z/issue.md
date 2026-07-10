---
local_id: raw-20260710T011202Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T011202Z-A
platform_ids:
  github:
    issue_id: '3858'
    url: https://github.com/chatterzhao/freely/issues/3858
    synced_at: ''
  gitee:
    issue_id: IK01F2
    url: https://gitee.com/zhaoquan/freely/issues/IK01F2
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T01:12:24Z'
updated_at: '2026-07-10T01:12:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
pr-create-guarded 的 Step 2c (IBM governance gate) 不检查 FREELY_SKIP_IBM_GATE 环境变量。pre-push hook 已支持此机制（per LAWS.md §304），但 pr-create-guarded 缺失。

纯文档修改（如 pre-scan-fix 批量对齐 frontmatter）被 IBM gate 拦截，无法通过正常流程提交。

## 修复
pr-create-guarded Step 2c: 检测 FREELY_SKIP_IBM_GATE 环境变量 → 调用 governance-merge-gate --skip-ibm-gate（与 pre-push hook 一致）

## 验收
- FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：纯文档修改" 环境下 pr-create-guarded 跳过 IBM gate
- docs/B1-docs/ + docs/B2-docs/ 路径变更放行
- 非 governance-only 路径仍然拦截

---
local_id: raw-20260706T050919Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3768'
    url: https://github.com/chatterzhao/freely/issues/3768
    synced_at: ''
  gitee:
    issue_id: IJZ04Q
    url: https://gitee.com/zhaoquan/freely/issues/IJZ04Q
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T05:09:40Z'
updated_at: '2026-07-06T05:09:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
多个门禁做全仓扫描(os.walk/find/ls)，历史遗留问题误伤当前 PR，
导致不得不用 --no-verify / --admin 绕过。

## 改造范围
### governance-merge-gate (核心)
- L829: os.walk(docs/B2-docs) → 只查 diff 中文件 + 它们 source_candidate/absorbed_into 引用的文件
- 已有 --staged 和 --range 参数，但部分检查未使用

### governance-check
- L854: ls -1 docs/B1-docs/ → 只查 diff 中涉及的 B1 目录
- L134: glob docs/pre-brainstorms → 只查 diff

### pr-review-guarded
- L175: find docs/B2-docs → 已大致 scoped，可优化但非必须

## 设计原则
- 扫变更的文件，验证它引用的东西。不扫没变的文件。
- --staged: 检查 staged diff 中文件
- --range develop..HEAD: 检查分支 diff 中文件
- 被 diff 中文件引用到的外部文件（如 source_candidate 指向的 candidate）也需检查

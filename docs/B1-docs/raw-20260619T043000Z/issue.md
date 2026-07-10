---
local_id: raw-20260619T043000Z00Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T043000Z-A
source_candidate: docs/B1-docs/raw-20260619T043000Z00Z/candidates.md#C-20260619T043000Z-A
platform_ids:
  github:
    issue_id: '3026'
    url: https://github.com/chatterzhao/freely/issues/3026
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T04:30:17Z'
updated_at: '2026-06-19T04:30:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

当前 gate 报错只描述"缺什么"，不引导开发者去读哪个 skill 的哪一节。skill 虽然示例格式大多正确，但没有门禁拦截速查列表、没有常见错误对照、没有 copy-paste 可用的规范示例。

实际踩坑(PR #3021 的 doc-only SVG 变更): gate 报错 10+ 次，每次排查都需读 gate 源码才能定位根因。

## 需改进的 skill

### B1_IBM-execution
新增章节: `## 常见门禁拦截速查`

| gate 报错 | 原因 | 正确格式 | 示例 |
|-----------|------|---------|------|
| cannot read C-xxx | source_candidate 需完整路径 | 文件路径#ID | docs/B1-docs/raw-{key}--{slug}/candidates.md#C-xxx |
| no valid source_candidate | candidates.md heading 需 ## 开头 | ## C-xxx | ## C-20260508T011858Z-A |
| phase_state is invalid | raw issue 合法值 | proposed/absorbed/dropped | phase_state: absorbed |
| no absorbed_into field | absorbed 必须写吸收目标 | I-* issue ID | absorbed_into: I-20260508T011858Z-A |
| milestone binding missing | active candidates 需绑 milestone | M-{key} | milestone: M-20260508T011858Z-A |

新增: `## 规范文档示例(copy-paste可用)`
- candidates.md 完整模板
- brainstorms.md 完整模板

### B2_IBM-execution
新增章节: `## 常见门禁拦截速查`

| gate 报错 | 原因 | 正确格式 |
|-----------|------|---------|
| verification_artifact_dir too broad | 需 /code-reviews 结尾 | docs/B2-docs/{epic}/code-reviews |
| implementation decision incomplete | 需 5 个字段 | decision/why_this/alternatives_considered/boundary_non_goals/residual_risk |

新增: `## 规范文档示例`
- I-* issue.md 完整模板(含所有必需字段)
- Implementation Decision Note 完整模板
- pre-tests.md 完整模板

### governance-merge-gate 自身
gate 报错信息增加引导:
```
→ 查看 skill:freely-doc-B1_IBM-execution §常见门禁拦截速查
→ 查看 skill:freely-doc-B2_IBM-execution §常见门禁拦截速查
```

### pr-review-guarded(无归属 skill)
review 文件缺少 issue_id: 
- pr-review-guarded 自动生成 review 时包含 issue_id/issue_path 字段
- 或相关 skill 的常见错误列表覆盖此坑

## 预期效果

开发者在 gate 报错后:
1. 看报错信息 → 知道去读哪个 skill 的哪一节
2. 在 skill 常见错误列表中找到自己的错误 → 看正确示例
3. 复制规范示例 → 改值 → 提交 → 通过

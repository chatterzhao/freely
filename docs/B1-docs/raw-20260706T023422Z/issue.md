---
local_id: raw-20260706T023422Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3761'
    url: https://github.com/chatterzhao/freely/issues/3761
    synced_at: ''
  gitee:
    issue_id: IJYYAF
    url: https://gitee.com/zhaoquan/freely/issues/IJYYAF
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T02:34:43Z'
updated_at: '2026-07-06T02:34:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed
absorbed_into: raw-20260710T005219Z---

\n\n## 背景

原始 refactor raw-20260705T155347Z (PR #3755) 设计了 B1-docs/B2-docs 新目录结构，但执行时有遗漏。

## 原始 B1 设计的范围 (P0-P6)

见 raw-20260705T155347Z brainstorms.md 的完整列表。执行后仍遗漏：

## 遗漏分类

### A. 生产代码旧路径 (P0-P1 漏改)
1. `bin/freely-watchdog:18` — `docs/pre-brainstorms/` 旧路径
2. `scripts/quality/governance-check` — 10 处 `docs/pre-brainstorms/`
3. `scripts/quality/checkpoint-guard:60` — `docs/pre-brainstorms/`
4. `governance-merge-gate:826` — `docs/epics/` 未改为 `docs/B2-docs/` (已在 PR #3760 修)

### B. verification_artifact_dir 缺 raw-{key} 层 (~50 I-* 文件)
门禁 regex 要求 4 层: `{epic}/{story}/raw-{key}/code-reviews`
但 ~50 个已有 I-* 文件写的是 3 层: `{epic}/{story}/code-reviews`
这些文件应更新 `verification_artifact_dir` 字段。

### C. Skill 模板路径过时
- `freely-doc-B2_IBM-execution` — 示例路径仍用 `docs/B2-docs/`，无 `raw-{key}` 层
- `freely-doc-B1_IBM-execution` — `source_candidate` 格式用 `docs/pre-brainstorms/`

### D. pr-review-guarded sed 格式
sed 期望单引号 `'path'`，但 skill 模板和已有文件都用反引号 `\`path\``。已通过的文件用反引号，新文件按 sed 只能写单引号。格式不统一。

### E. 测试文件 (~100+ 处旧路径)
低优先级，测试 setup 用旧路径创建目录

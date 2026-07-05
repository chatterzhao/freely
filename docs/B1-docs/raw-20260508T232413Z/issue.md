---
local_id: raw-20260508T232413Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260508T232413Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-29T13:43:02Z'
platform_ids:
  github:
    issue_id: '262'
    url: https://github.com/chatterzhao/freely/issues/262
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T23:24:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 背景

当前 pr-merge-guarded 报错输出缺少对 AI 工作流的引导。AI 反复 merge→fail→fix→merge，而不是先 dry-run 定位问题。

## 期望行为

merge 失败时应引导 AI 做三步：

1. **自我诊断**：是否 B1→B2→dev-loop 阶段不完整？
   - B1 only（`needs_research`）→ 不应 merge，gate 正确拦截
   - B1+B2（`in_b2_ibm`/\`in_dev`）→ 缺 dev-loop evidence
   
2. **读对应 skill**：fix 工位读 fix-execution，feature 工位读 feat-execution

3. **用 --range dry-run**：`./bin/governance-merge-gate --range develop..HEAD` 预检，不触发 ref update

## 改动

pr-merge-guarded 第 292-303 行报错输出改为：

```
┌─ Merge blocked ─────────────────────────────────────────┐
│  在继续之前，先自我诊断:                                   │
│                                                          │
│  1. 当前 IBM 阶段?                                        │
│     B1 (needs_research) → 仅研究，不应 merge               │
│     B1 (promoted) → 需 B2_IBM 创建 I-* issue              │
│     B2 (in_b2_ibm/in_dev) → 需 dev-loop evidence          │
│     dev-loop done → 检查下面具体错误                        │
│                                                          │
│  2. 读对应 skill 了解完整工作流:                            │
│     fix 工位 → skill:fix-execution                         │
│     feature 工位 → skill:feat-execution                    │
│                                                          │
│  3. 先用 --range dry-run 预检（不触发 ref update）:         │
│     ./bin/governance-merge-gate --range develop..HEAD     │
└──────────────────────────────────────────────────────────┘

<具体的 gate 错误>

修复后在 source worktree 重试: cd <worktree> && freely pr-merge-guarded ...
```
- pre_tests_path: docs/B2-docs/merge-error-ibm-guide/verification/pre-tests.md
- verification_artifact_dir: docs/epics/merge-error-ibm-guide/code-reviews

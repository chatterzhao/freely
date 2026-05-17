---
local_id: raw-20260506T1200Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
phase_state: completed
platform_ids:
  github:
    issue_id: '285'
    url: https://github.com/chatterzhao/freely/issues/285
    synced_at: '2026-05-10T09:30:28Z'
primary_platform: github
created_at: 2026-05-06 12:00:00+00:00
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/epics/ibm-skill-rename/verification/pre-tests.md
verification_artifact_dir: docs/epics/ibm-skill-rename/code-reviews
updated_at: 2026-05-17T04:47:25Z
platform_state: open
---

## 问题
doc-pre-brainstorm-execution / doc-ibm-execution 命名未体现 B1_IBM/B2_IBM。
I→B→M 骨架未被下层 skill 强制消费。

## 修复
1. 改名 doc-B1_IBM-execution / doc-B2_IBM-execution，全局替换
2. 两个 SKILL.md 加入 I→B→M 骨架
3. ibm-framework.md 术语统一


- pre_tests_path: `docs/epics/ibm-skill-rename/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/ibm-skill-rename/code-reviews`

---
b1_id: B1-20260619T043000Z
phase_state: completed
source_raw: raw-20260619T043000Z
source_url: https://github.com/chatterzhao/freely/issues/3026
produced_candidate: C-20260619T043000Z-A
created_at: 2026-06-19
---

# B1_IBM: IBM治理快速达标 — skill常见错误列表+规范示例+gate报错引导

## Input

- GitHub #3026
- Raw issue: docs/B1-docs/raw-20260619T043000Z/issue.md

## Problem

IBM gate 报错只说"缺什么"不引导去读哪个 skill。Skills 示例格式正确但无速查列表、无常见错误对照、无 copy-paste 模板。实际踩坑：PR #3021 因 candidates.md 单# heading 失败 10+ 次。

## Brainstorm

### Option A: 只改 gate 报错，加 skill 引用
简单但治标不治本——skill 没有速查列表，读者还是要从头读。

### Option B: skill 加门禁常见坑速查 + 规范模板 + gate 报错加引导
完整方案。与已有 fix-execution 的 `## 门禁常见坑速查` 约定一致。

## Decision: Option B

### Scope
1. B1_IBM skill：加 `## 门禁常见坑速查` 表格 + 规范模板
2. B2_IBM skill：加 `## 门禁常见坑速查` 表格 + 规范模板
3. governance-merge-gate：报错后加分组 footer 引导到对应 skill
4. fix-execution skill：已有速查表，更新交叉引用到 B1/B2

## Candidate
- candidate_id: C-20260619T043000Z-A
- status: promoted
- milestone: M-20260619T043000Z-A

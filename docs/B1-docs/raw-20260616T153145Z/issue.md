---
local_id: raw-20260616T153145Z45Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260616T044030Z-A
platform_ids:
  github:
    issue_id: '2857'
    url: https://github.com/chatterzhao/freely/issues/2857
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T15:32:01Z'
updated_at: '2026-06-16T15:32:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## Problem

`raw-20260616T044030Z30Z` (config.toml migration) 的 brainstorms.md 在 merge 时写的选定方案是"自动迁移（渐进式，保留 config.env 回退）"，但实际实现做的是"彻底 TOML-only，零 config.env 回退"。governance-merge-gate 只验证了文档存在性，没发现文档描述与实现不一致。

## 根因

governance-merge-gate 检查 IBM 产物存在性和结构化字段（candidate status、milestone entry），但不检查文档内容与实际 diff 是否一致。brainstorms.md 的 Decision 段落和 candidates.md 的 Solution/Acceptance Criteria 应该反映实际实现，但目前没有自动化验证。

## 需要修的

### 1. 修正 brainstorms.md 和 candidates.md（数据修复）

将 stash 中的改正提交——方案描述从"自动迁移"改为"彻底 TOML-only"，验收标准与实现对齐。

### 2. 评估 governance-merge-gate 增强（可选，未来）

考虑在 gate 中加入 diff-vs-doc 语义一致性检查，或至少警告当 brainstorms.md 的 "Decision" 段落与实现 diff 明显不一致时。但这是大工程，本 issue 不承诺做。

## 不做

- 不回退已合并的实现
- 不改变 config.toml 行为
- 不强制 governance-merge-gate 语义检查（那是独立 issue）

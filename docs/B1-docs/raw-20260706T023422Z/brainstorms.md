---
b1_id: B1-20260706T023422Z
phase_state: completed
source_raw: raw-20260706T023422Z
source_url: https://github.com/chatterzhao/freely/issues/3761
produced_candidate: C-20260706T023422Z-A
created_at: 2026-07-06
---

# B1: docs-structure-refactor 遗漏补完

## Input
- raw-20260706T023422Z (GitHub #3761)
- 原始 refactor raw-20260705T155347Z (GitHub #3755) 的 B1 设计文档

## Discovery

### 现状 vs 目标

原始 refactor (`raw-20260705T155347Z`) 设计了完整的 old→new 路径迁移方案（P0-P6），但执行时有遗漏。

### 遗漏分类

#### A. 生产代码旧路径 (P0-P1 漏改) — Phase 1 修复
- `bin/freely-watchdog:18` — `docs/pre-brainstorms/` → `docs/B1-docs/`
- `quality/governance-check` — 10 处 `docs/pre-brainstorms/` → `docs/B1-docs/`
- `quality/checkpoint-guard:60` — `docs/pre-brainstorms/` → `docs/B1-docs/`
- `governance-merge-gate:826` — `docs/B2-docs/` → `docs/B2-docs/` (已在 PR #3760 修)

#### B. verification_artifact_dir 缺 raw-{key} 层 — Phase 2 修复
门禁 regex: `docs/B2-docs/{epic}/{story}/raw-{key}/code-reviews`（4 层）
但 51 个已有 I-* 文件写的是 `docs/B2-docs/{epic}/{story}/code-reviews`（3 层）

修复方式：从 I-* 文件的 `issue_id` / `local_id` / `promoted_from` 字段提取 raw key，用脚本自动修正。

#### C. Skill 模板 — 已干净
workspace skills (`docs/system/workspace/skills/`) 已在原始 refactor 中更新为 B1-docs/B2-docs 路径。
全局 skills (`~/.claude/skills/`) 仍有旧路径引用，但那是安装层面的问题，不在本次 scope。

#### D. pr-review-guarded sed 格式 — 设计决策
sed 期望单引号 `'path'`，但 skill 模板和已有文件用反引号 `` `path` ``。
这造成了格式不统一。由于门禁 regex 是准确的（4 层 B2-docs），sed 提取是次要问题。
本次不修改 sed（改动面大），已在 Phase 2 文件中统一使用反引号格式。

### 脚本方法

Phase 2 修复脚本使用以下方法：
1. 扫描所有 `docs/B2-docs/**/I-*.md`
2. 从元数据字段提取 raw key：`issue_id` → `I-{raw_key}-{suffix}`，`local_id`，`promoted_from`
3. 从文件路径提取 epic/story
4. 逐行检查 `verification_artifact_dir` 和 `pre_tests_path`，缺少 `raw-{key}` 层则修正

## Decision

分阶段处理，独立 commit：
- Phase 1: 生产代码 3 文件直接替换
- Phase 2: 51 I-* 文件脚本修正（从文档字段提取 raw key）
- Phase 3+: （后续）历史文件目录迁移

## Candidate
- candidate_id: C-20260706T023422Z-A
- status: promoted
- milestone: M-20260706T023422Z-A

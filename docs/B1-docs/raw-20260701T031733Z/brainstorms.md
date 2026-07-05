---
b1_id: B1-20260701T031733Z
phase_state: completed
source_raw: raw-20260701T031733Z33Z
source_url: https://github.com/chatterzhao/freely/issues/3680
produced_candidate: C-20260701T031733Z-A
created_at: 2026-07-01
---

# B1_IBM: pr-create pre-flight self-check + skill-gate alignment

## Input
- **Raw issue**: raw-20260701T031733Z33Z
- **Platform**: GitHub #3680 / Gitee IJY0HM
- **Source**: 连续 3 个 PR 在门禁阶段反复失败，每次需 2-8 轮修复

## Problem

每个 PR 的门禁阶段平均需要 3-8 轮修复才能通过。根因是三个层面的不同步：

### 层面 1：Skill 模板缺字段
- B1 candidates.md 模板有 `promoted_issue_id` 但无 `promoted_issue_path`
- raw issue 模板无 `absorbed_into` 字段
- B2 pre-tests.md 示例使用反引号但 gate parser 不支持

### 层面 2：完全遗漏的步骤
- epics-map.svg 更新从未在任何 skill 中提到（每个 PR 都撞）
- evidence .log 文件被 gitignore，需要 force-add（skill 未提示）

### 层面 3：dev↔test 同步时机不明确
- dev-loop 提交后没有提醒 merge 到 test
- test-execution 只写 "cherry-pick 同步" 但没有明确 "先 merge dev 到 test"

## Brainstorm

### Option A：只修 skill 模板（被动方案）
修改 B1/B2/dev/test 4 个 skill 的模板和检查清单。
- ✅ 源头修正
- ❌ 仍然依赖执行者逐条检查
- ❌ 新增 gate 规则时容易再次遗漏

### Option B：pr-create-guarded 增加 pre-flight（主动方案）
在执行 gate 之前，先跑一遍已知的常见检查，不通过直接给修复建议。
- ✅ 主动发现，不等 gate 报错
- ✅ 新 gate 规则可以添加到 pre-flight
- ❌ 需要新增代码

### Option C：A + B 组合
同时修 skill 模板 + 加 pre-flight self-check。
- ✅ 最完整
- ✅ skill 指导正确 + gate 前自检双重保障

## Decision: Option A（本轮只修 skill 模板）

本轮 focus：修正 5 个 skill 文档的模板、示范和检查清单。pre-flight 代码逻辑较复杂，留到后续单独评估。

### 本轮 scope

| 文件 | 改动 |
|------|------|
| `freely-doc-B1_IBM-execution` | candidates.md 模板加 `promoted_issue_path`；raw issue 模板加 `absorbed_into` |
| `freely-doc-B2_IBM-execution` | pre-tests.md 模板去反引号、加 .log force-add 提醒、section 格式修正；完成自检清单加 epics-map.svg |
| `freely-dev-loop-execution` | 提交代码后增加"merge 到 test"提醒 |
| `freely-test-execution` | "同步最新代码"步骤改为 merge 优先 |
| `freely-workflow-guarded-execution` | 阶段 5 test-GREEN 前加 dev↔test 同步步骤 |

### 影响范围
- 5 个 skill 文档
- 仅文档变更，无代码变更
- 不改 gate 逻辑（gate 规则本身正确，只是 skill 引导没跟上）

## Candidate
- candidate_id: C-20260701T031733Z-A
- status: promoted
- milestone: M-20260701T031733Z-A
- promoted_issue_id: I-20260701T031733Z-A
- decision_reason: 本轮修 skill 模板和检查清单，从源头减少门禁失败
- next_action: B2 设计 → dev 逐一修改 skill 文档 → test 验证 → PR

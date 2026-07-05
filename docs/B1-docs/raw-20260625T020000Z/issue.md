---
local_id: raw-20260625T020000Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3453'
    url: https://github.com/chatterzhao/freely/issues/3453
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T00:08:36Z'
updated_at: '2026-06-25T00:08:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T020000Z-A
source_candidate: docs/B1-docs/raw-20260625T020000Z/candidates.md#C-20260625T020000Z-A
---

## 问题

IBM gate / pr-create-guarded 的修复体验差，根因是多层面的：

### 1. gate 原生错误消息零 skill 引用

`governance-merge-gate` 62 条错误输出全是技术描述：
```
- raw-xxx 的 source_candidate 是 'missing'      ← 用户："这是什么？去哪修？"
```
没有指向 `skill:freely-doc-B1_IBM-execution §candidate-recording.md` 或类似定位。

### 2. pr-create-guarded error prompt 不感知 fix/feat

wt-create 已经传了 `--skill` 参数，但 gate 错误框写死：
```
skill:freely-doc-B1_IBM-execution → brainstorm → candidate
skill:freely-doc-B2_IBM-execution → I-* → pre-tests → code-review
```
实际 fix 是 `dev→test→B1→B2`，feat 是 `B1→B2→dev→test`。提示应该按 --skill 类型给出正确阶段顺序。

### 3. 错误消息不指向 skill 的具体章节

gate 说 "source_candidate missing" → 应指向 B2_IBM skill 里 I-* issue 模板那节
gate 说 "phase_state invalid" → 应指向 B1_IBM skill 里 phase_state 合法值表
gate 说 "milestone binding missing" → 应指向 milestones.md 格式那节

### 4. 用户不看完整 skill

wt-create 已经说了"请阅读 skill:，Skill 是流程的唯一权威来源"，但用户和 agent 都倾向于看摘要而非逐节阅读。错误提示是最后一次机会——应该在报错时就给出精确的 skill 章节引用。

## 改动

### governance-merge-gate 错误消息增强

每个错误类型映射到具体的 skill + 章节：
- `source_candidate missing` → "修复方式：在 I-* issue.md 中添加 source_candidate 字段，格式见 skill:freely-doc-B2_IBM-execution §I-* issue 模板"
- `phase_state invalid` → "合法值见 skill:freely-doc-B1_IBM-execution §门禁常见坑速查"

### pr-create-guarded error prompt 上下文感知

从 branch 名判断 fix/feature，动态拼接：
- fix 分支："你是 fix 工位：实现已完成 → 补 B1→B2 治理。Fix first, govern later。"
- feature 分支："你是 feature 工位：B1→B2 治理 → 然后实现。Govern first, code later。"

### wt-create 输出强化

fix 和 feature 的提醒信息**差异化**，不仅仅是 prefix 不同。

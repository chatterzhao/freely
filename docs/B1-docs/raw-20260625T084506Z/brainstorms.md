---
b1_id: B1-20260625T084506Z
phase_state: completed
source_raw: raw-20260625T084506Z
source_url: https://github.com/chatterzhao/freely/issues/3494
produced_candidate: C-20260625T084506Z-A
created_at: 2026-06-25
---

# B1_IBM: B2_IBM skill 反糊弄铁律

## Input
- source: raw-20260625T084506Z (GitHub #3494)
- 问题: B2_IBM skill 当前只提供 pre-tests.md 模板，没有告诫用户不要凑字段糊弄门禁
- 用户倾向全部写 not_applicable + mock 绕过检查

## Problem
- pretests-retirement-gate 已合并反作弊检查（#3451），但 B2_IBM skill 本身没有反糊弄指导
- AI 在写 pre-tests.md 时缺乏明确的行为约束，容易产出全 mock/not_applicable 的垃圾测试方案
- 测试方案糊弄 = 浪费完整 dev→test→pr 流水线，且掩盖真实 bug

## Brainstorm
### Option A: 在 B2_IBM SKILL.md 模板前加醒目警告
- 直接在 pre-tests.md 模板前插入反糊弄铁律 blockquote
- 明确禁止行为：全 mock、ghost pass、not_applicable 无理由
- 强调端到端测试和集成测试是 AI 编程防失败最重要保证
- 语言力度：糊弄是严重失职行为，绝对不允许

### Option B: 单独创建反糊弄规范文档
- 新建独立文档链接到 B2_IBM skill
- 缺点：AI 可能不读链接文档，效果不如内嵌警告

## Decision: Option A
- 内嵌到 B2_IBM SKILL.md 模板前，AI 写 pre-tests.md 时必然看到
- 语言必须强硬——"严重失职行为"不是"浪费时间"
- 同步加强 pretests-retirement-gate：新增端到端/集成测试层级充分性硬拦截
- test-execution skill 同步加强（#3495）

## Candidate
- candidate_id: C-20260625T084506Z-A
- status: promoted
- milestone: M-20260625T084506Z-A

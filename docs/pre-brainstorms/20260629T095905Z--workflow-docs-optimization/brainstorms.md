---
b1_id: B1-20260629T095905Z
phase_state: completed
source_raw: raw-20260629T095905Z
source_url: https://github.com/chatterzhao/freely/issues/3620
produced_candidate: C-20260629T095905Z-A
created_at: 2026-06-29
---

# B1_IBM: 优化 workflow skill 覆盖缺口

## Input
- raw issue: raw-20260629T095905Z
- 发现问题：AI 在执行开发任务时跳过 B1_IBM/B2_IBM/RED 直接写代码
- 根因追踪：workflow skill 没有覆盖"无 raw issue"场景和"cd 到工位"操作

## Problem

freely-workflow-guarded-execution 是 Freely 所有开发工作的唯一流程入口。但实际使用中发现三个缺口：

1. **缺少"阶段 0：创建 raw issue"**：skill 定位是 feedback 之后加载，假设 raw issue 已存在。AI 遇到问题没有 raw issue 时不知道该先 feedback。

2. **缺少 cd 到开发工位**：wt-create 跑完后，skill 没有任何一步说"cd 到开发工位"。AI 继续在 develop 上操作，所有后续命令都违规。

3. **CLAUDE.md 链不够强制性**：CLAUDE.md 礼貌地说"完整治理规则请见 AGENTS.md"，AI 可能跳过不读。需要明确命令 AI 启动后第一件事是读 AGENTS.md。

## Brainstorm

### Option A: 只改 CLAUDE.md（单一入口）
在 CLAUDE.md 写全所有流程细节，不依赖 AGENTS.md 和 skill 链。
- 优点：入口单一，AI 必读
- 缺点：CLAUDE.md 膨胀，与 AGENTS.md/skill 重复维护，违背"skill 是权威来源"原则

### Option B: 在 workflow skill 增加阶段 0 + cd（当前方案）
在 freely-workflow-guarded-execution 增加"阶段 0"和 cd 提示，CLAUDE.md 强化强制性指向。
- 优点：skill 保持为单一权威来源，CLAUDE.md 轻量指向
- 缺点：需要 AI 跟链（CLAUDE.md → AGENTS.md → workflow skill）

### Option C: 在 AGENTS.md 增加场景分支
把"无 raw issue → feedback → wt-create → cd"写在 AGENTS.md 中，作为开发流程的第一步。
- 优点：AGENTS.md 已是操作入口
- 缺点：AGENTS.md 已经很长，增加场景分支会让它更复杂，且 skill 才是权威来源

## Decision: Option B

在 workflow skill 增加阶段 0 和 cd 提示，同时强化 CLAUDE.md 的强制性。

理由：
1. **skill 是权威来源**（LAWS.md 原则），流程变更必须在 skill 中体现
2. **CLAUDE.md 轻量指向**保持简洁，但用强制性语言确保 AI 跟链
3. **AGENTS.md 保持为操作速查**，不重复 skill 中的详细步骤
4. 改动面最小：3 个文件，约 30 行新增

## 自检
- [x] discovery：Input + Problem 完整
- [x] research：3 方案（A/B/C）含优缺点对比
- [x] decision：选 Option B，4 条理由
- [x] 下一跳明确：进入 `freely-doc-B2_IBM-execution` 创建 I-* issue + pre-tests + code-review

## Candidate
- candidate_id: C-20260629T095905Z-A
- status: promoted
- milestone: M-20260629T095905Z-A

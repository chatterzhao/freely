---
b1_id: B1-20260706T232728Z
phase_state: completed
source_raw: raw-20260706T232728Z
source_url: https://github.com/chatterzhao/freely/issues/3787
produced_candidate: C-20260706T232728Z-A
created_at: 2026-07-06
---

# B1: 封装命令文档系统化 — 意图→命令映射 + 为什么用封装

## Input
- raw-20260706T232728Z: 封装命令文档系统化
- GitHub issue #3787
- Kind: feature

## Discovery

### value_check: 当前状态
1. AGENTS.md 有命令速查表，但只列"✅正确 vs ❌禁止"，缺少"为什么"和"什么场景用什么"
2. SKILL.md 有铁律区域（禁止绕过），但都是负向约束，没有正向引导的意图→命令映射
3. `.githooks/bin/gh` wrapper 拦截消息告诉正确命令，但没有解释封装了什么
4. `pre-commit.sh` 和 `pre-push.sh` 被拦截时没有提示"你应该用什么命令"
5. 新建开发者/AI agent 没有集中的命令参考文档

### scope_check: 改动范围
- AGENTS.md: 增强速查表（加"意图"列 + "封装了什么"列）
- freely-workflow-guarded-execution SKILL.md: 铁律区域前加"意图→命令速查"章节
- `.githooks/bin/gh`: 拦截消息加"为什么"解释
- `.githooks/pre-commit.sh`: 拦截末尾加正向流程提示
- `.githooks/pre-push.sh`: 同上
- 新建 `docs/system/workspace/commands.md`: 封装命令权威参考

全部是纯文档/文本修改，无运行时行为变更。

## Problem

当前文档分散且不一致：
- 知道"不能做什么"（hook 拦截），但不知道"应该做什么"
- 不知道为什么必须用封装命令（以为是无意义的包裹）
- 没有从开发者意图出发的命令选择指南

## Brainstorm

### Option A: 只增强 AGENTS.md 速查表
- 加"意图"和"封装了什么"列
- 优点：改动最小，AGENTS.md 是入口文件
- 缺点：hook 拦截点仍然没有正向引导；没有集中参考

### Option B: 集中 commands.md + 各触点嵌入 ✅
- 新建 `docs/system/workspace/commands.md` 作为权威参考
- AGENTS.md 增强速查表（从意图出发）
- SKILL.md 加"意图→命令速查"章节（铁律之前，先正向引导）
- Hook 消息加"为什么"和"你应该用什么"
- 优点：每个触点都为该场景定制，commands.md 统一真源
- 缺点：改动 6 个文件

### Option C: 只增强 hook 消息
- `.githooks/bin/gh`、pre-commit.sh、pre-push.sh 加正向提示
- 优点：直接在拦截点解决问题
- 缺点：等被拦截才知道正确命令，不是主动引导

## Decision: Option B — 集中 + 分布

理由:
1. 不同位置的受众不同：AGENTS.md（入口）、SKILL.md（流程执行者）、hook 消息（被拦截者）、commands.md（查阅者）
2. 每个位置定制表述但不能互相矛盾——commands.md 作为统一真源，其余位置引用
3. hook 消息是最紧迫的改进点（直接减少"不知道该用什么"的挫败感）
4. "意图→命令"映射是这个 issue 的核心价值——让人从想做什么出发，不需要记住命令名

设计原则:
- **从意图出发**: 让用户从"我想做什么"找到对应命令
- **说清封装了什么**: 每个命令列出封装的步骤，让人理解这不是无意义包裹
- **被拦截时给正向引导**: hook 消息不只是说"你错了"，而是"你应该用什么"
- **一致性**: AGENTS.md ↔ SKILL.md ↔ hook 消息 ↔ commands.md 表述一致

## Candidate
- candidate_id: C-20260706T232728Z-A
- status: promoted
- milestone: M-20260706T232728Z-A

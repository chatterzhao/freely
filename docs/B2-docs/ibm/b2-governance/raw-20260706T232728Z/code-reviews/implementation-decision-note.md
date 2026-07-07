# Implementation Decision Note

- issue_id: I-20260706T232728Z-A
- milestone: M-20260706T232728Z-A
- created_at: 2026-07-06

## Decision

采用"集中真源 + 分布触点"架构：新建 `docs/system/workspace/commands.md` 作为封装命令唯一权威参考，同时在 AGENTS.md、SKILL.md、.githooks/ 等触点嵌入场景化的正向引导，各触点核心信息（命令名、封装步骤）与 commands.md 保持一致。

## Why This

1. **不同触点受众不同**：AGENTS.md 是入口（开发者第一次接触）、SKILL.md 是执行者（AI agent 遵循流程）、hook 消息是被拦截者（需要即时正向引导）、commands.md 是查阅者（需要完整参考）
2. **"意图→命令"映射是核心价值**：让开发者从想做什么出发，不需要记忆命令名——这比传统的"命令→作用"方向更符合心智模型
3. **hook 拦截消息是最高杠杆改进点**——直接减少"不知道该用什么命令"的挫败感

## Alternatives Considered

| 方案 | 描述 | 评估 |
|------|------|------|
| A: 只增强 AGENTS.md | 在现有入口文件加意图列和封装说明 | 改动最小但 hook 拦截点仍无正向引导，缺少集中参考 |
| B: 集中 commands.md + 各触点嵌入 | 新建真源 + 各触点场景化引导 | ✅ 选定：覆盖面完整，各触点各自优化 |
| C: 只增强 hook 消息 | 只在拦截点解决问题 | 等被拦截才知道正确命令，不是主动引导 |

## Boundary Non-Goals

- 不新增或修改封装命令本身（只文档化已有命令）
- 不修改运行时行为或脚本逻辑
- 不改变任何门禁规则（只增强门禁消息的可读性）
- 不涉及 `freely chat`、`freely daemon` 等非封装性质的命令

## Residual Risk

- **无运行时风险**：全部为纯文本/文档变更，零代码改动
- **一致性漂移风险**：未来新增封装命令时，如果只更新 commands.md 而忘记更新触点（AGENTS/SKILL/hooks），会导致不一致。缓解：commands.md 中有"为什么用封装命令"表格可作为触点更新的 checklist
- **翻译风险**：gh wrapper 部分消息从英文改为中文，需确认与现有 hook 消息风格一致

## 实现概述

纯文档变更，6 个文件。建立了"集中真源 + 分布触点"的封装命令文档体系。

## 改动文件

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `docs/system/workspace/commands.md` | 新建 | 封装命令权威参考，7 个命令的完整文档 |
| `AGENTS.md` | 修改 | 增强速查表：场景→意图+命令+封装了什么+禁止 |
| `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md` | 修改 | 铁律前增加"意图→命令速查"正向引导 |
| `.githooks/bin/gh` | 修改 | 3 个拦截 case 全部加"为什么"解释 |
| `.githooks/pre-commit.sh` | 修改 | develop 拦截末尾加正向流程提示 |
| `.githooks/pre-push.sh` | 修改 | push 拦截末尾加正向流程提示 |

## 设计决策

### 为什么是"集中命令真源 + 分布触点"的架构

- `commands.md` 是唯一的权威参考，面面俱到
- AGENTS.md、SKILL.md、hook 消息都是"触点"——各自场景定制表述
- 这样加新命令时只需更新 commands.md，触点引用即可
- 触点表述可以不一致（场景不同），但核心信息（命令名、封装步骤）必须一致

### 为什么 AGENTS.md 表用"你想做什么"而不是"场景"

从开发者心智模型出发，不是从命令类别出发。一个开发者不会想"我需要用封装命令"，而是想"我想提 PR"→ 查表 → 得到 `freely pr-create-guarded`。

### 为什么 hook 消息要包含完整流程

被 hook 拦截的开发者往往不知道自己在流程中的哪个位置。给出完整流程概览让他知道自己跳过了什么，才能理解为什么不能绕过。

## 无运行时影响

全部修改为纯文本/文档变更：
- 不改任何脚本逻辑
- 不改任何函数签名
- 不改任何运行时行为
- `freely deploy-skills` 只复制 SKILL.md 到部署目录

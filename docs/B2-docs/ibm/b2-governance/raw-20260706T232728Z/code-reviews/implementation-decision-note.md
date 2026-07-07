# Implementation Decision Note

- issue_id: I-20260706T232728Z-A
- milestone: M-20260706T232728Z-A
- created_at: 2026-07-06

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

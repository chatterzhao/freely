---
local_id: raw-20260516T014923Z23Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '354'
    url: https://github.com/chatterzhao/freely/issues/354
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T01:49:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## raw-20260516T014923Z23Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T014923Z23Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T01:49:23Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T014923Z23Z`。实现前请用 `wt-create --raw-key 20260516T014923Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
status: open
source: chat-inbox
created_at: "2026-05-16T01:49:23Z"
title: "Freely Agent 规范重构：合并 lead-agent、skill 角色归属、tool 清单标准化"

## 背景

对照行业标准（Google A2A、Anthropic Agent Design Patterns、OpenAI Agents SDK、NIST AI Agent Standards）审计 Freely 当前 agent 设计，发现以下系统性问题：

## 问题清单

### 1. lead-agent 角色冗余

现状：
- `docs/system/workspace/agents/lead-agent.md` 定义了一个独立的 lead-agent 角色
- 其职责（首跳路由、context source 判断、worktree 监督分派）实质上是 Manager 在 auto-loop 中的首跳职责
- 三个 agent（lead → manager → worker）的层次在实际运行时并不清晰：lead-agent 做完首跳后不 handoff 给另一个 agent，而是自己继续当 Manager

方案：
- 将 lead-agent 中有价值的内容（首跳协议、context-source-skill 调用、constitution-guard/laws-enforcer 预检）合并进 manager-agent.md
- 删除独立的 lead-agent.md
- 明确：Manager 在不同阶段承担不同职责（首跳路由 / 巡逻委派 / 收口判断），但始终是同一个角色

### 2. Skill 无角色归属

现状：
- `docs/system/workspace/skills/` 下有 36 个 skill，flat 组织
- `skills/README.md` 只列名称，不标注每个 skill 归属哪个 agent 角色
- `manager-agent.md` 的工具章节只列了 5 个 CLI 命令，0 个 skill 引用——Manager 不知道有 `freely-multi-worktree-supervision`、`freely-worktree-maintenance-governance`、`freely-premerge-reconcile` 等现成技能可用
- `worker-agent.md` 完全没有 skill/tool 引用
- 只有 `lead-agent.md` 引用了 10+ 个 skill

行业参考：
- Google A2A Agent Card：每个 agent 声明自己支持的能力（skills）
- Anthropic：worker 有明确的 tool-use 模式

方案：
- 按角色给 skill 打标签（lead/manager/worker/all）
- 每个 agent 定义文件增加 `## 可用技能` 章节，列出该角色应加载的 skill
- Manager 新增：`freely-multi-worktree-supervision`、`freely-worktree-maintenance-governance`、`freely-premerge-reconcile`、`freely-laws-enforcer` 等
- Worker 新增：`freely-laws-enforcer`、`freely-agent-execution-safety-review`、`freely-constitution-guard` 等

### 3. Agent 缺少可用工具清单

现状：
- `manager-agent.md` 的「工具」章节列了 5 个 CLI 命令
- `worker-agent.md` 没有工具清单
- 没有 standard agent 应有的 tools list

行业参考：
- 规范 agent 定义通常包含：可用 tools、tools 的用途、何时使用
- A2A Agent Card 包含 capabilities 声明
- Anthropic agent 模式推荐 poka-yoke（防错）工具设计

方案：
- 每个 agent 定义增加 `## 可用工具` 章节
- Manager 工具：live-status、fleet-status、task-source-scan、handoff.py、wt-create、pr-merge-guarded 等
- Worker 工具：git、bin/issue-sync、bin/pr-merge-guarded 等（执行级工具）
- 标注每个工具的使用条件和风险

### 4. 引用

- Google A2A Protocol: https://google.a2a.protocol
- NIST AI Agent Standards Initiative: https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative
- Anthropic Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- Anthropic Multi-Agent Research System: https://www.anthropic.com/engineering/built-multi-agent-research-system
- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents

## 范围

只改：
- `docs/system/workspace/agents/`（合并 lead → manager，更新 manager/worker）
- `docs/system/workspace/skills/README.md`（加角色归属标注）

不改：
- runtime 脚本
- skill 具体内容
- 工具实现

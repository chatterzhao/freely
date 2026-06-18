---
local_id: raw-20260618T094846Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2988'
    url: https://github.com/chatterzhao/freely/issues/2988
    synced_at: ''
primary_platform: github
canonical_issue_path: 'raw-20260618T094846Z'
absorbed_into: 'raw-20260618T094846Z'
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T09:49:02Z'
updated_at: '2026-06-18T09:49:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标

重绘 `docs/system/workspace/three-loop-lifecycle.svg`，使其完全符合当前项目实现，补全当前 SVG 缺失的五个架构层。

## 当前 SVG 的问题

当前 SVG 只画了三个 Loop 的 gate 序列（intake→routing→dispatch→test→pr-create→PR review→pr-merge→closeout），但完全缺失了让这个流程运转起来的核心架构层：

### 缺失 1：ACP 协议层
- `acp-bridge.py`：JSON-RPC 桥接守护进程，stdio ↔ Unix socket
- `run-acp-prompt.py`：ACP 客户端，四种启动类型
- 三级会话缓存：session/resume (L1 零成本) → session/new 同 prompt (L2 增量) → session/new 异 prompt (L3 全量)
- 启动类型决策：fresh / resume / fork / prompt
- `select_launch_kind` 决策树
- `ensure_runtime_tool_session_anchor` 会话锚定

### 缺失 2：A2A 协议层
- `a2a_server.py`：Starlette+Uvicorn，Unix socket，TaskStore (SQLite)
- `a2a_task.py`：CLI 客户端，a2a-exit / tasks/list / tasks/update
- Task 状态机：submitted → working → completed / failed / input-required
- SSE 推送：TaskStatusUpdateEvent → Manager 感知 Worker 完成
- Manager→Worker 委派全链路 14 步时序

### 缺失 3：Agent 角色层
- Manager Agent：运行在 develop worktree，18 个 M 类 skill，巡逻→scan→判断→委派
- Worker Agent：运行在 feature/fix worktree，8 个 W 类 skill，接收 intent_kind → 执行
- Manager prompt 组装：start-lead-agent.sh → manager-agent.md
- Worker prompt 组装：Task.message → prompt file → worker-agent.md
- 出口合同：stop_ai / delegate_workers / resume_manager / manager_working

### 缺失 4：Skill 路由层
- auto-loop-orchestrator → context-source-skill → 判断 discovery/milestone/continuation → target_skill
- 33 个 skill 的 A/M/W 三层分发
- feat-execution / fix-execution 作为组合 skill 串联子 skill
- 各 gate 对应的 skill（B1→doc-B1_IBM-execution，B2→doc-B2_IBM-execution，dev→dev-loop-execution）

### 缺失 5：Runtime 执行层
- Supervisor 主循环：while true { scan → build_prompt → select_launch_kind → monitor → exit_contract → delegate → sleep }
- Task mode gate：auto / wait / listen 三种模式的循环行为
- scan 机制：task-lifecycle-scan.py → CHAIN_ACTIONS 字典 → next_action 字段
- AI CLI Tool 层：opencode / cc / codex / iflow / kiro，经 registry 进入 ACP family
- 提示组装：build_prompt → start-lead-agent.sh → agent 角色 + 治理 + 上下文源 + 执行规则

## 新 SVG 设计方案

### 布局：五层架构 + 三 Loop 泳道

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1: auto-loop (Manager on develop)                     │
│  intake→routing→dispatch→test→pr-create→PR review→pr-merge→closeout │
│  [scan] [feedback+wt-create] [delegate] [test-pre-merge] ... │
├────────────────────────┬─────────────────────────────────────┤
│  Layer 2a: doc-loop    │  Layer 2b: dev-loop                  │
│  (Worker on feature/*) │  (Worker on feature/*)              │
│  B1_IBM → B2_IBM       │  implement → evidence               │
├────────────────────────┴─────────────────────────────────────┤
│  Layer 3: Agent Roles + Skills                               │
│  Manager (18 skills) ──A2A delegate──▶ Worker (8 skills)     │
│  context-source-skill → target_skill → execution             │
├──────────────────────────────────────────────────────────────┤
│  Layer 4: ACP + A2A Protocols                                │
│  ACP: acp-bridge.py ←→ run-acp-prompt.py (session/*)         │
│  A2A: a2a_server.py ←→ a2a_task.py (Task lifecycle + SSE)    │
├──────────────────────────────────────────────────────────────┤
│  Layer 5: AI CLI Tools                                       │
│  opencode / cc / codex / iflow / kiro                        │
│  adapter: acp (current product working mode)                 │
└──────────────────────────────────────────────────────────────┘
```

### 新增元素清单

1. **ACP 会话流**：在 Manager/Worker 与 AI CLI Tool 之间标注 ACP JSON-RPC（session/new, /resume, /prompt, stopReason）
2. **A2A 委派流**：Manager → a2a-exit → A2A Server → tasks/list → Worker，带 Task 状态机
3. **Agent 角色框**：Manager（develop, M-skills）和 Worker（feature/*, W-skills），标注技能集
4. **Skill 路由**：context-source-skill 的分支（discovery→doc-B1, milestone→doc-B2, continuation→dev-loop）
5. **Runtime 循环**：Supervisor while-true 循环 + task-mode gate
6. **AI CLI Tool 层**：底部工具矩阵，标注 canonical ACP 接入
7. **出口合同**：三个出口（stop_ai→停止, delegate_workers→启动Worker, resume_manager→继续巡逻）
8. **图例**：协议颜色约定（ACP=蓝, A2A=绿, Runtime=灰, Skill=紫）

### 尺寸

保持 1400×900 或适当扩展高度以容纳新增层。

## 影响文件

- `docs/system/workspace/three-loop-lifecycle.svg`：重绘
- `docs/system/workspace/three-loop-capability-lifecycle.md`：可能需要同步更新文字描述（另开 issue）

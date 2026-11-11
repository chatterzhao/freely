---
schema_version: '1'
local_id: raw-20261104T075903Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T075903Z-A
platform_ids:
  github:
    issue_id: '4162'
    url: https://github.com/chatterzhao/freely/issues/4162
    synced_at: ''
  gitee:
    issue_id: IKSW95
    url: https://gitee.com/zhaoquan/freely/issues/IKSW95
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/issues/I-20261104T075903Z-A.md
last_synced_comment_at:
  github: '2026-11-11T09:45:23Z'
  gitee: '2026-11-11T09:45:23Z'
hash: ''
created_at: '2026-11-04T07:59:03Z'
updated_at: '2026-11-11T10:04:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T075903Z-A
source_candidate: ''
completed_at: '2026-11-11T09:45:22Z'
closeout_note: ''
---

# refactor: 收口 agent 协调的协议、状态机与路由决策

workflow_kind: feature

## 根因
协调语义分散在 6 处：协议类型、客户端、路由/订阅、决策逻辑、理由枚举、角色真相。改一个协调行为需要跨 6+ 文件，外部项目无法只替换协调实现。

## 证据
- 协议类型：`runtime/a2a/a2a_types.py`（435 行）+ `runtime/a2a/a2a_server.py`（920 行）。
- 客户端：`runtime/a2a_task.py`（1,165 行）。
- 路由/订阅：`runtime/watchdog_sse.py`（562 行）。
- 决策逻辑：`runtime/freely` 的 `manager_exit_contract_kind`。
- 理由枚举：`docs/system/workspace/agents/input_required_reason.py`，靠 `watchdog_sse.py:16` 的 `sys.path.insert` 才能 import。
- 角色真相：`agents/agent-roles.toml`（技能）与 `.freely/agent-table.toml`（槽位/pool）。

## 影响
- 新增一个 input-required reason 或换通知机制需要改 6 处，任一处漏改即静默漂移。
- `sys.path` hack 让 import 关系不可静态分析。
- 协调语义无法单点演进，也无法被外部项目替换。

## 修复方案
1. 建 `contracts/coordination/`：Task 状态机、input-required reasons、SSE topics、exit contract 映射各一份机器可读定义。
2. 建 `scripts/coordination/`：server/client/router/决策单一实现；`runtime/freely` 只做读取-决策-调用。
3. `input_required_reason.py` 迁出 `agents/`，消除 `sys.path.insert`。
4. 角色配置明确边界，并用同一 schema 校验。
5. 加 import 图检查：`scripts/coordination/` 不得反向 import `runtime/freely`。

## 验收标准
- GREEN：`grep -rn "sys.path.insert.*agents"` 为 0。
- GREEN：新增一个 input-required reason 只需改契约 + 一处映射，diff 文件数 ≤2。
- GREEN：`scripts/coordination/` 的 import 图无环、无反向依赖。
- GREEN：协调契约有单页文档，列出状态机与 exit contract 的合法值。

### comment-20261111T094522Z
- source: system
- event: promote_finalized
- children: ["I-20261104T075903Z-A"]

拆解为以下任务:
1. [I-20261104T075903Z-A](will-be-updated)

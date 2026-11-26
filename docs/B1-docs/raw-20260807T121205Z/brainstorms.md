---
b1_id: B1-20260807T121205Z
phase_state: completed
source_raw: raw-20260807T121205Z
source_url: https://github.com/chatterzhao/freely/issues/4109
produced_candidate: C-20260807T121205Z-A
created_at: 2026-11-26
---

# B1_IBM: reviewer assign FAIL-CLOSED missing raw_key in SSE event

## 0. 设计意图审计（先于方案）

### B0 前置：关键词广搜 + 多文档交叉

- 关键词族表（≥3 组；搜 docs/ bin/ .freely/）:
  - 功能名 / 机制名: `needs-review:*` / `reviewer assign` / `FAIL-CLOSED` → `docs/system/workspace/scripts/runtime/coordination/input_required_reason.py`、`docs/system/workspace/scripts/runtime/watchdog_sse.py`、`docs/B1-docs/raw-20260807T121205Z/issue.md`
  - 字段名: `raw_key` / `metadata` / `state_update` → `docs/system/workspace/scripts/runtime/watchdog_sse.py:185-229`、`docs/system/workspace/scripts/runtime/a2a/a2a_server.py:779-803`、`docs/system/workspace/scripts/runtime/a2a_task.py:1136-1140`
  - 命令名: `a2a-exit` / `wt-create` → `docs/system/workspace/scripts/runtime/a2a_task.py:838-852`、`bin/freely`、`docs/system/workspace/scripts/runtime/freely:15909`
  - 门禁名 / raw key: `check-coordination-contract` / `test-coordination-contract.py` / `raw-20260807T121205Z` → `bin/check-coordination-contract`、`docs/system/workspace/scripts/tests/test-coordination-contract.py`、`docs/milestones.md`
- 怀疑多份文档: 是——`watchdog_sse.py` 当前实现、`a2a_server.py` PATCH 事件构造、raw issue 里记录的 2026-08-07 现场日志三处分别描述同一条 reviewer 路由链路；只看任何一份都会误判修复点。
- 三类分层表:
  - 当前生效实现: `docs/system/workspace/scripts/runtime/a2a_task.py`、`docs/system/workspace/scripts/runtime/a2a/a2a_server.py`、`docs/system/workspace/scripts/runtime/watchdog_sse.py`（权重：现状，本次修复对象）
  - 历史局部文档: `docs/B1-docs/raw-20260807T121205Z/issue.md` 的 Evidence 段（11:57-12:09Z 日志与 task id，权重：仅背景，不是当前代码证据）
  - 当前权威恢复点: `contracts/coordination/contract.yaml` + `docs/system/workspace/scripts/runtime/coordination/input_required_reason.py`（权重：reason 枚举与 SSE topic 的单一真源）
- 矛盾清单: `contracts/coordination/contract.yaml` 只列出 `needs-worker-retry` 等 reason 与 `input_required`/`task_state_update` 等 topic，未对 `needs-review:*` SSE 事件要求 `raw_key`；而 `watchdog_sse.py:229` 又把缺失 `raw_key` 定为 FAIL-CLOSED。契约的沉默与运行时的硬失败冲突——这不是「契约已覆盖 reviewer 失败路径」，恰恰是本轮要补的缺口。
- 二元决策: **继续**（附方向）——在 `a2a_task.py` 的 a2a-exit 更新路径把 `raw_key` 带入 PATCH，使 `state_update` SSE 事件携带它；对确实无法解析 `raw_key` 的 needs-review 转换 fail-closed 拒绝。不做 dropped：无其他 issue / 实现覆盖此失败路径。

### 外部锚点（引用原文，至少两类）

- 设计文档 / 契约: `contracts/coordination/contract.yaml:8`「"sse_topics": "watchdog_sse.py / a2a_server.py SSE event names"」——SSE 事件形状的契约真源在 watchdog 与 server，二者必须一致。
- 既有验收测试（必须拒绝类断言）: `docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py:63-64`「"test-a2a-task-cli-loadable" in aggregate_text」——既有 AT 用「测试必须被接进 bin/test-all」钉住回归防线，本轮沿用同一模式。
- 门禁源码注释 / 理由: `docs/system/workspace/scripts/runtime/watchdog_sse.py:229`「FAIL-CLOSED: missing raw_key for reviewer assign」——fallback 必须拒绝，不能因为方便就 fail-open。
- 既有同类实现: `docs/system/workspace/scripts/runtime/a2a_task.py:1143-1156` 新 worker task 路径已经强制 `--raw-key` 等必填字段；更新路径应沿用同一「必填字段 fail-closed」语义。
- 配置约束: `docs/system/workspace/scripts/runtime/coordination/input_required_reason.py:9`「# Worker → Reviewer (per-step review)」——`needs-review:*` 是明确的 reviewer 路由，不是 manager 兜底。

- 判定（五选一，必须给证据）: **bug**——`a2a_task.py:1136-1140` 的 update 调用漏传 `raw_key`，导致 SSE 事件无 `raw_key`，`watchdog_sse.py:229` 必然 FAIL-CLOSED；代码与契约意图不一致，不是设计错误。
- 与既有断言的冲突: 无。保留 `watchdog_sse.py` 的 FAIL-CLOSED 断言不动，只在更上游让合法 `raw_key` 被发出；AT 同时断言「缺失仍被拒绝」。
- 影响面: `docs/system/workspace/scripts/runtime/a2a_task.py`（实现）、`docs/system/workspace/scripts/tests/`（AT）、`bin/test-all`（CORE + CI_CORE 注册）、`contracts/coordination/contract.yaml`（不改，但作为 L0 锚点被核对）。

## 0.1 全局适配反思（四问）

- Q1 类别: 治理元数据修复（流程能力边界内的 runtime 字段传播 bug），不是生命周期变更或副本传播。
- Q2 职责边界: `a2a-exit` 拥有「状态转换字段」的最终判定，`a2a_server.py` 负责把字段广播为 SSE，`watchdog_sse.py` 负责消费并 fail-closed；本轮只修字段的生产端，不夺走下游职责。
- Q3 结构性冲突: 按字面实现不会要求「每个文档一个工位」或「每次同步都走 IBM」；修复局限在单次 CLI 更新调用。
- Q4 门禁失配: 现有门禁测的是 reason 枚举 / SSE topic 存在性（`bin/check-coordination-contract`），本轮缺陷是事件**字段**缺失；两者维度不一致 → 用 AT 钉住字段级判据（缺失拒绝 + 合法发出），不放宽也不绕过既有门禁。

## Input

- 来源: GitHub #4109 / Gitee IK78A5，raw key `20260807T121205Z`，workflow_kind=fix。
- 现象: worker 逐阶段 `a2a-exit --state input-required --reason needs-review:<phase>` 后 reviewer 池 busy=0，阶段审查被静默绕过。

## Problem

- 根因链: `a2a_task.py` a2a-exit 更新分支只发 state/summary/next/evidence/reason → `a2a_server.py` PATCH 只把 body 里的字段塞进 SSE → `watchdog_sse.py` 读不到 `metadata["raw_key"]` → line 229 FAIL-CLOSED → reviewer 永不分配。
- 影响: B1/B2/RED/dev/test 阶段审查全部缺失，未审查工作可流到 PR/merge。

## Brainstorm

### Option A: 在 a2a_task.py a2a-exit 更新路径补 raw_key

- 从 `--raw-key` 参数解析；参数缺省时用 `task_id` 回读任务记录取 `raw_key`；needs-review 且两者皆空则 fail-closed 拒绝并输出 `ok:false`。
- 优点：修复点即根因点，一处改动，下游零变更；fail-closed 语义与既有新任务必填校验一致。
- 缺点：只覆盖走本 CLI 的调用方；其他直接 PATCH 的调用方仍需各自保证字段。

### Option B: 在 watchdog_sse.py 用 task_id 回查 raw_key

- 优点：兜底所有 SSE 生产方。
- 缺点：把字段修复推到消费端，产生第二套 raw_key 解析真源；且 watchdog 侧无法阻止事件继续被其他消费者误用；不符合「单一真源」。

### Option C: 在 a2a_server.py PATCH handler 用 task store 补 raw_key

- 优点：服务端统一补齐，覆盖所有调用方。
- 缺点：`a2a_server.py` 依赖 a2a SDK，AT 无法在裸环境导入，测试成本高；且服务端补字段与已存在的「调用方必须声明必填字段」契约语义重复。

## Decision: Option A

- 理由：根因在 a2a-exit 更新调用漏字段；Option A 是最小、fail-closed、可独立 AT 验证的修复，且不引入第二套真源。
- 不做 B/C：B 会在消费端再造解析逻辑；C 虽更泛化但测试环境与真源边界成本更高，留作后续架构债，不夹带进本 fix。

## Candidate

- candidate_id: C-20260807T121205Z-A
- status: promoted
- milestone: M-20260807T121205Z-A

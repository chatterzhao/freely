---
b1_id: B1-20261126T114403Z
phase_state: completed
source_raw: raw-20261126T114403Z
source_url: https://github.com/chatterzhao/freely/issues/4722
produced_candidate: C-20261126T114403Z-A
created_at: 2026-11-26
---

# B1_IBM: close-orphans 批量模式复用平台读取

## 0. 设计意图审计（先于方案）
### B0 前置：关键词广搜 + 多文档交叉
- 关键词族表（≥3 组；搜 docs/ bin/ .freely/）:
  - 功能名：`close-orphans` / `close-local-id` → `bin/issue-sync.d/cmd-close.sh:132`、`docs/system/workspace/scripts/sync/platform-adapter.py:1304`
  - 机制名：`list_open_issue_records` / `find_open_replicas_by_local_id` / `replica_truth.summarize` → `platform-adapter.py:1279-1301`、`lifecycle/replica_truth.py:106`
  - 命令名：`issue-sync batch` / `issue-sync scan` → `bin/issue-sync.d/cmd-batch.sh`、`cmd-scan.sh`
  - 历史 raw key：`20261124T131119Z`（#4687 引入 close-orphans）→ `docs/B1-docs/raw-20261124T131119Z/issue.md`
- 怀疑多份文档: 是——显式列出「当前实现 / 历史局部 / 过期废弃 / 权威恢复点」
- 三类分层表:
  - 当前生效实现: `bin/issue-sync.d/cmd-close.sh:cmd_close_orphans`（逐 id 委托 adapter `close-local-id`，每次全量重扫）— 权重：现状
  - 历史局部文档: `docs/B1-docs/raw-20261124T131119Z/issue.md`（#4687 立项时只需关闭单条 stale 副本，无批量场景）— 权重：仅背景
  - 当前权威恢复点: `docs/system/workspace/scripts/sync/platform-adapter.py:close_local_id()` + `lifecycle/replica_truth.py:summarize()` — 权重：当前真相（副本判据单一来源）
- 矛盾清单: #4687 的文档承诺「关闭全部副本」，而当前调用模型使「全部」只对单个 local_id 成立；治理清理需要对 N 个 id 全部关闭，却只能重复 N 次平台全量读取，二者不在同一抽象层。
- 二元决策: **继续**（按项目意图补齐批量入口，保留单 id 入口与全部判据）。

### 外部锚点（引用原文，至少两类）
- 设计文档: `docs/system/workspace/commands.md:263`「`close-orphans <local_id> [linked|raw]` | 按 local_id 关闭全部平台副本（含 stale linked 孤儿），逐平台汇总；失败非零并打印重试命令」——命令契约已存在，缺的是批量维度。
- 既有验收测试: `docs/system/workspace/scripts/tests/test-close-orphans-command.py:59-63`「dispatcher registers close-orphans」「retry command is actionable」——测试覆盖单 id 语义，未覆盖 N id 复用读取。
- 门禁源码注释/理由: `platform-adapter.py:1308`「`close_issue`/`close-multi` only close ids listed in the document's `platform_ids` … This resolver unions the platform truth with the document mapping, so the retirement step and the gate agree on the same set.」——副本真源必须在 adapter，批量模式不得另造判据。
- 既有同类实现: `bin/issue-sync.d/cmd-batch.sh` 一次扫描批量处理多个 local_id，证明「一次读取 + 多 id 处理」符合本项目命令结构。
- 实测证据: 本会话 P1-3 运营，48 个 linked id 逐条调用，每条 60–90 秒；Gitee 抖动产生 rc=3 部分成功（`I-20260708T185138Z-A` 需重试）。

- 判定（五选一，必须给证据）: **实现未完成**（命令契约与 adapter 真源都已具备，缺批量编排层；不是设计错误，也不是门禁强度问题）。
- 与既有断言的冲突: 无。批量模式是新增 flag，不改 `close-orphans <local_id>` 既有签名与语义。
- 影响面: `bin/issue-sync.d/cmd-close.sh`、`bin/issue-sync` dispatcher、`docs/system/workspace/commands.md`、新增 AT；不改 `platform-adapter.py` 的副本判据。

## 0.1 全局适配反思（四问）
- Q1 类别: 流程能力（治理清理的吞吐与可操作性），不是生命周期变更。
- Q2 职责边界: adapter 拥有「哪些副本属于 id」的判定；命令层只负责编排与汇总。批量模式仍委托 adapter，不得自己拼 `platform_ids` 或直连平台。
- Q3 结构性冲突: 若批量模式自行推导 terminal 判据会产生第二套语义 → 必须复用本地 `phase_state ∈ {completed, dropped}` 的既有终态集合，与 `issue-sync batch` 一致。
- Q4 门禁失配: 现有 AT 测的是「单 id 关闭是否全平台覆盖」；本轮新增维度是「平台读取次数」与「多 id 汇总」。需新增 AT 而非放宽既有 AT。

## Input
- raw-20261126T114403Z / GitHub #4722 / Gitee IKY9I7，P2 feature。
- 现场：P1-3 批量清理 48 个 orphan id，逐 id 全平台重扫。

## Problem
- `cmd_close_orphans()` 每次调用都触发 `list_open_issue_records()` 全量拉取 GitHub+Gitee OPEN issue；平台读取次数 O(N)，运营耗时不可接受，且提高 Gitee 抖动命中率。

## Brainstorm
### Option A: 在 adapter 增加 `close_local_ids(ids, records)`，命令层一次读取后批量委托
- 优点：平台读取一次；判据仍归 adapter；可在 adapter 层做统一错误汇总。
- 缺点：adapter 公开接口扩大，需要兼容 `close-local-id` CLI 既有调用。

### Option B: 在命令层缓存 records，循环调用现有 `close_local_id(local_id, platform_ids, reason, kind, records=...)`
- 优点：改动面小；adapter 仍拥有判据（只把 records 作为参数注入）；单 id 路径零变化。
- 缺点：需要给 adapter CLI 增加可选 records 文件或 stdin 输入，避免每次进程重新启动导致缓存失效。

## Decision: Option B
- 理由：最小改动保持 adapter 为副本判据唯一真源；单 id CLI 行为逐字不变；进程内批量调用可共享一次平台读取。
- 实现要点：adapter 增 `read-open-records` 只读子命令输出 JSON（或 `close-local-ids` 批量子命令接收 id 列表），命令层 `--all-completed` 先读取一次 records，再对每个 terminal id 复用同一份 records 关闭。

## Candidate
- candidate_id: C-20261126T114403Z-A
- status: promoted
- milestone: M-20261126T114403Z-A

---
schema_version: '1'
local_id: raw-20261110T064015Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T064015Z-A
platform_ids:
  github:
    issue_id: '4254'
    url: https://github.com/chatterzhao/freely/issues/4254
    synced_at: ''
  gitee:
    issue_id: IKUA5K
    url: https://gitee.com/zhaoquan/freely/issues/IKUA5K
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T064015Z/issues/I-20261110T064015Z-A.md
last_synced_comment_at:
  github: '2026-11-10T10:55:21Z'
  gitee: '2026-11-10T10:55:21Z'
hash: ''
created_at: '2026-11-10T06:40:15Z'
updated_at: '2026-11-10T10:55:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T064015Z-A
source_candidate: ''
completed_at: '2026-11-10T10:55:20Z'
closeout_note: ''
severity: P1
---

# fix: 派发 CAS 幂等 + SSE watcher 单实例与 pid 互斥

workflow_kind: fix

workflow_kind: fix

## 来源
从 #4239 / IKU0CC（并发收口二）拆分。原 issue 三面，本轮已完成「`pkill -f` 项目路径正则转义」；本条承接剩余两面。scope 收敛理由同 R22（4 面做 2 面拆 #4246）与 R23.5（3 面做 2 面拆 #4252）：状态机与守护进程链路的改动需要独立真源普查与端到端验证，不能与「行为不变」的转义修复混在一个 PR。

## 问题 1：派发非幂等（两条派发器）
- 取 `submitted` → 先启动 worker → 再 `update --state working ... || true`（无事务、无租约，失败被吞）。崩溃后下一轮可能重复拉起第二个 worker。
- 同一队列存在第二个派发器，两条守卫强度不一致。
- 修复方向：启动前 CAS 抢占 `update --state launching --claimed-by <pid>`，抢占失败即跳过；删掉较弱的派发器。

## 问题 2：SSE 三重实例 + watch-in-watch
- `launch_sse_watchdog` + `_start_watchdog_sse_py` + 外层 `while true` 包内层 `while true`（后者死代码）。
- 两个消费者同时向 manager 注入同一条 `state_update`；`sse-watchdog.sh` 写 pid 无互斥。
- 修复方向：只保留一条链路，删死代码，pid 写入加互斥。

## 必须先重新做真源普查（重要）
issue 正文行号已漂移：在 develop `d82ba3e46` 上
- `grep -n "launch_sse_watchdog\|_start_watchdog_sse_py" docs/system/workspace/scripts/runtime/freely` **零命中**；
- `grep -n -- "--state working\|--status working\|launching" docs/system/workspace/scripts/runtime/freely` **零命中**；
- R23.5（#4246）刚改过 `consume_delegate_workers` 的派发管线（TSV → JSON Lines + NUL 流），派发状态机可能已迁移到 `a2a_task.py` / `consume_worker_tasks.py` / `decode_worker_tasks.py`。
**不要照 issue 正文的旧行号改代码**，先在最新 develop 上定位真实调用点再设计 RED。

## 验收标准
- RED：并发两次派发同一 `submitted` 任务 → 两个 worker 都被拉起（隔离夹具，不派发真实 agent）；修复后只有一个拿到 `launching`。
- RED：SSE 链路在隔离夹具里出现两个消费者同时注入同一条 `state_update`；修复后只有一条。
- GREEN：CAS 抢占失败即跳过；同队列只剩一个派发器调用点。
- GREEN：watch-in-watch 死代码删除，pid 写入有互斥（可用 `flock`，#4155 已建立项目范式）。
- GREEN：现有 `test-freely-*manager-worker-launch*` / SSE 相关回归基线对比 0 新增失败。

## 不退化边界
- 不改 R23.5 建立的 JSON Lines / NUL 流派发契约。
- 不改 R19（#4155）的启动锁与 DB 单实例实现。
- 不删 `sse-watchdog.sh` 的既有事件语义，只收敛实例数与 pid 写入。
- 并发夹具不得访问真实平台、不得杀本机进程。

## 明确不纳入
- 启动锁与 DB 单实例（#4155 已完成）。
- `pkill -f` 正则转义（本轮已完成）。
- 修 `pr-merge-guarded` 收尾 `unknown: origin` 噪音（#4136 覆盖）。

## 证伪
#4155 / R19（已合并）只做启动锁 TOCTOU 与 DB daemon 双实例；#4239（本轮）只做 pkill 转义；#4246 / R23.5（已合并）只做派发数据格式，不改状态机；#4157 / R25 是 watchdog 与日志可观测性，均不覆盖派发 CAS 与 SSE 实例收敛。

### comment-20261110T105521Z
- source: system
- event: promote_finalized
- children: ["I-20261110T064015Z-A"]

拆解为以下任务:
1. [I-20261110T064015Z-A](will-be-updated)

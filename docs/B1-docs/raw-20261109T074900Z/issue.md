---
schema_version: '1'
local_id: raw-20261109T074900Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261109T074900Z-A
platform_ids:
  github:
    issue_id: '4239'
    url: https://github.com/chatterzhao/freely/issues/4239
    synced_at: ''
  gitee:
    issue_id: IKU0CC
    url: https://gitee.com/zhaoquan/freely/issues/IKU0CC
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/issues/I-20261109T074900Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-09T07:49:00Z'
updated_at: '2026-11-10T06:48:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261109T074900Z-A
source_candidate: docs/B1-docs/raw-20261109T074900Z/candidates.md
completed_at: '2026-11-10T06:44:21Z'
closeout_note: ''
---

# fix: 派发非幂等 + SSE 三重实例 + pkill 未转义（并发收口二）

workflow_kind: fix

## 背景

从 #4155 / IKSPQC（启动锁与 DB 单实例）拆分而来。原 issue 列了 5 个并发安全面，其中「启动锁 TOCTOU」「DB daemon 双实例」后果最重（控制面分裂 / 全项目 DB 不可用），已在 #4155 本轮收口；本 issue 承接其余三个正交面。

## 问题 1：派发非幂等（两条派发器）

- 取 `submitted` → **先启动 worker** → 再 `update --state working ... || true`（无事务、无租约，失败被吞）。崩溃后下一轮会重复拉起第二个 worker。
- 同一队列还存在第二个派发器（TSV 通道，带 `worktree_has_active_worker` 闸），两条派发器守卫强度不一致。

修复方向：改为「启动前 CAS 抢占」——`update --state launching --claimed-by <pid>`，抢占失败即跳过；两条派发器删掉较弱的一条。

## 问题 2：SSE 三重实例 + watch-in-watch

- `launch_sse_watchdog` + `_start_watchdog_sse_py` + 外层 `while true` 包内层 `while true`（后者是死代码）。
- 两个消费者同时向 manager 注入同一条 `state_update`；`sse-watchdog.sh` 写 pid 无互斥。

修复方向：只保留一条链路，删死代码，pid 写入加互斥。

## 问题 3：`pkill -f` 前未转义项目路径

`freely` 内 5 处 `pkill -f`，其中 `:8913` / `:22238` 直接把 `${project}` 拼进正则，项目路径含正则元字符时会误杀同前缀的其他项目进程。与 #4156 同族。

修复方向：拼进正则前做转义（或改用 `pgrep -f` 精确匹配 + 显式排除自身）。

## 验收标准

- RED：并发两次派发同一 `submitted` 任务 → 当前可拉起两个 worker；修复后只有一个拿到 `launching`。
- RED：项目路径含 `.` / `+` 等正则元字符时，`pkill -f` 当前会匹配到同前缀的其他项目进程。
- GREEN：派发改为启动前 CAS，抢占失败即跳过；同队列只剩一个派发器调用点。
- GREEN：SSE 只保留一条链路，watch-in-watch 死代码删除，pid 写入有互斥。
- GREEN：`pkill -f` 前对项目路径做正则转义，且有反向断言（含元字符时不会误杀）。

## 不做

启动锁与 DB 单实例（已在 #4155 收口）。

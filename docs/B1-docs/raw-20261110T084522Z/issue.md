---
schema_version: '1'
local_id: raw-20261110T084522Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T084522Z-A
platform_ids:
  github:
    issue_id: '4264'
    url: https://github.com/chatterzhao/freely/issues/4264
    synced_at: ''
  gitee:
    issue_id: IKUCGS
    url: https://gitee.com/zhaoquan/freely/issues/IKUCGS
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T084522Z/issues/I-20261110T084522Z-A.md
last_synced_comment_at:
  github: '2026-11-10T09:13:46Z'
  gitee: '2026-11-10T09:13:46Z'
hash: ''
created_at: '2026-11-10T08:45:23Z'
updated_at: '2026-11-10T09:13:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T084522Z-A
source_candidate: ''
completed_at: '2026-11-10T09:13:45Z'
closeout_note: ''
severity: P1
---

# fix: 状态协议 ALLOWED_KEYS 漏登记 21 个 heredoc 写入键（兼容读取会抛错）

workflow_kind: fix

## 背景

R23.9 / #4252 交付了 `runtime/state_file.py`，其 `ALLOWED_KEYS` 注释声称：

> Whitelist derived from a full scan of the state write sites in `runtime/freely` (develop ea9f5b38c)

R23.12（本轮）做逐族迁移的真源普查时发现：**这个「全量扫描」漏掉了所有用 heredoc 写入的状态键**。

## 实测证据（develop `9038a2547`）

用「`cat >*.env <<EOF` 块内 `KEY=` 行 + `printf 'KEY=%s'` 模板」重新扫描，得到 90 个写入键，与 `ALLOWED_KEYS` 的 77 个比对，**21 个键未登记**：

```
ACTIVE_RUNNING_WORKER_COUNT          AVAILABLE_NEW_WORKER_SLOTS
LAST_MANAGER_CONTINUITY_CONSUMED    LAST_MANAGER_CONTINUITY_GENERATED
LAST_MANAGER_WORKER_PROMPTS_CONSUMED LAST_MANAGER_WORKER_PROMPTS_GENERATED
LAST_PREEMPTION_AT                  LAST_PREEMPTION_INTAKE_ID
LAST_PREEMPTION_MODE                LAST_PREEMPTION_PID
LAST_PREEMPTION_REASON              LAST_TESTED_AT
LAST_TESTED_COMMIT                  LAUNCHED_WORKER_PROMPTS
LOOP_GUARD_L1_STRIKES               LOOP_GUARD_L2_START_TIME
MAX_PARALLEL_WORKERS                QUEUED_WORKER_PROMPTS
QUEUED_WORKER_PROMPT_BLOCKERS       TEST_STATUS
UPDATED_AT
```

后果不是「写不了新格式」，而是**兼容读取承诺直接失效**：

```python
p.write_text('LAST_MANAGER_CONTINUITY_GENERATED="/a/b"\nQUEUED_WORKER_PROMPTS="x,y"\n')
state_file.read_state(p)
# -> StateFileError: unknown state key: 'LAST_MANAGER_CONTINUITY_GENERATED'
state_file.write_state(p, {...})
# -> StateFileError: unknown state key: ...
```

`read_state` 对每一行（含 legacy `KEY=value`）都调 `_check_key`，因此任何含未登记键的**存量**状态文件，一旦被迁到协议的族读取，就会整份抛错；`values` 的失败在 shell 侧被 `|| true` 吞掉 → 值静默回落到默认值。这比报错更危险：状态在迁移那一刻悄悄丢失。

## 为什么单独立项（不夹带 R23.12）

- R23.12 本轮迁的是 `execution-network-recovery.env`（4 个键全在白名单），不受此缺陷影响，可以独立验证。
- 该缺陷会阻塞**后续**族：`manager_worker_launch_state_file`（11 键）、`_loop_guard_*`（2 键）、test-gate 状态（2 键）等迁移时都会撞上。
- 修法与「逐族迁移」正交：改的是协议真源 + 扫描器，不是某个调用点。

## 修复方案

1. 把 21 个键补进 `ALLOWED_KEYS`（保留按字典序分组），并把注释从「full scan」改成准确描述。
2. 新增 `bin/check-state-file-keys`（或并入 `check-state-file-sources`）：**自动**从 `freely` 的 heredoc / printf 写入点抽取键集合，与 `ALLOWED_KEYS` 求差集，非空即失败。这样扫描器本身就是契约，不再依赖人工「全量」声明。
3. 白名单只增不减：新增状态键必须显式登记，删键必须先确认无写入点。
4. 不动 `read_state` / `write_state` 的拒绝语义（未知键仍应拒绝 —— 这是防止拼错静默产生新状态的护栏）。

## 验收标准

- RED：在 develop 上跑新 lint，`missing keys = 21`；用 `read_state` 读一个含 `LAST_MANAGER_CONTINUITY_GENERATED` 的 legacy 文件 → 抛 `StateFileError`。
- GREEN：lint 差集为空；21 个键的 legacy 文件与 TAB+JSON 文件都能 `read_state` / `write_state`，值逐字节相等。
- GREEN：反向守护 —— 一个**未登记**的伪造键仍被拒绝。
- GREEN：AT 覆盖「heredoc 抽取」与「printf 模板抽取」两种写入形态，防止扫描器本身漏判。
- GREEN：`bin/test-all --ci` 与 R23.9/R23.11/R23.12 的状态族 AT 全绿。

## 不做

- 不迁任何调用点（那是 R23.12 及后续族的工作）。
- 不放宽未知键拒绝语义。
- 不删除既有状态文件。

### comment-20261110T091346Z
- source: system
- event: promote_finalized
- children: ["I-20261110T084522Z-A"]

拆解为以下任务:
1. [I-20261110T084522Z-A](will-be-updated)

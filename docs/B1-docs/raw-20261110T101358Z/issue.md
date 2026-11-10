---
schema_version: '1'
local_id: raw-20261110T101358Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T101358Z-A
platform_ids:
  github:
    issue_id: '4272'
    url: https://github.com/chatterzhao/freely/issues/4272
    synced_at: ''
  gitee:
    issue_id: IKUDWN
    url: https://gitee.com/zhaoquan/freely/issues/IKUDWN
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T101358Z/issues/I-20261110T101358Z-A.md
last_synced_comment_at:
  github: '2026-11-10T10:24:33Z'
  gitee: '2026-11-10T10:24:33Z'
hash: ''
created_at: '2026-11-10T10:13:59Z'
updated_at: '2026-11-10T10:24:39Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T101358Z-A
source_candidate: ''
completed_at: '2026-11-10T10:24:32Z'
closeout_note: ''
severity: P0
---

# fix: a2a_task.py 顶层前向引用标注导致模块加载即 NameError（派发链路静默停摆）

workflow_kind: fix

## 背景

R23.10（#4254，派发 CAS 幂等 + SSE 实例收敛）做真源普查时发现：`runtime/a2a_task.py` **整个模块无法被 Python 加载**，因此派发链路里所有 `python3 "$_a2a_task_py" ... || true` 调用全部静默失败。

## 实测证据（develop `ab86c1b16`，Python 3.13.12）

```
$ python3 docs/system/workspace/scripts/runtime/a2a_task.py list --role worker --status submitted
Traceback (most recent call last):
  File ".../a2a_task.py", line 435, in <module>
    def _sse_pool() -> SSEPool:
                       ^^^^^^^
NameError: name 'SSEPool' is not defined
```

- `a2a_task.py:435` 用 `SSEPool` 作返回类型标注，但 `class SSEPool` 在 `:446` 才定义；
- 文件头**没有** `from __future__ import annotations`，Python 3.13 会在定义时求值标注 → 导入即失败；
- 全文件只此一处前向引用标注；
- `git diff develop -- a2a_task.py` 为空，说明是 develop 现状而非工位改动。

## 影响（比 #4254 更基础）

`runtime/freely::manager_runtime_launch_workers`（约 `:14130-14310`）的整条派发管线依赖该 CLI：

```
a2a_task.py list --role worker --status submitted 2>/dev/null
  | consume_worker_tasks.py | decode_worker_tasks.py > stream || true
```

以及 `latest-manager` / `latest-completed-worker` / `active-workers` / `insert` / `update`。模块加载失败时：

- `list ... 2>/dev/null || true` 产出空流 → 被当作「没有待派发任务」，**所有 worker 派发静默停摆**；
- `insert` / `update` 同样失败并被 `|| true` 吞掉 → handoff record 与 A2A 状态都不推进；
- 诊断被 `2>/dev/null` 与 `|| true` 双重掩盖，运维只能看到「没有任务」，看不到根因。

同类问题在 #4246 已修过一次（TSV 通道的 `except: pass` 让畸形输入表现为「没有待派发任务」），这次是 CLI 级失败被 shell 吞掉。**失败语义与可观测性**属同一族（R25 / #4157 是 watchdog 与日志可观测性，不覆盖本条）。

此外：`bin/test-all --ci` 全绿却没发现，说明**没有任何测试真正执行 `a2a_task.py` 的 CLI 入口**（`grep -rln a2a_task.py tests/` 只有 `test-reviewer-contract.py` 引用到文件名）。这也是「核心 runtime 变更缺 TDD 证据链」（R27 / #4165）的一个具体实例，但本条只修可加载性与最小冒烟。

## 为什么单独立项（不夹带 R23.10）

- 修的是「CLI 能否运行」，#4254 修的是「派发是否幂等 / SSE 是否单实例」，两者正交；
- #4254 的 RED 夹具必须能真实调用 `a2a_task.py`，不先修就无法构造可信 RED；
- 改动极小（一行 import 或改标注），可独立 RED/GREEN 完整验证。

## 修复方案

1. 在 `a2a_task.py` 文件头加 `from __future__ import annotations`（**选中**：一行修复所有前向引用，不改变运行时行为，也不影响已定义的类）；或把 `:435` 标注改成引号 `'SSEPool'`。
2. 新增最小冒烟 AT：`python3 a2a_task.py list --role worker --status submitted` 能返回合法 JSON（在隔离临时项目 / 临时 DB 上，不碰真实 `.freely/freely.db`），且 `update --task-id <fake>` 返回明确的「task not found」而非 `NameError`。
3. 可选：`bin/test-all --ci` 纳入该冒烟，防止再次出现「全绿但 CLI 起不来」。
4. **不改**任何状态机语义、不改 `--state`/`--status` 参数、不改 SSEPool 实现。

## 验收标准

- RED：develop 上跑冒烟 → `NameError: name 'SSEPool' is not defined`，rc≠0。
- GREEN：同样命令返回合法 JSON（或明确业务错误），无 `NameError`；`import a2a_task` 成功。
- GREEN：反向守护 —— 已有的 `a2a_task.py` 单测/回归不退化（尤其 `test-reviewer-contract.py`）。
- GREEN：`bin/test-all --ci` 全绿；冒烟进入 CI 或明确记录为何不需要。
- GREEN：派发循环的 `list → consume → decode` 三段在隔离夹具里能串起来（不派发真实 agent、不访问平台）。

## 不做

- 不改派发状态机 / CAS（#4254）。
- 不改 SSE watchdog 实例数（#4254）。
- 不改 `2>/dev/null || true` 的容错语义（#4157 / R25 范畴）——本条只消除触发它的根因。
- 不清理历史 B1 文档。

### comment-20261110T102433Z
- source: system
- event: promote_finalized
- children: ["I-20261110T101358Z-A"]

拆解为以下任务:
1. [I-20261110T101358Z-A](will-be-updated)

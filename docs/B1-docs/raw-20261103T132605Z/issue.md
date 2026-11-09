---
schema_version: '1'
local_id: raw-20261103T132605Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132605Z-A
platform_ids:
  github:
    issue_id: '4153'
    url: https://github.com/chatterzhao/freely/issues/4153
    synced_at: ''
  gitee:
    issue_id: IKSPQ8
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ8
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132605Z/issues/I-20261103T132605Z-A.md
last_synced_comment_at:
  github: '2026-11-09T08:36:14Z'
  gitee: '2026-11-09T08:36:14Z'
hash: ''
created_at: '2026-11-03T13:26:05Z'
updated_at: '2026-11-09T08:40:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132605Z-A
source_candidate: ''
completed_at: '2026-11-09T08:36:13Z'
closeout_note: ''
---

# refactor: 消除 source 即死的顶层 exit

workflow_kind: feature

## 根因
26,823 行的 `runtime/freely` 同时是 daemon、调度循环、session 管理、平台客户端、TUI 与 prompt 模板，并且既当可执行入口又当被 `source` 的库；顶层 `set -euo pipefail` + 顶层 `exit 1` 让「引用即副作用、缺文件即整进程退出」。

## 证据
- 体量与豁免：`docs/system/workspace/scripts/runtime/freely:1-2` `# file-size: skip (legacy 20K line monolith, split pending)`（`wc -l` = 26,823）。
- 被 source：`manager-watchdog.sh:5`、`sse-watchdog.sh:14`、`interruption-manager-handler:6`、`governance-promotion-gate:6`；265 个文件引用该路径（含全部 `scripts/tests/*`）。
- source 即副作用：`freely:19` `set -euo pipefail`；`:30-36` `source docs/system/workspace/skills/freely-watchdog-control-plane/scripts/availability-watchdog.sh`，缺失则 `exit 1`；`:38-43` 第二个库同样 `exit 1`。`BASH_SOURCE` 守卫（`:26820`）只保护 `main`，不保护顶层 `exit`。
- 库函数内部 `exit`：`stop_project_runtime:21998-22008` 调 `acquire_project_start_lock_or_wait ... || exit 1`，被 `cmd_restart:24019`、`cmd_task_mode set:24329` 复用 → 锁超时直接终止整个命令。
- 重复定义：`ai_cli_bin_for_project` 在 `freely:18631` 与 `interruption-manager-handler:11` 各定义一次（后者覆盖前者）。
- skills 反向依赖运行时：控制面 source 了 skills 目录里 1,951 行 shell，与 README「skills 是给 agent 的知识，不是运行时」直接矛盾。

## 影响
缺一个库文件 → watchdog / dispatcher / promotion gate / supervisor 同时以 1 退出，supervisor 侧表现为「watchdog 起不来」，30 秒后把整个 daemon 拉停（`freely:19273-19286`、`:22832-22837`）。以及：任何控制面改动的影响面无法静态界定——改一个函数，265 个调用点语义都可能变。

## 修复方案（分三步，每步可独立合并）
1. 把 `freely:32-43` 的顶层 `exit 1` 改为 `return 1`（或设 `FREELY_LIB_LOAD_ERROR` 后 return），由 `main` 统一判断并退出；`BASH_SOURCE` 守卫范围扩到库加载段。
2. `availability-watchdog.sh` 从 `docs/system/workspace/skills/freely-watchdog-control-plane/scripts/` 搬到 `scripts/runtime/`，skills 回到纯知识。
3. 抽出 `lib/state.sh`（状态读写）、`lib/proc.sh`（进程/pid）、`lib/platform.sh`（平台）三个无 `set -e`、无顶层 `exit`、无副作用 import 的库，入口只做 source + main；`stop_project_runtime` 等库函数内的 `exit` 改为返回码。

## 范围与非目标

- 本次只做「source 安全 + 库加载段退出码」，**不拆分** 26,823 行单体，**不迁移 Rust**；runtime 拆分与 Rust 迁移的主体另立 issue，本 issue 不作为其完成依据。
- 必须同步把 `check-file-size` 接入 pre-commit 与 CI，并把无扩展名的 `runtime/freely` 纳入扫描（按显式白名单），防止拆分前继续增长（该要求原在 #4146 第 5 项，按职责移入本条）。
- 不改变现有 551 个测试脚本的语义；拆分以「行为不变」为硬约束。

## 验收标准
- RED：写一个测试脚本 `source runtime/freely`（模拟现有 4 个调用方），当前因顶层副作用/缺文件直接退出；修复后 source 成功或返回可判定的错误码且不终止调用方 shell。
- RED：`grep -nE '^\s*exit [0-9]' runtime/freely | head -20` 在库加载段（前 60 行）为 0 处。
- GREEN：`stop_project_runtime` 的锁超时不再终止 `cmd_restart` 进程（返回非零而非 exit），有对应测试。
- GREEN：`bash -n` 通过且现有 551 个测试脚本行为不变（拆分不改语义）。
- GREEN：4 个已知 source 调用方（`manager-watchdog.sh` / `sse-watchdog.sh` / `interruption-manager-handler` / `governance-promotion-gate`）在库缺失时返回可识别错误而非整体退出，有回归测试覆盖。

### comment-20261109T083613Z
- source: system
- event: promote_finalized
- children: ["I-20261103T132605Z-A"]

拆解为以下任务:
1. [I-20261103T132605Z-A](will-be-updated)

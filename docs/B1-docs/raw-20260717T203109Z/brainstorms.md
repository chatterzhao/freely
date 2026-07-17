---
b1_id: B1-20260717T203109Z
phase_state: completed
source_raw: raw-20260717T203109Z
source_url: https://github.com/chatterzhao/freely/issues/3983
produced_candidate: C-20260717T203109Z-A
created_at: 2026-07-17
---

# B1_IBM: wt-close autonomous gate 两项遗留补全（agent_working STUB + _has_merge 未命中）

## Input

- raw issue 表面描述：① agent_working 查询段因 f-string 引号冲突为 STUB；② _has_merge 在 subshell 中未命中；③ usage/help 需同步 --force 新语义。
- PR #3980 已合入 `_autonomous_close_gate()` 核心判定，本 lane 是其收尾。

## Problem（实测根因 — 与 raw 表面描述不同）

逐项 bash -x 追踪 + python 直跑后，真实根因链是四个，均有复现证据：

### P1. gate 静默整体退出（吞掉 raw 描述的"STUB"问题）
- `agent_working.py` 的 `_db_rpc` 走 Unix socket `/tmp/freely-db-<sha256(project)[:16]>.sock`。
- socket 不存在（db daemon 未跑）时 `sock.connect` 抛 `FileNotFoundError` → python rc=1。
- gate 内 `_aw_row=$(python3 2>/dev/null <<PYAW…)` 赋值失败 + 脚本 `set -euo pipefail` → **整个 wt-close 静默死亡 rc=1，0 字节输出**（stderr 已被 2>/dev/null 吞）。这解释了此前三组 gate 测试全部 0 字节。

### P2. socket 按 project root hash 隔离 → 工位内永远连不上主仓 db
- gate 用 `$PROJECT_ROOT`（= 工位根）算 socket hash：`02fe6bdaf9…`；主仓 daemon 的 socket 是 `80d307e1…`。
- 即使 daemon 在跑，工位内执行 wt-close 也 100% 连不上 → agent_working 查询恒空。
- a2a 活跃检查同样指向 `$PROJECT_ROOT/.freely/freely.db`（工位内是 wt-create 时刻的**陈旧拷贝**），活跃 a2a task 恒查不到。
- B1 phase_state 读相对路径 `docs/B1-docs/...`，依赖 cwd，跨目录执行时静默 miss。

### P3. _has_merge 未命中 = grep -q SIGPIPE × pipefail 竞态（非 raw 描述的 subshell 环境差异）
- `git log … | grep -qiE …`：grep -q 命中即退，git 仍在写 → SIGPIPE → `set -o pipefail` 判整条 pipeline 失败 → `if` 条件为假 → `_has_merge` 恒 false。
- 终端直调"命中"是竞态侥幸（git 先写完则无 SIGPIPE）；bash -x 实测同一命令在脚本内不赋值 `_has_merge=true`。

### P4.（新发现，P1 修复后暴露）agent_working RPC 行序列化返回数字键
- `freely_db_manager.py` 的 `h_aw_get`/`h_aw_get_all` 用 `cols = [d[0] for d in PRAGMA table_info(agent_working)]` —— `d[0]` 是 **cid（列序号）**，列名在 `d[1]`（同文件 a2a_tasks 各 handler 均正确用 `desc[1]`）。
- 返回行键为 `'0'..'10'`，而**全部消费者**（watchdog_sse.py 三处、pr-review-guarded 两处、task-lifecycle-scan.py、wt-close teardown 段、gate 本身）用命名键 `row.get("worker_id")` → 恒 None。
- 实测复现：agent_assign 写入活跃 worker 行后，gate 仍判 "zero agent activity — allowing close"（本应 DENY）。
- 波及面：watchdog_sse 的 worker/reviewer **复用路径**同样失效（读不到已有 id → 每次走 agent_next_free 重新分配）。此为共享 handler 的一处修复，非独立改动面。

## Brainstorm

### Option A：gate 内改数字键取值适配现状
- 用 `row.get("7")` 取 worker_id。❌ 违背 RPC 命名键契约；watchdog_sse 等其余消费者仍坏；把 bug 固化成接口。

### Option B：修 handler 列名（d[0]→d[1]）+ gate 侧韧性四件套 ✅
1. `freely_db_manager.py` 两处 `d[0]` → `d[1]`（对齐 a2a_tasks handler 既有写法，全消费面一次修复）。
2. gate 内 python heredoc try/except 全包裹：db 不可用 = runtime 未跑 = 无活跃 agent，优雅降级为空，**gate 永不因基础设施缺席而静默杀死 wt-close**；赋值再加 `|| true` 双保险。
3. `_main_root` 经 `git rev-parse --git-common-dir` 解析主仓根：agent_working socket、a2a db、B1 phase_state（develop 权威版优先）全部指向主仓。
4. `_has_merge` 改 `git rev-list develop --merges --grep … --count`：无管道，彻底消除 SIGPIPE×pipefail 竞态；且 `--merges` 比原 grep 正则更精确。

### Option C：db 查询挪到 wrapper 外置预查
- ❌ 破坏 gate 单函数自治，增加调用面耦合。

## Decision: Option B

- 命名键是既有契约（所有消费者一致），handler 是唯一偏离点，修 handler 是根因修复。
- gate 降级语义明确：基础设施缺席 ≠ 拒绝关闭；查得到活跃 agent 才 DENY。
- 主仓根解析让 gate 在任意 cwd/工位内行为一致——这正是 raw 描述"subshell 未命中"的正解。
- usage/help 同步（raw 第 3 项）随 dev 一并完成，reason 文案变更同步 usage()。

## Candidate

- candidate_id: C-20260717T203109Z-A
- status: promoted
- milestone: M-20260717T203109Z-A

---
b1_id: B1-20260717T124926Z
phase_state: completed
source_raw: raw-20260717T124926Z
produced_candidate: C-20260717T124926Z-A
created_at: 2026-07-17
---

# B1_IBM: wt-close 自治化重构

## Input
2026-07-17 排查暴露 wt-close 六个设计缺陷（免交互门禁是补丁不是重构）。目标：agent 无需人类 `--force --reason` 即可正确收口；不丢任何既有功能。

## Problem

### D1 入口门禁依赖人类话术
当前 ownership_guard：未完成/异主 → 打印人类可读的 `--force --reason` 提示然后 exit 1。agent 不认识这个话术——a2a-exit 回来 error,agent 不会自己加 --force。自治系统需要 machine-actionable 的阻塞原因和替代路径。

### D2 Phase 4.5"收尸"不是"先收工"
查活跃 worker 的代码（L942-1010）语义是"删之前触发清理"：发 shutdown 消息→等 10s→不管 worker 有没有 a2a-exit 都 kill -9→然后继续删工位。正确自治流程应该是：发"请收工"→等 worker 自行 a2a-exit（可配超时）→来了就正常关,超时了降级给 manager 决策。

### D3 agent_working 不前置查询
wt-close 唯一的 agent_working 代码在 Phase 5（L1199）：删完所有东西后才 `agent_release_all`。关闭前不看 agent_working 表——不知道这个 raw_key 有没有 reviewer 正在审、有没有 worker 还在干。agent_working 是活的真源但被当坟头登记表。

### D4 test 工位静默 force
L1157 `git worktree remove --force "$_tp_wt" 2>/dev/null || true`——有未提交的测试证据直接扬,无 warn 无 event。

### D5 分支通配符匹配歧义
`_resolve_branch_from_raw_key` 用 `git branch --list "fix/raw-${_raw_key}-*" | head -1`——同名 raw 不同 slug 时 kill 错目标。

### D6 无回滚/分段确认
单体脚本串行无 checkpoint,失败不可逆。

## Brainstorm

### 各缺陷方案（保留全部既有功能,不删任何 closeout 步骤）

| # | 方案 |
|---|------|
| D1 | 当前 ownership_guard 替换为 `_autonomous_close_gate`：自有关闭(agent_working 无活跃+a2a_tasks 无进行中)→允许;自属未完成→拒绝并输出 JSON 阻塞原因(actionable:先 a2a-exit completed);他属已完成→允许(scan 收尾场景);他属未完成→拒绝;--force 保留人类例外场景,"未完成允许自主关闭的机器条件"与"拒绝的机器原因"并存 |
| D2 | Phase 4.5 前移为 Phase 0.5(在 branch resolve 之后、删除动作之前执行)：A2A session/prompt 通知 worker→poll task state 等待(可配,默认 120s)→completed 继续/超时→降级为 manager 决策(dropped 式事件升级)而非直接 kill;--force 路径保留 kill-and-continue |
| D3 | gate 内部查 agent_working：有活跃 reviewer_id→拒关;有 worker_id 但无对应活跃 a2a_tasks→僵尸,允许;同 D1 合并判定 |
| D4 | force-remove 前加 `git -C $_tp_wt status --porcelain` 检查,有未跟踪/修改且非空时 emit event+log(不阻断,自治能力优先) |
| D5 | 多条匹配时取 namespace 最短匹配,仍多条→拒绝并输出候选列表让 agent 决策;单条→直用 |
| D6 | 在 worktree remove 前加 `_last_chance_log()` 写一行 "closeout sequence started" event 作为回滚边界标记(subsequent lane——独立能力) |

### Option A（选定）：六点一体收敛于 wt-close 脚本内
每个点都是"替换判定语义→不删步骤"的局部改动,改动面小且封闭。
### Option B：拆成独立 closeout service
改动面大,否。自治化重构应轻量落地,service 化留给后续架构线。

## Decision: Option A

## 边界
- 只改 docs/system/workspace/scripts/worktree/wt-close（1259 行）
- 不改调用方（bin/wt-close wrapper、runtime/freely 的 cmd_wt_close、a2a-exit）
- --force 语义不变(人类例外场景);--platform-only 不受影响
- 保留全部既有关闭步骤

## Candidate
- candidate_id: C-20260717T124926Z-A
- status: promoted
- milestone: M-20260717T124926Z-A

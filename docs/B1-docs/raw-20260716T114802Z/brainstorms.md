---
b1_id: B1-20260716T114802Z
phase_state: completed
source_raw: raw-20260716T114802Z
produced_candidate: C-20260716T114802Z-A
created_at: 2026-07-16
---

# B1_IBM: stall 误判复发 — liveness 兜底信号链失效（niced 进程态 + unbound base_tool）

## Input

- 来源：GitHub #3944。原描述（"PR #3943 return 0 反向"）经 git log -L 证伪（453ed81a7 合入的即为正确 return 1），issue 描述已于 2026-07-16 feedback edit 修正
- 复发实证：2026-07-16 13:10:16Z manager AI 启动 → 13:11:47Z（91s）`runtime_stalled_ai_recovery_triggered reason=manager_ai_stalled_without_runtime_progress` → recovery 连锁 → AI rc=1。crash 证据显示 AI 正常执行中

## Problem（根因链，代码坐实）

`manager_ai_stalled_without_runtime_progress` 判 stall 前的兜底 `_ai_shows_liveness_acp`（runtime/freely ~L13901-13966）五路信号在真实 daemon 环境下逐一失效：

1. **Signal 1（debug log mtime）**：长推理/长输出期间无 tool 事件是正常行为（本日 17:34 实验 cycle 总时长 400s）——事件静默 >90s 时 S1 合法过期。S1 过期本身不是 bug，兜底链必须接住。06:11 场景：debug 输出共 3834 字节，事件集中在 cycle 前段，静默期触发检查。
2. **Signal 2（进程态）＝主 bug**：`[[ "$proc_state" == "R" || "$proc_state" == "S" ]]` 精确匹配。daemon 派生的 bridge/AI 进程在 macOS 上带修饰态（**SN**＝niced sleep，今日 ps 快照多次实证；另有 S+/Ss 等）→ 活得好好的进程匹配失败。
3. **Signal 3（socket 探活）**：`_acp_bridge_socket "$project" "$base_tool"` 中 `$base_tool` 在本函数**未定义**（L13928）。ensure-manager 进程 `set -u` 下命令替换失败 → socket 路径空 → 信号跳过。
4. Signal 4（fatal error）无 fatal → 继续；Signal 5（A2A workers）cycle 早期无 worker → 0 → **return 1 判死**。

链条：S1 合法过期 → S2 被修饰态击穿 → S3 被 unbound 变量击穿 → S5 空 → 误判死 → recovery 误杀活 manager。

## Brainstorm

### Option A：提高 90s 阈值
- 反对：治标；长推理可超任意固定阈值；且 S2/S3 的击穿仍在

### Option B：修复兜底链本身（选定）
- B-1（S2）：进程态改前缀匹配 `R*|S*`（覆盖 SN/S+/Ss；T/Z/D 仍排除——D 罕见且短暂，不放宽）
- B-2（S3）：函数内安全推导 `local base_tool="${AGENT_AI_TOOL%%-*}"`（缺省 claude），消除 unbound

### Option C：重构 liveness 为 bridge session 状态查询
- 方向正确但改动面大（涉及 acp-bridge 协议），留给后续能力 issue；本 lane 止血

## Decision: Option B

两处小修，直接堵住 06:11 误杀路径；S1 语义不动（过期即应走兜底）。

## 边界

- 只改 `_ai_shows_liveness_acp` 两处；不动阈值、不动 stall 判定结构、不动 direct 模式（`_ai_shows_liveness_pid_signals` 信号薄弱问题记录为已知残留，见 candidates open_questions→吸收为 residual）
- 与已合并 raw-20260717T004620Z / raw-20260717T004721Z 零重叠

## Candidate

- candidate_id: C-20260716T114802Z-A
- status: promoted
- milestone: M-20260716T114802Z-A

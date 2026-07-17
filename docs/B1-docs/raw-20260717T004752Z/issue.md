---
local_id: raw-20260717T004752Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T004752Z-A
platform_ids:
  github:
    issue_id: '3950'
    url: https://github.com/chatterzhao/freely/issues/3950
    synced_at: ''
  gitee:
    issue_id: IK1L8F
    url: https://gitee.com/zhaoquan/freely/issues/IK1L8F
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T00:48:15Z'
updated_at: '2026-07-17T00:48:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
2026-07-16 文档 vs 代码 vs raw issue 时间线三方审计确认，监督控制面架构文档系统性落后于已合并实现：

1. **heartbeat 机制零文档**（P0）：supervisor 存活检测主力（raw-20260531T125837Z 设计、3b156c2e1 合入，SUPERVISOR_HEARTBEAT_TIMEOUT_SECS=120、2s touch 子进程）在 three-loop-capability-lifecycle.md / three-loop-trace-contract.md / watchdog-control-plane SKILL / session-lifecycle-protocol.md 均无记载；代码注释所称已被替代的 L220-L240 grace chain 在代码中已不存在。
2. **trace-contract §11 缺 16+ 已实现检查点**（P0）：L090/L091/L092/L201/L202/L210/L211/L212/L225/L230/L231/L232/L300/L310/L320/L330-L336 在代码活跃使用但未注册。
3. **trace 契约执行缺口**（代码侧小修）：A-L240 恒 to=UNSET ok=0（L19292 未传 expected_next）；A-L041(ai_launch_observed) 实际在 cycle 尾部才发（2026-07-16 晚于 launch 94s，语义漂移）；A-L042 OUT to= 打印整个候选集而非实际下一跳（违反契约 §4/§8）。
4. **bridge 生命周期未文档化**（P1）：lazy-start/idle-sleep/auto-wake（raw-20260708T202424Z、d43c4af01）、per-cycle ensure 行为、健康检查 5s vs 冷启动 ~8s 约束。
5. **task_mode 语义未文档化**（P1）：auto(全功能)/wait(sleep+continue 跳过 prompt build)/listen(scan-only,发现 ready item 自动切 auto)/id:<scan-id>；AI_MODE 与 task_mode 区分（raw-20260715T063959Z）。
6. **storm 阈值与 Loop Guard L0-L3 零文档**（P2）：RESTART_STORM_WINDOW_SECS=30/COUNT=10/PEAK=10、LOOP_GUARD_L0 等。
7. SVG 残留：raw-20260711T023009Z（已 completed）修了大部分，但 ACP idle timeout 实为 180s+30s grace，文档只写 180s。

## 修复方向
文档为主（doc-only 变体），第 3 条含少量代码修改（trace 打点参数）。按 three-loop-trace-contract.md §10 先改逻辑再同步 trace 编号。

## 依据
逐条 file:line 对照见审计（代码 runtime/freely:8024/22491/19219/14065/22540/22596；文档 trace-contract.md:161-194、capability-lifecycle.md:37,111、SKILL.md:47）

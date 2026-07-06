# candidates: issue 状态字段重构

## C-20260505T121000Z-A: legacy issue

- candidate_id: C-20260505T121000Z-A
- title: 修正 scan 的 TERMINAL_RAW / DONE_STATES / ACTIVE_B2 常量
- scope: task-lifecycle-scan.py 第15-19行
- non_goals: 不改 scan 逻辑，只改常量
- priority: P0
- status: promoted
- milestone: M-20260505T121000Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260505T121000Z-A/issue.md

### 改动

- TERMINAL_RAW: 去掉 completed → {absorbed, dropped}
- DONE_STATES: 去掉 done, done_ibm → {done_b2_ibm, completed}
- ACTIVE_B2: 去掉 in_ibm → {in_b2_ibm, done_b2_ibm, in_dev, blocked_dev}
- 为所有已有 raw/I-* issue 补充 platform_state 字段（一次性迁移脚本）

### 验证

- scan 不再把 status=closed 的 raw 当 non-terminal
- scan 识别 done_b2_ibm 为 active 状态
- 历史 data 兼容（现有 179 个 completed 不受影响）
- 迁移后所有已有 platform_ids 的 issue 有正确的 platform_state

---

（C-B/C-C deferred to next iteration — detailed spec in brainstorms.md §D2/D5/D6）

## 决策记录

- C-D（迁移脚本）→ absorbed into C-A：迁移是实现的一部分，不作为独立 candidate
- C-A/C-B/C-C 各自 promote 到独立 I-*，按 A→B→C 依赖顺序执行

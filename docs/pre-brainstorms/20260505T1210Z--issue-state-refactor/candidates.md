# candidates: issue 状态字段重构

## C-20260505T1210Z-A: scan 常量对齐 IBM Framework

- candidate_id: C-20260505T1210Z-A
- title: 修正 scan 的 TERMINAL_RAW / DONE_STATES / ACTIVE_B2 常量
- scope: task-lifecycle-scan.py 第15-19行
- non_goals: 不改 scan 逻辑，只改常量
- priority: P0
- status: promoted
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: pending://I-20260505T1210Z-A

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

## C-20260505T1210Z-B: issue-sync 只写 platform_state

- candidate_id: C-20260505T1210Z-B
- title: issue-sync cmd_close/cmd_create 只更新 platform_state
- scope: bin/issue-sync 第522-543行（cmd_close）, 第377-401行（cmd_create）
- non_goals: 不改 promote/comment/update 逻辑
- priority: P0
- status: proposed
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: pending://I-20260505T1210Z-B

### 改动

- cmd_close: _fm_set_str platform_state closed（不写 status）
- cmd_create: _fm_set_str platform_state open
- 新增 _fm_set_nested 支持 platform_state 写入

### 验证

- issue-sync close raw-xxx 后 raw 的 status 保持 absorbed
- I-* 的 phase_state 保持 completed
- platform_state 正确更新为 open/closed

---

## C-20260505T1210Z-C: governance gate 拦截状态不一致

- candidate_id: C-20260505T1210Z-C
- title: governance-merge-gate 新增 platform_state vs phase_state 一致性门禁
- scope: governance-merge-gate 新增 G1/G2/G3 + S1/S2/S3 门禁
- non_goals: 不改变已有 gate 的行为
- priority: P1
- status: proposed
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: pending://I-20260505T1210Z-C

### 一致性门禁 (G1-G3)

| ID | 条件 | 级别 |
|----|------|------|
| G1 | phase_state=completed 且 platform_state=open | block merge |
| G2 | status=proposed 且 platform_state=closed | block |
| G3 | platform_state 不为空但 platform_ids 为空 | block |

### Schema 门禁 (S3)——兜底拦截非法值

| ID | 条件 | 级别 |
|----|------|------|
| S3 | phase_state 值不在合法集合中 | block |

合法值按 kind：
- raw.phase_state ∈ {proposed, absorbed, dropped}
- I-*.phase_state ∈ {in_b2_ibm, done_b2_ibm, in_dev, blocked_dev, in_verification, completed}

（S1/S2 不再需要——raw 和 I-* 统一用 phase_state 字段名，无跨字段污染）

### 验证

- 写入非法状态值（如 raw status=closed）→ gate 拦截
- raw 误设 phase_state → gate 拦截
- I-* 误设 status → gate 拦截

---

## C-20260505T1210Z-D: 现有 issue 加 platform_state（迁移）

- candidate_id: C-20260505T1210Z-D
- title: 为所有已有 raw/I-* issue 补充 platform_state 字段
- scope: 一次性迁移脚本
- non_goals: 不修改已有 status/phase_state 值
- priority: P1
- status: proposed
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: pending://I-20260505T1210Z-A

### 算法

```
for each raw/I-* issue:
  if platform_ids 非空:
    query GitHub state → platform_state = open|closed
  else:
    platform_state = open  # 默认
```

### 注意

- 已 absorbed 且平台已关的 raw: platform_state=closed, status=absorbed（符合预期）
- 已 completed 且平台已关的 I-*: platform_state=closed, phase_state=completed（符合预期）

---

## 决策记录

- C-D（迁移脚本）→ absorbed into C-A：迁移是实现的一部分，不作为独立 candidate
- C-A/C-B/C-C 各自 promote 到独立 I-*，按 A→B→C 依赖顺序执行

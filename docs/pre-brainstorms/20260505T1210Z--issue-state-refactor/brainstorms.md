# brainstorms: issue 状态字段重构

## 现状审计

### raw issue frontmatter 现状

```yaml
status: proposed | absorbed | closed    # ← closed 是 issue-sync 污染进来的
platform_ids: {github: {issue_id: '…'}} # ← 有 issue_id 但没 platform_state
```

### I-* issue frontmatter 现状

```yaml
status: completed          # ← raw 和 I-* 都有 status，语义不同
phase_state: completed     # ← IBM Framework §89 定义
platform_ids: {github: {issue_id: '…'}}
```

### scan 常量偏差

| 常量 | 当前 | 应改为 |
|------|------|--------|
| TERMINAL_RAW | absorbed, dropped, completed | absorbed, dropped |
| DONE_STATES | done, done_ibm, completed | done_b2_ibm, completed |
| ACTIVE_B2 | in_b2_ibm, done_b2_ibm, in_dev, blocked_dev, in_ibm | in_b2_ibm, done_b2_ibm, in_dev, blocked_dev |

### issue-sync 跨层污染

cmd_close 第540行: `_fm_set_str "$file" "status" "closed"` — 无条件写 status，对 raw 覆盖 absorbed。

### raw/I-* 平台 issue 共享不一致

- 20260504T1132Z: raw 和 I-* 共享 GitHub #203 ✅
- 20260502-1028: raw→#213, I-*→#210（两个平台 issue）❌

## 设计决策

### D1: 双字段方案

每个本地 issue 有两个正交的状态字段：

| 字段 | 归属 | 语义 | 取值 |
|------|------|------|------|
| `status` | raw issue | freely B1 消费状态 | proposed / absorbed / dropped |
| `phase_state` | I-* issue | freely B2 开发生命周期 | in_b2_ibm → done_b2_ibm → in_dev → blocked_dev → in_verification → completed |
| `platform_state` | 两者都有 | 平台 issue 镜像 | open / closed |

理由: 平台状态和 freely 内部状态是正交的。平台不区分 raw/I-*。

### D2: issue-sync 职责边界

- create: 设 platform_state=open
- close: 设 platform_state=closed
- 永不死 status 或 phase_state

### D3: raw 和 I-* 共享平台 issue

promote 时 I-* 继承 raw 的 platform_ids，不创建新 issue。

### D4: 字段分组

raw issue（无 phase_state 字段）：
```yaml
# ── 标识 ──
local_id: raw-20260505T1210Z
kind: raw

# ── 状态 ──
status: proposed                    # freely B1 消费状态
platform_state: open                # 平台镜像

# ── 平台关联 ──
primary_platform: github
platform_ids:
  github:
    issue_id: '214'

# ── 生命周期关联 ──
absorbed_into: I-20260505T1210Z-A   # promote 后的目标

# ── 元数据 ──
issue_title: "…"
created_at: '…'
updated_at: '…'
author: human
channel: github
session_refs: []
```

I-* issue（无 status 字段）：
```yaml
# ── 标识 ──
local_id: I-20260505T1210Z-A
kind: linked

# ── 状态 ──
phase_state: in_b2_ibm              # freely B2 开发生命周期
platform_state: open                # 平台镜像

# ── 平台关联 ──
primary_platform: github
platform_ids:
  github:
    issue_id: '214'                 # ← 和 raw 共享同一个

# ── 生命周期关联 ──
promoted_from: raw-20260505T1210Z   # 来源 raw

# ── 元数据 ──
issue_title: "…"
created_at: '…'
updated_at: '…'
session_refs: []
```

### D5: 门禁规则

| 规则 | 条件 | 动作 |
|------|------|------|
| G1 | phase_state=completed, platform_state=open | **block** merge to develop |
| G2 | status=proposed, platform_state=closed | **block** — 平台已关但 B1 未开始 |
| G3 | I-* 有 platform_state 但无 platform_ids.issue_id | **block** — 状态和 ID 不一致 |

## 非目标

- chat-inbox consumed 逻辑
- 平台 issue label 体系
- raw/I-* 目录结构变更
- candidate status 字段

## 实现顺序

1. task-lifecycle-scan.py: 修正 TERMINAL_RAW / DONE_STATES / ACTIVE_B2
2. 为所有本地 raw/I-* 添加 platform_state 字段（迁移脚本）
3. bin/issue-sync: cmd_close/cmd_create 只写 platform_state
4. governance-merge-gate: 新增 G1/G2/G3 门禁

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
| `phase_state` | raw issue | B1 消费阶段 | proposed / absorbed / dropped |
| `phase_state` | I-* issue | B2 开发生命周期 | in_b2_ibm → done_b2_ibm → in_dev → blocked_dev → in_verification → completed |
| `platform_state` | 两者都有 | 平台 issue 镜像 | open / closed |

理由: 平台状态和 freely 内部状态是正交的。平台不区分 raw/I-*。

### D2: issue-sync 职责边界

- create: 设 platform_state=open
- close: 设 platform_state=closed
- 永不写 phase_state

### D3: raw 和 I-* 共享平台 issue

promote 时 I-* 继承 raw 的 platform_ids，不创建新 issue。

### D4: 字段分组

统一使用 `phase_state`——raw 和 I-* 共用一个字段名，不同阶段用不同值：

raw issue：
```yaml
# ── 标识 ──
local_id: raw-20260505T1210Z
kind: raw

# ── 状态 ──
phase_state: proposed               # B1: proposed → absorbed → dropped
platform_state: open                # 平台镜像: open → closed

# ── 平台关联 ──
primary_platform: github
platform_ids:
  github:
    issue_id: '214'

# ── 生命周期关联 ──
absorbed_into: I-20260505T1210Z-A

# ── 元数据 ──
issue_title: "…"
created_at: '…'
updated_at: '…'
author: human
channel: github
session_refs: []
```

I-* issue：
```yaml
# ── 标识 ──
local_id: I-20260505T1210Z-A
kind: linked

# ── 状态 ──
phase_state: in_b2_ibm              # B2: in_b2_ibm → … → completed
platform_state: open                # 平台镜像: open → closed

# ── 平台关联 ──
primary_platform: github
platform_ids:
  github:
    issue_id: '214'                 # ← 和 raw 共享同一个

# ── 生命周期关联 ──
promoted_from: raw-20260505T1210Z

# ── 元数据 ──
issue_title: "…"
created_at: '…'
updated_at: '…'
session_refs: []
```

### D5: Schema 约束——每个字段只能是合法值

防止状态值被误写（如 issue-sync 写入 `closed` 到 raw status），定义每个字段的合法值集合，非法值在任何阶段都应被拦截。

raw issue phase_state：
| 值 | 含义 |
|----|------|
| `proposed` | B1 待消费 |
| `absorbed` | 已消费（promote 到 I-*） |
| `dropped` | 丢弃 |

I-* issue phase_state（IBM Framework §89）：
| 值 | 含义 |
|----|------|
| `in_b2_ibm` | B2 设计阶段 |
| `done_b2_ibm` | B2 设计完成 |
| `in_dev` | 开发中 |
| `blocked_dev` | 开发阻塞 |
| `in_verification` | 验证中 |
| `completed` | 完成 |

兜底位置：
- **scan**: 扫到 phase_state 不在合法集合 → `schema_violation`，stage=`invalid`
- **issue-sync**: 写 phase_state 前校验，非法值拒绝
- **merge gate**: merge 前检查字段合法性

### D6: 门禁规则

| 规则 | 条件 | 动作 |
|------|------|------|
| G1 | phase_state=completed, platform_state=open | **block** merge |
| G2 | phase_state=proposed, platform_state=closed | **block** |
| G3 | platform_state 不为空但 platform_ids.issue_id 为空 | **block** |
| S3 | phase_state 值不在合法集合中 | **block** |

合法值按 kind：
- raw: {proposed, absorbed, dropped}
- I-*: {in_b2_ibm, done_b2_ibm, in_dev, blocked_dev, in_verification, completed}

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

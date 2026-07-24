---
b1_id: B1-20260721T223133Z
phase_state: completed
source_raw: raw-20260721T223133Z
source_url: https://github.com/chatterzhao/freely/issues/4070
produced_candidate: C-20260721T223133Z-A
created_at: 2026-07-21
---

# B1_IBM：生命周期命令与 raw 元数据状态合同

## Discovery

### 现象

1. `pr-create-guarded` 对已有 PR 执行 merge dry-run 后才受控 push；本地含 reviewer 修复而远端仍是旧 head 时，dry-run 先以 head 不相等失败，形成更新死锁。
2. `raw-issue-pull` 默认物化 `phase_state: proposed`，但 `wt-create` 成功后无条件改成 `absorbed`，未同时提供 `absorbed_into` 与 `canonical_issue_path`。
3. 约 751 个历史 raw issue 已出现 72 种字段组合和 102 种字段顺序；142 个 `absorbed` 缺吸收目标。部分 scan/gate 仍以字段行存在性判断，而非值和跨字段组合。

### 数据流

```text
feedback → platform issue → raw-issue-pull → issue.md → wt-create
                                              ↓
scan/index/gate → PR create/review/merge → closeout/sync
```

错误不是孤立写入点，而是生产者、状态迁移与消费者没有共享同一合同。

### 范围

本 raw 统一覆盖两个直接阻塞自举的命令缺陷：

- PR 已存在时的多平台受控更新；
- 新 raw metadata 的固定 schema、合法状态迁移和值驱动消费。

历史 raw 文件不批量迁移；消费者继续读取旧格式，新创建 raw 严格遵守新合同。

## Research

### 观测字段

现代 raw 主字段包括：`local_id`、`kind`、`phase_state`、`absorbed_into`、`platform_ids`、`primary_platform`、`canonical_issue_path`、`last_synced_comment_at`、`hash`、`created_at`、`updated_at`、`intake_id`、`author`、`channel`、`session_refs`、`platform_state`。此外存在历史 `status`、`title`、`priority`、`completed_at`、`closeout_note`、`force_closed_*` 等漂移字段。

### 消费者风险

- `task-lifecycle-scan.py` 的 phase 主判断按值，但空值与缺失混合。
- `pre-scan-fix.sh`、`migrate-issue-phase-state`、`governance-merge-gate` 部分分支按键/文本存在性判断。
- `issue-index` 仍读旧 `status`，并写死空 canonical 路径。
- `pr-create-guarded` 只判断 `absorbed`，没有校验 canonical 组合。
- `pr-merge-guarded` 将空 phase 当作 proposed。
- `batch-closeout-raw-issues` 依赖字段行正则存在。

## Brainstorm

### Option A：仅删除 wt-create 的 absorbed 写入

优点：改动最小。缺点：生产者仍会生成不同字段集，scan/gate 继续误判；无法处理 PR 更新死锁和多平台状态。

### Option B：嵌套 schema 并迁移全部历史文件

优点：数据结构清晰。缺点：需要一次性重写大量 Shell/Python 消费者和 751 份历史数据，风险与当前自举阻塞不匹配。

### Option C：固定扁平 schema，新文件严格、旧文件兼容

- 以单一 Python 模块定义字段顺序、初始值、序列化、合法组合和状态迁移。
- `feedback` 建立完整初始 payload；pull 只回填平台值；`wt-create` 不改变生命周期。
- 新 schema 文件字段只改值，不增删、不改顺序。
- 旧文件读取时兼容，不自动批量重写。
- scan/gate/PR/closeout 对新 schema 严格校验值和组合；旧文件沿兼容规则读取，但危险状态仍 fail closed。
- PR 更新按配置动态发现平台并分类 remote head，再由 adapter 受控 push/PR 更新。

## Decision：Option C

该方案兼顾确定性与迁移风险。固定扁平 schema 可减少现有 Shell 消费者改造面；版本字段允许区分严格新合同与遗留兼容。PR 更新和 metadata 状态统一由“观测实际状态 → 分类 → 校验 → 受控迁移”模型处理。

### 状态约束

```text
proposed:
  absorbed_into = ''
  canonical_issue_path = ''

absorbed:
  absorbed_into = 有效 I-* ID
  canonical_issue_path = 存在的 canonical 文档

dropped:
  closeout_reason = 非空
```

`wt-create` 只创建工位，不是 B2 absorption 事件。只有 canonical I-* 物化时，才原子更新 absorbed 三元组。

### 新文件固定字段顺序

```text
schema_version
local_id
kind
phase_state
absorbed_into
canonical_issue_path
platform_ids
primary_platform
platform_state
last_synced_comment_at
hash
created_at
updated_at
intake_id
author
channel
session_refs
closeout_reason
closed_at
```

平台详细引用继续保留在 `platform_ids` 映射中；所有配置平台由 adapter registry 动态发现，不写死平台名或 remote。

## Candidate

- candidate_id: C-20260721T223133Z-A
- status: promoted
- milestone: M-20260721T223133Z-A
- promoted_issue_id: I-20260721T223133Z-A

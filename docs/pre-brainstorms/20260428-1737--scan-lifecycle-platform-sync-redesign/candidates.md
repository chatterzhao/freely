# Candidates — Scan Lifecycle + Platform Sync Redesign

## C-20260428-1737-A: 统一生命周期 Scan 模块

- status: proposed
- scope: 重构 task-source-scan.py 为 task-lifecycle-scan.py，输出统一生命周期定位
- priority: P0
- milestone: M-20260306-workspace-routing-foundation

### 核心改动

1. 时间戳即身份：raw-YYYYMMDD-HHMM → I-YYYYMMDD-HHMM-A，B1 目录 YYYYMMDD-HHMM--slug
2. 8 阶段生命周期：B1_proposed → brainstorming → candidate → promoted → B2_active → verifying → 收口 → completed
3. 平台状态交叉：本地 phase_state + GitHub/Gitee open/closed → 综合判定
4. 评论同步检查：本地 comment → platform_ids 是否完整
5. 区分"状态未改"和"事情没做"，给出不同 next_action

### Non-Goals

- 不迁移历史 0000 格式的 ID
- 不实现平台→本地评论拉取（独立任务）
- 不改 issue-sync 的 comment 同步（独立任务）

## C-20260428-1737-B: 修复 I-* ID 格式（HHMM）

- status: proposed
- scope: 所有新创建的 I-* issue 使用 YYYYMMDD-HHMM 格式
- priority: P0
- milestone: M-20260306-workspace-routing-foundation

### 核心改动

1. ibm-framework.md 示例改为 HHMM 格式
2. B1 预研目录生成使用 HHMM（复用 raw 时间戳）
3. I-* issue 创建时继承 B1 目录时间戳

### Non-Goals

- 历史 I-20260426-0000-A 保持不变

## C-20260428-1737-C: 评论 sync + 回写 platform_ids

- status: proposed
- scope: issue-sync comment 后回写平台 comment_id 到本地
- priority: P1
- milestone: M-20260306-workspace-routing-foundation

### 核心改动

1. bin/issue-sync comment：同步后回写 platform_ids 到本地 comment 元数据
2. last_synced_comment_at 按平台记录
3. Scan 检查评论是否全部同步

## C-20260428-1737-D: 多平台去重

- status: proposed
- scope: scan 外部平台时检测重复 issue
- priority: P2
- milestone: M-20260306-workspace-routing-foundation

### 核心改动

1. scan_external 检查本地是否已有相同 raw
2. 匹配条件：title 相似度
3. 已有 → 补 platform_ids

## C-20260428-1737-E: issue-sync comment 统一工具

- status: proposed
- scope: 完善 bin/issue-sync comment 命令
- priority: P1
- milestone: M-20260306-workspace-routing-foundation

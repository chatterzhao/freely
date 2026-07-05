# Candidates — Issue Lifecycle + Scan + Platform Sync

- promoted_issue_path: ""
- milestone: M-20260306-workspace-routing-foundation
- session_refs:
  - {tool: "manual", session_id: "pre-brainstorm-creation", jsonl_path: "unavailable"}

## C-20260428-1737-A: 统一生命周期 Scan 模块（task-lifecycle-scan.py）

- status: proposed
- scope: 一个 raw→I 链条一个 JSON 对象，只输出未完成项，8 项 completion checklist
- type: 脚本
- priority: P0

### 核心逻辑

1. 收集所有 raw + I-*，按时间戳 key 配对
2. 一个 raw 可关联多个 I-*（-A/-B/-C 后缀），输出为 children 数组
3. 逐个检查：phase_state / platform closed / comments resolved
4. 全部通过 → 排除；任一未通过 → 输出，列具体 blockers
5. 区分"状态未改"（platform 已关但 phase_state 未更新）和"事情没做"（真没实现）

## C-20260428-1737-B: 修复 I-* ID 格式（HHMM + 后缀）

- status: proposed
- scope: raw-YYYYMMDD-HHMM（无后缀），I-YYYYMMDD-HHMM-A/B/C（有后缀），B1 目录 YYYYMMDD-HHMM--slug
- type: 脚本 + 文档
- priority: P0

### 核心逻辑

1. AI 创建 B1 目录时使用 HHMM（复用 raw 时间戳，不用 0000 序列号）
2. AI 创建 candidate 时使用 C-YYYYMMDD-HHMM-A 格式
3. issue-sync promote 时创建 I-YYYYMMDD-HHMM-A
4. 门禁: candidate_key.startswith(raw_key)，candidate_key == issue_key（去前缀）
5. 历史 0000 格式不管

## C-20260428-1737-C: issue-sync promote 完整流程

- status: proposed
- scope: 一个脚本调用完成 raw→I 的全部 sync 操作
- type: 脚本
- priority: P0

### 核心逻辑

```
issue-sync promote raw-xxx:
  1. 读取 raw，找到所有已 promote 的 candidates
  2. 对每个 candidate:
     a. 创建 I-* issue.md 本地
     b. 创建平台 I-* issue（带 kind/linked 标签 + phase 标签）
     c. 回写 platform_ids
  3. 所有 candidates promote 完毕:
     a. 在 raw 平台 issue 上添加 closing comment:
        "拆解为以下任务: [I-xxx-A](url) [I-xxx-B](url)"
     b. 关闭 raw 平台 issue（GitHub + Gitee）
     c. 更新 raw 本地: status=absorbed
```

## C-20260428-1737-D: issue-sync pull + normalize

- status: proposed
- scope: 拉取平台 issue 和评论到本地；自动修正标签
- type: 脚本
- priority: P1

### 核心逻辑

```
issue-sync pull:
  1. 拉取 GitHub + Gitee open issues
  2. 合并去重（按 platform_ids 匹配本地已有 issue）
  3. 新 issue → 创建本地 raw-YYYYMMDD-HHMM
  4. 新评论 → 追加为本地 ### comment（status: pending）
  5. normalize: 无 kind/* 标签的平台 issue → 加 kind/raw
  6. I-* 格式标题但无 kind/linked 标签 → 仍按 raw 处理
```

## C-20260428-1737-E: 评论消费状态

- status: proposed
- scope: 评论 status 字段（pending/resolved/noted），scan 检查未消费评论
- type: 脚本 + AI prompt
- priority: P1

### 核心逻辑

```
本地 comment 元数据:
  {source: github, status: pending, platform_ids: {github: {comment_id: "12345"}}}

AI 消费:
  pending → 读取 → 判断 →
    resolved: 已回复解答
    noted: 仅记录
    new_raw: 超出范围，开新 raw，push reply

scan 检查:
  有 status=pending 的 comment → incomplete: "unresolved_comments:N"
```

## C-20260428-1737-F: 门禁 raw→C→M→I 链（GATE 6.3）

- status: proposed
- scope: governance-merge-gate 验证 raw→C→M→I 完整身份链
- type: 脚本
- priority: P1

### 核心逻辑

```
gate 检查:
  1. 每个 promoted candidate 必须有对应 raw，raw_key 前缀匹配
  2. I-* 的 promoted_from 指向 raw
  3. raw 的 status=absorbed（如果所有 C 都已 promote）
  4. raw 平台 issue 已关闭（如果已 promote 完毕）
```

## C-20260428-1737-G: 更新 three-loop 图

- status: proposed
- scope: three-loop-capability-lifecycle.md 补充 raw 入口、platform sync、promote、评论消费
- type: 文档
- priority: P2

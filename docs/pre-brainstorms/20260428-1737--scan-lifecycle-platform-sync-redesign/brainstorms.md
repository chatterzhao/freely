# Brainstorm: Scan Lifecycle + Platform Sync 重新设计

## 问题背景

当前 scan 和 sync 各自独立，存在 5 大缺陷：

1. **无生命周期关联**：raw→I-* 同一个工作项，扫出两个 item，AI 自己判断
2. **linked_issues 只扫评论**：phase_state 过期但无评论就不触发
3. **平台状态不交叉**：GitHub/Gitee open/closed 和本地 phase_state 无关联
4. **无统一 stage**：每个 scan 给碎片信息，AI 重新翻文档
5. **next_action 为空**：scan 不推导下一步，AI 每次重新判断

## 核心设计原则

### 1. 时间戳即身份

```
raw-20260428-1737         ← HHMM 时间格式
B1 dir: 20260428-1737--xxx  ← 复用 raw 的时间戳
I-20260428-1737-A           ← 复用 raw 的时间戳，加 split letter

同一个工作项三个阶段共享同一时间戳。
门禁通过 raw_key/issue_key/candidate_key 的 startswith 验证身份链。
```

### 2. 一个 Item 一条命

Scan 输出：每个工作项一个 item，包含完整生命周期定位。

```json
{
  "item_id": "20260428-1737",       // 共享时间戳 key
  "raw_id": "raw-20260428-1737",    // 可能为 null（平台直接创建的）
  "linked_id": "I-20260428-1737-A", // 可能为 null（未 promote）
  "lifecycle_stage": "B2_verifying",
  "next_action": "关闭 Gitee issue IJFOXX",
  "next_action_kind": "platform_close",
  "ready_for_worker": true
}
```

### 3. 区分"状态未改"和"事情没做"

```
情况 A：phase_state=completed, GitHub closed, Gitee OPEN
  → 事情做了，平台没收口
  → next_action: "issue-sync close gitee"

情况 B：phase_state=in_verification, 无 code-review
  → 真没做完
  → next_action: "完成验证：补充 code-review"
```

## 完整生命周期（8 个 Stage）

```
Stage 1: Raw 创建
  来源：chat 插话 / 平台 issue / runtime anomaly
  产物：docs/issues/raw-YYYYMMDD-HHMM/issue.md
        kind=raw, status=proposed
  判定：raw issue 存在
  
Stage 2: B1 proposed
  判定：raw 存在，无 B1 目录
  next_action: "进入 B1 预研"

Stage 3: B1 brainstorming
  判定：B1 目录存在，brainstorms.md 存在
  next_action: "产出 candidate"

Stage 4: B1 candidate
  判定：candidates.md 存在，candidate.status != terminal
  next_action: "决策 promote/absorb/drop"

Stage 5: Promote（B1→B2 过渡）
  本地：I-* 创建，raw.absorbed_into=I-*, milestones.md 更新
  平台：I-* issue 创建，raw issue 关闭，评论 sync
  判定：I-* 存在，platform_ids 有值

Stage 6: B2 implementation
  判定：phase_state in (in_b2_ibm, done_b2_ibm, in_dev, blocked_dev)
  next_action: "继续实现"

Stage 7: B2 verification
  判定：phase_state=in_verification
  next_action: "完成验证，准备收口"

Stage 8: Complete
  判定 ALL：
    phase_state=completed ✓
    GitHub I-* issue CLOSED ✓
    Gitee I-* issue CLOSED ✓
    所有本地评论有 platform_ids ✓
  缺少任一项 → Stage 7.5（收口中）
```

## 平台评论链路

```
本地 issue.md → ## Comments → ### comment-YYYYMMDDTHHMMSSZ
  {source: chat, platform_ids: {}}
  "评论文本"

    ↓ issue-sync comment

平台创建真实评论：
  GitHub: comment_id="12345"
  Gitee: comment_id="67890"

    ↓ 回写

本地 issue.md 更新：
  ### comment-YYYYMMDDTHHMMSSZ
  {source: chat, platform_ids: {github: {comment_id: "12345"}, gitee: {comment_id: "67890"}}}
  "评论文本"
```

关键规则：
- 评论永远以本地 `### comment-{local_id}` 为主键
- 平台 comment_id 是元数据，回写到 platform_ids
- 评论不同步到 issue description（body），始终作为平台"评论"
- Scan 通过 platform_ids 判断评论是否同步

## 多平台去重

当用户在 GitHub 和 Gitee 上同时有 issue：
- scan_external 拉取时检查本地是否已有相同 raw
- 匹配条件：title/content 相似度
- 已有 → 只更新 platform_ids（补上缺失平台）
- 无 → 创建新 raw

## 与现有代码的关系

| 模块 | 当前 | 重构后 |
|------|------|--------|
| task-source-scan.py | 8 个独立 scan 函数 | task-lifecycle-scan.py（统一） |
| issue-sync | 只做了 create/close | 加 comment sync + sync 回写 |
| 门禁 raw_key | 已有 | 强化 HHMM 格式校验 |
| 平台拉取 | scan_external_* | 加去重 + 评论拉取 |

## 待决策

1. HHMM 格式：是否强制新 ID 必须用 HHMM？（建议：是，历史不管）
2. B1 目录格式：`YYYYMMDD-HHMM--slug` vs `YYYYMMDD-0000--slug`？（建议：统一 HHMM）
3. 多平台去重：用 title 相似度还是 hash？（建议：title 模糊匹配 + 人工确认）
4. 平台→本地扫描：是否实现拉取平台评论到本地？（建议：需要，作为独立任务）

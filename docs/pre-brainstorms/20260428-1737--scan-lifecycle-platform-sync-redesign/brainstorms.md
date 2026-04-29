# Brainstorm: Issue 生命周期 + Scan + Platform Sync 完整设计

## 全局链路（脚本做的 vs AI 做的）

```
┌─ Phase 1: Raw 创建 ─────────────────────────────────────────────┐
│                                                                    │
│  来源 A: chat 插话                                                 │
│    [脚本] freely chat --new-issue                                  │
│    [脚本] _write_chat_to_issue → docs/issues/raw-YYYYMMDD-HHMM/   │
│    [脚本] issue-sync create raw-xxx → GitHub + Gitee             │
│    [脚本] issue-sync normalize → 确保平台有 kind/raw 标签          │
│                                                                    │
│  来源 B: 平台直接创建（人手动开 issue）                              │
│    [脚本] issue-sync pull → 拉取平台 open issues                   │
│    [脚本] 按 platform_ids 去重 → 无匹配则创建本地 raw               │
│    [脚本] issue-sync normalize → 补 kind/raw 标签                 │
│                                                                    │
│  来源 C: runtime anomaly / review 发现                             │
│    [脚本] 同来源 A（通过 chat 自动化）                              │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ Phase 2: B1 预研 ───────────────────────────────────────────────┐
│                                                                    │
│  [AI] 读取 raw issue，判断是否需要预研                              │
│  [AI] 创建 docs/pre-brainstorms/YYYYMMDD-HHMM--slug/              │
│  [AI] 写 brainstorms.md（发散→收敛→决策）                          │
│  [AI] 写 candidates.md（一个或多个 C-YYYYMMDD-HHMM-A/B/C）         │
│  [脚本] gate 检查 candidate_key.startswith(raw_key)               │
│                                                                    │
│  raw 状态变迁:                                                     │
│    status: proposed → (预研中) → (candidate 产出)                  │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ Phase 3: Promote（raw → I-*）────────────────────────────────────┐
│                                                                    │
│  [AI] 决策 promote C-xxx-A → I-xxx-A                               │
│  [脚本] issue-sync promote raw-xxx C-xxx-A → I-xxx-A              │
│    ① 本地创建 I-xxx-A/issue.md                                    │
│       kind=linked, promoted_from=raw-xxx, phase_state=in_b2_ibm    │
│    ② 平台创建 I-xxx-A（带 kind/linked 标签）                       │
│    ③ 回写 platform_ids 到本地 I-xxx-A                             │
│                                                                    │
│  所有 candidate 都 promote 完毕 →                                  │
│  [脚本] raw close on platforms:                                    │
│    ① 评论: "拆解为以下任务: [I-xxx-A](url) [I-xxx-B](url)"        │
│    ② 关闭 raw issue（GitHub + Gitee）                              │
│  [脚本] raw 本地: status=absorbed, absorbed_into 留空（多个子）    │
│                                                                    │
│  raw 关闭后 → 所有后续讨论在各自 I-* 下进行                        │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ Phase 4: B2 实现 ───────────────────────────────────────────────┐
│                                                                    │
│  [AI] worker 在 feature worktree 上开发                            │
│  [AI] 更新 phase_state: in_b2_ibm → done_b2_ibm → in_dev           │
│  [脚本] phase_state 变更时 issue-sync update I-xxx                 │
│  [脚本] 更新平台 issue 的 phase 标签                               │
│                                                                    │
│  评论处理:                                                         │
│  [脚本] issue-sync pull → 拉取平台评论 → 追加为本地 ### comment    │
│  [AI] 读取未消费评论，判断:                                        │
│    ├─ 回复解答 → [脚本] issue-sync comment push reply              │
│    ├─ 超出范围 → [AI] chat --new-issue 开新 raw                   │
│    ├─ 需要改 body → [AI] 修改 issue.md                            │
│    └─ 仅记录 → [AI] 标记 status: noted                            │
│  [AI] 标记评论 status: resolved / noted                            │
│  [脚本] scan 检查: 有未消费评论 → incomplete                       │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ Phase 5: 验证 + 完成 ───────────────────────────────────────────┐
│                                                                    │
│  [AI] worker 完成验证: phase_state=in_verification → completed    │
│  [脚本] merge-guarded hook:                                       │
│    issue-sync update I-xxx（更新 phase label）                     │
│    issue-sync close I-xxx（GitHub + Gitee CLOSED）                │
│  [脚本] milestones.md 移到 completed_issues                        │
│                                                                    │
│  [脚本] scan lifecycle check:                                      │
│    ALL: phase=completed + github closed + gitee closed            │
│         + all comments resolved + no unsynced comments             │
│    → 排除（已完成）                                                │
│    任一未满足 → 输出 item, 列出具体未完成项                        │
└────────────────────────────────────────────────────────────────────┘
```

## Scan 输出格式

一个 raw→I 链条一个 JSON 对象。只输出未完成的。完成的不出现。

```json
{
  "items": [
    {
      "key": "20260428-1737",
      "raw_id": "raw-20260428-1737",
      "stage": "promoting",
      "children": [
        {"linked_id": "I-20260428-1737-A", "phase_state": "in_dev", "platform_created": true},
        {"linked_id": "I-20260428-1737-B", "phase_state": null, "platform_created": false}
      ],
      "incomplete": [
        "child_I-20260428-1737-B_not_created_on_platform",
        "raw_still_open_on_github"
      ],
      "next_action": "issue-sync promote C-B → I-B; 所有 promote 完毕后关闭 raw",
      "ready": false
    }
  ]
}
```

## 评论生命周期

```
[脚本] pull 平台评论 → 本地 ### comment-YYYYMMDDTHHMMSSZ
  {source: <platform>, status: pending, platform_ids: {<plat>: {comment_id: "xxx"}}}

[AI] 读取 → 判断:
  resolved: 已回复解答，无需进一步行动
  noted: 已记录，不回复
  new_raw: 超出范围 → chat --new-issue → [脚本] push reply "已开 raw-xxx 跟进"

[脚本] scan: 有 status=pending 的评论 → incomplete: "unresolved_comments:N"
```

## 平台分类（标签判別）

```
[脚本] issue-sync pull 拉取平台 issue:

  if issue.labels 包含 "kind/linked" → I-*（freely 代码专属标签）
  else → raw

[脚本] issue-sync normalize:
  for each platform issue without kind/* label:
    add "kind/raw" label
  never add/remove "kind/linked"（only issue-sync promote does that）
```

## 新问题处理

```
插话 → [AI] 判断归属:
  ├─ 属于已有 I-* scope → comment 到该 I-*
  └─ 新问题 → chat --new-issue → 新 raw → 独立 B1 → 独立 I-*

raw 关闭后不再重开。新问题 = 新 raw = 新时间戳 = 新生命周期。
```

## AI 做 vs 脚本做

| 环节 | AI | 脚本 |
|------|-----|------|
| raw 创建 | 判断是否新开 | create + sync to platforms |
| B1 预研 | 发散收敛、写 brainstorms/candidates | gate 验证 ID 链 |
| promote | 决策 promote/absorb/drop | issue-sync promote（创建+关闭+评论） |
| 评论消费 | 读评论、判断回复/开新 raw | pull + push comment + 回写 ID |
| 实现 | 写代码、改文档 | issue-sync update phase/close |
| scan | 消费 scan 结果做路由判断 | 扫描所有源、输出 incomplete items |
| normalize | 无 | 补平台标签、去重 |

## 待实现候选

| ID | 内容 | 类型 | 优先级 |
|----|------|------|--------|
| C-1 | task-lifecycle-scan.py（统一 scan） | 脚本 | P0 |
| C-2 | 修复 ID 格式（HHMM + 后缀） | 脚本+文档 | P0 |
| C-3 | issue-sync promote 完整流程 | 脚本 | P0 |
| C-4 | issue-sync pull + normalize | 脚本 | P1 |
| C-5 | 评论消费状态（pending/resolved/noted） | 脚本+AI | P1 |
| C-6 | 门禁 raw→C→M→I 链 | 脚本 | P1 |
| C-7 | 更新 three-loop 图 | 文档 | P2 |

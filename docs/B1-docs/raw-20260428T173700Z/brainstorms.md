# Brainstorm: Issue 生命周期 + Scan + Platform Sync 完整设计

## 全局链路（脚本做的 vs AI 做的）

```
┌─ Phase 1: Raw 创建 ─────────────────────────────────────────────┐
│                                                                    │
│  来源 A: chat 插话                                                 │
│    [脚本] freely chat --new-issue                                  │
│    [脚本] _write_chat_to_issue → docs/B1-docs/raw-YYYYMMDD-HHMM/   │
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
│  [AI] 创建 docs/B1-docs/raw-YYYYMMDD-HHMM--slug/              │
│  [AI] 写 brainstorms.md（发散→收敛→决策）                          │
│  [AI] 写 candidates.md（一个或多个 C-YYYYMMDD-HHMM-A/B/C）         │
│  [脚本] gate 检查 candidate_key.startswith(raw_key)               │
│                                                                    │
│  raw 状态变迁（scan 通过文件存在性推导，不依赖单一状态字段）:       │
│    status=proposed + 无 B1 目录 → B1_proposed                       │
│    status=proposed + 有 B1 目录 → B1_brainstorming                  │
│    status=proposed + 有 candidates.md → B1_candidate                │
│    status=promoting + 部分 I-* 已创建 → promoting                   │
│    status=absorbed + 全部 I-* 创建 + raw 平台关闭 → 完成            │
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
│  [脚本] raw 本地更新:                                              │
│    status=absorbed                                                 │
│    promoted_children: ["I-xxx-A", "I-xxx-B"]  ← 多个子的列表       │
│    absorbed_into 留空（1:N 关系，不用单字段）                       │
│                                                                    │
│  注意：promote 是逐个进行的，不要求全部同时。                       │
│  每个 candidate promote 后就创建对应 I-*。                          │
│  每次 promote 后更新 raw frontmatter:                               │
│    promoted_children: ["I-xxx-A"] → ["I-xxx-A", "I-xxx-B"]         │
│  最后一个 promote 完成时触发 raw close。                            │
│  如果只 promote 了部分 → raw 保持 open → scan 显示 "promoting"     │
│                                                                    │
│  raw 关闭后 → 所有后续讨论在各自 I-* 下进行                         │
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
│    元数据: {source: <plat>, status: pending, platform_ids: {...}}  │
│  [AI] 读取 status=pending 的评论，判断:                             │
│    ├─ 回复解答 → 本地写 reply → [脚本] issue-sync comment push     │
│    │   → 回写 reply 的 platform_ids                                │
│    ├─ 超出范围 → [AI] chat --new-issue 开新 raw                    │
│    │   → [脚本] push reply "已开 raw-xxx 跟进"                     │
│    ├─ 需要改 body → [AI] 修改 issue.md → [脚本] issue-sync update │
│    └─ 仅记录 → [AI] 标记 status: noted                            │
│  [AI] 标记原评论 status: resolved / noted                          │
│  [脚本] scan: 有 status=pending 的评论 → incomplete                │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ Phase 5: 验证 + 完成 ───────────────────────────────────────────┐
│                                                                    │
│  [AI] worker 完成验证: phase_state=in_verification → completed    │
│  [脚本] pr-merge-guarded hook:                                       │
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
      "raw_id": "raw-20260428T173700Z",
      "stage": "promoting",
      "children": [
        {"linked_id": "I-20260428T173700Z-A", "phase_state": "in_dev", "platform_created": true},
        {"linked_id": "I-20260428T173700Z-B", "phase_state": null, "platform_created": false}
      ],
      "incomplete": [
        "child_I-20260428T173700Z-B_not_created_on_platform",
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

## 同步触发点总览

```
生命周期事件                  sync 动作                  防重机制
──────────────────────────────────────────────────────────────────
chat --new-issue             issue-sync create raw      platform_ids 检查
issue-sync pull 发现新平台 issue  本地创建 raw + normalize   platform_ids 匹配
candidate promote（逐个）     issue-sync promote single   I-* platform_ids 检查
最后一个 candidate promote   raw close + closing comment  raw platform_ids 检查
phase_state 变更             issue-sync update           content hash 比对
chat --issue 评论            issue-sync comment          comment platform_ids
merge to develop（hook）     issue-sync update + close   merge diff 中的 issue 列表
AI 回复评论                  issue-sync comment push     同上
AI 修改 issue body           issue-sync update           同上
issue-sync pull 发现新评论   追加本地 ### comment         comment platform_id 去重
```

所有 sync 由脚本/ hook 触发，不依赖 AI 判断。

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

详见 candidates.md。7 个 candidate（C-A ~ C-G），P0-P2 优先级。

| ID | 内容 | 类型 | 优先级 |
|----|------|------|--------|
| C-A | task-lifecycle-scan.py（统一 scan） | 脚本 | P0 |
| C-B | 修复 ID 格式（HHMM + 后缀） | 脚本+文档 | P0 |
| C-C | issue-sync promote 完整流程 | 脚本 | P0 |
| C-D | issue-sync pull + normalize | 脚本 | P1 |
| C-E | 评论消费状态（pending/resolved/noted） | 脚本+AI prompt | P1 |
| C-F | 门禁 raw→C→M→I 链（GATE 6.3） | 脚本 | P1 |
| C-G | 更新 three-loop 图 | 文档 | P2 |

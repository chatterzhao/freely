# Scan 输出设计

## 核心原则

**完成的不记，只记没完成的。一个 raw→I 链条一个 JSON 对象。**

```
scan 检查 completion checklist → 全部通过 → 不输出
                               → 任一未通过 → 输出，只列未通过项
```

## 输出格式

```json
{
  "items": [
    {
      "key": "20260428-1737",
      "stage": "B2_verifying",
      "raw_id": "raw-20260428-1737",
      "linked_id": "I-20260428-1737",
      "title": "修复 daemon 重启循环",
      "incomplete": ["gitee_issue_not_closed", "unsynced_comments: 2"],
      "next_action": "issue-sync close gitee; issue-sync comment 推送 2 条未同步评论",
      "ready": true
    },
    {
      "key": "20260428-1800",
      "stage": "B1_proposed",
      "raw_id": "raw-20260428-1800",
      "linked_id": null,
      "title": "scan 生命周期重构",
      "incomplete": ["no_b1_directory", "no_candidate", "not_promoted"],
      "next_action": "创建 B1 预研目录并开始发散收敛",
      "ready": true
    }
  ]
}
```

## Completion Checklist（8 项）

对于每个 raw→I 链条，检查以下 8 项。**全部通过 → 已完成，不输出。**

```
□ 1. raw_status_terminal
     raw 的 status 是 absorbed / dropped / completed
     如果 raw 不存在（平台直接创建的 I-*）→ N/A，算通过

□ 2. linked_exists
     I-* issue 已创建（kind=linked）
     如果 raw 被 absorb 到其他 I-* → 跟随 absorbed_into 检查那个 I-*

□ 3. phase_completed
     I-* 的 phase_state = "completed"
     如果 I-* 未创建 → 未通过

□ 4. github_closed
     I-* 的 GitHub issue 状态为 CLOSED
     如果 platform_ids 无 github → N/A

□ 5. gitee_closed
     I-* 的 Gitee issue 状态为 CLOSED
     如果 platform_ids 无 gitee → N/A

□ 6. raw_platform_closed
     raw issue 在平台上的状态为 CLOSED
     仅当 raw 曾被 sync 到平台时检查（platform_ids 非空）
     如果 raw 从未同步 → N/A

□ 7. comments_synced
     本地所有 ### comment 的 platform_ids 包含 github 和 gitee 的 comment_id
     last_synced_comment_at >= 最新本地 comment 时间

□ 8. milestone_completed
     milestones.md 中 issue 在 completed_issues 队列
     如果 issue 不在 milestone 中 → N/A
```

## 生命周期缺口分析

### 缺口 1：平台 raw 未被 pull

```
平台上有 open raw issue，但本地没有对应的 raw-*
→ 当前 scan 不可见（scan 只看本地）
→ 修复：scan 应检查 scan_external_* 结果
→ incomplete: ["raw_not_pulled_from_github"]
→ next_action: "issue-sync pull"
```

### 缺口 2：raw 已 promote 但平台 I-* 创建失败

```
本地 I-* 存在，platform_ids 为空
→ sync 失败或未执行
→ incomplete: ["platform_i_not_created"]
→ next_action: "issue-sync create I-xxx"
```

### 缺口 3：评论只在一侧平台同步

```
本地 comment 有 github comment_id 但无 gitee comment_id
→ incomplete: ["comment_not_synced_to_gitee"]
→ next_action: "issue-sync comment I-xxx"
```

### 缺口 4：I-* 存在但 canonical doc 缺失

```
I-* issue.md 的 canonical_issue_path 指向的文件不存在
→ 实现文档丢失
→ incomplete: ["canonical_doc_missing"]
→ next_action: "检查 epic docs 是否已删除或路径错误"
```

### 缺口 5：同一时间戳有多个 raw 或多个 I-*

```
raw-20260428-1737 和 raw-20260428-1737-2 同时存在
→ 重复创建（并发或 bug）
→ scan 应检测到重复并标记
→ incomplete: ["duplicate_raw"]
```

## Stage 判定逻辑

```
for each raw/I pair:
  if raw exists and status is proposed and no B1 dir:
    stage = "B1_proposed"
  elif B1 dir exists and no candidates.md:
    stage = "B1_brainstorming"
  elif candidates.md exists and candidate.status not terminal:
    stage = "B1_candidate"
  elif I-* exists and phase_state in (in_b2_ibm, done_b2_ibm, in_dev, blocked_dev):
    stage = "B2_active"
  elif I-* exists and phase_state == "in_verification":
    stage = "B2_verifying"
  elif I-* exists and phase_state == "completed":
    stage = "收口"  # checks 4-8 determine if truly done
  elif raw absorbed into existing I-*:
    stage = "absorbed"  # follow absorbed_into
  else:
    stage = "unknown"
```

## 与旧 scan 的区别

| | 旧 task-source-scan | 新 task-lifecycle-scan |
|---|---|---|
| 输出粒度 | 每个源一个 item | 一个 raw→I 一个 item |
| 完成项 | 全部列出 | 不输出 |
| 未完成项 | 不精确 | 精确列出具体 blockers |
| 平台状态 | 独立列表 | 交叉关联到 item |
| comment sync | 不检查 | 检查 platform_ids |
| stage | AI 判断 | scan 直接给出 |
| next_action | 读文档字段（常空） | scan 推导 |

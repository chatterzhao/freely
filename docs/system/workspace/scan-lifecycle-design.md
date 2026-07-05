# Scan Lifecycle — 统一任务扫描与进度定位

## 目标

一次 scan 输出每个工作项的**完整生命周期定位**，AI 不需要自己翻文档判断阶段。

```
scan → 输出:
  item_id: raw-20260428-1539
  lifecycle_stage: B1_proposed        ← AI 一眼知道在哪
  next_action: "进入 B1 预研"          ← AI 不需要猜
  next_action_kind: brainstorm
  ready_for_worker: false              ← 还不能委派 worker
```

## 5 个生命周期阶段

| stage | 含义 | 物理位置 | 下一步 |
|-------|------|---------|--------|
| `B1_proposed` | raw issue 待预研 | `docs/B1-docs/raw-*/` | 发散收敛 → candidate |
| `B1_brainstorming` | 预研进行中 | `docs/B1-docs/{id}/` | 产出 candidate |
| `B1_candidate` | candidate 待决策 | `docs/milestones.md candidate_issues` | promote/absorb/drop |
| `B2_active` | 正式 issue 执行中 | `docs/B2-docs/ibm/_legacy-issues/I-*/` , milestone committed | in_dev → in_verification |
| `B2_verifying` | 等待验证收口 | progress / code-review | 验证 → completed |
| `completed` | 已完成 | 全部标记 completed | 从 scan 排除 |

## 判定逻辑（按优先级）

### 第 1 步：收集所有 item

```
raw issues:    docs/B1-docs/raw-*/issue.md
linked issues: docs/B2-docs/ibm/_legacy-issues/I-*/issue.md  
pre_brainstorms: docs/B1-docs/*/
milestones:    docs/milestones.md
progress:      docs/B2-docs/**/*.md
platforms:     github/gitee issue state
```

### 第 2 步：交叉关联

```
raw-xxx → 查找 promoted_to 或 absorbed_into → 关联到 I-yyy
I-yyy   → 查找 canonical_issue_path → 关联到 epic issue doc
        → 查找 progress_path → 关联到 progress doc
        → 查找 platform_ids → 关联到 github/gitee issue
```

### 第 3 步：判定 stage

```
for each item:
  if raw issue:
    status=absorbed/dropped → skip（已完成）
    status=proposed, no brainstormal dir → B1_proposed
    有 brainstorm dir, no candidate → B1_brainstorming
    有 candidate, not promoted → B1_candidate
    有 promoted_issue_path → 合并到 I-* item

  if linked issue (I-*):
    phase_state=completed → skip
    phase_state in (in_b2_ibm, done_b2_ibm, in_dev, blocked_dev) → B2_active
    phase_state=in_verification → B2_verifying
    无 phase_state, status=completed, 平台未关闭 → B2_verifying（需收口）
    无 phase_state, status=completed, 平台已关闭 → skip

  if pre_brainstorm:
    无 candidate → B1_brainstorming
    有 candidate, status not terminal → B1_candidate

  if progress item:
    phase_state not terminal → B2_active or B2_verifying
```

### 第 4 步：输出

```json
{
  "scan_version": "lifecycle-v1",
  "generated_at": "...",
  "summary": {
    "total_active": 3,
    "by_stage": {"B1_proposed": 1, "B2_verifying": 2},
    "ready_for_worker": 1,
    "needs_human": 0
  },
  "items": [
    {
      "item_id": "I-20260419-1505-A",
      "lifecycle_stage": "B2_verifying",
      "phase_state": "in_verification",
      "next_action": "Close out verification: update phase_state to completed, close platform issues",
      "next_action_kind": "closeout",
      "ready_for_worker": true,
      "owner_hint": "worker",
      "cross_refs": {
        "linked_issue": "docs/B2-docs/ibm/_legacy-issues/I-20260419-1505-A/issue.md",
        "github_issue": "#156 (closed)",
        "gitee_issue": "IJFOxx (open)"
      }
    }
  ]
}
```

## 与原 scan 的区别

| 维度 | 原 scan | 新 scan |
|------|--------|---------|
| 输出粒度 | 每个源一个 item（同一个东西扫出多个） | 每个工作项一个 item |
| 阶段判定 | AI 自己翻文档判断 | scan 直接给出 stage |
| next_action | 从文档字段读（常为空） | scan 推导 |
| 平台关联 | 独立列表 | 交叉关联到 item |
| token 节省 | AI 需读 3-5 个文档 | 一次 scan 全部定位 |

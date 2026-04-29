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

## 门禁链：raw → C → M → I

当前门禁验证 C → M → I（candidate → milestone → issue）。需要扩展为 **raw → C → M → I**。

```
raw-20260428-1737          raw_key → "20260428-1737"
C-20260428-1737-A           candidate_key → "20260428-1737-A"
I-20260428-1737-A           issue_key → "20260428-1737-A"

门禁验证：
  candidate_key.startswith(raw_key)      → "20260428-1737-A" starts with "20260428-1737" ✓
  issue_key.startswith(raw_key)          → same check ✓
  milestones.md 中 issue 有 promoted_from 指向 raw ✓
  raw issue 的 absorbed_into 指向 I-*  ✓
```

新增 gate GATE 6.3：raw→I 身份链完整性。

## 双向同步设计

同步不依赖 AI——全部由脚本和 hook 驱动。

### Push（本地 → 平台）

```
触发点                动作                         防重
─────────────────────────────────────────────────────────
chat --new-issue      issue-sync create raw-*      检查 platform_ids 是否已有
candidate promoted    issue-sync promote raw→I     检查 I-* 是否已创建
phase_state 变更       issue-sync update             检查 content hash 是否变化
chat --issue 评论      issue-sync comment            检查 comment platform_ids 是否已有
merge to develop      issue-sync close + update     merge-guarded hook 触发
```

推送后回写：
- create → 回写 `platform_ids.{platform}.issue_id`
- comment → 回写 `platform_ids.{platform}.comment_id` 到对应 ### comment 元数据
- close → 更新 `updated_at`

### Pull（平台 → 本地）

```
issue-sync pull：
  1. 拉取 GitHub open issues
  2. 拉取 Gitee open issues
  3. 合并去重：
     - 按 platform_ids 匹配本地已有 issue → 只更新状态
     - 无匹配 → 创建 raw-YYYYMMDD-HHMM（仅 raw，不创建 I-*）
     - I-* 格式标题的 issue → 仍当 raw 处理（平台不应有外部 I-*）
  4. 拉取评论：
     - 按 comment platform_id 匹配本地 ### comment
     - 已有的 comment_id → 跳过
     - 新的 comment_id → 追加为 ### comment-{新本地ID}
```

## 防重设计（四层）

### 第 1 层：Issue 创建防重（平台侧）

```
push create 前：
  if platform_ids.{platform}.issue_id 已存在 → SKIP
  if .scan-state 中 synced_issues 有此 ID + hash 匹配 → SKIP

push create 后：
  回写 platform_ids 到本地 issue.md frontmatter
  更新 .scan-state synced_issues hash
```

### 第 2 层：Issue 拉取防重（本地侧）

```
pull create 前：
  if 本地已有 issue 的 platform_ids 包含此平台 issue → SKIP
  if 本地已有同 title 的 raw → MERGE（补 platform_ids）
  if 无匹配 → CREATE raw-YYYYMMDD-HHMM
```

### 第 3 层：评论推送防重（平台侧）

```
push comment 前：
  if ### comment 的 platform_ids.{platform}.comment_id 存在 → SKIP
  if last_synced_comment_at.{platform} >= comment 时间 → SKIP

push comment 后：
  回写 platform_ids.{platform}.comment_id 到 comment 元数据行
  更新 last_synced_comment_at.{platform}
```

### 第 4 层：评论拉取防重（本地侧）

```
pull comment 前：
  if 本地已有 ### comment 的 platform_ids 包含此 comment_id → SKIP
  
pull comment 后：
  创建 ### comment-YYYYMMDDTHHMMSSZ（新本地 ID）
  元数据：{source: <platform>, platform_ids: {<platform>: {comment_id: "xxx"}}}
```

## 评论规范

```
规则 1：评论永远不写到 issue description（body）
  平台 issue body = 元数据表 + 摘要 + 链接
  评论 = 平台原生"评论"功能

规则 2：本地主键 = ### comment-YYYYMMDDTHHMMSSZ
  本地 ID 在创建时立即生成，不依赖平台返回

规则 3：平台 ID 是回写元数据
  {platform_ids: {github: {comment_id: "12345"}, gitee: {comment_id: "67890"}}}
```

## 双平台对齐

```
保证两边一致的原则：
  1. 本地是真相源，平台是镜像
  2. push 同时推到两个平台（对称）
  3. pull 从两个平台拉取，合并到本地
  4. 合并逻辑：
     - 同一 issue 在两个平台都有 → platform_ids 包含两边 ID
     - 一边有评论另一边没有 → push 补齐缺失平台的评论
     - 两边都有同一评论 → 按 comment_id 去重（不重复创建本地 comment）
```

## 平台保护

```
规则：
  - 平台上只允许 raw-* 类型的外部创建（人类/其他系统）
  - I-* 类型 issue 只能由 freely 的 issue-sync promote 创建
  - pull 时检测到 I-* 格式标题 → 视为 raw 处理（当作外部误操作）
  - 禁止在平台上手动创建 I-* 格式的 issue
```

## 待决策

1. HHMM 格式：是否强制新 ID 必须用 HHMM？（建议：是，历史不管）
2. B1 目录格式：`YYYYMMDD-HHMM--slug` vs `YYYYMMDD-0000--slug`？（建议：统一 HHMM）
3. 多平台去重：用 title 相似度还是 hash？（建议：title 模糊匹配 + 人工确认）
4. 平台→本地扫描：是否实现拉取平台评论到本地？（建议：需要，作为独立任务）
5. 门禁扩展 raw→C→M→I：是否需要新增 GATE？（建议：需要，作为独立候选）

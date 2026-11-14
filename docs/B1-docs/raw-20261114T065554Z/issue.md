---
schema_version: '1'
local_id: raw-20261114T065554Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T065554Z-A
platform_ids:
  github:
    issue_id: '4642'
    url: https://github.com/chatterzhao/freely/issues/4642
    synced_at: ''
  gitee:
    issue_id: IKVANY
    url: https://gitee.com/zhaoquan/freely/issues/IKVANY
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261114T065554Z/issues/I-20261114T065554Z-A.md
last_synced_comment_at:
  github: '2026-11-14T07:29:24Z'
  gitee: '2026-11-14T07:29:24Z'
hash: ''
created_at: '2026-11-14T06:55:54Z'
updated_at: '2026-11-14T07:29:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T065554Z-A
source_candidate: ''
completed_at: '2026-11-14T07:29:24Z'
closeout_note: ''
severity: P1
---

# fix: wt-close 误判 merge 后追加提交，缺补合并优先路径

workflow_kind: fix

## fix: wt-close 误判 merge 后追加提交，缺补合并优先路径

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T065554Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T06:55:54Z |
| updated | 2026-11-14T06:55:54Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T065554Z`。实现前请用 `wt-create --raw-key 20261114T065554Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（本轮真实案例，差点白干）

R33.16 的 PR #4442 已合并到 develop，但分支上有一个 **merge 之后追加的提交** `712e7550c`（`chore: record the last synced comment watermark`），内容只有 3 个副本字段：`platform_state: closed`、`last_synced_comment_at`、`updated_at`。

`wt-close` 报「未合并提交」，我一度按 `--discard-unmerged` 方案准备丢弃。用户追问「既然是提交，就要判断是否有用，没有用又不合并要有理由丢弃，否则不是白干了」——复核后发现：**这个提交内容是正确的、且 develop 正缺它**，正确解法是把 develop 合进分支后补一个 PR（#4641）合并进去，最后 `wt-close` 干净收口，无需任何强制参数。

## 查证：规范不存在（已读源码确认）

| 位置 | 现状 | 缺口 |
|---|---|---|
| `docs/system/workspace/scripts/worktree/wt-close:782-813`（未合并提交守卫） | 提示语断言「没有 merge」「大概率是 pr-merge-guarded 还没执行成功」；保留工作只有 `freely chat --new-issue "extract: ..."` | **没有「补合并 PR」路径**；把「已 merge + 追加提交」误报成「没 merge」 |
| `wt-close:1290-1306`（第二处提示） | 一律「分支未合并到 develop，无法安全删除」+ 直接给出 `--force --discard-unmerged` 命令 | 同上，且**主动诱导丢弃** |
| `wt-close:427` 合法理由清单 | `--discard-unmerged` 只有「该方案已被否决，未合并的提交确认不再需要」 | 把「丢弃」等同于「方案被否决」；本轮提交是正确副本状态，不属于此类，却只能套这条理由 |
| `wt-close:442-445` `_require_reason` | 只校验 `--reason` 前缀格式 | 不校验「逐提交判定」，理由可笼统填写 |
| `docs/system/workspace/commands.md:193-194` | 仅 `--force` / `--discard-unmerged` 语法说明 | 无决策规范 |
| `skills/freely-workflow-guarded-execution/SKILL.md:270-275` 阶段 9 | 只有两行收口命令 | 无 merge 后残留提交的处理 |
| `docs/LAWS.md` | 只有「依赖未合并父分支」的派生工位规则 | 不同主题 |

**结论**：能力面里只有「丢弃」及其理由模板，没有「merge 后提交先判断是否有用、优先补合并」这条规范。会话 goal 里写的纪律不是能力面，不会约束下一次执行。

## 关键发现：不是能力不足，是已有信息没接线

`wt-close:198-201` 已经能判断这个 raw 是否 merge 过：

```bash
_merge_count=$(git -C "$PROJECT_ROOT" rev-list develop --merges --grep "raw-${target_key}" --count ...)
[[ "$_merge_count" -gt 0 ]] && _has_merge=true
```

但这段逻辑只用于别处（closeout gate），**未合并提交守卫没有用它**，所以「PR 已 merge + 之后追加提交」被误判成「从来没 merge」。

## 期望：三层落地，权威只在 skill

### 1. 声明层（规范权威）— `freely-workflow-guarded-execution` 阶段 9 新增一节

该 skill 自称「流程唯一权威」（SKILL.md:42），规范必须在这里定义：

1. **先分情形**：`_has_merge` 为真且存在 `develop..branch` 提交 → 是「PR 已 merge + 追加提交」，**不是**「没 merge」；
2. **逐提交判定**（不能一刀切）：
   - 内容有用 → **优先补合并 PR**：`git merge develop` → `pr-create-guarded` → review → `pr-merge-guarded` → 正常 `wt-close`；
   - 内容确实无用 → 必须说明**哪个提交、为什么无价值**，不能套「方案被否决」模板；
   - 内容已等价落盘（见下）→ 允许丢弃，零损失；
3. **顺序铁律**：先落盘、再丢弃；顺序反了就是真丢数据；
4. **two-dot diff 坑**（本轮实测）：`governance-merge-gate --range develop..HEAD` 用 two-dot，分支落后 develop 时会把 develop 的新提交算成反向差异，看着像夹带 `bin/`、`runtime/` 等实现改动。**先 `git merge develop` 再判**，diff 就只剩真实改动，本轮 rc=0 直接通过、无需任何 skip。

### 2. 执行层（机器约束）— `wt-close` 未合并提交守卫

- 用 `_has_merge` 区分两种情形，打印不同诊断，纠正「大概率没 merge」的误导；
- **用可验证事实代替人工填理由**：对 `develop..branch` 的每个提交算 `git patch-id`，与 develop 比对；
  - 已等价包含 → 允许 `--discard-unmerged`（内容已落盘，零损失），并在输出里列出比对结果；
  - 未包含 → **默认拒绝丢弃**，提示补合并 PR 的具体命令；仅当显式给出「工作已另行抽取」的 raw issue 编号才放行；
- 这样既防「乱丢」，又**不是补字段就过**（用户明确反对强制字段式门禁）：校验的是 git 事实，不是人类填写的文字。

### 3. 提示层 — 两处报错提示语

负责把规范喊出来并**追问清楚**（不是只给 `--force` 命令）：
- 列出每个未合并提交的 hash + subject；
- 逐条问：有用？→ 给补合并命令；已落盘？→ 给比对结果；无用？→ 要求写明该 hash 与具体理由；
- 附上「先 merge develop 再判」与 two-dot diff 提示。

### 4. 同步

- `commands.md` 的 `--discard-unmerged` 说明补「仅当内容已等价落盘或已另行抽取」；
- `wt-close` 的合法理由清单（420-438）补「内容已等价落盘」一类，删掉把「丢弃」等同于「方案被否决」的隐含假设；
- `wt-close` USAGE（51 行）同步。

## 验收（AT，带基线红）

1. 「PR 已 merge + 追加提交」场景：守卫**不得**打印「没有 merge / pr-merge-guarded 未成功」，必须打印「已 merge，有 N 个追加提交」；
2. 追加提交的 patch-id 已被 develop 包含 → 允许丢弃并列出比对证据；未包含 → 拒绝丢弃且提示补合并命令；
3. 「从未 merge」场景保持原提示强度（不得放宽）；
4. 提示语含逐提交 hash + 补合并命令 + two-dot diff 说明；
5. skill 阶段 9 / commands.md / 合法理由清单三处文本与实现一致（静态断言）；
6. 基线（develop）各条红。

## 边界

- **不放宽** `--force` / `--discard-unmerged` 的现有拒绝判定；本轮是收紧；
- 不改 GATE 1、不改 `pr-merge-guarded`、不改 verdict 契约；
- 不把「逐提交判定」做成可补字段通过的门禁（用 patch-id 事实校验）；

### comment-20261114T072924Z
- source: system
- event: promote_finalized
- children: ["I-20261114T065554Z-A"]

拆解为以下任务:
1. [I-20261114T065554Z-A](will-be-updated)

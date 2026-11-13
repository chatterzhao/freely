---
schema_version: '1'
local_id: raw-20261113T115957Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T115957Z-A
platform_ids:
  github:
    issue_id: '4343'
    url: https://github.com/chatterzhao/freely/issues/4343
    synced_at: ''
  gitee:
    issue_id: IKV7I5
    url: https://gitee.com/zhaoquan/freely/issues/IKV7I5
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T115957Z/issues/I-20261113T115957Z-A.md
last_synced_comment_at:
  github: '2026-11-13T12:05:51Z'
  gitee: '2026-11-13T12:05:51Z'
hash: ''
created_at: '2026-11-13T11:59:57Z'
updated_at: '2026-11-13T12:12:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T115957Z-A
source_candidate: ''
completed_at: '2026-11-13T12:05:51Z'
closeout_note: ''
severity: P1
---

# fix: wt-close 未收口全部 I-* children 且路径错误，会删掉未完成的工位

workflow_kind: fix

## fix: wt-close 未收口全部 I-* children 且路径错误，会删掉未完成的工位

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T115957Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T11:59:57Z |
| updated | 2026-11-13T11:59:57Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T115957Z`。实现前请用 `wt-create --raw-key 20261113T115957Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

一个 raw issue 可以 promote 出多个 I-*（promoted_children: [A, B, ...]），但**一个 raw 只有一个 worktree**。wt-close 删除 worktree 之后，未完成的 I-* 就再也没有工位可以实现。

审计 docs/system/workspace/scripts/worktree/wt-close 后发现三处实现缺陷（**设计本身是完整的**）：

### 缺陷 1：I-* 文档路径写错，整段关闭逻辑永不执行

wt-close 第 949 行附近：

    _wt_i_file="$wt_path/docs/B1-docs/$_wt_i_absorbed_i/issue.md"
    [[ -f "$_wt_i_file" ]] || _wt_i_file="$PROJECT_ROOT/docs/B1-docs/$_wt_i_absorbed_i/issue.md"

但 I-* 文档的实际位置是 docs/B2-docs/{epic}/{story}/raw-{key}/issues/I-{key}-{suffix}.md（issue-sync 的 _issue_file_for 就是这么解析的）。
实测：docs/B1-docs/I-20261112T031638Z-A/issue.md 不存在 → 两个候选路径都不存在 → 整段「Also close the absorbed I-* issue」被跳过，什么也没关。

### 缺陷 2：只关 absorbed_into 一个，漏掉 promoted_children 其余

    _wt_i_absorbed_i="$(_fm_get "$issue_file" "absorbed_into")"

absorbed_into 是单个值（promote-finalize 选定的 canonical child），而 raw 的 promoted_children 是列表。
实测 raw-20261112T031638Z：absorbed_into 为 I-...-A，promoted_children 为 [I-...-A, I-...-B] → B 永远不会被这段逻辑关闭。
这正是「linked 残留（phase_state: completed 却仍 OPEN）」反复出现的直接原因。

### 缺陷 3：「must already be terminal」只是注释，没有实现

wt-close Phase 3 注释：

    # Raw and linked issue metadata must already be terminal before cleanup starts.
    # wt-close performs platform/worktree cleanup only and never writes issue files.

但 Phase 1 只检查 **raw** 的 phase_state，没有任何代码遍历 children。
若某个 I-* 仍是 in_dev，wt-close 会照常删 worktree（以及 test 工位），该 I-* 从此无法实现，且没有任何告警。

## 设计意图（已核实）

- bin/issue-sync 头注释：B1 promotion_started (1:N children) → promotion_finalized (absorbed/open) → configured-platform close。
- cmd-promote-finalize.sh：关闭 raw 前会把 promoted_children 列成 comment，说明 children 是**集合**而非单个。
- wt-close 自己的注释与函数 _close_platform_ids_readonly（读 platform_ids → adapter close-multi）都证明：作者**已经设计**了「wt-close 关闭 I-*」，只是实现没接对。

## 期望（按设计补实现，不放宽门禁）

1. wt-close 解析 promoted_children（列表），用 issue-sync 同一套解析器（_issue_file_for 或等价的 B2 路径查找）定位每个 I-* 文档。
2. **前置检查（新增门禁）**：删除任何工位前，遍历全部 children：
   - 每个 child 的 phase_state 必须是终态（completed / dropped）；
   - 任一非终态 → **拒绝 wt-close**，打印「哪个 I-* 还没完成、应回到工位继续实现」，并给出可执行命令；
   - 这比现状更严：现状是静默删工位、把未完成 I-* 变成孤儿。
3. **封装关闭**：对终态且 platform_state != closed 的每个 child，用 _close_platform_ids_readonly 逐个关闭（复用现有单点，不新开通道）；单个失败则停止并保留工位（fail-closed）。
4. 关闭后再走原有 Phase 4/5/6 清理；--dry-run 全程零副作用；--force 的语义不变（但仍应先打印未完成 children 清单）。
5. AT：
   - 2 个 children（A completed 未关、B completed 未关）→ wt-close 后**两个**都关闭，且调用次数为 2；
   - 一个 child in_dev → wt-close 拒绝、工位仍在、平台零写入（负向控制）；
   - I-* 文档位于 B2-docs 时能被正确定位（路径回归）；
   - 基线（develop）同场景下：A 未被关（路径错）、B 未被关（只取 absorbed_into）、in_dev 也能删工位 —— 三条红。

## 边界

- 不改 raw 的 validate() 与 promote/promote-finalize 语义；
- 不改 issue-sync batch 的 linked 分支（batch 仍是批量兜底路径），但 wt-close 必须能独立完成本 raw 的 children 收口；
- 不手工关平台 issue；不放宽 protected branch / reason gate / closeout gate；
- 需要更新 test-wt-close-protected-branch-guard 或新增 AT 时，保持既有断言强度。

### comment-20261113T120551Z
- source: system
- event: promote_finalized
- children: ["I-20261113T115957Z-A"]

拆解为以下任务:
1. [I-20261113T115957Z-A](will-be-updated)

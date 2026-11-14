---
schema_version: '1'
local_id: raw-20261114T033013Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T033013Z-A
platform_ids:
  github:
    issue_id: '4554'
    url: https://github.com/chatterzhao/freely/issues/4554
    synced_at: ''
  gitee:
    issue_id: IKV9OU
    url: https://gitee.com/zhaoquan/freely/issues/IKV9OU
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261114T033013Z/issues/I-20261114T033013Z-A.md
last_synced_comment_at:
  github: '2026-11-14T03:48:24Z'
  gitee: '2026-11-14T03:48:24Z'
hash: ''
created_at: '2026-11-14T03:30:13Z'
updated_at: '2026-11-14T03:56:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T033013Z-A
source_candidate: ''
completed_at: '2026-11-14T03:48:23Z'
closeout_note: ''
severity: P1
---

# fix: I-* 收口链路三处实现与设计不一致

workflow_kind: fix

## fix: I-* 收口链路三处实现与设计不一致

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T033013Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T03:30:13Z |
| updated | 2026-11-14T03:30:13Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T033013Z`。实现前请用 `wt-create --raw-key 20261114T033013Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 设计意图（先对齐，再判缺陷）

来自 `docs/system/workspace/ibm-framework.md` 与 `bin/issue-sync` 头注释：

1. **本地文档是唯一真相源，平台是 replica**；`issue-sync` 是唯一本地→平台桥梁。
2. **sync 由确定性生命周期事件驱动**，不是 AI 判断。事件表原文：
   - `phase_state 变更` → `issue-sync update`（daemon worker 完成状态更新后）
   - `merge 到 develop` → `issue-sync close`（关闭已完成的 I-*），触发者是 **pr-merge-guarded post-merge hook**
   - `cleanup 完成` → `issue-sync close`
3. `platform_state` 字段语义（同文档字段表）：「平台同步状态 open|closed。**由 issue-sync create/close 自动管理**」——对 raw 与 I-* 同等适用。
4. `raw_lifecycle_effects.close_linked` 文档字符串：「`issue-sync batch` drives the retirement with the SAME phase_state == completed predicate」——linked 收口判据是 `completed`。
5. `wt-close` 的既有契约（`wt-close:906-924`）：「pr-merge-guarded writes platform_state: closed to the worktree **before merge**」；若缺失，wt-close 应当拒绝并提示走正规流程。

## 三处实现与该意图不一致（已逐条验证）

### 1. merge hook 看不到 B2 的 linked 文档 → 「merge 关闭已完成 I-*」从未发生

`pr-merge-guarded` 的 post-merge sync：

```bash
changed_issues=$(git diff --name-only "$_target" "$_src_branch" -- "docs/B1-docs" ...)
issue_file="$issues_dir/$local_id/issue.md"
```

只扫 `docs/B1-docs`，而 linked 文档在 `docs/B2-docs/**/issues/I-*.md`。所以 `case` 里的
`linked/in_dev`、`linked/completed` 等分支是**不可达代码**——设计里「merge 时关闭
completed I-*」永远不会触发。这是 linked 残留的根因，而 `batch` 成了唯一补救。

附带两处同源问题：
- 同步后只 `git add docs/B1-docs/`，即使改了 B2 文档也不会提交，工位必然变脏。
- 它调用 `issue-sync close <I-id>`，而 `cmd_close` 已按 R33.12 拒绝 linked（单一驱动原则）→ 即使能看到也会失败。

### 2. `cmd-create` 不给 linked 写 `platform_state` → 收口判据永远缺一半

`bin/issue-sync.d/cmd-create.sh:122-126`（develop 现状）：

```bash
# `platform_state` is a raw-issue field; linked I-* documents do not declare
# it and adding it would silently change their schema.
if _fm_has_key "$file" "platform_state"; then
  _fm_set_str "$file" "platform_state" "open"
fi
```

与字段表「由 issue-sync create/close 自动管理（raw 与 I-* 同）」直接矛盾。
后果：新建的 I-* 没有 `platform_state`，`wt-close` 的 children 预检必判「未关闭」，
必须人工跑一次 `batch` 才能通过。

（说明：R33.18 的 review 声称 FR-1 已完成，实际该改动在同轮 `git reset --hard` 中丢失。
这是实现与陈述偏离，本轮一并纠正，并在验收里断言字段真的被写入。）

### 3. `wt-close` 的 children 预检读 `develop` 副本，而不是被关闭工位的副本

`wt-close:964`：`_wt_children_report="$(python3 - "$PROJECT_ROOT" "$issue_file" ...)"`，
glob 的是 `$PROJECT_ROOT/docs/B2-docs/**`。

但 `platform_state` 是工位内由 merge 前同步写入、随分支合并才到 develop 的；
若分支上有任何未合并的状态（或 merge 时同步缺失），预检读到的就是旧值。
实测 R33.16：工位副本 `platform_state: closed`，develop 副本无该字段 → wt-close 拒绝，
而平台侧 #4441 已是 CLOSED。

关闭语义上，**工位副本才是被裁决对象的当前状态**，develop 只是它的祖先。

## 期望（三处一起改，保持单一驱动与单一真相源）

1. **merge hook 覆盖 B2**：`changed_issues` 同时扫描本 lane 的 `docs/B2-docs/**/issues/I-*.md`；对 linked 只做「phase 推进」（`in_dev|in_b2_ibm|done_b2_ibm` → `in_verification`），收口交给 `issue-sync batch <raw-key>`（单一驱动，判据 `completed`）；同步后 `git add docs/B1-docs/ docs/B2-docs/`（仅本 lane 路径）并 push，使 merge 完成时工位已干净、develop 已带 `platform_state: closed`。
2. **`cmd-create` 对 linked 也写 `platform_state: open`**，去掉 `_fm_has_key` 守卫，并在注释里引用字段表。
3. **`wt-close` 预检优先读工位副本**（`$wt_path` → 回退 `$PROJECT_ROOT`），并在拒绝消息里区分「工位也未关闭」与「develop 落后」。
4. AT（每条都要有基线红）：
   - merge hook：本 lane 内一个 `completed` linked + 一个 `in_dev` linked → 前者被关闭、后者推进到 `in_verification`；**其它 raw 的文档零变更**；
   - create：新建 linked 后 `platform_state: open` 必须存在（负向控制：raw 行为不变）；
   - wt-close：工位副本 closed / develop 缺失 → 通过；工位副本缺失 → 拒绝。

## 边界

- 不放宽 GATE 1；不让 merge hook 关闭非本 lane 的 issue（沿用 `issue-sync-scope.py`）；
- 不改 `close_linked` 的 `phase_state == completed` 判据；
- 不恢复「`issue-sync close` 直连 linked」第二通道；
- 不手工关平台 issue、不手工造字段。

### comment-20261114T034824Z
- source: system
- event: promote_finalized
- children: ["I-20261114T033013Z-A"]

拆解为以下任务:
1. [I-20261114T033013Z-A](will-be-updated)

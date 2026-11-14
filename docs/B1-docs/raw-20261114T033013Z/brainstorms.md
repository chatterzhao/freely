# B1 Brainstorm — raw-20261114T033013Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `docs/system/workspace/ibm-framework.md`——「本地是唯一真相源。平台数据丢失时从本地重建」；「sync 触发是确定性的生命周期事件（candidate promoted、phase_state 变更、merge），不是 AI 判断」；事件表「merge 到 develop → `issue-sync close`（关闭已完成的 I-*）→ `pr-merge-guarded` post-merge hook」；字段表「`platform_state` … 由 issue-sync create/close 自动管理」。
  - 既有验收测试: `test-wt-close-children.py`（children 必须 completed + 已关闭才允许删工位）；`test-issue-sync-close-linked.py`（linked 只能由 batch 收口）。
  - 门禁源码注释/理由: `raw_lifecycle_effects.close_linked`——「`issue-sync batch` drives the retirement with the SAME phase_state == completed predicate」；`wt-close:906`——「pr-merge-guarded writes platform_state: closed to the worktree **before merge**」。
  - 既有同类实现: `pr-merge-guarded::_sync_issues_changed_in_merge` 自身的 `linked/*` case（设计存在，不可达）；`issue-sync-scope.py`（按 raw-key 限定范围）。
  - 配置约束: 无。
- 判定（五分类）: **实现未完成**（merge hook 的 B2 覆盖面缺失）+ **实现偏差**（cmd-create 的 linked 分支被 `_fm_has_key` 挡住）+ **bug**（wt-close 预检读错副本）。三者同属「I-* 收口链路」，设计本身正确。
- 与既有断言的冲突: 无。本轮不修改任何既有断言，只补齐未实现的分支与读取源。
- 影响面: `pr-merge-guarded`、`bin/issue-sync.d/cmd-create.sh`、`wt-close`；新增 `scripts/worktree/merge_issue_sync.py` 与一条 AT。不改 `close_linked` 判据、不放宽 GATE 1。

## 1. 问题（三处，同一条链路）

### 1.1 merge hook 看不到 B2（本轮主目标）

`_sync_issues_changed_in_merge` 只 `git diff -- docs/B1-docs`，而 linked 文档在 `docs/B2-docs/**/issues/I-*.md`。
因此 `case` 里的 `linked/in_dev`、`linked/completed` 等分支**永远不可达**：
- 「merge 时关闭已完成 I-*」从未发生 → linked 残留；
- 同步后只 `git add docs/B1-docs/`，B2 变更不会进提交 → 工位必脏；
- 分支里还调 `issue-sync close <I-id>`，而 R33.12 已让 `cmd_close` 拒绝 linked → 即使能看到也会失败。

### 1.2 `cmd-create` 不给 linked 写 `platform_state`

`if _fm_has_key "$file" "platform_state"` 使新建 I-* 永远没有该字段，与字段表矛盾；
`wt-close` 预检必判「未关闭」，只能人工补跑 batch。

### 1.3 `wt-close` 预检读 develop 副本

`_wt_children_report` 用 `$PROJECT_ROOT` glob。但 `platform_state` 是工位内写入、随 merge 才进 develop；
R33.16 实测：工位 `closed`、develop 缺失、平台已 CLOSED，却被拒绝。

## 2. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 抽取纯 Python 决策模块 `merge_issue_sync.py`（发现 / 判定 / 落 phase），hook 调它；linked 收口统一调 `issue-sync batch <raw-key>`；只 `git add` 被改的文档 | 可单测、单一驱动、范围可控 ✅ |
| B | 直接在 bash 里把 `-- docs/B1-docs` 改成两个目录 | 仍不可测；`git add` 范围仍会误带其他 raw |
| C | 让 hook 调 `issue-sync close` 关 linked | 恢复第二通道，违反 R33.12 的单一驱动 |

采用 A。

## 3. 关键取舍

1. **只推进 phase，不直接关单**：linked 的收口判据是 `completed`，推进（`in_dev → in_verification`）与关闭是两件事；关闭交给 `batch <raw-key>`，与 `close_linked` 的文档字符串一致。
2. **只 `git add` 本轮真正改过的文件**，不用 `git add docs/B2-docs/`——否则会把 daemon 无范围 batch 写脏的其他 raw 文档一起带进 PR，直接撞 GATE 1。
3. **orphaned branch（无 raw key）保持旧行为**：只处理 B1，不调用 batch（无法限定范围）。
4. **phase 写入用行替换**，不用 `yaml.dump`：raw 的 strict 契约要求字段集合与顺序，重排会判红。

## 4. 证伪

- 「hook 已经能关 linked」→ 否：diff 只看 B1，且 close 对 linked 会报错。
- 「只要把 `git add` 扩到 B2 就行」→ 否：不发现 B2 就没有可 add 的内容；而且盲目 add 会带上其他 raw。
- 「直接让 batch 全量跑」→ 否：违反 GATE 1，且会跨 raw 改文档（已实测污染 100+ 文件）。

## 5. 边界

- 不改 `close_linked` 的 `completed` 判据；不恢复 `issue-sync close` 直连 linked；
- 不放宽 GATE 1；不手工关平台 issue；
- daemon 无范围 batch 的问题由 `raw-20261114T031043Z` 单独处理，不夹带。
## 6. 修正记录（P0 复核推翻了一个方向）

本轮初稿曾把「`wt-close` 预检优先读工位副本」当成 bug 修（理由：R33.16 工位有
`platform_state: closed`、develop 没有、平台已 CLOSED，却被拒绝）。

复核 `docs/system/workspace/commands.md` 后推翻：
- `wt-close` 的**执行位置是 project-root（develop 工位）**，前提是「PR 已合并」；
- Phase 1 读的就是 `$ISSUES_DIR`（develop 树），`wt-close:906` 也写明
  「pr-merge-guarded writes platform_state: closed to the worktree **before merge**」；
- 因此 develop 缺失 `platform_state` 是**真信号**：merge 时的同步没发生（正是 1.1 的缺口），
  而不是「读错了副本」。

若改成读工位副本，分支上未合并的状态也能通过预检——属能力降级，会掩盖漂移。
故：**该改动已撤销**，AT 改为钉住「wt-close 对 develop 检查」这一设计事实。

R33.16 的收口阻塞由 1.1（merge hook 看不到 B2）解释，修好 1.1 后按正常流程重跑即可。

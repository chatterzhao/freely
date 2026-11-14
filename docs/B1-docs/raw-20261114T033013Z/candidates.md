# B1 Candidates — raw-20261114T033013Z

## C-20261114T033013Z-A：I-* 收口链路对齐设计

- status: promoted
- promoted_issue_id: I-20261114T033013Z-A
- promoted_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261114T033013Z/issues/I-20261114T033013Z-A.md
- milestone: M-20261114T033013Z-A
- kind: fix
- decision: 方案 A——新增 `merge_issue_sync.py` 供 merge hook 使用；linked 收口统一走 `issue-sync batch <raw-key>`；`cmd-create` 对 linked 写 `platform_state: open`。**不**改 `wt-close` 的读取源（它按设计读 develop，见 brainstorms §6）。
- design_verdict: 实现未完成 + 实现偏差 + bug（同一条链路）
- anchor_refs: ibm-framework.md 事件表/字段表；raw_lifecycle_effects.close_linked docstring；wt-close:906 注释
- 范围:
  1. 新增 `docs/system/workspace/scripts/worktree/merge_issue_sync.py`：发现（B1 + B2）、按 raw-key 限定、判定动作、行替换落 phase。
  2. `pr-merge-guarded::_sync_issues_changed_in_merge`：改调该模块；linked 改由 `issue-sync batch <raw-key>` 收口；只 `git add` 被改文件。
  3. `bin/issue-sync.d/cmd-create.sh`：去掉 `_fm_has_key` 守卫，linked 也写 `platform_state: open`。
  4. 新增 AT `test-closeout-chain.py`（含「wt-close 对 develop 检查」的设计钉子），CORE/CI_CORE 各 +1。
- 验收:
  - 发现层：同一 diff 里 B1 raw + B2 linked 都能被找到；其他 raw 被 `--raw-key` 过滤；
  - 判定层：raw proposed→absorbed、absorbed→close；linked in_dev→in_verification、completed→close；
  - 落盘层：phase 行替换不改变其他字段顺序与取值；
  - hook 层：显式调用 `issue-sync batch <raw-key>`，且 `git add` 只作用在被改文件；
  - create 层：新 linked 文档有 `platform_state: open`（raw 行为不变）；
  - wt-close 层：仍以 develop 为准（读取源不得改成工位副本）；
  - 基线（develop）各条必须红。
- 不退化边界:
  - 不改 `close_linked` 判据、不恢复第二关闭通道、不放宽 GATE 1；
  - 不改 `issue-sync batch` 的收口判据；
  - 不处理 daemon 无范围 batch（另一 raw）。

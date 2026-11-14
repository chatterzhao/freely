# B1 Candidates — raw-20261114T031043Z

## C-20261114T031043Z-A：batch 范围过滤修复 + daemon 只限定范围

- status: promoted
- promoted_issue_id: I-20261114T031043Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-sync-modules/raw-20261114T031043Z/issues/I-20261114T031043Z-A.md
- milestone: M-20261114T031043Z-A
- kind: fix
- decision: 方案 A——过滤比较 `${issue_file#*/docs/}`；输出 `scope=`；daemon 在 lane 内传 raw key、在受保护分支跳过并提示。
- design_verdict: bug + 实现未完成
- anchor_refs: runtime/freely:24146；cmd-batch.sh 范围注释；issue-sync-scope.py
- 范围:
  1. `bin/issue-sync.d/cmd-batch.sh`：过滤改为相对 `/docs/` 的路径；打印 `scope=`。
  2. `docs/system/workspace/scripts/runtime/freely`：daemon 前置 batch 解析当前工位 raw key 并传参；无法解析（develop/main/test-pre-merge）则跳过并提示治理车道。
  3. 新增 AT `test-batch-scope-filter.py`，CORE/CI_CORE 各 +1。
- 验收:
  - 工位路径含 raw key 时，其它 raw 零变更（AT 用名为 `fix-raw-<key>-slug` 的临时目录构造）；
  - `scope=` 输出存在；
  - daemon 段在受保护分支不调用 batch；在 lane 内传 key；
  - 基线（develop）各条红。
- 不退化边界:
  - 不改收口判据、不改 GATE 1、不引入治理车道（另一条 raw）。

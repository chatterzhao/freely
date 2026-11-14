# PRD: batch 范围过滤修复与 daemon 只限定范围

- issue_id: I-20261114T031043Z-A
- source_raw: raw-20261114T031043Z
- workflow_kind: fix
- milestone: M-20261114T031043Z-A
- story: platform/issue-sync-modules（复用既有 story）

## 目标

让 `--raw-key` 真正限定范围（修掉「绝对路径被工位名误匹配」），并让 daemon 不再无参全量同步：
lane 内传本 lane key，受保护分支/无 key 分支跳过并指向治理车道。

## 唯一改动范围

- `bin/issue-sync.d/cmd-batch.sh`：过滤改为比较 `${issue_file#*/docs/}`；命令头打印 `scope=<key|ALL>`。
- `docs/system/workspace/scripts/runtime/freely`：daemon 前置 batch 解析当前分支 raw key 并传参；`main|develop|test-pre-merge-*` 与无 key 分支跳过。
- 新增 AT `test-batch-scope-filter.py`，CORE/CI_CORE 各 +1。

## 不退化边界

- 不改 `batch` 的收口判据（`completed` / `absorbed|dropped`）；
- 不改 GATE 1；不引入治理车道与字段类判据（`raw-20261114T051655Z`）；
- 不新增「任意文档可改」的通道。

## 功能需求

- FR-1：工位目录名含 raw key 时，其它 raw 的文档零变更。
- FR-2：`batch` 输出 `scope=<key|ALL>`。
- FR-3：daemon 在 lane 分支传本 lane key。
- FR-4：daemon 在受保护分支/无 key 分支**不调用** batch，并提示治理车道。
- FR-5：基线在 FR-1/FR-3/FR-4 上必须红。

## 验收

AT-001 GREEN `10 ok / 0 failed`；基线（develop `763248747`）`2 ok / 8 failed`；
`bin/test-all --ci` 全绿。

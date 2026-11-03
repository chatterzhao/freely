# PRD: 双平台活跃面 issue 对齐

- issue_id: I-20261103T091157Z-A

## Goal
让 GitHub 与 Gitee 的 open issue 集合按 raw key 完全一致；每个 open issue 都有本地 raw 文档并记录双平台编号；平台已有镜像的历史文档补齐编号；Gitee 搜索不再因单页截断而丢历史镜像。

## Modules
- `docs/system/workspace/scripts/sync/platform-adapter.py`：`GiteeHandler.search_raw_issue` 分页（100/页，最多 20 页）。
- `docs/system/workspace/scripts/tests/test-platform-adapter-gitee-search.py`（新）：分页单元测试（第 2 页命中）。
- `docs/system/workspace/scripts/tests/test-platform-open-parity.py`（新）：实时 parity 校验。
- 数据面：13 个双平台 open raw 文档物化；4 个 Gitee 漂移镜像关闭；13 个历史本地文档 platform_ids 回填；2 个已吸收文档补平台编号。

## Invariants
- open 集合按 raw key 相等；不新增/删除平台 issue（漂移关闭除外，且须有 GitHub 孪生 closed 证据）。
- 编号回填只在标题前缀唯一匹配时进行，不猜。
- 历史 closed 总量差异记录为遗留债，不在本 PR 内处理。

## Non-Goals
- 不批量补建历史 closed 镜像、不追求两平台历史总量相等。
- 不改 scan/gate/lifecycle 语义。

## Eval Plan
- unit：Gitee 搜索分页测试。
- integration：parity 测试实时调用两平台 API + 本地文档。
- real-environment：即 parity 测试本身（真实平台）。

## Dev-Loop Handoff
先 RED：分页测试失败 + parity 测试失败；再修分页、物化/关闭/回填；最后 GREEN 两测试。

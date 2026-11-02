# PRD: 副本观测三态化与债账本

## Goal

把“读不到”与“确实没有”分开，让门禁只在**事实**上阻塞：

`transport (retry) → status ∈ {ok, missing, unknown, ambiguous} → reconcile → decision ∈ {allow, allow_degraded, block} → caller records debt`

## Modules

- `platform-adapter.py::discover_raw_replicas`：transport 读取带 3 次有界重试；异常映射为 `unknown`（带 `reason`）；只有“搜索成功且 0 命中”才是 `missing`。
- `raw_reconciliation.py::reconcile`：`unknown` 进 `degraded`，默认阻塞；新增 `allow_degraded` 后放行并输出 `debt`。
- `raw-reconciliation-gate.py`：新增 `--allow-degraded`，输出 `decision` 与 `debt`；**仍只读**。
- `wt-create`：以 `allow_degraded` 调用；`decision=allow_degraded` 时把债写入 `.freely/state/sync-debt.json`。
- `sync-debt.py`：`record` / `list` / `clear` 三个纯文件操作。

## Invariants

- `missing`、`ambiguous`、`diverged`、`raw_key_mismatch` 在任何开关下都阻塞。
- 默认 `allow_degraded=False`：既有行为与既有测试完全不变。
- 所有 configured platform 都不可读时（无 baseline）阻塞——不能凭“一无所知”放行。
- receipt 不写磁盘、不调写接口；记账由调用方完成。
- 债条目必须带 `platform`、`reason`、`raw_key`、`since`、`attempts`。

## 非目标

- 不实现债的偿还（`issue-sync reconcile`），由 C-20261102T113816Z-B 立项。
- 不改 `close-multi` 的全平台语义。
- 不让 `pull_raw_issue`（materialize）接受 degraded：该路径没有本地副本可核对。

## Dev-loop handoff

先写 RED：证明 transport 异常被记成 `error`、`reconcile` 把 `unknown` 当阻塞事实、且无重试；再改 adapter 与 reconcile；最后接 `wt-create` 与账本。

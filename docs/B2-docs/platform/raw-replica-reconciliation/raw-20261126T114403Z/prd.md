# PRD: raw-20261126T114403Z

## Goal
治理清理时以一次平台读取关闭全部 terminal local_id 的 OPEN 副本，保持 adapter 副本判据单一真源与 fail-closed 语义。

## 模块划分
1. **adapter 批量子命令**：`platform-adapter.py` 新增 `close-local-ids <ids_json> <kind>`，内部一次 `list_open_issue_records()`，对每个 id 复用同一份 records 调用 `close_local_id` 的判据逻辑；输出逐 id 逐平台结果，退出码 0/3/1。
2. **命令层批量入口**：`bin/issue-sync.d/cmd-close.sh` 新增 `cmd_close_orphans_all()`，枚举本地 `phase_state ∈ {completed, dropped}` 的 raw/linked 文档，委托 adapter 批量子命令，汇总结果并打印 retry 命令。
3. **dispatcher + 文档**：`bin/issue-sync` 注册 `--all-completed`，`commands.md` 增加用法与 rc 语义。

## 关键决策
- 副本判定仍在 adapter（`replica_truth.summarize`），命令层不得自己拼 `platform_ids` 或直连平台；
- 单 id 入口 `close-orphans <local_id>` 逐字不变；
- 平台读取失败仍 fail-closed，不得把未读平台当成空副本集。

## Dev-Loop Handoff
RED：AT 对 develop 基线应因缺批量入口失败；GREEN：结构 + stub 行为全绿，既有 close-orphans AT 13/13 回归。

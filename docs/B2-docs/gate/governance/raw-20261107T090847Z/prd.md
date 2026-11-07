# PRD: 两代 receipt 兼容 + 审计链总能跑完

- issue_id: I-20261107T090847Z-A
- source_raw: raw-20261107T090847Z
- workflow_kind: fix
- milestone: M-20261107T090847Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

补齐 README 宣称三层治理的第三层：`governance-check` 的 post-merge receipt 审计既不能对合法新值误报，也不能因 `set -e` 提前退出而形同虚设。

## 唯一改动范围

`docs/system/workspace/scripts/quality/governance-check` 一个真源：
1. `merge_path` allowlist 接受两代合法值。
2. 加固 5 处控制流（`check_entry_naming` / `check_no_tbd` / `check_three_loop_reference` / `check_fixed_string` / 空 entries 守卫 / audit 调用），不改变任何 `fail()`/`warn()` 调用。
3. 新增回归测试 `test-governance-receipt-audit`。

## 不退化边界

- 不删除或削弱任何既有检查；不改 `pr-merge-guarded` 写入值、`commit-msg.sh`、`post-checkout`、backfills/break-glass ledger。
- 历史 `merge-guarded*` 仍被接受；非法/缺失值仍 fail。
- 9 个回归以未修改 develop HEAD 基线对比零新增失败。

## 功能需求

- FR-1: 两代 receipt 都被接受，审计不再对合法 `pr-merge-guarded` 误报。
- FR-2: 完整脚本在预存 `[FAIL]` 存在时仍跑完 receipt 审计并输出汇总行。
- FR-3: 恢复审计能力后，真实 develop HEAD 上 `PROBE_ERRORS=0`。
- FR-4: 回归覆盖 6 个隔离仓库场景 + 9 条静态断言。

## 验收

AT-001 基线 RED 3 失败 / 5 既有能力 PASS → GREEN 全通过；9 个回归基线对比 0 新增失败；真实 develop 复验无假阳性。

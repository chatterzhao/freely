# B1 Candidates — raw-20261114T080106Z

## C-20261114T080106Z-A：安装态自检一等入口 + 文档对齐

- status: promoted
- promoted_issue_id: I-20261114T080106Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261114T080106Z/issues/I-20261114T080106Z-A.md
- milestone: M-20261114T080106Z-A
- kind: fix
- decision: 方案 A——新增 `bin/install-state-check` 薄投影（转发 `quality/install-state-check.py`），修 `.freely/goal-arch-debt.md` 与 `docs/system/workspace/commands.md` 的命令写法，新增 AT。**不改 `runtime/freely`**（27158 行预算）。
- design_verdict: 实现未完成 + 文档偏差
- anchor_refs: `goal-arch-debt.md:22`（「install-state-check --json → ok:true 吃狗粮前提」）；`quality/install-state-check.py`（「Thin wrapper — every rule lives in install_state.py」）；`check-runtime-size`（`ok (27158 lines, budget 27158)`）
- 范围:
  1. 新增 `bin/install-state-check`（≤8 行，`exec python3 "$ROOT_DIR/docs/system/workspace/scripts/quality/install-state-check.py" "$@"`）。
  2. `.freely/goal-arch-debt.md`：把 `install-state-check --json` 改为 `./bin/install-state-check --json`（含当前权威恢复点与历史留痕处的关键写法，至少改权威段）。
  3. `docs/system/workspace/commands.md`：补一行说明该入口与 `freely doctor` 的关系。
  4. 新增 AT `test-install-state-cli.py`，CORE/CI_CORE 各 +1。
- 验收:
  - `./bin/install-state-check --json` 返回 `ok:true` 且 `project_head / active_version / packaged_from / command_path` 与真源脚本一致；
  - 不一致场景返回非 0 / `ok:false` 并给出 `freely-package --version auto --activate`；
  - goal 与 commands.md 的命令写法与实际入口一致（静态断言）；
  - `runtime/freely` 行数不变、`check-runtime-size` 仍绿；薄投影不复制判定逻辑（静态断言无 `install_state` 逻辑）；
  - 基线（develop）各条红。
- 不退化边界:
  - 不改 `runtime/freely` / `cmd_doctor()` / `freely-package` / `install_state.py`；
  - 不放宽任何门禁；不新增第二份安装态真相源；不自动修复不一致。

# PRD: 安装态自检一等入口 + 文档对齐

- issue_id: I-20261114T080106Z-A
- source_raw: raw-20261114T080106Z
- workflow_kind: fix
- milestone: M-20261114T080106Z-A
- story: platform/issue-sync-entrypoint

## 目标

让「安装态是否与 develop 一致」有一个 goal 可照抄、机器可读的一等命令，消除「文档声明的命令跑不通 → 无法确认是否吃到过期安装态」的风险。

## 唯一改动范围

1. 新增 `bin/install-state-check`：≤8 行薄投影，`exec python3 "$ROOT_DIR/docs/system/workspace/scripts/quality/install-state-check.py" "$@"`。
2. `docs/system/workspace/commands.md`：「意图→命令速查」加一行 + 新增 `### ./bin/install-state-check` 说明（唯一真源、与 `freely doctor` 关系、不一致时给修复命令、不自动修复、预算原因）。
3. `.freely/goal-arch-debt.md`（主仓本地文件，不随 git 走）：把权威段与纪律段的命令写法改为 `./bin/install-state-check --json`。
4. 新增 AT `test-install-state-cli.py`，CORE/CI_CORE 各 +1；`projection.lock` 重录。

## 不退化边界

- **不改** `docs/system/workspace/scripts/runtime/freely`（正处 27158/27158 行预算）、不改 `cmd_doctor()`、不改 `freely-package`、不改 `quality/install_state.py`；
- 不复制自检判定逻辑、不新增第二份安装态真相源；
- 不放宽 `check-runtime-size` / `check-bin-projection`；不新增硬门禁；
- 自检不自动修复：不一致只报告并给出 `freely-package --version auto --activate`。

## 功能需求

- FR-1：`./bin/install-state-check --json` 存在且输出与真源脚本逐字一致（薄投影转发契约）。
- FR-2：不一致时 rc≠0、`ok:false`，非 JSON 输出含 `freely-package --version auto --activate`。
- FR-3：`commands.md` 与 goal 的命令写法与实际可执行入口一致。
- FR-4：`runtime/freely` 行数不变、无 dispatch 行；`check-runtime-size` 仍绿。
- FR-5：薄投影不含 `install_state` 判定逻辑（静态断言）。
- FR-6：基线（develop）在 FR-1/3/5 上红。

## 验收

AT-001 GREEN `15 ok / 0 failed`；基线 `4 ok / 7 failed`；`bin/test-all --ci` 全绿；`check-bin-projection` / `check-runtime-size` / `projections verify` 均绿。

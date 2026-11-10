# Tasks: 运维底座六项收口
- issue_id: I-20261110T120124Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T120124Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create` 建 fix/test 工位（基于 `83ba84a74`）。逐项普查 6 个分项；确认 `--output` 守卫已由 #4158 落地、不重复做；确认 `--key` 进 history 属用户显式输入，本轮只把落盘路径改 env。
- [x] T2: 写 AT-001（7 静态 + 4 行为），基线 RED `0 ok / 11 failed`。三次修夹具：tmp 需 `resolve()`；package 输出父目录需先建；ai-cli 断言要精确到 python argv 形态。
- [x] T3: 分项 1：watchdog 建日志、`tail -F`、`PRE_CHECK_MAP || continue`、pid + 二次启动 no-op、退出清理、WORKTREES_ROOT 可覆盖。
- [x] T4: 分项 2/3：`append_runtime_event` 内生成 severity/trace_id（不改签名）；新增 `_prune_logs_by_count`，cycle 保留 50、crash 保留 20。
- [x] T5: 分项 4/5：package 复制后排除 `__pycache__`/`*.bak.py` 并按产物计数；gitee token 改 `Authorization: Bearer`；codex key 改 `FREELY_CODEX_API_KEY` env。
- [x] T6: 分项 6：`SCHEMA_VERSION=1`、`PRAGMA user_version` 读取/写入、迁移失败 `raise`（review_stage 的 duplicate-column 例外）。
- [x] T7: GREEN `11 ok / 0 failed`；真实 `gitee-issue.py get IKUEK0` header 认证通过；新 AT 进 `CORE`/`CI_CORE`；12 项回归 + `test-all --ci` `9 ok / 0 failed`；local 仅既有 known-broken。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity / 前置评审） |
| T3 | 静态 1 + 行为 4 |
| T4 | 静态 2/3 + 行为 1/2 |
| T5 | 静态 4/5/6 + 行为 3 + 真实 Gitee 只读 |
| T6 | 静态 7 |
| T7 | 全量 GREEN + 回归 + CI |

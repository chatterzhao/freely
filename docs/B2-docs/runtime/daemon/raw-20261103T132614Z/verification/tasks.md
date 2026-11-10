# Tasks: 注册表路径单一所有者 + raw key 入口规范化
- issue_id: I-20261103T132614Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261103T132614Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create` 建 feature/test 工位（基于 `56d4cd2c9`）。重做真源普查：面 1 只剩 `bin/deploy-skills:72` 与 `runtime/freely:21469` 两处（`bin/ensure-acp-binary` 已不存在）；面 2 的 `wt-create:279-284` 仍只告警。面 3–6 由 #4179 / #4166 / #4161 承接，不拆新 raw。
- [x] T2: 写最终版 AT-001（6 静态 + 3 registry 行为 + 4 raw key 行为）；`git archive develop` 基线只注入 AT → RED `1 ok / 12 failed`（唯一 PASS 是显式 `--tools claude` 守卫）。
- [x] T3: 新增 `runtime/paths.sh`（`freely_tool_registry_path` / `_query_path`）；`runtime/freely` 按 `_freely_lib_missing` 范式 source 并让 `TOOL_REGISTRY` 由函数产出；`_init_acp_tool_setup` 缺失即 `log_error + return 1`；`bin/deploy-skills` source 同一库、缺失 `exit 1`、删除 claude fallback。
- [x] T4: `raw_key_canon.py` 增加 legacy 匹配（4/6 位）+ 分支名内嵌 legacy 提取 + `__main__` CLI；`wt-create` 验证段改调 canon，规范化失败即拒绝，成功则打印 normalised 并写回 `raw_key`。
- [x] T5: GREEN `13 ok / 0 failed`。首轮 `9 ok / 3 failed`：负向扫描把注释里的旧路径算命中 → 改注释；present 断言 rc=0 不成立（注册表含未支持的 `cline`，脚本本就 rc=1）→ 改为断言读到 cline；分支名 legacy 需二次提取。补齐两个 wt-create 夹具的 canon 依赖后 13 项回归全绿；`test-all --ci` `8 ok / 0 failed`；local 仅既有 known-broken。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity / 前置评审） |
| T3 | AT-001（静态 1/2/3/4 + registry 行为 3 项） |
| T4 | AT-001（静态 5/6 + raw key 行为 4 项） |
| T5 | AT-001 GREEN + 回归 + CI 接线 |

# Pre-Tests: 注册表路径单一所有者 + raw key 入口规范化
- issue_id: I-20261103T132614Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: tool-registry 路径只有一个所有者（`runtime/paths.sh`），缺失时 `deploy-skills` 与 ACP setup fail-closed；legacy raw key 在 `wt-create` 入口经 `runtime/raw_key_canon.py` 规范化为 `YYYYMMDDTHHMMSSZ`
- acceptance_target: 不再有第二份路径字面量；任何 legacy raw key 进入工位前都变成 canonical 形式
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 隔离基线 / 工位真源；AT 在临时目录搭建只含 `bin/deploy-skills` + `paths.sh` + `tool-registry-query.py` + 真实 `tool-registry.toml` + 空 skills 的最小树；canon 用真实 `raw_key_canon.py` CLI。不访问平台、不创建真实工位、不写入 `~/.claude/skills`
- required_evidence: 6 静态 + 3 registry 行为 + 4 raw key 行为 = 13 项全 GREEN；基线 RED `1 ok / 12 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-contract-single-source.py
- test_command: python3 docs/system/workspace/scripts/tests/test-contract-single-source.py
- expected_output: SUMMARY: 13 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok / 12 failed（唯一 PASS 是守卫：显式 `--tools claude` 在改前改后都成功）
- actual_RED_output: develop `56d4cd2c9` 基线 + 最终版 AT-001 → `SUMMARY: 1 ok, 12 failed`（AT-001-RED.log）。关键：`registry present: registry tools are read (cline detected)` FAIL（旧代码 fallback claude，从不读注册表）、`registry missing: deploy-skills fails closed` FAIL（rc=0）、`wt-create normalizes raw keys` FAIL、canon 4 项 FAIL（无 CLI、不认 legacy）。
- actual_output: 工位同一断言 → `SUMMARY: 13 ok, 0 failed`（AT-001-GREEN.log）；含 `registry present: registry tools are read (cline detected)`、`registry missing: deploy-skills fails closed`、`branch name yields canonical key`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261103T132614Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组断言 `deploy-skills` 走 `freely_tool_registry_path` 且无 claude fallback、`_init_acp_tool_setup` 用 `$TOOL_REGISTRY`、`paths.sh` 拥有函数、三份生产文件无错误路径、`wt-create` 调用 canon、canon 有 legacy 与 CLI。行为 A 在最小树里跑 `--dry-run`：present 时从真实注册表读出 `cline`（fallback 不会输出 cline），missing 时非零退出且 stderr 含 tool-registry，显式 `--tools claude` 仍成功。行为 B 跑 canon CLI 的四种输入（legacy 4 位/6 位、canonical、legacy 分支名）。
- red_how: `git archive develop | tar -x -C /tmp/r24-base`，只拷最终版 AT-001，以 `--source-dir /tmp/r24-base` 运行。
- implementation_findings: 首轮 GREEN `9 ok / 3 failed`：①负向扫描把注释里的旧路径也算命中 → 改注释措辞；②`present` 断言 rc=0 不成立（注册表里有未支持的 `cline`，`deploy-skills` 末尾本就 rc=1）→ 改为断言「真的读到 cline」，同时补一条显式 `--tools` 守卫；③分支名里的 legacy key 需要 `_EXTRACT_LEGACY` 二次提取。三处均由行为断言暴露，不是静态断言能发现的。

## End-to-End
- acceptance_target: 真实 `deploy-skills` 的 fail-closed 与真实 canon CLI 的规范化
- testing_layer: end-to-end
- target_environment: 临时最小树 + 真实注册表副本
- required_evidence: AT-001（7 项行为）+ `bin/test-all --ci`
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-contract-single-source.py
2. bin/test-all --ci

## Unit
- acceptance_target: 静态所有权与负向扫描
- testing_layer: unit
- target_environment: feature/raw-20261103T132614Z-contract-single-source
- required_evidence: AT-001（6 项静态）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-contract-single-source.py

## Integration
- acceptance_target: wt-create / 并发单例 / DB 单写者 / 副本 / 状态契约不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 13 项回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
2. bash docs/system/workspace/scripts/tests/test-wt-create-top-level-return all
3. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-create.py
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
5. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
6. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
7. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py
8. python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py
9. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
10. python3 docs/system/workspace/scripts/tests/test-install-state.py
11. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
12. python3 docs/system/workspace/scripts/tests/test-dispatch-cas-sse-singleton.py
13. bash docs/system/workspace/scripts/tests/test-materialize-h1 all
14. python3 bin/check-state-file-sources
15. bin/check-state-file-keys
16. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 夹具在临时目录重建最小树，只复制真实 `deploy-skills` / `paths.sh` / `query` / 注册表；空 skills 目录保证不写任何工具目录。canon 直接调用真实模块。不创建工位、不触碰 `.freely/freely.db`、不访问 GitHub/Gitee。
- real_environment_reason: AT-001 RED `1 ok / 12 failed` → GREEN `13 ok / 0 failed`；13 项回归全绿；`bin/test-all --ci` `8 ok / 0 failed` 且执行新 AT；local `11 ok / 1 failed`，唯一失败是既有 `test-github-label-autocreate.py`（develop 基线同样失败）。
- regression_fixture_fix: `test-wt-create-four-state-dir` 与 `test-wt-create-top-level-return` 的隔离夹具此前只复制 `worktree/wt-create` 与 `worktree-common.sh`；wt-create 新增 canon 依赖后需把 `runtime/raw_key_canon.py` 一并复制。首轮回归 6+3 项失败，补齐夹具依赖后 `13 ok` / `20 ok` 全绿（与 R18「夹具补齐 CLI 依赖」同类，不是产品回归）。

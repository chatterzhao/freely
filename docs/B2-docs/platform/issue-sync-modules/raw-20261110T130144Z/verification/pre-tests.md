# Pre-Tests: issue-sync 拆模块 + 平台投影单一契约 + bootstrap delete 收口
- issue_id: I-20261110T130144Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `bin/issue-sync` 退化为 dispatcher（≤ 1330/2 行、不含任何 `cmd_*` 定义），9 个子命令各自成为 `bin/issue-sync.d/cmd-*.sh` 里可 source 的函数；平台 body 与标签由 `sync/issue_create_contract.py` 单点渲染，`feedback` 与 `issue-sync create` 输出逐字相同；`issue-sync-bootstrap --delete` 经 `platform-adapter.py issue-write-one github delete` 完成，`gh` 收到 adapter 解析出的 repo
- acceptance_target: 子命令可独立 source/断言；平台投影（含 frontmatter 围栏）只有一份实现；平台删只剩 adapter 一处
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 隔离基线 / 工位真源；行为测试用临时目录夹具 + PATH 前置 `gh` stub，不访问真实平台、不改真实 issue
- required_evidence: 24 静态 + 11 行为 = 35 项全 GREEN；基线 RED `6 ok / 29 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-modules.py
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-modules.py
- expected_output: SUMMARY: 35 ok, 0 failed
- expected_RED_output: SUMMARY: 6 ok / 29 failed
- actual_RED_output: develop `d32546e19` 基线 + 最终版 AT-001 → `6 ok, 29 failed`（AT-001-RED.log）：1330 行单文件、无 `issue-sync.d`、无契约模块、`feedback` 含标签字面量、`bootstrap` 直连 `gh issue delete https://… --yes`、平台 body 无围栏且把 `### comment-` 正文当正文发出。
- actual_output: 工位同一断言 → `35 ok, 0 failed`（AT-001-GREEN.log）；主文件 161 行、`issue-sync.d/` 14 个模块。
- evidence_file: docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态断言行数上限、模块存在与函数归属、主文件无 `cmd_*`、契约 API、`feedback` 无标签字面量、bootstrap 无直连删；行为上 source 主文件后要求 9 个 `cmd_*` 与 `_issue_body`/`_labels` 全部可调用，`_labels` 与契约对 P0/legacy 两种文档一致，`_issue_body` 与契约输出**逐字节相同**且只含一处 `schema_version`、保留 `workflow_kind`/表格/人类正文、丢弃 `## Comments` 段，最后用 stub `gh` 跑 `bootstrap --delete <url>` 断言 `issue delete 42 --repo acme/demo --yes` 与 adapter 的 JSON 回执。
- red_how: `git archive develop | tar -x -C /tmp/r27-base`，只注入最终版 AT-001，`--source-dir` 运行。
- implementation_findings: ①模块文件头必须逐行加 `#`——多行 docstring 只有首行被注释时 bash 会把第二行当命令执行（首轮 GREEN 因此全军覆没）；②`pull_raw_issue()` 依赖平台 body 的 frontmatter 围栏，所以「统一 body」必须保留围栏，不能顺手删；③adapter 依赖 `scripts/runtime/freely_user_env.py`，夹具缺它会把「导入失败」误报成产品缺陷；④夹具复制 `bin/issue-sync` 时必须同时复制 `bin/issue-sync.d/`，否则 fail-closed 直接报模块缺失。

## Unit

- acceptance_target: 平台投影契约的纯函数与 shell 包装的一致性（`labels_for` / `strip_frontmatter` / `split_workflow_kind` / `drop_comment_channel`）
- testing_layer: unit
- target_environment: 工位真源 + `git archive develop` 隔离基线（`/tmp/r27-base`）
- required_evidence: AT-001 的静态 24 项 + 契约与 `_labels`/`_issue_body` 的一致性断言；14 个模块逐个 `bash -n`
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-issue-sync-modules.py`（静态段 24 项：行数、模块归属、契约 API、标签字面量、bootstrap 直连）
2. 同一 AT 的行为段比对 `_labels`（P0 与 legacy 文档）与 `python3 ... issue_create_contract.py labels --file`，要求完全相等
3. 同一 AT 比对 `_issue_body` 与 `issue_create_contract.py body` 输出，要求**逐字节相同**
4. `for f in bin/issue-sync.d/*.sh; do bash -n "$f"; done` 与 `python3 -m py_compile issue_create_contract.py platform-adapter.py`
## Integration

- acceptance_target: 拆分后的 9 个子命令仍可从主文件 source 后调用，既有 issue-sync 测试链不退化
- testing_layer: integration
- target_environment: `test-pre-merge-20261110T130144Z-issue-sync-modules` test 工位（`test-gate run`）+ `git archive develop` 基线
- required_evidence: `test-gate` 的 `rc=0` 与 `.freely/run/test-evidence.log`；AT-001 RED `6 ok / 29 failed` → GREEN `35 ok / 0 failed`
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2`（23/0）
2. `bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first`（27/0）
3. `bash docs/system/workspace/scripts/tests/test-issue-sync-protected-branch-guard`（PASS）
4. `bash docs/system/workspace/scripts/tests/test-platform-write-channel`（22/0，基线 3 failed 本轮修绿）
5. `python3 .../test-feedback-severity.py`（30/0）、`test-frontmatter-ownership.py`（21/0）、`test-command-lifecycle-raw-metadata.py`（13/13）、`test-platform-sync-entrypoint.py`（4/0）
6. AT 行为段：source 主文件后 `declare -F` 需列出 9 个 `cmd_*` 与 `_issue_body`/`_labels`
## End-to-End

- acceptance_target: 拆分后的代码路径能真的创建、吸收并关闭双平台 issue；`bootstrap --delete` 走 adapter 的删除契约
- testing_layer: end-to-end
- target_environment: 本轮真实执行 `issue-sync promote` / `promote-finalize`（GitHub #4287 + Gitee IKUF1G）；`bootstrap` 用 PATH 前置 `gh` stub
- required_evidence: promote/finalize 的平台回执；AT-001 的 bootstrap 行为断言
- blocker_taxonomy: execution_pending_or_failed
1. `./bin/freely issue-sync promote raw-20261110T130144Z I-20261110T130144Z-A` → GitHub #4287 / Gitee IKUF1G created
2. `./bin/freely issue-sync promote-finalize raw-20261110T130144Z` → 双平台 `closed`，raw 相位 `absorbed`
3. AT 行为段：`issue-sync-bootstrap --delete https://github.com/acme/demo/issues/42` → stub `gh` 收到 `issue delete 42 --repo acme/demo --yes` 且 stdout 为 adapter JSON 回执
4. `bin/test-all --ci`（12/0）与 local `bin/test-all`（15/1，仅既有 `test-github-label-autocreate.py`）
## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮在真实平台上完成了 promote（GitHub #4287 / Gitee IKUF1G 创建，body 由新契约渲染并已被平台接受）与 promote-finalize（双平台 closed），说明拆分后的模块加载、`main()` 分派、契约渲染在真实路径上可用；`bootstrap --delete` 因需真删 issue 未对真实平台执行，用 stub 覆盖其命令形态与回执，属工具性命令，不涉及运行时状态机。

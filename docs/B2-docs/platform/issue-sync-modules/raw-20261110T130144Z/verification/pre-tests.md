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

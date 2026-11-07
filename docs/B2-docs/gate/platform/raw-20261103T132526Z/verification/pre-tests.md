# Pre-Tests: 平台写通道失败必报、部分成功可追
- issue_id: I-20261103T132526Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: gitee 写调用走真实 CLI 契约（`--repo <repo> <sub> --flag`）且失败原样非零；bash 侧不再用未赋值的 `GITEE_TOKEN` 跳过整段通道；`_gitee_repo_from_url` 对 scp-like / ssh / https 三种形态都产出 `owner/repo`；一平台成一平台败时 `create` 退出 3、只落成功平台 id、`platform_state` 保持原值；平台探测区分「未安装/未认证/超时/无权限」且不再报 `unsupported platform`；`create-issue` 与 `feedback` 退出码 0/3/1 且按平台汇报
- acceptance_target: 让平台写通道的失败可见、可诊断、可重试；「部分成功」不再伪装成成功或全部失败
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离夹具项目树（stub `gh` + stub `gitee-issue.py`）+ develop HEAD 基线对比 + 真实仓库只读核验
- required_evidence: 新增回归测试 6 项静态断言 + 16 个行为场景全 GREEN；9 个相关回归基线对比零新增失败；真机只读核验 repo 身份与双平台探测
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-write-channel
- test_command: bash docs/system/workspace/scripts/tests/test-platform-write-channel all
- expected_output: SUMMARY: 22 ok, 0 failed
- expected_RED_output: SUMMARY: 15 failed（静态 3 项 FAIL：`|| echo` 兜底仍在、`GITEE_TOKEN` 门禁仍在、`grep -A2` 仍在；行为：gitee create 契约失配、三条 repo url 全错、partial create rc=1、`unsupported platform` 仍出现、partial create-issue rc=1）
- actual_RED_output: develop HEAD 基线快照（`git archive HEAD -- bin docs`）运行最终版 AT-001 —— 静态 3 项 FAIL，行为 12 项 FAIL：`gitee create` 因 argparse 契约失配 rc≠0、`repo url` 三种形态全部返回空、`partial create` 退出 1 且 platform_ids 为空、缺 `gh` 时输出 `unsupported platform`、`partial create-issue` 退出 1；汇总 `SUMMARY: 7 ok, 15 failed`（AT-001-RED.log）
- actual_output: 工位运行同一份断言：静态 6 项全 ok（无 `|| echo` 兜底、无 `GITEE_TOKEN` 门禁、无 JSON 位置参数、freely 无固定上下文 grep、两文件语法通过）；行为 16 项全 ok（gitee create 成功/失败两态、三种 URL 形态、partial create rc=3 且只落 github id 且 platform_state 未写、full create rc=0 双 id + platform_state=open、缺 gh 报 not installed、不再出现 unsupported platform、all-failed rc=1、partial create-issue rc=3 且两平台状态并列）；汇总 `SUMMARY: 22 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261103T132526Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态组在真实文件上断言「不得再出现」的四类静默模式；行为组在隔离夹具项目树里用 stub `gh` 与 stub `gitee-issue.py` 驱动**真实的** `bin/issue-sync`（通过 `BASH_SOURCE` 守卫作为库加载、`ROOT_DIR` 可覆盖），断言退出码、frontmatter 落盘内容与 argv 形态；adapter 组用「PATH 里没有 gh」制造 FileNotFoundError，断言错误文案包含 not installed 且不含 unsupported platform，并用 stub gh + 无 token 的 Gitee 制造部分成功断言 rc=3。
- red_how: fix RED — `git archive HEAD -- bin docs` 出基线快照，把最终版测试拷入后运行，基线文件一个不改。

## Unit
- acceptance_target: 静态契约（静默模式清零、语法可解析）
- testing_layer: unit
- target_environment: fix/raw-20261103T132526Z-platform-write-silent-failure
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-platform-write-channel static

## Integration
- acceptance_target: 读通道、reconciliation、adapter、raw-metadata 等既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
2. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
3. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py

## End-to-End
- acceptance_target: 真实仓库上 repo 身份与双平台探测可读
- testing_layer: end-to-end
- target_environment: 真实 fix 工位（只读）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash -c 'source bin/issue-sync; _gitee_repo'  → zhaoquan/freely
2. python3 docs/system/workspace/scripts/sync/platform-adapter.py → Available: ['github', 'gitee']

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全部改动在真实 fix 工位执行；RED 取自 `git archive HEAD`（不改基线）；真机只读核验 `_gitee_repo` 由 `git@gitee-zhaoquan:zhaoquan/freely.git` 解析为 `zhaoquan/freely`，adapter 探测 `Available: ['github', 'gitee']`（github=chatterzhao/freely、gitee=zhaoquan/freely）；9 个相关回归以未修改 develop 基线对比零新增失败；最终以真实 `pr-create-guarded` / `pr-merge-guarded` / `wt-close` 闭环。未真实创建平台 issue（避免污染），写通道行为由 stub CLI 驱动真实脚本覆盖。

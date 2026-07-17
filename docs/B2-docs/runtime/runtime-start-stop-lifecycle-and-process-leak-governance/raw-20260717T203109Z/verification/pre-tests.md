# Pre-Tests: wt-close autonomous gate 收尾（静默退出/merge 竞态/RPC 数字键根修）
- issue_id: I-20260717T203109Z-A

RED 方式：AT-001/002/005 对 **HEAD 已提交版本**（`git show HEAD:` 提取 wt-close + worktree-common.sh 到临时目录）执行；AT-003/004 对 **HEAD 版本 freely_db_manager.py** 起临时 daemon 执行。GREEN 用工位当前版本。
统一入口：`bash <harness>.sh <wtclose_script> ...`，harness 位于 `verification/harness/`。

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: agent_working 查询段不再是 STUB（HEAD 版活跃 worker 行存在时误放行）；修复后查询生效，且 db daemon 不可达时 gate 降级不静默死——三态矩阵均有可见 [closeout-gate] stderr
- acceptance_target: STUB 补全 + gate 静默退出根修（B1 P1/P2）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T203109Z-gate-stub-complete
- required_evidence: RED=HEAD 版沙箱 deny 阶段无 DENIED（STUB 不查询）；GREEN=三态矩阵 stderr 均非空含预期判定行
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at001-gate-matrix.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at001-gate-matrix.sh <wtclose> <dev_wt>
- expected_output: AT001_RESULT: PASS
- expected_RED_output: at004 harness 对 HEAD 版 wt-close + HEAD 版 runtime，deny 阶段无 "DENIED" → AT004_RESULT: FAIL（证明 STUB 未实现查询）
- actual_RED_output: at004 harness(HEAD wt-close+HEAD rt): deny 阶段输出 'zero agent activity — allowing close'（应 DENIED）→ AT004_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/test-evidence/acceptance-1-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: RED 用 at004-active-worker-deny.sh <HEAD版wt-close> <HEAD版runtime>（纯未实现态）——deny 阶段不产生 DENY，证明 STUB 未实现查询。初版设计"HEAD 矩阵 0 字节"意外 PASS（静默死只存在于 lane 内中间态：无 try/except 的 heredoc + FileNotFoundError + set -e，bash -x trace 已留档），按 RED skill 已修正测试设计。GREEN 用 at001 矩阵断言可见输出（db 不可达降级不阻断）

### acceptance-2
- id: AT-002
- requirement: 已合并 raw key（raw-20260717T004620Z, caa39491d）连续 5 轮全部判 "allowing sweep"，_has_merge 无 SIGPIPE×pipefail 竞态
- acceptance_target: _has_merge 检测根修（B1 P3）
- testing_layer: integration
- target_environment: test-pre-merge-20260717T203109Z-gate-stub-complete
- required_evidence: 5/5 轮 stderr 含 "allowing sweep"
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at002-has-merge.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at002-has-merge.sh <wtclose> <dev_wt> 5
- expected_output: AT002_RESULT: PASS
- expected_RED_output: HEAD 版对已合并 key 无 "allowing sweep"（静默死或 DENIED foreign unfinished）→ AT002_RESULT: FAIL
- actual_RED_output: rounds passed: 0/3, stderr='DENIED foreign unfinished raw-20260717T004620Z' → AT002_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/test-evidence/acceptance-2-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: HEAD 版 grep -q 早退触发 git SIGPIPE，pipefail 判整条 pipeline 失败 → _has_merge 恒 false；bash -x trace 已证（_has_merge=true 从未赋值）

### acceptance-3
- id: AT-003
- requirement: agent_working.get / get_all RPC 返回命名键（worker_id 等），非数字键 '0'..'10'
- acceptance_target: RPC 行序列化根修（B1 P4，PRAGMA table_info d[0]→d[1]）
- testing_layer: unit
- target_environment: 临时 project 独立 daemon（socket 按临时路径 hash，不碰主仓）
- required_evidence: upsert 后 get 行含 worker_id 键且值以 w01 开头；get_all 行同
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at003-rpc-named-keys.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at003-rpc-named-keys.sh <runtime_scripts_dir>
- expected_output: AT003_RESULT: PASS
- expected_RED_output: get keys 为 ['0','1',...,'10'] 数字键 → AT003_RESULT: FAIL
- actual_RED_output: get keys: ['0','1','10','2',...,'9'] 数字键 → AT003_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/test-evidence/acceptance-3-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: 对 HEAD 版 freely_db_manager.py 起临时 daemon，agent_assign + agent_list_by_raw_key，行键为数字（主仓 live daemon 已实测同现象：活跃行存在但 gate 判 zero activity）

### acceptance-4
- id: AT-004
- requirement: 沙箱主仓 E2E — 活跃 worker 行存在 → gate DENY（stderr 含 w=w07）；agent_release_all 后 → allowing close
- acceptance_target: gate 活跃阻断链路整体（_main_root 解析 → 主仓 hash socket → 命名键 → 判定矩阵）
- testing_layer: end-to-end
- target_environment: mktemp 沙箱 git 主仓 + 独立 daemon
- required_evidence: deny.log 含 "DENIED self-owned" + "w=w07"；allow.log 含 "allowing close"
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at004-active-worker-deny.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at004-active-worker-deny.sh <wtclose> <runtime_scripts_dir>
- expected_output: AT004_RESULT: PASS
- expected_RED_output: deny 阶段无 DENIED（数字键 → 读不到 worker_id → 误判 zero activity 放行）→ AT004_RESULT: FAIL
- actual_RED_output: at004 harness(工位已修wt-close+HEAD rt): deny 阶段 'zero agent activity — allowing close'（应 DENIED w=w07）→ AT004_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/test-evidence/acceptance-4-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: RED 用 at004.sh <工位已修wt-close> <HEAD版runtime>——gate 侧修复在位但 db_manager 数字键仍使 deny 阶段误放行，单变量隔离 P4 是链路阻断点。主仓 live daemon 亦实测同现象（agent_assign 写 gate-test-agent 行后 gate 判 "zero agent activity — allowing close"，行已即时清理）

### acceptance-5
- id: AT-005
- requirement: usage() --force 描述与 autonomous gate 语义同步（提及绕过自治门禁拒绝判定）
- acceptance_target: raw issue 第 3 项 usage/help 同步
- testing_layer: unit
- target_environment: 工位内直跑 --help
- required_evidence: --help 输出中 --force 段含 "自治门禁"
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at005-usage-sync.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/harness/at005-usage-sync.sh <wtclose>
- expected_output: AT005_RESULT: PASS
- expected_RED_output: HEAD 版 --force 描述为旧文案（无"自治门禁"）→ AT005_RESULT: FAIL
- actual_RED_output: --force 段为旧文案'永久丢弃。必须配合 --raw-key 和 --reason。'，无自治门禁描述 → AT005_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/verification/test-evidence/acceptance-5-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: git show HEAD: 版 usage() --force 行为"永久丢弃。必须配合 --raw-key 和 --reason。"，无 autonomous gate 语义描述

## Unit
- acceptance_target: RPC 行序列化命名键（AT-003）、usage 文案（AT-005）
- testing_layer: unit
- target_environment: 临时 project daemon / 工位直跑
- required_evidence: AT003/AT005_RESULT: PASS
- blocker_taxonomy: execution_pending_or_failed
1. at003-rpc-named-keys.sh — 临时 daemon RPC get/get_all 命名键断言
2. at005-usage-sync.sh — --help 文案断言

## Integration
- acceptance_target: _has_merge 稳定性（AT-002）
- testing_layer: integration
- target_environment: test-pre-merge-20260717T203109Z-gate-stub-complete
- required_evidence: AT002_RESULT: PASS（5/5 轮）
- blocker_taxonomy: execution_pending_or_failed
1. at002-has-merge.sh — 已合并 key 连续 5 轮 allowing sweep

## End-to-End
- acceptance_target: gate 三态矩阵可见输出（AT-001）+ 活跃 worker 阻断全链（AT-004）+ feature→test-pre-merge→develop guarded merge
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T203109Z-gate-stub-complete → develop merge chain
- required_evidence: AT001/AT004_RESULT: PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. at001-gate-matrix.sh — 三态矩阵 stderr 可见性
2. at004-active-worker-deny.sh — 沙箱主仓活跃阻断/释放放行

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 主仓 live daemon 上实测复现 AT-004 RED 现象（活跃行被误判 zero activity）并即时清理测试行；handler 修复的 live 生效依赖合并后 daemon 重启（residual_risk 已在 IDN 记录，降级行为等同现状无回退）

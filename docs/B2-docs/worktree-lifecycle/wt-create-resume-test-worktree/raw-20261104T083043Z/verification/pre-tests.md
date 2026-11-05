# Pre-Tests: wt-create 中断恢复与 test-pre-merge 工位补建
- issue_id: I-20261104T083043Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: wt-create 具备幂等恢复状态机、可复用的 test 工位初始化真源、legacy 补建分支，且帮助文本与实现一致
- acceptance_target: 标准模式中断后可恢复；恢复出的 test 工位与正常创建完全等价
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261104T083043Z-wt-create-resume-test-worktree
- required_evidence: 回归测试静态断言组全部 PASS，且 wt-create 通过 bash -n 语法校验
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree
- test_command: bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree static
- expected_output: PASS: wt-create resume contract holds
- expected_RED_output: RED: resume contract missing (status machine, init helper, legacy branch or help text)
- actual_RED_output: RED: 11/13 断言失败 — resume_mode 状态机、幂等 no-op、不一致拒绝、_init_test_worktree_state、三处复用、恢复跳过 replica、恢复跳过 fuzzy、legacy 三项与 usage 说明均缺失（AT-001-RED.log）
- actual_output: PASS: wt-create resume contract holds，13/13 断言通过（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T4
- case_design: 对 docs/system/workspace/scripts/worktree/wt-create 做 bash -n 语法校验，并断言 resume_mode 四态判定、_init_test_worktree_state 函数定义、恢复分支调用该函数、幂等 no-op 分支、legacy 对 test-pre-merge-* 的识别与 base 推导、以及 usage 中的恢复说明；任一缺失即 RED。
- red_how: fix RED — 在当前未修复的 wt-create 上运行该断言组，确认恢复契约不存在。

### acceptance-2
- id: AT-002
- requirement: dev 工位存在而 test 工位缺失时，重跑同一 wt-create 命令能补建并初始化 test 工位；再次重跑为幂等 no-op
- acceptance_target: 中断残留可通过官方命令恢复，不产生重复工位
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时 git 仓库（隔离环境）
- required_evidence: 临时仓库中 test 工位目录、分支、.freely/run/test-gate.env 均存在；第二次重跑退出码 0 且输出已存在状态；worktree 数量不增加
- evidence_level: real_env
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree
- test_command: bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree e2e
- expected_output: PASS: wt-create resumes an interrupted run and is idempotent
- expected_RED_output: RED: Branch already exists / 恢复的 test 工位缺失或缺少 test-gate.env
- actual_RED_output: RED: 6/7 断言失败 — 重跑被 replica gate 拒绝（Branch already exists 路径），test 分支、工位、test-gate.env 均未产生（AT-002-RED.log）
- actual_output: PASS: wt-create resumes an interrupted run and is idempotent，7/7 断言通过；隔离仓库中 test 工位与 test-gate.env 齐全，二次重跑 worktree 计数 3 -> 3 不变（AT-002-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/verification/test-evidence/AT-002-RED.log,AT-002-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3
- case_design: 在 mktemp 临时目录建 git 仓库，复制 wt-create 真源与 worktree-common.sh 真源/shim，创建 develop 初始提交、fix/raw-<key>-<slug> 分支与对应 dev 工位（模拟 Step 1 完成、Step 2 未执行），然后执行同一条标准 wt-create 命令；断言 test-pre-merge 分支与工位出现、test-gate.env 内容为 not_tested；再执行一次断言幂等退出码 0、worktree 计数不变。
- red_how: fix RED — 当前实现会在存在性检查处 exit 1（Branch already exists），test 工位不会被创建。

## Unit
- acceptance_target: 恢复状态机、初始化函数、legacy 分支、帮助文本的结构正确性
- testing_layer: unit
- target_environment: fix/raw-20261104T083043Z-wt-create-resume-test-worktree
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree static`

## Integration
- acceptance_target: 恢复路径创建的 test 工位与标准路径产物一致（seed / .freely 状态 / test-gate.env）
- testing_layer: integration
- target_environment: 临时 git 仓库（隔离环境）
- required_evidence: AT-002
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree e2e`

## End-to-End
- acceptance_target: 真实项目中重跑 wt-create 不破坏已存在的双工位
- testing_layer: end-to-end
- target_environment: fix/raw-20261104T083043Z-wt-create-resume-test-worktree → develop merge chain
- required_evidence: AT-002 + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree e2e`
2. `freely pr-create-guarded` → `freely pr-review-guarded` → `freely pr-merge-guarded`

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮 wt-create 标准模式已在真实项目执行 1m57s 并成功创建 dev + test 双工位（含 seed 与 test-gate.env），可作为正常路径基线；恢复路径由 AT-002 的隔离真实 git 仓库覆盖。

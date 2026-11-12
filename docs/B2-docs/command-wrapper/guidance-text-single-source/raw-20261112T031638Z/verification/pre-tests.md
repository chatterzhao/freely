# Pre-Tests: 指引文案单源化 + raw-issue-pull 工位路径正确性
- issue_id: I-20261112T031638Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 全部活代码/模板/文档的指引只引用真实 skill 名且 wt-create 指引含必填 `--kind`；全域扫描白名单外零幽灵名；负向控制证明扫描非永真；白名单不得豁免本轮必修项
- acceptance_target: 「零幽灵名 + 必填 --kind」成为 CI 守护的全域不变量
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线（RED）/ fix 工位真源（GREEN）
- required_evidence: AT-001 静态 + 负向控制全 GREEN；`test-wt-close-protected-branch-guard` 整体 PASS；Step 2.5 pass
- evidence_level: real_env
- artifact_ref: docs/system/workspace/scripts/tests/test-guidance-text-single-source.py
- test_command: python3 docs/system/workspace/scripts/tests/test-guidance-text-single-source.py --source-dir .
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: develop `91473740c` 基线 + 最终版 AT-001 → 全域扫描判红并列出 `bin/issue-sync`、`pretests-gate`、`wt-close`、`runtime/freely`、hooks 模板、2 份文档的残留；`--kind` 缺失断言判红；反向断言判红。
- actual_RED_output: `git archive develop | tar -x -C /tmp/r336-base.*`，只注入最终版 AT，`--source-dir` + `--protected-root <主仓>` 运行 → `SUMMARY: 5 ok, 15 failed, 1 skipped`（rc=1，AT-001-RED.log）。15 项红全部指向真实缺口：S1–S9（文案残留）、S11–S14（CI/epics/unit 未接线）、B1（真机 guard 输出含幽灵名，`guarded=True, ghosts=[freely-fix-execution, freely-feature-execution]`）、S15（未传 --project）。5 项绿是有意义的不退化基线事实（S10 白名单诚实、B2 负向控制、S16/S17 ROOT_DIR 未改、B4 guard 仍拦截）。
- actual_output: AT `21 ok, 0 failed, 1 skipped`（唯一 skip 是 B3b post-merge 项，合并后补证）；`t-guidance-01.sh` `12 ok, 0 failed`；`test-wt-close-protected-branch-guard` PASS（含反向断言）；`bin/test-all --ci` → `24 ok, 0 failed, known-broken=590`；三门禁全过（projections 63 一致、runtime 27158/27158、bin 100、epics 17/218）。B3 真机：修复后的 `raw-issue-pull` 在 fix 工位内 rc=0、无 guard 噪音、`create complete`；机制对照见 at002-mechanism.log（同一脚本不给 --project → guard 命中 rc=1；给 --project → rc=0）。
- evidence_file: docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/verification/test-evidence/AT-001-GREEN.log,docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/verification/test-evidence/at002-mechanism.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态项（S1 `bin/issue-sync` guard 只引用真实 skill / S2 guard workflow 含 `--kind` / S3 `pretests-gate` 无幽灵名 / S4 `wt-close` UNMERGED 无幽灵名 / S5 `runtime/freely` 5 处指引含 `--kind` / S6 hooks 模板无重复相同选项且含 `--kind` / S7 `AGENTS.md.example` 与 `three-loop-capability-lifecycle.md` 含 `--kind` / S8 `pr-create-guarded` 注释语义正确 / S9 全域扫描白名单外零命中 / S10 白名单路径均真实存在且不含四个必修项 / S11 AT 进 CORE 与 CI_CORE / S12 epics story 存在且 check-epics-map ok / S13 `test-wt-close-protected-branch-guard` Test6 为反向断言且用 grep -E）；行为项（B1 真实触发 issue-sync protected guard，输出无幽灵名且含 `--kind` / B2 负向控制：沙箱内往非白名单文件注入幽灵名后扫描必须判红）。
- red_how: `git archive develop | tar -x -C /tmp/r336-base`，只注入最终版 AT-001，`--source-dir` 运行；基线含全部残留文案，故静态与行为同时判红。
- implementation_findings: ①R33.5 的 AT 把 `22 ok` 写死，本轮新增测试后必红——改为断言「0 failed 且 >=22 ok」这一稳定性质（subset 只增不减由 S8 钉住），属典型的「验收标准冻结易变事实」；②AT 初版把行为项在 nested 下记成 `ok` 造成假绿，改为独立 `[SKIP]` 计数且不计入 ok；③`git archive` 快照无 `.git`，B1/B4 需 `--protected-root` 显式指向真仓库根才能真正触发 guard；④沙箱 `git init` 无法触达 guard（脚本先解析 issue 文档并导入兄弟模块），故必须用真实树；⑤`wt-create` 的 ROOT_DIR 被 `bin/worktree-common.sh:17` 重绑到主仓，因此合并前 wt-create 必然调主仓旧版 raw-issue-pull——这是自举时序事实，B3 改为直接真机验证修复后的脚本，端到端留待合并后补证。

### acceptance-2
- id: AT-002
- requirement: `raw-issue-pull` 调 `issue-sync create` 显式传 `--project <工位根>`；真实新建一次 fix 工位输出无 protected-root ERROR/WARN；主仓 develop 上直接调 issue-sync create 仍 exit 1（guard 未削弱）
- acceptance_target: wt-create 不再产生 protected-root 噪音，platform title 归一化正常执行
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix 工位真源；行为项真实执行 wt-create（非 mock）
- required_evidence: AT-002 静态 + 行为 + 反向全 GREEN；真实 wt-create 输出留痕
- evidence_level: real_env
- artifact_ref: docs/system/workspace/scripts/tests/test-guidance-text-single-source.py
- test_command: python3 docs/system/workspace/scripts/tests/test-guidance-text-single-source.py --source-dir .
- expected_output: AT-002 各项 ok；真实 wt-create 输出不含 `refuses to run on protected branch` 与 `issue-sync create failed`
- expected_RED_output: develop `91473740c` 基线真实 wt-create 输出含 `[ERROR] issue-sync refuses to run on protected branch: develop` 与 `[WARN] raw-issue-pull: issue-sync create failed`（本轮开工位输出 /tmp/r336-wt-create-before.log 即为证据）。
- actual_RED_output: `git archive develop | tar -x -C /tmp/r336-base.*`，只注入最终版 AT，`--source-dir` + `--protected-root <主仓>` 运行 → `SUMMARY: 5 ok, 15 failed, 1 skipped`（rc=1，AT-001-RED.log）。15 项红全部指向真实缺口：S1–S9（文案残留）、S11–S14（CI/epics/unit 未接线）、B1（真机 guard 输出含幽灵名，`guarded=True, ghosts=[freely-fix-execution, freely-feature-execution]`）、S15（未传 --project）。5 项绿是有意义的不退化基线事实（S10 白名单诚实、B2 负向控制、S16/S17 ROOT_DIR 未改、B4 guard 仍拦截）。
- actual_output: AT `21 ok, 0 failed, 1 skipped`（唯一 skip 是 B3b post-merge 项，合并后补证）；`t-guidance-01.sh` `12 ok, 0 failed`；`test-wt-close-protected-branch-guard` PASS（含反向断言）；`bin/test-all --ci` → `24 ok, 0 failed, known-broken=590`；三门禁全过（projections 63 一致、runtime 27158/27158、bin 100、epics 17/218）。B3 真机：修复后的 `raw-issue-pull` 在 fix 工位内 rc=0、无 guard 噪音、`create complete`；机制对照见 at002-mechanism.log（同一脚本不给 --project → guard 命中 rc=1；给 --project → rc=0）。
- evidence_file: docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/verification/test-evidence/AT-001-GREEN.log,docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/verification/test-evidence/at002-mechanism.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T8,T9
- case_design: 静态项（S14 `raw-issue-pull` 调 issue-sync 时含 `--project` / S15 ROOT_DIR 默认推导未被改动 / S16 STDOUT 单 JSON 契约与 exit 0/3/1 语义保持）；行为项（B3 真实新建一次 fix 工位，输出无 ERROR/WARN 且 raw issue 物化 / B4 反向：主仓 develop 上直接调 `issue-sync create` 必须 exit 1）。
- red_how: 基线 `raw-issue-pull:133` 未传 `--project`，真实 wt-create 必然撞主仓 develop guard。
- implementation_findings: ①R33.5 的 AT 把 `22 ok` 写死，本轮新增测试后必红——改为断言「0 failed 且 >=22 ok」这一稳定性质（subset 只增不减由 S8 钉住），属典型的「验收标准冻结易变事实」；②AT 初版把行为项在 nested 下记成 `ok` 造成假绿，改为独立 `[SKIP]` 计数且不计入 ok；③`git archive` 快照无 `.git`，B1/B4 需 `--protected-root` 显式指向真仓库根才能真正触发 guard；④沙箱 `git init` 无法触达 guard（脚本先解析 issue 文档并导入兄弟模块），故必须用真实树；⑤`wt-create` 的 ROOT_DIR 被 `bin/worktree-common.sh:17` 重绑到主仓，因此合并前 wt-create 必然调主仓旧版 raw-issue-pull——这是自举时序事实，B3 改为直接真机验证修复后的脚本，端到端留待合并后补证。

## Unit

- acceptance_target: 文案不变量与 `--kind` 判定的函数级行为；满足 Step 2.5（本轮触及 runtime/freely）
- testing_layer: unit
- target_environment: fix 工位真源
- required_evidence: `tests/unit/t-guidance-01.sh` 全 PASS；Step 2.5 判 pass
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/unit/t-guidance-01.sh`
2. `bash docs/system/workspace/scripts/tests/unit/run.sh`

## Integration

- acceptance_target: 全域不变量在 CI 子集内被守护；真实 wt-create 路径正确
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: `bin/test-all --ci` 全绿；`test-gate run` rc=0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`
2. `./bin/freely test-gate run --worktree <test 工位> --command '<标准命令串>'`

## Real Environment

- real_environment_status: passed
- real_environment_reason: 真机已验证两件事：①修复后的 raw-issue-pull 在 fix 工位内 rc=0 且无 guard 噪音（B3）；②guard 未被削弱——主仓 develop 上直接调 issue-sync create 仍 exit 1 并打印修正后的指引（B1/B4，guard_fired=True）。端到端 wt-create 因 ROOT_DIR 重绑主仓须待合并后生效，已列为合并后补证项。
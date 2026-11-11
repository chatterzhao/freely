# Pre-Tests: 投影一致性检查
- issue_id: I-20261104T080259Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `.githooks/` 只剩 wrapper；`projection.lock` 覆盖四类投影；`freely projections verify` 一致 0 / 篡改非 0 / 缺 lock 2；AGENTS 生成器与模板零幽灵 skill 名；CI 每次 PR 校验
- acceptance_target: 投影与真源的一致性可被机器证明，漂移无法静默存在
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；篡改用完整沙箱树（复制 lock 引用的全部路径），确保只有被篡改项报错
- required_evidence: 16 静态 + 4 行为 = 20 项全 GREEN；unit 17 文件 111 断言；`test-all --ci` 21/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-projection-consistency.py
- test_command: python3 docs/system/workspace/scripts/tests/test-projection-consistency.py
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 19 failed
- actual_RED_output: develop `27e91e50c` 基线 + 最终版 AT-001 → `1 ok, 19 failed`（AT-001-RED.log）：6 个非 wrapper 文件仍在（含 issue 未提的 pre-push.bak / reference-transaction.debug）、post-checkout 非委托形态、无 projection.lock、无 verifier、runtime 无 projections 分派、生成器与模板含 freely-fix-execution / freely-feature-execution / freely-feat-execution、AT 未接线、epics 无 story。唯一 ok 是「8 个 wrapper 都存在」——基线事实，非缺陷证据。
- actual_output: 工位同一断言 → `20 ok, 0 failed`（AT-001-GREEN.log）；`freely projections verify --project .` → `[projections] ok (63 projections consistent)`；`unit/run.sh` → 17 文件 111 ok；`bin/test-all --ci` → `21 ok / 0 failed`（known-broken=591 与基线一致）；`check-runtime-size` → ok (27158/27158)；`check-bin-projection` → ok (100 bin entries, 38 registered)；`check-epics-map` → 17 epics / 216 stories。
- evidence_file: docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态 16 项（死副本清零 / 只剩 wrapper / 8 个 wrapper 齐 / 全部委托真源 / lock 存在 / 头完整 / 声明四类且仓库含三类 / 每条五字段 / 路径存在 / hash 与真源一致 / verifier 可执行 / runtime 分派到 bin/projections / 零幽灵名 / 模板名字全真 / 双 CI 接线 / epics story）；行为 4 项（一致树 0、真源篡改与委托切断都非 0、缺 lock 为 2、`freely projections verify` 端到端可达）。
- red_how: `git archive develop | tar -x -C /tmp/r33-base`，只注入最终版 AT-001，`--source-dir /tmp/r33-base` 运行。
- implementation_findings: ①**投影分 copy 与 delegate 两种**：第一版按字节比对 wrapper 与真源导致 61/62 全红，改为 mode 字段（delegate pin 真源 hash + 校验 exec 指向）后归零；②skills 部署目标在 $HOME，写进仓库 lock 会提交单机绝对路径，改为 machine-local sibling lock；③agents 投影校验「名字集合」而非字节，且提取规则必须是 `skill:` 前缀（裸 substring 命中 mktemp 模板 `freely-a2a-worker-prompt.XXXXXX`，反引号命中 provenance 标记 `freely-runtime-fallback`）；④**R31 行数门禁把本轮自己拦下**（27162 > 27158），按契约不上调预算，改用 `harness-status` 的内联 exec 先例，省掉 4 行函数；⑤BSD grep 无 `\s`，单测正则须用 `[[:space:]]`（本会话第三次同族坑）；⑥篡改 wrapper 时追加注释不算漂移（exec 仍在），必须真正切断委托才算——断言据此精确化。

## Unit

- acceptance_target: verifier 的 copy/delegate 判定、lock 形状、退出码三态
- testing_layer: unit
- target_environment: 工位真源 + 沙箱树
- required_evidence: `tests/unit/t-projection-01.sh` 13 断言；unit 全量 17 文件 111 断言
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/unit/t-projection-01.sh`（13/0）
2. `bash docs/system/workspace/scripts/tests/unit/run.sh`（17 文件 111/0）
3. lock 声明四类 kind、含 copy 与 delegate 两种 mode、每条 delegate hash 等于当前真源 hash
4. verify 三态：一致 0 / 缺 lock 2 / 切断委托 1

## Integration

- acceptance_target: 新增门禁不拖红既有回归，且三个既有门禁仍成立
- testing_layer: integration
- target_environment: test-pre-merge-20261104T080259Z-projection-consistency test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`test-all --ci` 21/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（21/0）
2. 七个既有 AT：R27 21、R28 21、R28.5 18、R29 16、R30 17、R31 16、R32 16
3. `./bin/check-runtime-size`（27158/27158，未上调）、`./bin/check-bin-projection`（100 入口）、`python3 bin/check-epics-map`（17/216）
4. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`

## End-to-End

- acceptance_target: 真实 PR 链路上投影校验与 runtime RED 门禁同时生效
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `pr-review-guarded` / `pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；Step 2.5 因改了 runtime 且已加 `tests/unit/` 单测而 pass
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR，body 含 RED 证据段
2. `freely pr-review-guarded <branch>` → Step 2.5 `pass: N runtime file(s), M unit test(s)`
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮改了 `.githooks/`（git 真正执行的入口）与 runtime 分派，属真实环境面：①`post-checkout` 三种入参真机冒烟（非分支 checkout → 0、develop 分支 → 0、真源缺失 → 2），行为与迁移前一致；②本轮所有 commit 都经过改造后的 `.githooks/pre-commit` 等 8 个 wrapper，等于每次提交都在自证；③`freely projections verify` 在真实工位跑出 63 条一致；④`bin/check-runtime-size` 真的拦下了本轮超预算的写法，迫使我们改用内联 exec，这是门禁在真实环境生效的直接证据。合并后 followthrough 重新打包，届时可在安装态再跑一次 verify。

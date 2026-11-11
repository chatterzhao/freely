# Pre-Tests: 核心 runtime 建立函数级 RED→GREEN 证据链
- issue_id: I-20261104T080007Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `docs/system/workspace/scripts/tests/unit/` 提供 ≥10 个函数级测试（状态机 / 锁 / 退出码三类各 ≥3），runner 能真的失败；`worktree/pr_body.py` 让每个 PR body 带 `## RED 证据`（runtime 变更缺证据则 exit 3）；`quality/runtime_red_gate.py` 让 `pr-review-guarded` 对 runtime 变更缺单测或缺证据时 exit 1 拒绝、非 runtime 变更 exit 2 跳过
- acceptance_target: 核心 runtime 的「先红后绿」成为可执行的门禁，而不是靠人回忆
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；PR body 与 review gate 用临时 fixture 项目（含 `pre-tests.md` 与证据文件），不访问真实平台
- required_evidence: 6 项静态 + 4 组行为 = 21 项全 GREEN；基线 RED `2 ok / 19 failed`；单元语料 14 文件 / 68 断言
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-runtime-tdd-evidence.py
- test_command: python3 docs/system/workspace/scripts/tests/test-runtime-tdd-evidence.py
- expected_output: SUMMARY: 21 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 19 failed
- actual_RED_output: develop `d315b5409` 基线 + 最终版 AT-001 → `2 ok, 19 failed`（AT-001-RED.log）：无 `tests/unit/`、无 `pr_body.py`、无 `runtime_red_gate.py`、PR body 仍是裸文案、review 侧无任何 RED 检查。
- actual_output: 工位同一断言 → `21 ok, 0 failed`（AT-001-GREEN.log）；`tests/unit/run.sh` → `14 file(s), 68 ok, 0 failed`。
- evidence_file: docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/test-evidence/AT-001-GREEN.log,docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/test-evidence/BACKFILL-A-RED.log,docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/test-evidence/BACKFILL-B-RED.log,docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/test-evidence/BACKFILL-C-RED.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态断言语料规模/分类覆盖/每个测试 source harness 并加载运行时、两个契约脚本存在、`pr-create-guarded` 与 `pr-review-guarded` 的接线位置；行为上跑真实 runner（含「故意失败的 probe 必须让 runner 非零退出」的反向证明）、用 fixture 项目跑 `pr_body.py render` 的三种情形（不适用 / 缺证据 exit 3 / 有证据引用）与 `runtime_red_gate.py` 的三种判定（skip 2 / refuse 1 / pass 0）。
- red_how: `git archive develop | tar -x -C /tmp/r28-base`，只注入最终版 AT-001，`--source-dir` 运行。三个补录 RED 用 `git archive 6715a67a2` / `83ba84a74` 快照注入 `tests/unit/` 后跑对应分组。
- implementation_findings: ①运行时是 sourceable 库（`_FREELY_IS_SOURCED`，#4153），65ms 即可加载，不需要重构；②运行时里有故意 `exit 1` 的守卫，测试必须每个文件独立进程；③`freely_db_manager.py` 用裸模块名导入同级 helper，探针要先 `sys.path.insert`；④`SystemExit("字符串")` 退出码是 1，要区分「缺证据」必须显式 `SystemExit(3)`；⑤仓库没有 PR 模板且 `gh pr create --body` 会覆盖模板，所以 RED 字段只能落 body 组合器。

## Unit

- acceptance_target: 状态机 / 锁 / 退出码三类的单函数契约
- testing_layer: unit
- target_environment: 工位真源（`source runtime/freely`）+ `git archive` 历史快照
- required_evidence: 14 个 `t-*.sh` / 68 条断言；三个补录 RED 日志
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/unit/run.sh`（state 4 / lock 4 / exit 4 / event 1 / db 1）
2. `bash docs/system/workspace/scripts/tests/unit/run.sh lock` 在 `6715a67a2` 快照上 → 3 文件 FATAL（补录 A）
3. `bash .../run.sh event` 与 `... run.sh exit-04` 在 `83ba84a74` 快照上 → 5 failed / FATAL（补录 B）
4. `bash .../run.sh db` 在 `83ba84a74` 快照上 → 4 failed（补录 C）

## Integration

- acceptance_target: PR body 与 review gate 的接线不影响既有 PR 流程
- testing_layer: integration
- target_environment: `test-pre-merge-20261104T080007Z-runtime-tdd-evidence` test 工位（`test-gate run`）
- required_evidence: `test-gate` `rc=0` 与 `.freely/run/test-evidence.log`
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-runtime-tdd-evidence.py`
2. `bin/test-all --ci`（14/0）
3. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`（29/0）、`test-verdict-contract`（13/0）、`test-command-lifecycle-pr-update.py`（OK）
4. `python3 bin/check-epics-map`（runtime epic 新增 tdd-evidence story）

## End-to-End

- acceptance_target: 真实 PR 流程里 RED 证据出现且不阻断非 runtime 变更
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded`
- required_evidence: 本 PR 的 body 含 `## RED 证据`；review Step 2.5 输出 skip/pass 之一
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → PR body 含 `## RED 证据` 段（不适用或引用证据）
2. `freely pr-review-guarded <branch>` → Step 2.5 打印 `skipped (no runtime change)` 并继续 review
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮不改 `runtime/freely`，因此真实运行时的行为不变；新增门禁在真实 PR 链路上跑过一次（`pr-create-guarded` 组出的 body 被双平台接受，`pr-review-guarded` 的 Step 2.5 正常 skip）。补录 RED 用的是历史提交快照，属可复现的仓库内证据，不需要真实运行时环境。

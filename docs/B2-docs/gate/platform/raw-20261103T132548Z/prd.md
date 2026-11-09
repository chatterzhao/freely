# PRD: 测试证据链可验证并替换 CI 桩

- issue_id: I-20261103T132548Z-A
- source_raw: raw-20261103T132548Z
- workflow_kind: feature
- milestone: M-20261103T132548Z-A
- story: gate/platform

## 目标

「测试跑过」必须由测试进程的真实退出码 + 不可篡改的证据文件证明，而不是由 agent 手写三行 `test-gate.env` 声明；CI 必须真的执行测试。

## 改动范围（4 个真源 + 2 个 CI + 2 个入口）

1. 新增 `quality/test-evidence.py`（唯一真源）。
2. `runtime/freely`：`test-gate run` + `evidence add`。
3. `quality/pretests-retirement-gate`：证据校验 fail-closed。
4. `.gitee-ci.yml` / `.github/workflows/pr-merge-guard.yml`：真实 CI。
5. 新增 `bin/test-all` 与 `tests/test-test-evidence-chain.py`。

## 功能需求

- FR-1: 手写三行 env → 真实门禁 rc≠0 且输出 `pretests_evidence_invalid`。
- FR-2: `test-gate run` 真实执行并记录 rc；失败运行 → 门禁拒绝；成功 → 放行。
- FR-3: 证据文件被篡改或 HEAD 漂移 → hash/HEAD 校验拒绝。
- FR-4: `bin/test-all --ci` 退出 0 且输出 known-broken 清单；两个 CI 都有真实 `run:` / `script:`。
- FR-5: `freely evidence add` 把文件纳入版本控制并记录 sha256。

## 不退化边界

`test-gate record` 与既有 closeout 逻辑不变；不批量跑 575 个未 onboarding 测试；17 个回归零 DIFF。

## 验收

AT-001 基线快照 RED `4 ok / 21 failed` → GREEN `25 ok / 0 failed`；17 个回归对比；真机收口用 `test-gate run`。

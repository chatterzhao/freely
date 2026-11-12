# Tasks: registry 契约测试机器无关化
- issue_id: I-20261112T015715Z-A
- pre_tests_path: docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/verification/pre-tests.md

## 任务分解

- [x] T1: B1 预研（四方案评估、develop 基线双跑证伪、stub 补齐前提后基线与分支同为 13/0）；`wt-create` 建 fix + test 工位。
- [x] T2: B2 全套产物（I-* issue / prd / brainstorm / pre-tests / tasks / IDN / review doc）+ milestone `M-20261112T015715Z-A`。
- [x] T3: 写 AT-001（10 静态 + 3 行为，含负向控制）；`git archive develop` 基线 RED。
- [x] T4: 改 `test-contract-single-source.py::registry_checks`：自建 cline stub + 三处 `env=env`；两条行为断言语义不变。
- [x] T5: `bin/test-all` 的 `CORE` / `CI_CORE` 各加一行 AT；注册 `gate/ci-machine-independence` story 并同步 `docs/epics-map.svg`。
- [x] T6: GREEN：干净 PATH 下 AT-001 13/0、原测试 13/0、`test-all --ci` 22/0；三个门禁与既有 AT 全绿。
- [x] T7: `issue-sync promote` + `promote-finalize`；GREEN 证据 `git add -f` 提交。
- [x] T8: `test-gate run`（不带 shim）→ `pr-create-guarded` → `pr-review-guarded` → `pr-merge-guarded` → `wt-close`。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity / 文档门禁） |
| T3 | AT-001（全部 13 项） |
| T4 | AT-001 静态 S1–S6 + 行为 B1 / B3 |
| T5 | AT-001 静态 S8–S10 + 行为 B2 |
| T6 | 回归 / CI / 门禁 |
| T7, T8 | E2E / Real-Environment |

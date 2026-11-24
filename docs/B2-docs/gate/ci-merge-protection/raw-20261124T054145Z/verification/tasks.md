# Tasks: I-20261124T054145Z-A

- owner_issue: I-20261124T054145Z-A
- pre_tests: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/pre-tests.md

## T1 — RED 测试先行
- 编写 `docs/system/workspace/scripts/tests/test-ci-merge-protection.py`，在 develop 基线跑出 RED（AT-001 三项失败 + AT-003 404）。
- 记录 RED 输出到 pre-tests.md 的 actual_RED_output 与证据文件。

## T2 — workflow 权限修复
- `.github/workflows/pr-merge-guard.yml` 增加 `permissions: contents: read / checks: write`。
- 不改 job 结构与 check 名。

## T3 — 移除自签 fallback
- `_set_governance_check_pass()` 在 check 缺失时报错退出；PATCH/查询失败非零返回；移除 `|| true`。
- 保留函数签名与调用点，不改其他治理门禁。

## T4 — 接入回归
- 新 AT 接入 `bin/test-all` 的 CORE 与 CI_CORE；跑 `bin/test-all --ci` 全绿（AT-002）。

## T5 — 平台分支保护设置
- 按 workflow 注释设置 develop 分支保护（一次性设置），用 `gh api` 只读验证并留存 AT-003 证据。

## T6 — GREEN 与交付
- 在 test-pre-merge 工位跑全量 GREEN；写 code-review；pr-create-guarded → review → merge → wt-close。

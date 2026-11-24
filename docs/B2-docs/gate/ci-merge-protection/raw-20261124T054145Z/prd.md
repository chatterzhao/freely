# PRD: CI 合并保护链 fail-closed 收口

- issue_id: I-20261124T054145Z-A
- source_candidate: docs/B1-docs/raw-20261124T054145Z/candidates.md#C-20261124T054145Z-A

## Goal

使 `CONSTITUTION.md:49`「hook/gate bypass 永久禁止」在 GitHub 平台层成为可验证事实：CI 能创建阻塞 check、develop 分支保护强制该 check、只有治理门禁通过后才置 success；任何 check 缺失或 API 失败都显式暴露而非自签吞掉。

## 实现方案

1. `.github/workflows/pr-merge-guard.yml` 顶层增加 `permissions`：`contents: read`、`checks: write`，使 guard job 的 `checks.create` 有权限。不改变 job 结构、check 名称或 verify job。
2. `docs/system/workspace/scripts/worktree/pr-merge-guarded` 的 `_set_governance_check_pass()`：
   - 查询 `governance/pr-merge-guard` check run；
   - 存在则 PATCH 为 success，PATCH 失败非零返回；
   - 不存在则**不再自行创建 success check**，而是报错退出（fail-closed），提示先运行 CI；
   - 移除所有 `|| true` 吞错。
3. develop 分支保护按 workflow `:9-31` 注释执行一次性设置（`required_status_checks.contexts=["governance/pr-merge-guard"]`、`enforce_admins: true`），并把 API 读取结果作为验收证据留存。
4. 新增自动化测试 `docs/system/workspace/scripts/tests/test-ci-merge-protection.py`，覆盖：workflow permissions 静态断言、自签 fallback 移除的源码断言、check 缺失时 pr-merge-guarded 非零退出。

## 不退化边界

- 不改变 `governance/pr-merge-guard` check 名称、verify job 的 `bash bin/test-all --ci`、SUMMARY 行格式。
- 不修改既有 governance gate 的判据或放宽任何门禁。
- 不触碰平台 issue 生命周期与 feedback/issue-sync 语义。
- 分支保护是平台侧一次性设置，不属于代码回归测试范围；本轮只要求结果可验证。

## Dev-Loop Handoff

见 `verification/pre-tests.md`：3 个 AT，AT-001 为端到端源码+行为回归（接入 `bin/test-all` CORE/CI_CORE），AT-002/003 为静态与分支保护证据断言。RED 阶段在 develop 基线上应失败，GREEN 阶段在工位应全绿。

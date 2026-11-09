---
schema_version: '1'
local_id: raw-20261103T132548Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132548Z-A
platform_ids:
  github:
    issue_id: '4151'
    url: https://github.com/chatterzhao/freely/issues/4151
    synced_at: ''
  gitee:
    issue_id: IKSPQ6
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ6
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/platform/raw-20261103T132548Z/issues/I-20261103T132548Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:25:48Z'
updated_at: '2026-11-09T05:55:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132548Z-A
source_candidate: ''
completed_at: '2026-11-09T05:43:50Z'
closeout_note: ''
---

# feat: 让测试证据链可验证并替换 CI 桩

workflow_kind: feature

## 根因
架构承诺「证据 + 门禁 > agent 自述」，但唯一能证明「测试跑过」的机器证据，是由 daemon 起停写的时间戳，而不是测试进程的退出码；唯一 CI 是打印 `CI OK` 的桩。

## 证据
- 唯一 CI 是桩：`.gitee-ci.yml:1-13` 注释直言 `Minimal CI — satisfies Gitee's "must pass tests" merge requirement`，`script: - echo "CI OK"`；`only` 覆盖 `develop / feature/* / hotfix/*`，而本仓特性分支是 `fix/*` → 连桩都未必触发。`.github/workflows/pr-merge-guard.yml:39-63` 只 `checks.create({status:'in_progress'})`，无任何 `run:` 步骤。
- 无聚合 runner：`package.json:4-15` 的 `typecheck` 等脚本无 CI 调用；`bin/` + `scripts/` 内无测试循环。测试资产 551 个 `scripts/tests/` + 15 个 `tests/` + 32 个 `bin/test-*`。
- 「测过」= daemon 起停：`docs/system/workspace/scripts/runtime/freely:8583-8601` 的 `_update_test_gate` 只写 `TEST_STATUS / LAST_TESTED_AT / LAST_TESTED_COMMIT`，无任何执行测试的动作；调用点 `:22216`（stop）、`:22586`（start）。
- 读侧只做弱校验：`docs/system/workspace/scripts/quality/pretests-retirement-gate:128-150` 只判 `TEST_STATUS != not_tested` + 时间非 1970 + commit 与 HEAD 相等；该文件是明文本地文件 `.freely/run/test-gate.env`，无签名、无 hash。
- 项目自己已记录：`docs/B1-docs/raw-20261102T103231Z/issue.md:44`（「只能人工写 test-gate.env，evidence 链不完整」）。
- 证据进不了 PR：`.gitignore` 排除 `*.log` 与 `.freely/`，但仓库有 304 个已跟踪 `.log`（全部靠 `git add -f`）；`docs/system/workspace/scripts/quality/pretests-gate:594-607` 只校验 `artifact_ref` 文件在本地存在。

## 影响
`printf` 三行写进 `test-gate.env` 即可让 `pretests-retirement-gate` 返回 0；回归只能靠人记得跑哪几个脚本，519 个无 `bin/` 入口的测试处于永久无人执行状态。所有质量声明（含本机构自身）都建立在作者自述之上，#4146 的 fail-open 又把这份自述放行到底。

## 修复方案
1. `_update_test_gate` 改为**由测试 runner 调用**，写入 `test_command`、`exit_code`、`HEAD`、证据文件 sha256；`pretests-retirement-gate` 校验 hash 与 `HEAD` 一致，不一致即失败。
2. `.github/workflows` 增加真实 job：`typecheck` + 可跑的 `scripts/tests` 子集 + `check-file-size` + `check-supply-chain-baseline`；`.gitee-ci.yml` 删掉 `echo "CI OK"`，并把 `fix/*` 加进 `only`。
3. 提供聚合入口（如 `bin/test-all` 或 `freely test`）：遍历 `scripts/tests/test-*` 与 `bin/test-*`，输出结果与退出码；首批只跑「已确认能跑」的子集，其余标 known-broken 并纳入 TODO（避免一上来全红）。
4. 证据进入版本控制：提供 `freely evidence add <file>`（内部 `git add -f` 并记录 hash），替代让人手工记 `-f`；`pretests-gate` 从「本地存在」改为「在 PR diff 中且 hash 匹配」。

## 验收标准
- RED：手写 `.freely/run/test-gate.env`（三行、HEAD 正确），`pretests-retirement-gate` 当前返回 0；修复后必须非零（缺 `test_command`/`exit_code`/hash）。
- RED：让一个测试失败后经 runner 写入，`exit_code` 非 0，`pretests-retirement-gate` 必须拒绝。
- GREEN：`grep -c 'echo "CI OK"' .gitee-ci.yml` = 0，且 `only` 含 `fix/*`。
- GREEN：`bin/test-all` 在干净 checkout 上退出码为 0，或输出明确的 known-broken 清单；CI job 有真实 `run:` 步骤。

---
candidate_id: C-20261112T015715Z-A
status: promoted
source_raw: raw-20261112T015715Z
created_at: 2026-11-12
milestone: M-20261112T015715Z-A
---

# Candidates

被否决方案（Option B/C/D）见 brainstorms.md。

## C-20261112T015715Z-A: registry 契约测试机器无关化（自建 cline stub）

- candidate_format_version: v2
- title: 让 `test-contract-single-source.py` 自建 tempfile stub 并注入 subprocess PATH，使 CI 不再依赖本机安装 cline
- status: promoted
- decision_reason: 产品侧「只部署 `command -v` 找得到的工具」是正确语义，缺陷在测试把「本机装了 cline」当成未声明前提。自建 stub 后断言真正验证 registry 被读取，且保留 registry missing fail-closed 与 explicit --tools 两条行为断言；改动面最小，不扩散到产品代码，CI 立刻机器无关。
- next_action: AT-001（静态 + 行为 + 不退化）→ develop `e003532b5` 基线 RED → 只改测试文件 → GREEN → `test-all --ci` 在干净 PATH 下 21/0 → `test-gate run` 不带 shim rc=0 → PR。
- revisit_trigger: registry 里 `cline` 段的 `test_command` 首词改名、或 `deploy-skills` 更换 installed 判据时，必须同步更新 stub 名并重跑 AT-001。
- acceptance_criteria:
  - RED：develop `e003532b5` 上直接跑 `test-contract-single-source.py` 为 `12 ok / 1 failed`；`test-all --ci` 为 `20 ok / 1 failed`；测试源码不含自建 stub 与 `env=` 注入。
  - GREEN：测试用 `tempfile.TemporaryDirectory()` 自建可执行 `cline` stub，并把 stub 目录前置到 `subprocess.run(..., env=...)` 的 PATH；不含任何硬编码机器路径、不写仓库、不修改 `os.environ` 全局。
  - GREEN：在**不含 cline、不带任何外部 shim** 的干净 PATH 下单跑该测试 `13 ok / 0 failed`，其中 registry missing fail-closed 与 explicit --tools 两条行为断言仍通过。
  - GREEN：`bin/test-all --ci` 在同样干净 PATH 下 `21 ok / 0 failed`；`freely test-gate run` 不带 shim 可 `TEST_STATUS=completed` / `TEST_EXIT_CODE=0`。
  - GREEN：AT-001 进 `bin/test-all` 的 `CORE` / `CI_CORE`，epics 注册 story，双 CI 接线。
  - 不退化：不修改 `bin/deploy-skills`、`bin/test-all` 的既有成员、`test-gate` 或任何门禁；其余现有 AT 全绿；`check-runtime-size` / `check-bin-projection` 仍 ok。
- promotion_gate: AT-001 RED → GREEN + 干净 PATH 下 `test-all --ci` 21/0 + `test-gate run` 不带 shim rc=0 + 三个门禁全过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 在 develop 基线与 R33 分支双跑同一测试证伪「本轮引入」；读 R33 diff 确认不触达；临时 stub 补齐前提后基线与分支同为 13/0，证明补的是环境前提而非放松判据；四个方案逐一评估并否决 C/D 两类放宽门禁做法。
  - verdict: pass
- promoted_issue_id: I-20261112T015715Z-A
- promoted_issue_path: docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/issues/I-20261112T015715Z-A.md
- milestone: M-20261112T015715Z-A
- session_refs: []

---
candidate_id: C-20261103T132548Z-A
status: promoted
source_raw: raw-20261103T132548Z
created_at: 2026-11-09
milestone: M-20261103T132548Z-A
---

# Candidates

被否决的替代方案（继续信任自述、一次跑全部、写进提交信息、上 PKI）见 brainstorms.md。

## C-20261103T132548Z-A: 测试证据链可验证 + 替换 CI 桩

- candidate_format_version: v2
- title: `test-evidence.py` 单一真源（8 字段 + sha256 校验）、`freely test-gate run` 真实执行、门禁 fail-closed、`bin/test-all` 聚合入口、Gitee/GitHub 真实 CI、`freely evidence add`
- status: promoted
- decision_reason: 手写三行 `test-gate.env` 即可让门禁返回 0；唯一 CI 是 `echo "CI OK"` 且 `fix/*` 不触发；519 个测试无聚合执行入口。R12.5 只解决了「谁来写」，没解决「写的是不是真的」。
- next_action: 建 AT-001（静态接线 + 隔离夹具真实驱动 `pretests-retirement-gate`、evidence 校验、test-all），改 4 个真源 + 2 个 CI 文件 + 新增 2 个入口。
- revisit_trigger: 若引入远端 CI runner 或把证据改成签名制品，需重新对齐 `EVIDENCE_FILE` 绝对路径语义与 hash 绑定。
- acceptance_criteria:
  - RED：隔离夹具手写三行 `test-gate.env`（HEAD 正确）→ 真实门禁返回 0；修复后必须非零且明确报出证据不可验证。
  - RED：runner 写入 `exit_code≠0` → 门禁拒绝。
  - GREEN：`.gitee-ci.yml` 中 `echo "CI OK"` 计数为 0 且 `only` 含 `fix/*`；GitHub workflow 有真实 `run:` 步骤。
  - GREEN：`bin/test-all` 在干净 checkout 退出 0 或输出明确 known-broken 清单；`test-gate run` 真实执行并写合法证据。
  - 回归：既有 test-gate / pretests / 生命周期 / 门禁测试与 develop 基线退出码一致。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 真机隔离夹具复现手写三行放行；逐行核对 CI 桩、gate 读侧、R12.5 record 写入；证伪 #4216/#4146/#4147/#4198/#4075 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261103T132548Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261103T132548Z/issues/I-20261103T132548Z-A.md
- milestone: M-20261103T132548Z-A
- session_refs: []

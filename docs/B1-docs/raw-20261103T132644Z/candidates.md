---
candidate_id: C-20261103T132644Z-A
status: promoted
source_raw: raw-20261103T132644Z
created_at: 2026-11-10
milestone: M-20261103T132644Z-A
---

# Candidates

被否决方案与其余 6 个分项的承接见 brainstorms.md。

## C-20261103T132644Z-A: supervisor 失败退出码 + Python 版本前置

- candidate_format_version: v2
- title: `will now stop` 分支改 `exit 1` 并记录 `exit_kind=degraded_no_recovery`；`bin/freely` 在 exec 前检查 Python >= 3.11
- status: promoted
- decision_reason: 无恢复路径时以 0 退出让 systemd/tmux 视为正常停止、不触发重启；Python 版本不足时首错是深处的 `ModuleNotFoundError`，与真实原因相距很远。两者都是「失败被表达成正常/不可诊断」。
- next_action: AT-001（3 静态 + 3 行为）→ develop 基线 RED → 改 exit 1 + 事件补 exit_kind + 入口前置检查 → GREEN → 回归 → PR。
- revisit_trigger: 若 supervisor 的外层调用方约定「0 = 已处理、非 0 = 需要重启」发生变化，或 Python 最低版本提升/降低，需重述断言。
- acceptance_criteria:
  - RED：基线 `will now stop` 后为 `exit 0`；`bin/freely` 无版本检查；stub 旧版本仍能跑到 runtime。
  - GREEN：AT-001 `6 ok / 0 failed`；旧版本非零退出且文案含 `Python >= 3.11`；新版本与真实环境 `--help` rc=0。
  - GREEN：不改 `append_runtime_event` 签名、不动 120 个调用点、不改其它退出路径。
  - GREEN：CLI help / 并发 / DB / 派发 / 契约 / wt-create 回归 0 新增失败；`test-all --ci` 执行新 AT。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 在 `runtime/freely:24144-24149` 确认 `exit 0`；确认 `bin/freely-package:95-108` 已有 output 守卫（分项 5 过时）；确认 `bin/freely` 无任何版本检查；用 `git archive develop` 基线跑最终版 AT 得到 RED `2 ok / 4 failed`；用 stub python3 预演旧/新版本两条路径。
  - verdict: pass
- promoted_issue_id: I-20261103T132644Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132644Z/issues/I-20261103T132644Z-A.md
- milestone: M-20261103T132644Z-A
- session_refs: []

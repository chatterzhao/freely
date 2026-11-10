---
candidate_id: C-20261110T101358Z-A
status: promoted
source_raw: raw-20261110T101358Z
created_at: 2026-11-10
milestone: M-20261110T101358Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T101358Z-A: 恢复 a2a_task.py CLI 可加载性并纳入 CI 冒烟

- candidate_format_version: v2
- title: 文件头加 `from __future__ import annotations`；新增 `test-a2a-task-cli-loadable.py` 并同时接入 `bin/test-all` 的 `CORE` / `CI_CORE`
- status: promoted
- decision_reason: `:435` 的前向引用标注让模块导入即抛 `NameError`，派发循环所有 `python3 a2a_task.py ... || true` 静默失败，worker 派发停摆且 CI 全绿无感知；是 #4254 的前置阻塞。
- next_action: 建 AT-001（3 静态 + 5 行为）→ 一行修复 → 接入 CI → RED/GREEN → 回归。
- revisit_trigger: 若将来把 `a2a_task.py` 拆成包或改用 py3.14 延迟标注，需重述冒烟断言。
- acceptance_criteria:
  - RED：develop 基线 `import` / `list` / `update` 全部 `NameError`，冒烟未接入 test-all。
  - GREEN：AT-001 `8 ok / 0 failed`；CLI 返回业务错误而非 NameError；`SSEPool` 等类仍定义。
  - GREEN：`bin/test-all --ci` 实际执行新冒烟且全绿；`test-reviewer-contract.py` 等既有回归不退化。
  - GREEN：不改状态机语义、不改 `--state`/`--status` 参数、不改 SSEPool 实现、不改 shell 容错语义。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 实测 develop 与安装态均 `NameError`；`git diff develop` 确认为现状；`git log -S` 定位引入提交；确认无 future import、仅一处前向引用；在文件副本上预演修复后 CLI 返回明确业务错误；确认 `bin/test-all` 两个列表结构。
  - verdict: pass
- promoted_issue_id: I-20261110T101358Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T101358Z/issues/I-20261110T101358Z-A.md
- milestone: M-20261110T101358Z-A
- session_refs: []

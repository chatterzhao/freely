---
candidate_id: C-20261104T075903Z-A
status: promoted
source_raw: raw-20261104T075903Z
created_at: 2026-11-11
milestone: M-20261104T075903Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075903Z-A: 协调契约 + 枚举迁出 agents/（第一阶段）

- candidate_format_version: v2
- title: `contracts/coordination/` 单一契约 + `scripts/runtime/coordination/` 包 + 消除 agents sys.path + lint + 单页文档
- status: promoted
- decision_reason: 协调语义无机器可读真源，且 reason 枚举靠 sys.path hack 才能 import；先做零语义变化的契约与迁移，给后续 server/client/router 收敛留出可机检的落点。
- next_action: AT-001（14 静态 + 2 行为）→ develop `90abdd4f4` 基线 RED `1 ok / 15 failed` → 实现 → GREEN `16 ok / 0 failed` → 回归 + CI → PR。
- revisit_trigger: 后续收敛 a2a_types/a2a_server/a2a_task 时，契约的 task_states/sse_topics 必须与实现做机器校验（本阶段只记录真源，不强校验）。
- acceptance_criteria:
  - RED：无契约、无 coordination 包、watchdog 仍注入 agents/、裸名导入、枚举仍在 agents/、无 lint、无单页文档、AT 未进 CI、epics-map 无 story。
  - GREEN：契约四段齐全且 stdlib 可解析；12 个 reason 与 Enum 逐项一致。
  - GREEN：runtime 与 tests 中 `sys.path.insert.*agents` 为 0；watchdog 与三个测试都走 `coordination` 包导入。
  - GREEN：lint 对契约/枚举漂移 rc≠0、对合规 rc=0；coordination 包无反向 import `runtime/freely`。
  - GREEN：单页文档列出状态机与 exit contract 合法值；AT 进 CORE/CI_CORE；epics-map 注册 story。
  - 不退化：不改 a2a_types/a2a_server/a2a_task 一行；不改 `manager_exit_contract_kind` 逻辑；不改 workflow 全链路。
- promotion_gate: AT-001 RED → GREEN + `test-all --ci` 17/0 + epics-map 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行确认 watchdog 的两处 sys.path（修正 BSD grep 误判）；全仓扫描 3 个测试的同族依赖；用 `git archive develop` 快照复现 RED；用临时 fixture 验证 lint 的漂移/合规退出码。
  - verdict: pass
- promoted_issue_id: I-20261104T075903Z-A
- promoted_issue_path: docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/issues/I-20261104T075903Z-A.md
- milestone: M-20261104T075903Z-A
- session_refs: []

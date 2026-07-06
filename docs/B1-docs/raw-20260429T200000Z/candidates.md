# Candidates - 20260429-2000--gate-dev-experience-preflight

### C-20260429T200000Z-A: legacy issue

- title: `Gate dev experience: --range pre-flight + secret detection FP fix`
- status: `promoted`
- scope: governance-merge-gate --range 文件读取修复、pr-merge-guarded 预检集成、pre-commit 密钥检测误报修复
- priority: `P1`
- type: `improvement`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `done_pre_brainstorm`
- promoted_issue_path: `docs/B2-docs/gate/gate-dev-experience-preflight/raw-20260429T200000Zissues/I-20260429T200000Z-A.md`
- session_refs:
  - {tool: ccds, session_id: "20260429-gate-dev-exp", jsonl_path: "unavailable://manual", role: "author"}
- acceptance_criteria:
  - --range 从 develop 可以读取 feature 分支的新文件
  - pr-merge-guarded 在 feature→test-pre-merge 时自动预检
  - milestones.md 提交不再触发密钥误报
- promotion_gate: `governance-merge-gate`
- open_questions: []
- acceptance_reviews:
  - reviewer: `human`
  - status: `pending`
- next_action: `Merge into develop.`

# Candidates - 20260429-1745--bash32-daemon-compat-fix

### C-20260429-1745-A

- title: `Fix daemon self-detection suicide + bash 3.2 pipefail crash`
- status: `promoted`
- scope: macOS bash 3.2 兼容性修复，两处防御性代码改动
- priority: `P0`
- type: `bugfix`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `chat_intake`
- phase_state: `done_pre_brainstorm`
- promoted_issue_path: `docs/B2-docs/runtime/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md`
- session_refs:
  - {tool: ccds, session_id: "20260429-bash32-fix", jsonl_path: "unavailable://manual", role: "author"}
- acceptance_criteria:
  - daemon 在 macOS bash 3.2 上可正常启动不再自杀
  - supervisor 首次启动能正确进入 main loop
- promotion_gate: `governance-merge-gate`
- open_questions:
  - 是否需要为 Homebrew bash 5.x 做兼容性回归测试
- acceptance_reviews:
  - reviewer: `human`
  - status: `pending`
- next_action: `Merge into develop via test-pre-merge batch.`

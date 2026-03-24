# Progress: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- phase_state: `in_progress`
- summary: `pre-test-merge` dogfood 暴露出新一层 handoff contract gap：manager 已生成 latest continuity 与 worker prompts，但 prompt 本体缺少 runtime 可稳定解析的 worker target header，导致 generated truth 未被消费成真实 worker launch。
- current_focus:
  - harden worker prompt contract so runtime accepts both stable `Worktree/Branch` headers and the current natural-language worker sentence
  - re-run dogfood after merge to verify latest continuity resumes launching worker runtimes

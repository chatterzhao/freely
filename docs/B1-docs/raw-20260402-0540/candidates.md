# 候选：runtime-loop-log-timezone-label-followthrough

- id: `C-20260402-0540-A`
- candidate_format_version: `v2`
- title: Label runtime loop log timestamps with the host timezone
- source_brainstorm: `docs/B1-docs/raw-20260402-0540/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/issues/runtime-human-readable-time-display-governance.md`
- reopen_reason: `a repo-wide audit found that loop.log headers still printed local wall-clock time without a timezone label after the runtime time-display owner had otherwise closed`
- problem: `freely` loop logs still expose one human-readable timestamp surface without the timezone label required by the canonical host-local display rule.
- why_now:
  - the code fix is tiny and already isolated, but the develop merge gate correctly refuses candidate-less followthrough patches
  - leaving the log header unlabeled keeps a human-facing runtime surface inconsistent with the rest of the time-display policy
  - this is narrower than reopening the original runtime-wide owner and should close immediately after merge replay
- acceptance_criteria:
  - the reopen is recorded as a narrow followthrough of the completed runtime human-readable time display owner
  - `freely` loop log headers render host-local time with a timezone label
  - a focused regression checks `loop.log` directly in a deterministic timezone
  - no stored RFC3339/epoch truth or UTC naming truth changes
- promotion_gate:
  - keep scope limited to the loop log header and its focused regression
  - do not reinterpret this followthrough as permission to localize stored truth or backup naming
  - attach the owner to `workspace-routing-foundation`, not the frontend probe family
- open_questions:
  - none; the canonical rule is already frozen and this owner only closes the last discovered display leak
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The remaining gap is a single human-readable loop log header that already uses host-local time but omits the timezone label. Narrow followthrough is the correct governance shape.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - the runtime display contract is already canonical, so a fresh narrow followthrough is smaller and clearer than widening or reopening the previous owner
  - the merge gate requires a full candidate -> issue -> progress -> review trace even for tiny develop-bound fixes
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-loop-log-timezone-label-followthrough-governance/issues/runtime-loop-log-timezone-label-followthrough-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260402-0540-A` owns the loop log display-label closeout and the minimal develop-bound writeback needed for merge replay.
- revisit_trigger:
  - reopen only if additional human-readable runtime time surfaces are found after this loop log label followthrough lands

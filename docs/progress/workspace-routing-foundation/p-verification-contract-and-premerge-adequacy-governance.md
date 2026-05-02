# Progress: verification-contract-and-premerge-adequacy-governance

- issue_id: `I-20260408-1205-A`
- phase_state: `completed`
- summary: verification contract 已从“提示词约束”收紧为运行时与 merge gate 都会消费的 machine-readable 真源。worker launch intake 与 worker runtime state 现在会投影 owner issue、pre-tests 路径、artifact 目录、required test lanes、acceptance item ids、最低 evidence level、target environment、closeout gate；`pretests-gate` 同时把四个必备章节的 schema、有限 `not_applicable` 理由和 `replacement_evidence` 兜底落成可执行门禁。
- next_action: `completed`
- revisit_trigger: 若后续发现 test-pre-merge 或 develop push 仍能在缺少 owner lifecycle evidence、缺少 replacement evidence、或 recovery 丢失 verification contract 投影时放行，则继续开 follow-on issue 收紧 protected merge / recovery followthrough。
- current_focus:
  - worker verification contract is written into delegated intake and worker runtime state
  - pre-tests four-section schema is machine-readably enforced
  - develop-bound merges must carry same-line owner lifecycle evidence instead of bare code changes
  - absorbed stale-prebrainstorm follow-on `C-20260411-1417-B` is now explicitly tracked back to this canonical owner so future reconcile-only batches do not reopen a duplicate launch-time verification lane

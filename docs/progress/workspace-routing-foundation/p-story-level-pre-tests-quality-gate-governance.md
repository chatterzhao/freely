# Progress: story-level-pre-tests-quality-gate-governance

- issue_id: `I-20260325-0410`
- phase_state: `in_verification`
- summary: story-level `pre-tests.md` 质量 gate 已从 umbrella testing candidate materialize 成独立 issue，并已写回 `doc-ibm-execution`、其 references、`three-loop-capability-lifecycle`、`LAWS.md` 与 `pre-test-merge` acceptance truth。当前最小 contract 已冻结：`pre-tests.md` 至少要表达 acceptance target、testing layer、target environment、required evidence 与 blocker taxonomy；最小 blocker taxonomy 明确区分 `definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`。当前批次已通过 `./bin/governance-check` 与多轮并行评审，保持 `in_verification`，等待后续 manager merge review / canonical absorption。
- next_action: 保持 `in_verification`，等待 manager merge review / canonical absorption；这一批只收敛 story-level `pre-tests.md` 质量 gate，不继续扩写 testing ladder / real-environment harness。
- revisit_trigger: 当 `I-20260325-0410` 被 manager 吸收为 completed，或 review 发现 `LAWS.md` / `three-loop-capability-lifecycle.md` 仍有与本 issue 冲突的 truth wording 时，再回到 doc-loop 修正并决定 umbrella candidate `C-20260325-0333-A` 的后续切口。
- current_focus:
  - 确认 capability truth wording 在 merge review 中无新的 contract 冲突
  - 保持 umbrella candidate `C-20260325-0333-A` 继续 active，只把首个 slice `C-20260325-0333-B` 视为已 materialize

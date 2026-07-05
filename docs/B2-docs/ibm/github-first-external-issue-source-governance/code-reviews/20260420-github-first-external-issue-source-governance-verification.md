# Verification: github-first-external-issue-source-governance

- issue_id: `I-20260407-1042-A`
- issue_path: `docs/B2-docs/ibm/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`
- verification_date: `2026-04-20`
- verifier: `codex`

## Scope Verdict

- `PASS`: the owner package explicitly limits raw scan to open and unconsumed source issues, closing the ambiguity that would otherwise let patrol treat every open GitHub issue as fresh intake.
- `PASS`: canonical repo-native linkage remains the decisive dedupe authority and external labels/comments stay advisory only, which matches the three-loop internal-owner boundary.
- `PASS`: source-routing consumer truth now uses `external issue` as the durable family term in `context-source-skill`, `source-classification`, `lead-agent`, and the startup prompt template.
- `PASS`: the remaining protected-branch acceptance surface for this owner is guarded premerge replay plus canonical develop absorption, not new runtime/API automation.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
2. `bash docs/system/workspace/scripts/tests/test-human-chat-routing`
3. `./bin/governance-check`
4. `git diff --check`
5. `rg -n "external issue|source_consumption_state|publication_mode|canonical repo-native linkage" docs/B1-docs/raw-20260407T104200Z docs/B2-docs/git-worktree/github-first-external-issue-source-governance docs/system/workspace/skills/context-source-skill docs/system/workspace/agents/lead-agent.md docs/system/workspace/scripts/compose-context-source-prompt.sh`

## Residual Risks

1. Runtime implementation still has to decide whether canonical source metadata can stay document-driven or whether a bounded local mapping artifact is required.
2. Public-status vocabulary is intentionally minimal; future publication automation may still need a small follow-on owner if external expectations widen.

## Implementation Decision Note

- decision: `Keep the first external-source owner GitHub-first and documentation-facing, and require any real provider automation to start from this frozen contract instead of widening the current lane.`
- why_this: `The observed gap was contract drift in source-routing truth, not missing provider API calls. The smallest lawful fix is to freeze the intake, dedupe, and closeout boundary in the owner package already linked to the source candidate.`
- alternatives_considered: `Leave the work in candidate-only pre-research; widen directly into GitHub/Gitee provider automation; change source-facing docs ad hoc without owner materialization.`
- boundary_non_goals: `This owner does not implement provider APIs, does not make GitHub the canonical owner truth, and does not widen into generic multi-platform publication policy.`
- residual_risk: `A later implementation owner may still need a bounded local mapping artifact or a narrower shared scan helper if document-driven linkage stops being sufficient.`

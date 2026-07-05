# Issue: github-first-external-issue-source-governance

- issue_id: `I-20260407-1042-A`
- title: `GitHub-first external issue source governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `github-first-external-issue-source-governance`
- issue-name: `github-first-external-issue-source-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260407-1042/candidates.md#c-20260407-1042-a`
- source_brainstorm: `docs/B1-docs/raw-20260407-1042/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-github-first-external-issue-source-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
- created_at: `2026-04-20`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely has already contracted durable source families to `human interruption` and `external issue`, but the runtime-facing source contract still exposes the older loose `github issue` wording and does not yet freeze how raw external issues become canonical intake.

Without a bounded owner here:

1. standing-source patrol can drift toward “scan every open issue”
2. stale external labels/comments can be mistaken for decisive truth
3. source issue intake, canonical owner linkage, and public tracking can collapse back into one GitHub object
4. later runtime implementation would have no stable contract for discard closeout, accept-and-bind closeout, or source dedupe

This owner freezes the GitHub-first contract and lands the first consumer-facing truth in `context-source-skill` before widening into runtime API automation.

## Scope

1. Freeze the GitHub-first raw source scan contract for open and unconsumed external issues.
2. Freeze the canonical source metadata and `source_consumption_state` contract needed for dedupe and closeout.
3. Freeze source closeout behavior for discard versus accept-and-bind.
4. Freeze when `source issue` may double as `publication target` and when a separate public tracking issue is required.
5. Update source-facing agent/skill/prompt truth so Freely talks about `external issue` as a durable source family rather than the older loose `github issue` term.
6. Carry the minimum owner/progress/review/test evidence needed so later implementation can start from a stable contract.

## Non-Goals

1. Do not implement GitHub or Gitee API create/sync automation in this owner.
2. Do not widen this owner into generic multi-platform abstraction.
3. Do not make GitHub the canonical owner truth for milestone, issue, progress, or completion state.
4. Do not reopen human-interruption family semantics from this owner.

## Acceptance

1. Canonical docs define that raw external issue scan covers only open and unconsumed source issues, not all open issues.
2. Canonical docs define that canonical repo-native linkage is decisive dedupe authority and external labels/comments are hints only.
3. Canonical docs define the minimum canonical source metadata contract, including `source_family`, `source_kind`, `source_ref`, `source_consumption_state`, and `publication_mode`.
4. Canonical docs define discard closeout, accept-and-bind closeout, and the default issue-comment writeback surface.
5. `context-source-skill`, its source-classification reference, and adjacent lead-agent/startup prompt truth all use `external issue` as the source-family term and mention the family boundary clearly enough for follow-on implementation.
6. `./bin/governance-check`, `git diff --check`, and focused routing/doc tests pass in the feature worktree.

## IBM Handoff

- implementation_scope_summary:
  - This owner freezes the GitHub-first external-source contract and lands the first consumer-facing documentation updates in the source-routing skill stack.
  - Follow-on implementation should start from this contract when adding actual external-source scan, canonical metadata persistence, and closeout/writeback behavior in runtime code.
- required_doc_refs:
  - `docs/B1-docs/raw-20260407-1042/brainstorms.md`
  - `docs/B1-docs/raw-20260407-1042/candidates.md`
  - `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/brainstorms/b-github-first-external-issue-source-governance.md`
  - `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/tasks.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/context-source-skill/references/source-classification.md`
  - `docs/system/workspace/scripts/compose-context-source-prompt.sh`

## Verification

- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/tests/test-human-chat-routing`
- `./bin/governance-check`
- `git diff --check`
- `rg -n "external issue|source_consumption_state|publication_mode|canonical repo-native linkage" docs/B1-docs/raw-20260407-1042 docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance docs/system/workspace/skills/context-source-skill docs/system/workspace/agents/lead-agent.md docs/system/workspace/scripts/start-lead-agent.sh`

## Completion

- `docs/B1-docs/raw-20260407-1042/brainstorms.md`
- `docs/B1-docs/raw-20260407-1042/candidates.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/brainstorms/b-github-first-external-issue-source-governance.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/prd.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-decision.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- `docs/progress/workspace-routing-foundation/p-github-first-external-issue-source-governance.md`
- `docs/system/workspace/skills/context-source-skill/SKILL.md`
- `docs/system/workspace/skills/context-source-skill/references/source-classification.md`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/scripts/compose-context-source-prompt.sh`
- `docs/system/workspace/scripts/start-lead-agent.sh`

## Next

- Complete IBM-level followthrough only if new acceptance items are needed for runtime implementation.
- Open a separate implementation owner when runtime is ready to persist canonical source metadata and perform real external closeout/writeback actions.

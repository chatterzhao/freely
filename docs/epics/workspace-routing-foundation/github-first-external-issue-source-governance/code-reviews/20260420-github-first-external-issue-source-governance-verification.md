# Verification Review: github-first-external-issue-source-governance

- owner_issue: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`
- review_scope: `bounded GitHub-first external-source contract materialization plus source-routing consumer truth updates`

## Findings

1. The source contract now explicitly limits raw scan to open and unconsumed source issues, which closes the main ambiguity that would otherwise let patrol treat every open GitHub issue as fresh intake.
2. The owner package now makes canonical repo-native linkage the decisive dedupe authority and keeps external mirrors secondary, which matches the three-loop internal-owner boundary.
3. The routing truth now uses `external issue` as the durable family term in `context-source-skill`, `source-classification`, `lead-agent`, and the startup prompt template, which reduces the risk of reintroducing GitHub-object collapse in follow-on implementation.

## Residual Risks

1. Runtime implementation still has to decide whether canonical source metadata can stay document-driven or whether a bounded local mapping artifact is required.
2. Public-status vocabulary is intentionally minimal; future publication automation may still need a small follow-on owner if external expectations widen.

## Verification Commands

- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/tests/test-human-chat-routing`
- `./bin/governance-check`
- `git diff --check`

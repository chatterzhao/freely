# Brainstorms - 20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition

## Context

- source: continuation from `I-20260405-0027-A` verification and the user request to decide when the switch backend should split into a standalone app
- related owner: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- observed local skeleton: `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch`

## Observations

1. Freely now has the first strong Codex contract for slot bundle save/switch/probe, but the implementation still lives in `docs/system/workspace/scripts/runtime/ai-cli` and watchdog shell.
2. IBM docs already froze the long-term direction as a standalone CLI-first backend named `ai-switch-cli`, with Freely acting as control plane and JSON consumer.
3. The existing local repository skeleton is not yet a real product baseline:
   - the repository name and README still say `codex-account-switch`
   - the repo has no commits
   - current contents are mostly governance scaffolding, not a stable backend implementation
4. Splitting too early would create two moving truth surfaces:
   - Freely-internal slot logic would still be evolving
   - the standalone repo would either duplicate unstable shell logic or become an empty promise

## Decision Frame

The split should happen only after the backend boundary is stable enough that Freely can consume a CLI contract rather than importing tool-private file knowledge. That implies extraction should be gated by capability maturity, not by the mere existence of a placeholder repository.

## Candidate Threshold

Extract to standalone `ai-switch-cli` only when all of the following are true:

1. command surface is frozen for `list/current/login/save/switch/delete/probe/best/status`
2. JSON envelope is frozen and already consumable by Freely without extra stdout parsing quirks
3. at least one tool, currently Codex, has verified save/switch/probe/materialization semantics including backup-before-mutation for user-home config
4. shared helper surfaces that are not tool-specific, such as file-backup and generic slot inventory plumbing, are already separated from one-off inline script code
5. a follow-on owner explicitly defines which parts stay in Freely control plane and which move into the backend

## Skeleton Disposition

The current local skeleton should not continue as `codex-account-switch`.

Recommended handling:

1. keep the directory as disposable local scaffolding until extraction is formally started
2. when the extraction owner begins, rename the repo to `ai-switch-cli`
3. rewrite `README.md`, `PROJECT_INTENT`, `AGENTS.md`, and top-level naming before the first real commit
4. do not copy current Freely implementation into that repo until the extraction owner defines the move boundary
5. if the skeleton contains no useful repo-local truth beyond boilerplate, it is acceptable to discard it and create a fresh `ai-switch-cli` repo instead

## Non-Goals

1. do not start packaging or releasing a standalone backend from this brainstorm
2. do not move current `ai-cli` code out of Freely in the same lane as Codex verification
3. do not treat the empty skeleton as canonical evidence that extraction has already begun

# PRD: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

## Problem

Freely claims a CLI-first bootstrap path for arbitrary target projects, but canonical replay still shows two first-hop defects:

1. `sync-tooling` can leave target config truth anchored to the source repo.
2. Fresh projects still need manual `.githooks` copying before `init`.

## User Outcome

An operator should be able to:

1. create or point at a fresh git project with the canonical Freely docs,
2. run `freely sync-tooling --source-project <authoritative-project> --project <fresh-git-project>`,
3. inspect `freely baseline-status --project <fresh-git-project>` or `freely status --project <fresh-git-project> --view baseline`,
4. run `freely init --project <fresh-git-project> ...`,

without seeing the source project leak back into target status output or needing manual hook copying.

## Product Boundaries

1. This owner only repairs managed bootstrap surfaces: target-local config retargeting and hook rematerialization.
2. It does not broaden into runtime lifecycle semantics or generalized project cloning.
3. It must keep the command surface machine-checkable through focused behavior tests, not only manual docs claims.

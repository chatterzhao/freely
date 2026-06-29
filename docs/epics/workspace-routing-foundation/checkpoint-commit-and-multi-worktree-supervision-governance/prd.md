# PRD: checkpoint-commit-and-multi-worktree-supervision-governance

## Goal

让 Freely 在自举开发 Freely 自己时，能用 CLI-first 方式监督多个 worktree 工位，并在合适时机强制 checkpoint，而不是持续累积跨 issue 脏树。

## Product Surface

- `./bin/checkpoint-guard`
- `./bin/wt-fleet-status`
- `freely baseline-status --project <worktree>`
- `pre-commit` staged scope gate

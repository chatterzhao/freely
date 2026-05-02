# Code Review: worktree-maintenance-governance

## Scope Reviewed

- `docs/system/workspace/skills/worktree-maintenance-governance/**`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Findings

- No blocking findings.

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Residual Risks

- 目前只是治理与 prompt 能力，还没有把 merge-prep 自动化成 CLI；一旦后续需要自动生成冲突面或 retirement checklist，应从新 candidate 继续展开，而不是把这条 skill 无限扩写。

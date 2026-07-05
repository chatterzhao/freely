# PRD: kiro-cli-runtime-availability-failure-governance

## Problem

Freely already had availability governance for Codex/OAuth-oriented failure families, but Kiro's observed monthly-limit and subscription-status-service-error outputs still fell through as ordinary `rc=0` exits. That produced false healthy state and immediate relaunch churn.

## Product Decision

The first owner stays narrow and Kiro-specific:

1. classify the two observed strings,
2. emit a canonical `slot_switch_reason`,
3. stop local blind relaunch, and
4. defer follow-on recovery to the watchdog / manager control plane.

This slice explicitly does not widen into generic cross-tool fallback orchestration.

## User / Runtime Outcome

- operators and runtime artifacts no longer see a fake healthy `ai_exit_rc_0`
- control-plane truth carries a concrete Kiro reason
- the same supervisor does not immediately relaunch into the same known-unusable path

## Proof

- runtime classifier in `docs/system/workspace/scripts/runtime/freely`
- focused regression in `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- tooling / availability truth writeback in `docs/system/workspace/tools.md` and `docs/system/workspace/skills/ai-cli-availability-manager/references/limit-patterns.md`

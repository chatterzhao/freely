# Brainstorm - 20260405-1505--manager-semantic-loop-active-worker-suppression

## Problem

Canonical `develop` still fails `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface` at the assertion that semantic-loop suspicion must clear once a worker is already running.

## Observed Runtime Facts

- The failing assertion is reproducible on current canonical `develop` after the 2026-04-04 missing-run-dir guard landed.
- `I-20260322-0445` already completed its latest continuity / prompt generated-consumed truth contract and explicitly says future queue or active-worker evolution should continue in a new lifecycle instead of reopening that owner.
- The semantic-loop signal is meant to stay conservative: active worker execution or no available capacity must suppress the loop suspicion, not coexist with it.

## Routing Judgment

- This is a new follow-on owner on `workspace-routing-foundation`.
- It should not reopen `latest-manager-continuity-worker-consumption-governance`; that owner remains the completed record for latest generated/consumed truth and missing-run-dir parser quieting.
- The new owner should freeze a stricter semantic-loop suppression contract: when runtime already has authoritative active worker evidence or the current launch-state still records active workers, `live-status` / `fleet-status` must not report a semantic loop.

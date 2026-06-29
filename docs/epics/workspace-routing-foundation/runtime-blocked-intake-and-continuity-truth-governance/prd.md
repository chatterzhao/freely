# PRD: runtime-blocked-intake-and-continuity-truth-governance

## Goal

冻结 runtime supervision 在 blocked execution surface 下的 intake / continuity truth，避免系统继续以 “prompt 在刷新，所以 manager 还活着” 的 false-active 状态掩盖 claim / continuity 没有前进的事实。

## Why Now

`2026-04-04` 的 canonical `develop` 现场已经给出足够强的真实证据：

1. human intake durability 仍正常
2. prompt assembly 仍正常
3. 但 continuity materialization 和 intake claim writeback 没有前进

这说明现有 owner 虽然分别覆盖了 network taxonomy、bootstrap continuity、delegated absorption 和 latest consumption，但还缺一个专门定义 blocked supervision truth 的 narrow contract。

## Product Surface

- current runtime surfaces:
  - `.freely/intake/*/meta.env`
  - `.freely/run/prompt-*.txt`
  - `.freely/run/manager-continuity-*.md`
  - `freely live-status`
  - `freely fleet-status`
- current evidence families:
  - execution-time websocket permission denied
  - shared slot-switch busy before launch
  - local fork/resource exhaustion

## Non-Goals

- redesigning generic network retry / cooldown policy
- changing slot or cross-tool fallback semantics
- redefining delegated intake closure for successful rounds
- implementing GitHub issue automation or unrelated supervisor orchestration

## Problem Contract

The blocked state targeted by this owner is specifically:

1. intake is durably present
2. prompt generation or refresh still happens
3. but runtime cannot successfully move into one of the truthful next states:
   - intake claimed
   - continuity materialized
   - blocked handoff artifact written

Without a dedicated truth surface, the control plane appears active while machine-readable progress is frozen.

## Required Truth Surfaces

The follow-on implementation owner must choose a bounded design that makes all three truths explicit:

1. intake truth
   - no indefinite misleading `STATUS="new"` once prompt-visible blocked supervision is confirmed
2. continuity truth
   - either a new manager continuity file exists, or an equivalent blocked artifact explains why not
3. status truth
   - `live-status` / `fleet-status` expose that prompt visibility advanced but claim / continuity did not

## Current Trigger Family

The owner currently treats these as candidates for the same blocked family:

1. websocket `Operation not permitted` / permission-denied execution failures
2. shared slot-switch busy that prevents launch progress
3. local `fork: Resource temporarily unavailable` or similar process-capacity exhaustion

This is a supervision-truth family, not a statement that all three reasons share the same recovery mechanics.

## Boundary With Neighbor Owners

### Runtime network failure taxonomy keeps

1. classifying execution failures
2. retry / cooldown semantics
3. same-slot bounded relaunch rules

### This owner keeps

1. blocked intake / continuity truth after prompt visibility
2. blocked-state artifact requirements
3. machine-readable status surface for false-active supervision

### Bootstrap continuity owner keeps

1. startup path from first prompt publication to continuity materialization
2. worker-dispatch parsing during successful bootstrap

### Delegated intake closure owner keeps

1. successful manager-owned absorption closure
2. absorbed lifecycle writeback after continuity exists

## First Implementation Slice

The first dev-loop should stay narrow:

1. reproduce prompt-visible-but-unclaimed supervision in a deterministic test or harness
2. add blocked-state writeback with the minimum artifact set
3. expose the blocked state in status surfaces
4. prove prompt churn no longer masquerades as healthy progress

It should not:

1. redesign generic watchdog policy
2. widen slot/tool fallback logic
3. reopen semantic-loop recovery

## Acceptance Summary

This owner is complete only when the docs make all three statements explicit:

1. prompt visibility without claim / continuity advance is a dedicated blocked supervision state
2. the blocked state is separate from generic network taxonomy and separate from successful delegated absorption closure
3. a later implementation owner can update runtime truth surfaces without re-researching the family boundary

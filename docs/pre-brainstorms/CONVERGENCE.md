# Candidates Convergence (Phase-1)

Date: 2026-03-05

## Convergence Rule
Each candidate is checked by reverse constraints before entering issue queue:

1. Intent fit (`docs/PROJECT_INTENT.md`)
2. Constitution/Laws fit (`docs/CONSTITUTION.md`, `docs/LAWS.md`)
3. Flow fit to unified loop diagram (A1 -> A2 -> IBM/DDD -> A3)
4. Implementation feasibility in current architecture/scope
5. Value > Cost (if changing loop/flow logic)

Only candidates passing all 5 checks become issue-ready.

## Issue-Ready (Enter Queue Now)

### Batch P0-Core
1. `C-20260304-601` Owner Loop Contract
- route: A1/A2 -> doc-loop(IBM)
- output target: loop contract + state transitions
- dependency: none

2. `C-20260304-602` Gate Contract
- route: A1/A2 -> doc-loop(IBM)
- output target: enforceable gate definitions
- dependency: C-20260304-601

3. `C-20260304-603` Recovery Contract
- route: A1/A2 -> doc-loop(IBM)
- output target: resume/bridge protocol
- dependency: C-20260304-601

4. `C-20260304-604` Issue Discovery + Router Kernel
- route: A1 -> A2 -> auto-loop(ADD)
- output target: source scan + routing decision logic
- dependency: C-20260304-601

5. `C-20260304-607` Doc Contract Compiler
- route: doc-loop(IBM) -> dev-loop(DDD)
- output target: acceptance -> executable checks
- dependency: C-20260304-602

6. `C-20260303-101` CLI Orchestration MVP
- route: auto-loop(ADD) / dev-loop(DDD)
- output target: command orchestration + retry/timeout/log
- dependency: C-20260304-601

7. `C-20260303-102` Integration-Test-First Gate
- route: dev-loop(DDD)
- output target: integration gate before promotion
- dependency: C-20260304-602, C-20260304-607

8. `C-20260304-201` Backend API Contract v1
- route: doc-loop(IBM)
- output target: stable API for frontend decoupling
- dependency: C-20260304-601, C-20260304-602

### Batch P1-Next
9. `C-20260304-203` Backend-first execution gate
10. `C-20260303-003` Acceptance contract + self-contained checker
11. `C-20260303-103` Session lifecycle (resume/compress/new session)
12. `C-20260304-202` Multi-project UI isolation implementation
13. `C-20260304-606` Promotion & Cleanup Enforcer

## Needs Research (Keep in Candidate Pool)
1. `C-20260303-002` Independent auditor gate
- reason: needs minimal implementable boundary for current phase.

2. `C-20260304-501` Freely-on-OpenClaw profile
- reason: external runtime assumption needs current-architecture re-check.

3. `C-20260304-605` Sub-agent batch orchestrator
- reason: concurrency boundary and rollout scope not converged.

## Dropped (Out of Current Architecture Scope)
1. `C-20260304-301` EvoMap integration as P2 plugin
2. `C-20260304-401` Acceptance-to-capability asset mapping

## Next Action
- Convert Batch P0-Core into executable issue specs first.
- Keep all flow/contract changes behind value-proof checks.

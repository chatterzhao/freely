---
issue_id: I-20261103T124003Z-A
issue_path: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/issues/I-20261103T124003Z-A.md
phase_state: completed
---

- issue_id: I-20261103T124003Z-A
- issue_path: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/issues/I-20261103T124003Z-A.md

## Implementation Decision Note

- decision: GraphQL 失败重试一次后回退 REST（gh api --paginate --slurp），list_open_issues 从 records 派生。
- why_this: REST 不受 GraphQL 504 影响；改 handler 一处同时修复 parity 与 scan；返回结构不变。
- alternatives_considered: 只给测试加重试（生产仍坏）；全量切 REST（改动大、丢掉 GraphQL 正常时性能）。
- boundary_non_goals: 不改 scan/parity 语义；不引入新依赖。
- residual_risk: 失败时仍返回 {}，transport error 与"没有 open issue"仍不可区分；建议后续单独 feedback。

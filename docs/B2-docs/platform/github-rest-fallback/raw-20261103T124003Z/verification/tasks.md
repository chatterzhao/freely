# Tasks: I-20261103T124003Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | RED：REST fallback 单测 | test-platform-adapter-github-rest-fallback.py | - | AT-001 |
| T2 [x] | 实现 GraphQL 重试 + REST 回退 | platform-adapter.py | T1 | AT-001 |
| T3 [x] | parity 连续 3 次验证 | AT-002 log | T2 | AT-002 |

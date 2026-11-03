# Tasks: I-20261103T055554Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | RED 单测（标题优先/多身份/兜底/no match） | test-platform-adapter-raw-identity.py | — | AT-001/AT-003 |
| T2 [x] | 实现 _resolve_raw_identity 并接入 _discover_one/_unique_raw_issue | platform-adapter.py | T1 | AT-001/AT-003 |
| T3 [x] | 真机 discover 验证（20260807T114900Z） | AT-002 证据 | T2 | AT-002 |
| T4 [x] | 证据归档 | verification/test-evidence/ | T1-T3 | 全部 |

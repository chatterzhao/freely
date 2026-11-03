# Tasks: I-20261102T130603Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | RED 单测（缓存/重试/结构化错误） | test-platform-handler-probe.py | — | AT-001/AT-002/AT-003 |
| T2 [x] | 实现 _probe_handler/_HANDLER_PROBE_CACHE/_ensure_handler | platform-adapter.py | T1 | AT-001/AT-002/AT-003 |
| T3 [x] | guarded_pr_update execute 循环接入 _ensure_handler | platform-adapter.py | T2 | AT-004 |
| T4 [x] | 证据归档 | verification/test-evidence/ | T1-T3 | 全部 |

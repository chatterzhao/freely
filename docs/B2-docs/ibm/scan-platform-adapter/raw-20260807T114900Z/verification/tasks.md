# Tasks: I-20260807T114900Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | 顶部加 importlib.util + 缓存 _get_pa(project) | task-lifecycle-scan.py | — | AT-002 |
| T2 [x] | 替换三处直接 import 为 _get_pa(project).<symbol> | task-lifecycle-scan.py | T1 | AT-002/AT-003 |
| T3 [x] | RED 测试脚本（修复前失败） | test-scan-platform-adapter-import.py | — | AT-001/AT-002/AT-003 |
| T4 [x] | 真机 scan GREEN 证据 | verification/test-evidence/ | T2 | AT-001 |

# Tasks: I-20260807T114900Z-A

- [ ] 顶部加 `import importlib.util` + 缓存 `_get_pa(project)` helper
- [ ] 替换 L451 `_detect_platforms` → `_get_pa(project).configured_platforms()`
- [ ] 替换 L502 `get_platform_open_issues` → `_get_pa(project).list_open_issue_records()`
- [ ] 替换 L548 `get_all_platform_issue_states` → `_get_pa(project)._handlers()` / `._safe`
- [ ] 测试脚本 test-scan-platform-adapter-import.py（RED→GREEN）

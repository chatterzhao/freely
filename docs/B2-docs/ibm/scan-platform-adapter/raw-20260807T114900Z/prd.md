# PRD: task-lifecycle-scan platform_adapter import 断裂修复

- issue_id: I-20260807T114900Z-A
- raw_key: raw-20260807T114900Z

## Goal

修复 `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` 对 `platform-adapter.py`（连字符文件名）的失败导入，使 scan 恢复平台 issue 可见性（`platform_health` 健康、`total > 0`，87 个 open platform issues 重新可见）。

## 背景

三处直接 `from platform_adapter import ...`（原 L451/502/548）因模块名与文件名不一致抛 ImportError → `get_platform_open_issues` 返回 `{"__degraded__": ...}` → `platform_health: degraded`。之前治理链断裂：raw-20260623T022909Z 的代码修复 commit `2b2f4c77f` orphaned 未 merge，`3d67e39a1` 只关 issue 没改代码（phantom closure）。

## 实现方案

在 `task-lifecycle-scan.py`：

```python
import importlib.util  # 顶部

_PA_MODULE = None
_PA_PROJECT = None

def _get_pa(project: Path):
    global _PA_MODULE, _PA_PROJECT
    sync_dir = project / "docs" / "system" / "workspace" / "scripts" / "sync"
    if _PA_MODULE is None or _PA_PROJECT != project:
        spec = importlib.util.spec_from_file_location(
            "platform_adapter", str(sync_dir / "platform-adapter.py"))
        _PA_MODULE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_PA_MODULE)
        _PA_PROJECT = project
    return _PA_MODULE
```

替换三处：
- `_detect_platforms`: `from platform_adapter import configured_platforms` → `_get_pa(project).configured_platforms()`
- `get_platform_open_issues`: `from platform_adapter import list_open_issue_records` → `_get_pa(project).list_open_issue_records()`
- `get_all_platform_issue_states`: `from platform_adapter import _handlers, _safe` → `_get_pa(project)._handlers()` / `_get_pa(project)._safe`

保留现有 `sys.path.insert` 以维持向后兼容（无害）。

## Dev-Loop Handoff

| 项 | 值 |
|----|----|
| 实现文件 | `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` |
| 测试脚本 | `docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py` |
| RED 判定 | scan JSON `platform_health: degraded` 复现 |
| GREEN 判定 | scan JSON `platform_health` 非 degraded 且 `total > 0` |
| 测试 lane | feature-local（dev 工位）/ premerge-integration（test-pre-merge 工位） |

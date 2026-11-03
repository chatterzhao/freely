---
issue_id: I-20260807T114900Z-A
issue_path: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/issues/I-20260807T114900Z-A.md
phase_state: completed
---

- issue_id: I-20260807T114900Z-A
- issue_path: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/issues/I-20260807T114900Z-A.md

## Implementation Decision Note

- decision: task-lifecycle-scan.py 顶部加 `import importlib.util`，新增缓存 `_get_pa(project)` helper 用 `spec_from_file_location("platform_adapter", <project>/docs/system/workspace/scripts/sync/platform-adapter.py)` 加载模块，并将三处直接 `from platform_adapter import ...`（configured_platforms / list_open_issue_records / _handlers/_safe）替换为 `_get_pa(project).<symbol>`
- why_this: 根因是模块名与文件名不一致——文件叫 platform-adapter.py（连字符，刻意约定防 pip 包冲突），`import platform_adapter` 必然 ImportError。importlib 按真实文件路径加载是最贴近根因的最小修复，且复用 orphaned commit 2b2f4c77f 已验证过的先例设计（按其当前结构重写：project 相对路径 + 新符号名）
- alternatives_considered: Option B 重命名 platform-adapter.py → platform_adapter.py（破坏全仓路径引用与防冲突约定，改动面失控，否决）；Option C 在 sync/ 加 shim 模块（新增文件 + 导入链变长，藏问题，否决）
- boundary_non_goals: 不改 platform-adapter.py 自身逻辑；不改其它消费 platform-adapter.py 的脚本；不改变 scan 平台检测/回退语义之外的任何行为
- residual_risk: `_PA_MODULE` 全局缓存按 project 失效；若未来 platform-adapter.py 顶层 import 增加新依赖，loader 需同步满足其 sys.path 需求（当前模块内部已自管理 adapter/runtime 目录）

---
candidate_id: C-20260807T114900Z-A
status: promoted
source_raw: raw-20260807T114900Z
created_at: 2026-08-07
milestone: M-20260807T114900Z-A
---

# Candidates

## C-20260807T114900Z-A: task-lifecycle-scan platform_adapter import 断裂修复（importlib 加载器）

- candidate_format_version: v2
- title: 修复 task-lifecycle-scan platform_adapter 直接导入（文件名连字符导致 ImportError）
- status: promoted
- decision_reason: 根因是模块名与文件名不一致（platform-adapter.py 连字符无法被 `import platform_adapter` 解析）。importlib `_get_pa()` 加载器直接按真实文件加载，是贴近根因的最小修复；复用 orphaned commit 2b2f4c77f 的先例设计但按当前结构（project 相对路径、`list_open_issue_records` 符号）重写。
- next_action: B2 物化 I-20260807T114900Z-A → RED 复现（scan platform_health=degraded）→ dev 实现 importlib loader + 替换三处导入 → GREEN（scan platform_health 健康、total>0）
- revisit_trigger: 无（已 promote，直接进入实现）
- acceptance_criteria:
  - `freely task-source-scan --project <project> --json` 输出 `platform_health` 不为 degraded，`total > 0`，categories 包含平台 issue 来源类别
  - task-lifecycle-scan.py 中三处直接 `from platform_adapter import ...`（原 L451/502/548）全部替换为 `_get_pa(project).<symbol>`
  - 顶部存在 `import importlib.util` 与缓存的 `_get_pa()` helper（spec_from_file_location 加载 `docs/system/workspace/scripts/sync/platform-adapter.py`）
  - 非平台类别（如 agent_dead）扫描行为不回归
- promotion_gate: importlib loader 实现且三处导入替换完成；RED 阶段确认 bug 可复现（platform_health=degraded）；GREEN 阶段 scan 健康
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: independent-readonly-review
  - summary: 根因明确（模块名/文件名不一致），方案贴近根因、改动面单文件、有 prior art 可复用；替换点精确到当前结构的 L451/502/548
  - verdict: pass
- promoted_issue_id: I-20260807T114900Z-A
- promoted_issue_path: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/issues/I-20260807T114900Z-A.md
- milestone: M-20260807T114900Z-A
- session_refs: []

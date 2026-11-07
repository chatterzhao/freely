# Brainstorms: raw-20261105T122053Z

## 问题

平台读通道把「读取失败」与「该平台确实没有 open issue」压成同一个返回值 `{}`。2026-11-05 实测：`platform-adapter.list_open_issue_records()` 返回 50 条全是 `gitee:*`，而同时直接执行 `gh issue list --json` 报 `Bad Gateway`；按平台分别重试后 GitHub 有 57 条。生命周期扫描因此会把 57 条真实 open issue 当作不存在，parity 检查报出并不存在的 `gitee-only` 差异。

## 覆盖域与 scope

一个独立问题（读通道失败可观测性），一个 candidate。改动面 2 个真源：`platform-adapter.py`（handler 读健康状态 + 模块级聚合层）与 `test-platform-open-parity.py`（降级时跳过）。`task-lifecycle-scan.py` 经评审**不需要改动**。

## 评审中的关键发现（决定方案）

1. **scan 已内建降级消费逻辑**：`task-lifecycle-scan.py:773` 有 `if "__degraded__" in platform_issues: platform_health = "degraded"; ... pop(...)`，`get_platform_open_issues()` 直接返回 adapter 的聚合结果。因此只要聚合层在读失败时产出 `__degraded__` 标记，scan 就能进入既有降级语义——**无需改 scan 真源**，也满足「调用方无需改动」。issue 修复方案第 3 条建议改 `get_platform_open_issues()`，经评审属多余改动，未执行（已在 IDN / review 中说明）。
2. **健康路径必须零变化**：验收标准要求「两平台均正常时返回 107 条，结构不变」。因此 `__degraded__` 只在有失败平台时插入；健康时返回纯 `{platform:issue_id -> record}` 字典，不附加任何键，记录字段也不变。
3. **`_safe` 是缺陷链的最后一环**：它把异常转成 `{"status": "error", "error": ...}`，旧聚合层 `**record` 会对字符串抛 TypeError，或生成 `github:status` / `github:error` 假记录。修复后聚合层显式 try/except，并跳过任何非 dict 的 record。
4. **REST 回退必须保留**：GraphQL 两次失败后仍调用 `_open_issue_records_via_rest()`；REST 返回合法响应（哪怕空数组）表示读取成功（该平台确实没有 open issue），只有 REST 本身失败才 `ok=False`。这一区分正是修复的核心。
5. **`pull_raw_issue()` 的读源选择语义不动**（R6 刚修）；写通道不动；`_discover_one` 的 unknown/missing 语义不动。

## 关键设计

- `PlatformHandler` 基类新增 `read_health`（`ok` / `error` / `partial`），健康默认；GitHub / Gitee 的 `list_open_issue_records()` 每次调用开头重置，所有失败路径显式置为 `ok=False`，GraphQL 成功或 REST 合法响应置回健康。
- 模块级 `list_open_issue_records()`：逐个 handler 显式 try/except，收集失败平台；健康的记录照常合并；任一失败时在结果附加 `__degraded__`（含 platform / platforms / error / ok=False / partial=True）。空字典不再是「正常的空清单」的同义词。
- `test-platform-open-parity.py`：`collect_open_issues()` 返回 `(openings, degraded_platforms)`；main 在降级时打印 SKIP + 重试提示并 return 0，绝不基于部分清单计算 `github-only`/`gitee-only`。
- 新增 `test-open-list-read-degraded.py`（9 项）：健康 107 条结构不变、单平台失败标记、所有平台失败标记、handler 异常不产生假记录、scan 产出 `__degraded__`、scan 既有消费者存在、parity 降级跳过、parity 健康仍比较。

## 自举评审

本轮未发现「现有 open issue 未覆盖」的新缺陷。相邻现象（R11/#4149 平台写静默失败、R8/#4146 fail-open、R6 已修的 pull 读源选择）均已被覆盖或已完成，未重复立项。

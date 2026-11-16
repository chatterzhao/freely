# PRD — 标题规范化前移到 scan 漏斗

## Goal

让「从平台拿到 raw issue 之后」的所有本地环节都看到 canonical 标题：`[RAW-<key>] <human>`。不达标标题在 `freely task-source-scan` 收集阶段即被修达标；PR 门禁保留兜底；门禁本体与 scan 分析器保持只读。

## 实现方案

1. 新增 `docs/system/workspace/scripts/runtime/raw_title_normalize.py`：纯函数 + adapter 编排。
   - `normalize_open_raw_titles(project, dry_run=False, adapter_module=None) -> dict`：从 `platform-adapter.list_open_issue_records()` 读 OPEN issue；对每条用 `extract_raw_key(title + "\n" + body)` 取权威 raw key（不猜 `created_at`）；用 `canonical_raw_title(key, human)` 算应然标题；只对 `kind/raw`（由 key 可解析且标题含/应含 raw 身份）且标题不达标者，经 `adapter.update_issue(local_id, platform_ids, canonical, "")` **只写标题**；stdout 打印 `issue 标题不规范已执行规范标题命令：<platform> #<id> "旧" → "新"`。
   - 幂等：标题已达标零平台写；`--dry-run` 零平台写只打印；部分平台写失败返回 rc≠0 且不宣称成功。
2. `runtime/freely.cmd_task_source_scan()`：在调用 `task-lifecycle-scan.py` **之前**调用上述模块（失败只告警、不阻断 scan）；刷新 `bin/freely` 投影锁。
3. `pr-create-guarded` Step 0b：新增 preflight——当门禁 receipt 含 `non_canonical_title` 时调用同一规范化入口，打印 from→to 后重跑只读门禁；其余 fact 继续 fail-closed。
4. `raw-reconciliation-gate` / `worktree-common.sh`：新增 `non_canonical_title` 结构化诊断（scope / observed_title / expected_title / suggested_command），并把打印从整份 JSON receipt 改成精简摘要（完整 receipt 落临时文件路径）。gate 仍零平台写。

## 不变量

- `pre-scan-fix.sh` 与 `task-lifecycle-scan.py` 分析器零平台写。
- 不改 `canonical_raw_title()` / `_resolve_raw_identity()` 语义；不放宽 `ambiguous`。
- 不自动修 body / comments / labels / 本地文档；不追溯重写历史 CLOSED raw 标题。
- 平台写只走 `platform-adapter.py`；禁止 `gh` / `gitee-issue.py` 直连。

## Dev-Loop Handoff

按 `verification/pre-tests.md` 的 AT-001/AT-002 先跑 RED（develop 基线），再实现 T1–T5，最后在 test-pre-merge 工位跑 GREEN。

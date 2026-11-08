# PRD: create/close 以平台侧发现为身份判定源

- issue_id: I-20261108T092758Z-A
- source_raw: raw-20261108T092758Z
- workflow_kind: fix
- milestone: M-20261108T092758Z-A
- story: platform/raw-replica-reconciliation

## 目标
一个平台在 pull 时抖动（R6 降级 fallback 记 sync-debt、只写可读平台的 `platform_ids`）后，任何后续 `issue-sync create` 不得因「本地缺 id」而重复建单，`issue-sync close` 不得因「本地缺 id」而漏关。身份判定以平台侧按 `[RAW-key]` 的发现结果为唯一事实，本地 `platform_ids` 降级为可回填的缓存。零退化：健康路径逐字节不变。

## 改动范围（1 新增真源 + 1 真源接线 + 1 测试）
1. 新增 `docs/system/workspace/scripts/sync/replica_guard.py`（纯函数 + CLI）：解释 `discover-raw` receipt → present/absent/indeterminate。
2. `bin/issue-sync`：新增 `_replica_receipt` / `_replica_decide` / `_backfill_close_replicas`；`cmd_create` 增加守卫分支、`cmd_close` strict 前增加回填。
3. 新增 `docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py`（AT-001）。
4. `docs/milestones.md` 追加 `M-20261108T092758Z-A`。

## 不退化边界
- `platform-adapter.py search_raw_issue`（`--state all`、全量分页、模糊兜底）、`_resolve_raw_identity`（fail-closed ambiguous）、`close_platforms` 四段式与 0/3/1 退出码（R12）、`bin/raw-issue-pull`：全部逐字未改。
- 健康路径（`platform_ids` 已含全部配置平台）零 discover I/O、零建单、零文件改写。
- `indeterminate`（降级/ambiguous）不改 `_failed`/`platform_state` 认证语义：拒绝建单、不误报成功。
- 仅在 `raw-*` + `kind: raw` 生效；linked/I-* 的 create/close 不受影响。
- `cmd_close` 回填仅在终态（absorbed/dropped）执行，保 R12「非终态零写入」不变量。
- `docs/epics-map.svg` 未改（复用既有 story，check-epics-map 16 epics/206 stories aligned）。

## 功能需求
- FR-1: create 本地缺 id 且平台 present → 回填真实 issue_id/url，不建单。
- FR-2: create 本地缺 id 且平台 missing → 原路径建单（不阻断合法补建）。
- FR-3: create 本地缺 id 且平台 unknown/ambiguous → 失败关闭，拒绝建单，不认证成功。
- FR-4: close strict 前用平台 present 回填 partial platform_ids，close-multi 覆盖全部真实副本；非终态不写。
- FR-5: 纯判定 `classify_receipt` 覆盖 8 形态，present 需带真实 id/url，其余 indeterminate 一律失败关闭。

## 验收
AT-001 develop 基线 `a24ad958a` RED `7 ok / 13 failed` → GREEN `28 ok / 0 failed`；6 个相关回归基线对比 0 新增失败；真机 `discover-raw`→`replica_guard` 组合 present/indeterminate 正确。

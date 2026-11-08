---
candidate_id: C-20261108T092758Z-A
status: promoted
source_raw: raw-20261108T092758Z
created_at: 2026-11-08
milestone: M-20261108T092758Z-A
---

# Candidates

被否决方案（收窄搜索、自动删副本、只改 pull、每次无条件 discover、present 走 update）见 brainstorms.md，均经证伪后收窄，不另立 candidate。

## C-20261108T092758Z-A: create/close 以平台侧发现为身份判定源（幂等 + 失败关闭 + 回填）

- candidate_format_version: v2
- title: 新增纯模块 `replica_guard.py` 解释 `discover-raw` receipt；`issue-sync cmd_create` 仅在本地缺 id 时咨询平台侧，present→回填不建、absent→照旧建、indeterminate→失败关闭拒绝建；`cmd_close` 在 strict 关闭前用同机制回填 partial platform_ids
- status: promoted
- decision_reason: 本地 `platform_ids` 是缓存，降级 pull 后可为 partial；「本地缺 id」不等于「平台无副本」。以 `discover_raw_replicas`（与 reconciliation-gate 同一身份解析器）为事实源，才能根除重复建单与漏关，且天然满足 R7「读失败不是事实」。
- next_action: 建 AT-001（8 静态 + 8 单元 + 10 行为，隔离 mock 无真实平台）；实现 `replica_guard.py` + `bin/issue-sync` 两处；相关回归基线对比。
- revisit_trigger: 若将来引入 `issue-sync reconcile` 统一在平台恢复后回填并清 sync-debt，create 侧的按需 discover 可改为直接消费该账本；`raw-issue-pull` 顺带减噪也可纳入；届时保持健康路径零 I/O。
- acceptance_criteria:
  - RED(baseline `a24ad958a`)：partial platform_ids + 平台已有唯一 canonical 副本时，`cmd_create` 新建重复副本；`cmd_close` 的 close-multi 只带已登记平台；degraded/ambiguous 时仍建单。
  - GREEN：`cmd_create` present 不建单且回填真实 id；absent 照旧建；unknown/ambiguous 拒绝建（失败关闭）；健康路径（缓存完整）零 discover I/O、零行为变化。
  - GREEN：`cmd_close` strict 前回填 partial 缓存，close-multi 带全部真实副本；非终态 raw 关闭不产生任何本地写入（R12 不变量）。
  - 零退化：`search_raw_issue` 的 `--state all` / 全量分页 / 模糊兜底、`_resolve_raw_identity` fail-closed、close 四段式与 0/3/1 退出码、`raw-issue-pull` 全部未改。
- promotion_gate: AT-001 RED → GREEN + 相关回归基线对比 + governance gate + 人工四层 TDD review
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复核 R14 现场证据与 `cmd_create`/`cmd_close`/`discover_raw_replicas`/`_resolve_raw_identity` 调用链；证伪 5 个高风险字面方案、7 个相邻 open issue 覆盖；AT-001 develop 基线 `7 ok / 13 failed` → 工位 `28 ok / 0 failed`；真机 `discover-raw`→`replica_guard` 组合验证 present/indeterminate。
  - verdict: pass
- promoted_issue_id: I-20261108T092758Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261108T092758Z/issues/I-20261108T092758Z-A.md
- milestone: M-20261108T092758Z-A
- session_refs: []

## 证伪：确认未被现有 open issue 覆盖（逐条）
- #4182(R6, 已合并)：只修「pull 不可读即 FATAL」，新增降级 fallback；未触及 create/close 的身份判定。
- #4188(Q2, 已合并)：created_at 反推 key 漂移，与平台副本重复无关。
- #4195(R7, 已合并)：读通道降级标记（list_open_issue_records），读侧聚合；本条是写侧 create/close 未消费平台侧发现。
- #4149(R11, 已合并)：平台写通道静默失败；本条不是失败表达，是「成功创建了不该创建的副本」。
- #4184(R12, 已合并)：close 非终态部分成功；本条是 platform_ids 不全导致漏关，非退出时序。
- #4154(open)：代码层契约常量/正则/枚举多副本，非平台副本重复。
- #4166(open)：双平台同步入口收敛的重构，非具体「create 重复副本」正确性缺陷。
以上均不覆盖，故独立立项。优先级最高：吃狗粮每轮 wt-create 都可能因平台抖动触发，且已在 R14 实际阻断收口。

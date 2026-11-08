---
schema_version: '1'
local_id: raw-20261108T092758Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261108T092758Z-A
platform_ids:
  github:
    issue_id: '4225'
    url: https://github.com/chatterzhao/freely/issues/4225
    synced_at: ''
  gitee:
    issue_id: IKTR2N
    url: https://gitee.com/zhaoquan/freely/issues/IKTR2N
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261108T092758Z/issues/I-20261108T092758Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-08T09:27:58Z'
updated_at: '2026-11-08T10:30:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261108T092758Z-A
source_candidate: ''
completed_at: '2026-11-08T10:40:00Z'
closeout_note: ''
---

# fix: 降级 pull 后 create 重复建 raw 副本致 identity ambiguous

workflow_kind: fix

workflow_kind: fix

## 根因
`bin/raw-issue-pull:130-134` 在物化成功后无条件调用 `bin/issue-sync create <local_id>`（目的是让 `_platform_title()` 做标题达标）。`issue-sync cmd_create` 用 `_already_on_platform()` 判断某平台是否已有副本，而该函数只读**本地** `issue.md` 的 `platform_ids`（`bin/issue-sync:181`）。当 R6(#4182) 的降级 pull 只在一个平台可读时，`pull_raw_issue()` 只把可读平台写入 `platform_ids` 并记 sync-debt（另一平台读失败 ≠ 不存在）。随后任何一次 `issue-sync create`（包括 raw-issue-pull 的标题归一化步骤、或 wt-create 恢复/重跑）都会把「本地 platform_ids 缺该平台」误判成「该平台无副本」，于是 `discover_raw_replicas` 明明能按 `[RAW-key]` 找到已存在的副本，create 却仍新建一条。结果同一平台出现 2 条 canonical-title 副本，`_resolve_raw_identity` 返回 `ambiguous`，`raw-reconciliation-gate` 直接 block，PR/收口全链路被阻断。身份判定应基于平台侧按 raw-key 的发现结果，而不是本地缓存的 platform_ids。

## 证据
- 本机 R14 现场复现：`wt-create --raw-key 20261103T132556Z --source-platform gitee`（GitHub 当时 `search_unreadable/empty response`）→ 物化 issue.md 的 platform_ids 只有 gitee IKSPQ7、primary_platform=gitee。
- GitHub 恢复后重跑 `./bin/freely raw-issue-pull --raw-key 20261103T132556Z` → `issue-sync create` 输出 `[issue-sync] GitHub: creating issue... #4224`，而真实副本 #4152 早已存在且 `discover-raw` 当时返回 `github ok 4152`。
- 重复副本出现后 `raw-reconciliation-gate --require-local` 返回 `ok:false / decision:block / [ambiguous] raw key 20261103T132556Z is ambiguous: 2 canonical title matches`。
- `--state all` 使「仅关闭 #4224」也无法解除 ambiguous（实测 close-multi 后仍 block），只能删除重复副本才恢复 `ok:true/allow`。
- 与 R6 同源：R6 引入「降级 pull 记 sync-debt 并继续」，但 `issue-sync create` 未随之改为按平台侧发现做幂等判定。

## 影响
- 任一平台在 pull 时抖动（work log 多次记录 GitHub GraphQL `Bad Gateway`、读超时），后续 create/重跑即产生重复 raw 副本；此后该 raw key 的 identity 永久 ambiguous，PR 门禁与 wt-close 都被阻断，必须人工介入删库。
- 另一后果：partial platform_ids 会让 `issue-sync close` 的 `close-platforms` 只关闭本地已登记的那一个平台，另一个平台的 raw 副本残留 open → 平台 parity 不成立（属同一根因的另一面）。
- 这是「可信度根基」家族缺陷（R7 读、R11 写、R10 判定之后）——身份解析没有以平台侧事实为准。

## 修复方案
1. `issue-sync cmd_create` 在「缺某平台」时，先调用 `platform-adapter.discover_raw_replicas(raw_key)`（或 `search_raw_issue`）按 `[RAW-key]` 查询平台侧：若该平台已存在唯一 canonical 副本，则把其 `issue_id/url` 回填到本地 `platform_ids`（幂等、不新建），并对标题达标走 update 而非 create；仅当平台侧确认「not found」时才真正 create。
2. `raw-issue-pull` 的 create-backfill 步骤在 partial（退出码 3 / sync-debt）场景下不应触发可能重复建单的 create；或由 `issue-sync reconcile` 统一在平台恢复后回填 platform_ids 并清 debt。
3. `issue-sync close` 关闭前应以 discover 结果为准补齐 platform_ids，保证所有真实副本都被关闭。
4. 前置：确认 `search_raw_issue` 的 `--state all` + `--limit 20` 在多副本场景下的判定期望（与 R1 证伪过的「精确搜索不能退化」一致，勿削减分页/状态范围）。

## 验收标准
- RED：构造 platform_ids 只含单平台、但两平台都已存在 canonical 副本的本地 issue.md；调用 `issue-sync create`，断言会新建重复副本（当前行为），且 discover 变 ambiguous。
- RED：同上调用 `issue-sync close`，断言只关一个平台、另一个残留 open（当前行为）。
- GREEN：修复后 `issue-sync create` 在该夹具下不新建、回填缺失的 platform_ids，两平台副本数不变、reconciliation `ok:true/allow`。
- GREEN：`issue-sync close` 关闭全部真实副本，本地 platform_state=closed，三份 fingerprint 一致。
- 零退化：健康路径（platform_ids 已含全部平台）行为逐字节不变；不削弱 `search_raw_issue` 的 `--state all` / 分页 / 模糊匹配兜底（R1/#4154）。

## 不退化边界
- 保留 R6 的降级 pull + sync-debt 机制（不删除、不改退出码 3 语义）。
- 保留 `_resolve_raw_identity` 的 fail-closed ambiguous 判定（Q2/#4188），不得为了让 create 通过而放宽身份解析。
- 保留 `discover_raw_replicas` 的并发读取与 read_health 降级标记（R7/#4195）。
- 不改动 `issue-sync close` 的四段式与 0/3/1 退出码（R12/#4184）、平台写通道的 0/3/1（R11/#4149）。

## 明确不纳入
- 不重构 `issue-sync` 整体入口收敛（#4166 范围）。
- 不处理契约常量/正则多副本（#4154 范围）。
- 不改 `platform-adapter` 的 create-issue 返回码约定（R11 已定）。
- 不补 Gitee 侧历史遗留的 GitHub-only 副本（历史遗留判定项）。

## 证伪（确认未被现有 open issue 覆盖）
- #4182(R6, 已合并)：只修「pull 不可读即 FATAL」，新增降级 fallback；未触及 create 的幂等身份判定。
- #4188(Q2, 已合并)：created_at 反推 key 漂移，与平台副本重复无关。
- #4195(R7, 已合并)：读通道降级标记，读侧；本条是写侧 create + 身份解析。
- #4149(R11, 已合并)：平台写通道静默失败；本条不是失败表达问题而是「成功创建了不该创建的副本」。
- #4184(R12, 已合并)：close 非终态部分成功；本条涉及的是 platform_ids 不全导致的漏关，非退出时序。
- #4154(open)：代码层契约常量/正则/枚举多副本，非平台副本重复。
- #4166(open)：双平台同步入口收敛的重构，非具体「create 重复副本」正确性缺陷。
以上均不覆盖本条根因，故独立立项。优先级高： eats-own-dogfood 每轮都可能因平台抖动触发，且已实际阻断 R14。

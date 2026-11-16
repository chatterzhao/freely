---
schema_version: '1'
local_id: raw-20261116T050414Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261116T050414Z-A
platform_ids:
  github:
    issue_id: '4657'
    url: https://github.com/chatterzhao/freely/issues/4657
    synced_at: ''
  gitee:
    issue_id: IKVLKU
    url: https://gitee.com/zhaoquan/freely/issues/IKVLKU
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/issues/I-20261116T050414Z-A.md
last_synced_comment_at:
  github: '2026-11-16T06:14:33Z'
  gitee: '2026-11-16T06:14:33Z'
hash: ''
created_at: '2026-11-16T05:04:14Z'
updated_at: '2026-11-16T06:14:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261116T050414Z-A
source_candidate: ''
completed_at: '2026-11-16T06:14:32Z'
closeout_note: ''
severity: P2
---

# fix: 副本门禁标题不规范无可操作指引，已物化 raw 自动规范化入口不可达

workflow_kind: fix

## fix: 副本门禁标题不规范无可操作指引，已物化 raw 自动规范化入口不可达

| Field | Value |
|-------|-------|
| local_id | `raw-20261116T050414Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-16T05:04:14Z |
| updated | 2026-11-16T05:04:14Z |

---

> **Freely 治理**：这是 raw issue `raw-20261116T050414Z`。实现前请用 `wt-create --raw-key 20261116T050414Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（2026-11-14 #4653 真机，已复现）

`pr-create-guarded` Step 0b 被 `raw-reconciliation-gate` 拦下时，终端打印的是**整份 JSON receipt**（含平台 issue body 全文，数千字符），末尾只有一句 `[PR-CREATE] raw replicas are inconsistent; resolve explicitly, then retry.`

- 错误信息里**没有「标题不规范」字样**，也没有任何可执行命令；receipt 的 `ambiguous: 3 matches` 要读者自己去翻 `_resolve_raw_identity()` 源码，才能推出根因是 #4653 标题缺 `[RAW-20261114T101138Z]` 前缀。
- 实际修复命令存在且很窄：`freely feedback edit --raw-key 20261114T101138Z --title "fix: dropped 收口应自动写关闭理由并防重新物化"`（内部走 `canonical_raw_title()` → `[RAW-20261114T101138Z] fix: ...`）。因为错误无指引，排查耗掉一整轮。
- 用户期望二选一：① 门禁提示「标题不规范，请执行 <命令>」；② 直接执行命令并打印「issue 标题不规范已执行规范标题命令，标题结果从 X 变为 Y」。两者都应让「标题不规范」被自动处理，不再靠人肉读 JSON 猜根因。

## 根因（逐条已核实源码）

1. `raw-reconciliation-gate.py` docstring 明确 `Read-only lifecycle gate`，`reconcile()` 是 `write-free receipt`；包装函数 `freely_wt_assert_raw_reconciled_readonly()` 直接 `cat "$_receipt"`，把面向程序的结构化 receipt 原样倒给人看。已有正向先例：`missing_local_title` 诊断会写「re-materialize with raw-issue-pull」——**门禁给可执行指引是既有设计**，只是标题类诊断缺失。
2. `discover_raw_replicas()` 在身份不明时只返回 `{"status":"ambiguous","error":"raw key X is ambiguous: 3 matches"}`，**不带候选标题**，所以门禁自己也拿不到 from→to。
3. `_resolve_raw_identity()`（`platform-adapter.py:988-1016`）只认标题前缀 `[RAW-<key>]`；`raw_title_contract.canonical_raw_title()` 是纯 stdlib、零 I/O 函数——门禁完全可以只计算「应然标题」而不写平台。
4. `platform-adapter.pull_raw_issue()`（约 `:1534-1555`）**本来会自动规范化**：非达标标题遍历所有 replica 写 canonical 并打印 `[title] {plat}: normalized to {canonical}`。但 #4653 这类已 absorbed / 全 CLOSED 副本被 11-14 新增的 fail-closed「防重新物化」守卫（约 `:1494-1501`）挡住，这条自动路径对 PR 场景**不可达**。即：能力存在、入口错位。
5. `issue-sync update`（11-14 修好 `hash` 写入 / dedup 后已可用）也能推 canonical 标题，但它同时重写 body 与 labels；作为「只改标题」的窄修复动作副作用过大。

## L0 评审结论：门禁内部不自动写平台

- Q2 门禁强度：门禁若既判定又写平台，receipt 不再独立；自愈会掩盖真实 drift，审计无法区分「本来就达标」与「刚被改达标」。
- Q4 第二套语义：不能把只读 gate 变成第二个平台写通道；平台写必须继续只走 `platform-adapter.py`。
- 因此用户选项 ② 的「直接执行」应放在**门禁之外的显式修复命令**（可由 `pr-create-guarded` 在门禁前自动调用），而不是塞进 gate 本体。门禁负责精确诊断 + 给出命令 + 给出 from→to；写动作可审计、可 dry-run、可拒绝。

## 方案对比（B1 阶段需再评估，不在此定案）

| 方案 | 做法 | 优点 | 缺点 |
|---|---|---|---|
| A 只加可操作提示 | receipt 加 `non_canonical_title` 诊断 + `suggested_command` + from→to；pr-create 打印精简摘要 | 改动最小、零平台写、完全保持只读契约 | 仍需人工执行一条命令 |
| B 显式修复命令 + pr-create 自动 preflight（倾向） | 新增窄命令 `freely raw-title-normalize --raw-key <key>`（名字待定）；Step 0b-pre 仅在 `non_canonical_title` 时调用，打印 from→to，然后重跑门禁 | 满足「自动处理」；写动作独立、幂等、可 dry-run、留痕 | 多一个命令面；需明确 opt-out 与审计 |
| C 门禁内直接自愈 | 在 `reconcile()` 里写平台 | 一步到位 | **否决**：破坏只读 receipt 与 fail-closed 审计 |
| D 静默放宽 ambiguous | 允许无前缀标题直接放行 | 省事 | **否决**：身份唯一性失效，正是 #4653 被拦的原因 |

## 期望设计（供 B2 细化，不是最终方案）

1. receipt 新增结构化诊断，例如 `{"scope":"github","code":"non_canonical_title","observed_title":"fix: ...","expected_title":"[RAW-...] fix: ...","suggested_command":"freely raw-title-normalize --raw-key ..."}`。身份来源优先用本地 `docs/B1-docs/raw-<key>/issue.md` 的 `platform_ids.<platform>.issue_id` 按号直取，避免 search 猜候选。
2. 新增窄修复命令（候选名 `freely raw-title-normalize --raw-key <key> [--dry-run]`）：只改标题（adapter `update-issue` 传空 body）、双平台一致、幂等、部分失败整体非零；打印 `issue 标题不规范已执行规范标题命令：github #4653 "fix: ..." → "[RAW-20261114T101138Z] fix: ..."`。
3. `pr-create-guarded` Step 0b-pre：仅当 receipt 含 `non_canonical_title` 时调用该命令 → 打印 from→to → **重跑门禁**；其余 fact（`ambiguous` 多身份、`content_diverged`、`missing`、`raw_key_mismatch`）仍 fail-closed。提供 `--no-normalize-title` 关闭，并在 PR body 留痕。
4. `freely_wt_assert_raw_reconciled_readonly()` 改为打印精简摘要（code / detail / suggested_command / from→to），完整 receipt 落临时文件路径供排障，不再倾倒 body 全文。
5. 明确不做：不改 `canonical_raw_title()` 契约、不改 `_resolve_raw_identity()` 的唯一身份前缀判定、不自动改本地文档凑 fingerprint、不自动修 body/comments/labels、不追溯重写历史 raw 标题、不用 `--allow-degraded` 绕过事实。

## 验收（AT，带基线红）

1. 构造标题缺前缀的 raw 副本（FakeHandler / 隔离测试仓），跑门禁 → 诊断必须是 `non_canonical_title` 且含 `observed_title` / `expected_title` / `suggested_command`；develop 基线无该字段 → RED。
2. 跑修复命令 → 双平台标题变为 expected；stdout 含 from→to；再跑一次 → 幂等且零平台写。
3. `--dry-run` → 零平台写但打印 from→to。
4. 部分平台写失败 → rc≠0、不宣称成功、不继续重跑门禁。
5. `pr-create-guarded` 在 `non_canonical_title` 场景自动 preflight 后门禁转 allow 且 PR body 留痕；在 `content_diverged` / `ambiguous(>1 prefixed)` 场景**不触发**自动写、仍 rc=1。
6. 门禁自身零平台写：FakeHandler 记录调用，断言 gate 调用期间无任何 update / create / close。

## 证伪（本轮已逐条做，确认未覆盖）

- `I-20261105T051136Z-A`（#4593 / #4543 / #4459 / #4432 / #4367 仍 OPEN）`phase_state: completed`，范围是「标题契约单一真源 + pull / feedback edit 时达标」，**不含**门禁诊断与已物化 raw 的修复。
- `I-20260725T030511Z-A`（#4598）`completed`：配置驱动 discovery + 纯 read-only receipt。
- `I-20261102T113816Z-A`（#4600）`completed`：unknown 三态化与债账本。
- 本地 `raw-20261103T055554Z`（前缀精确匹配）、`raw-20261104T082542Z` / `raw-20261110T093145Z`（本地 H1 物化导致 content_diverged）均属不同问题。
- #4435「GATE 1 不给指引」是另一道门禁、另一套机制，只作为「门禁应给可执行指引」这一项目价值的旁证。
- 平台全状态抽样 300 条 raw：6 条标题不规范且**全部 CLOSED**（历史 / 手工创建），当前 5 条 open raw 全部达标 → 低频，但一旦命中就 100% 阻断 PR；取 severity P2。

## 归属

属 `platform / raw-replica-reconciliation` 能力面；本轮只创建 raw 与评审结论，**不实现、不建工位、不夹带任何 PR**，按 goal 队列排到队尾，后续单独走完整 IBM 流程。

### comment-platform-1
- source: platform
- event: mirrored

## 方案修订（2026-11-16）：规范化主入口改为 `freely task-source-scan`

**本条是对原 body「B 方案：pr-create preflight 为主」的修订，后续 B1/B2 以本条为准。** 用户判断：所有平台 raw 都经 scan 收集后才交给本地任务；scan 发现标题不达标就应就地把它改达标，让「从平台拿到 raw 之后」一律是标准标题。

### 一、本轮全仓搜索证据（历史实现与既有约束）

1. **已有自动规范化实现**：`docs/system/workspace/scripts/sync/platform-adapter.py` 的 `pull_raw_issue()`（约 `:1534-1555`）——非达标标题时遍历 replica 写 canonical，并打印 `[title] {plat}: normalized to {canonical}`。来自历史提交 `c0b1af50b`（raw-20261105T051136Z）。
2. **它当初明确不接 scan**：该 raw 的 B1 Decision 原文「不改平台读取通道、不改 scan 状态机」。所以能力一直只在**物化时**触发；已 absorbed / 全 CLOSED 副本又被 11-14 新增的防重新物化守卫挡住 → 对 PR 场景不可达。这是缺口的历史来源，不是没实现过。
3. **真正的 scan 入口**：`freely task-source-scan` → `cmd_task_source_scan()`（`runtime/freely:26089`）→ `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`；daemon 在 scan 前还会调 `pre-scan-fix.sh`（`runtime/freely:17907`）。
4. **pre-scan 只读是既有硬约束**：`pre-scan-fix.sh` 文件头原文「This entry is deliberately read-only: scan preparation must not create lifecycle facts, worktrees, PRs, commits, or platform side effects.」→ **平台写不能塞进 pre-scan 辅助脚本**，但可以作为 scan 命令自身的一个显式 preflight 步骤。
5. **scan 已经握有权威 raw key**：`extract_raw_key(title + "\n" + body)`（`task-lifecycle-scan.py:381-384`、`:809`）即使标题缺前缀，也能从 body 里的 `local_id: raw-<key>` 取出 key；但 `_build_raw_key_index()`（`:518-540`）**只用 title** 建索引，标题不达标会让该 fallback 索引缺失。规范化必须在建索引**之前**发生。
6. `issue-sync scan`（`bin/issue-sync.d/cmd-scan.sh`）是纯本地报告，文件头写明 `no writes`；它不是平台 raw 收集入口，**不改**。

### 二、修订后的落点：一个主入口 + 三道既有防线

| 位置 | 动作 | 状态 |
|---|---|---|
| `freely task-source-scan`（`cmd_task_source_scan`，scan 命令本体） | **主入口**：调用 `task-lifecycle-scan.py` 之前，对平台 OPEN raw（label `kind/raw`）做标题规范化 preflight。用 `extract_raw_key(title+body)` 定 key、`canonical_raw_title()` 算应然标题、只经 adapter `update-issue` 改标题、打印 `issue 标题不规范已执行规范标题命令：<platform> #<id> "旧" → "新"`。必须发生在 `_build_raw_key_index()` 之前，使索引与下游任务拿到的标题一律达标。幂等；支持 `--dry-run`；部分失败留痕不静默吞。 | **新增（本 raw 实现）** |
| `pull_raw_issue()` | 保留既有自动规范化（第二道防线，覆盖直接物化/重新拉取）。 | 已有 |
| `pr-create-guarded` Step 0b-pre | 覆盖 scan 看不到的 absorbed / CLOSED raw：仅当 gate 报 `non_canonical_title` 时调用同一规范化命令，打印 from→to 后**重跑门禁**。 | **新增（本 raw 实现）** |
| `feedback create/edit`、`issue-sync create/update` | 已经经 `raw_title_contract.platform_title()` 达标；补 AT 钉住，不改行为。 | 已有 |

### 三、不变边界

- `pre-scan-fix.sh` 与 `task-lifecycle-scan.py` **分析器本身保持只读、零平台写**；规范化是 scan 命令的独立 preflight，由 `platform-adapter.py` 唯一通道执行，可审计。
- 门禁本体仍 write-free；不改 `_resolve_raw_identity()` 的唯一前缀判定，不静默放宽 `ambiguous`。
- 不自动修 body / comments / labels，不自动改本地文档凑 fingerprint，**不用 `created_at` 猜 key**（key 一律来自 `title+body` 的 `raw-<key>`）。
- 部分平台写失败：不宣称成功、留痕、scan 继续（可带 degraded 标记），不因标题问题丢弃任务。
- 不追溯重写历史 CLOSED raw 标题（抽样 6 条仅作样本）。

### 四、验收补充（在原 AT 清单之后新增）

1. 造一个标题缺前缀但 body 含 `raw-<key>` 的 OPEN raw，跑 `freely task-source-scan` → 标题变 canonical、stdout 含 from→to、scan 输出含该 key 的任务；develop 基线 RED（标题不变、无 from→to）。
2. 同场景跑两次 → 第二次零平台写（幂等）。
3. `--dry-run` → 零平台写但打印 from→to。
4. 标题已达标 → 零平台写、无噪声。
5. 用 FakeHandler 断言 `task-lifecycle-scan.py` 分析器与 `pre-scan-fix.sh` 调用期间无任何 update/create/close。
6. `_build_raw_key_index()` 在规范化后能索引到该 raw（修订前只用 title 会漏）。
7. `pr-create-guarded` 对 absorbed/CLOSED raw 的 preflight 仍按原 AT-005 生效；`issue-sync scan` 行为不变（no writes）。

### 五、结论

主入口从「pr-create 时才修」前移到「scan 收集时就修」，因为 scan 是所有平台 raw 进入本地任务的唯一漏斗；pr-create preflight 降级为兜底，覆盖 scan 看不到的 CLOSED/absorbed raw。两处合起来实现用户要求：**从平台拿 raw issue 的那一刻起，后面看到的都是标准标题。**


#### resolution-20261116T061228Z
- status: adopted
- reason: 方案修订评论已完整纳入 B1 Decision（Option C：scan 主入口 + pr-create 兜底），并作为 brainstorms/candidates 的锚点；原 body 的 pr-create 为主降级为兜底。
- resolved_by: freely-agent
- comment_ref: comment-platform-1

### comment-20261116T061433Z
- source: system
- event: promote_finalized
- children: ["I-20261116T050414Z-A"]

拆解为以下任务:
1. [I-20261116T050414Z-A](will-be-updated)

---
b1_id: B1-20261125T071429Z
phase_state: completed
source_raw: raw-20261125T071429Z
source_url: https://github.com/chatterzhao/freely/issues/4699
produced_candidate: C-20261125T071429Z-A
created_at: 2026-11-25
---

# B1_IBM: wt-close 以本地 platform_state 放行，平台 I-* 未关仍能收口

## 0. 设计意图审计（先于方案）

### B0 前置：关键词广搜 + 多文档交叉

- 关键词族表（≥3 组；搜 docs/ bin/ .freely/）:
  - 门禁名: `wt-close` → `docs/system/workspace/scripts/worktree/wt-close`（1576 行，Phase 2.5 在 1069-1147）
  - 字段名: `platform_state` → `wt-close:950,979-981,1107-1126`、`bin/issue-sync.d/cmd-batch.sh:64`、`lifecycle/raw_lifecycle_effects.py:242`
  - 命令名: `issue-sync batch` → `bin/issue-sync.d/cmd-batch.sh`、`worktree/pr-merge-guarded:568-573`
  - 命令名: `close-multi` / `close-raw` → `sync/platform-adapter.py:903-916,1728+`
  - 身份解析: `_already_on_platform` → `bin/issue-sync.d/lib-state.sh:45`
  - 历史 raw: `raw-20260621T185519Z`（绕过机制清单）、`raw-20261113T130925Z`（single closeout predicate）、`raw-20261102T113816Z` / `raw-20260725T030511Z`（副本一致性）
- 怀疑多份文档: 是——显式列出四类
- 三类分层表:
  - 当前生效实现: `docs/system/workspace/scripts/worktree/wt-close`（权重：现状）
  - 历史局部文档: `docs/B1-docs/raw-20260621T185519Z/issue.md`（权重：仅背景，记录当时的绕过清单）
  - 当前权威恢复点: `.freely/goal-arch-debt.md`「恢复点（2026-11-25T07:33Z）」与 `docs/system/workspace/commands.md`（权重：当前真相）
- 矛盾清单:
  - `ibm-framework.md:128` 说「平台 issue 是 I 的真源，本地是副本」，而 `wt-close:1119-1126` 用本地副本字段当放行判据——**方向相反**。
  - `commands.md` 写「正常收口 = 双平台 close issue」，而 `wt-close:1150-1151` 注释说「never writes issue files」，实际路径在 `platform_state: closed` 时直接跳过关闭（`wt-close:979-981`）。
  - `raw-20260621T185519Z` 已把 `wt-close --skip-platform` 标为「无验证」并要求补调用者验证，此后从未实现。
- 二元决策: **继续**（附方向：判据改为平台取证 + 关闭通道对账 + 去吞错 + 去重复创建；硬拦截另立 raw，不夹带）

### 外部锚点（引用原文，至少两类）:

- 设计文档: `docs/system/workspace/ibm-framework.md:128`「IBM Framework 的 I（Input source）统一为 github/gitee issue。平台 issue 通过 scan 下载到本地，AI 只读写本地副本。」
- 门禁源码注释/理由: `docs/system/workspace/scripts/worktree/wt-close:1150-1151`「Raw and linked issue metadata must already be terminal before cleanup starts. / wt-close performs platform/worktree cleanup only and never writes issue files.」
- 门禁源码注释/理由: `bin/issue-sync.d/cmd-batch.sh:64`「Skip fully-synced: platform_state=closed means both sides agree」
- 门禁源码注释/理由: `docs/system/workspace/scripts/worktree/pr-merge-guarded:568-570`「Single retirement driver: batch owns the phase_state == completed predicate and the platform write.」
- 既有验收测试: `docs/system/workspace/scripts/tests/test-wt-close-children.py`（只断言 frontmatter 驱动的拒绝，无平台取证断言）
- 历史绕过清单: `docs/B1-docs/raw-20260621T185519Z/issue.md`「| `wt-close --skip-platform` | wt-close | 平台 issue 关闭 | 无验证 |」「后续需要为每个绕过机制加上 `--reason` / 调用者验证 / AI 拦截提示。」
- 既有同类实现: `docs/system/workspace/scripts/sync/platform-adapter.py:925+ close_dropped()` 用 `_unique_raw_issue(handler, raw_key)` 在每个平台按身份解析——drop 路径会对账，正常收口路径不对账。

- 判定（五选一，必须给证据）: **实现偏差**——设计意图（wt-close 只做只读终态门禁、平台是 I 的真源）正确，但实现把「终态」判定建立在本地自述字段上，与 `ibm-framework.md:128` 的真源方向相反；另含一处**未完成加固**（`--skip-platform` 无调用者验证，2026-06-21 已登记未实现）。
- 与既有断言的冲突: 有。`test-wt-close-children.py` 断言「platform_state != closed 即拒绝」，本轮不改该断言，只在其前增加平台取证；冲突点是 `cmd-batch.sh:64` 的「closed 即双方一致」假设必须删除，否则门禁取证与 batch 跳过继续互相掩盖。谁该改：batch 与 wt-close 同时改，判据模型统一为「平台 OPEN 副本数 == 0」。
- 影响面: `wt-close` Phase 2.5、`issue-sync batch`、`raw_lifecycle_effects.close_linked`、`platform-adapter`（只读枚举）、`pr-merge-guarded`（fail-closed）、`commands.md`/workflow SKILL 的字段语义。

## 0.1 全局适配反思（四问）

- Q1 类别: 副本传播（平台副本的关闭与观测）+ 生命周期变更（I-* 终态判据）。
- Q2 职责边界: `wt-close` 拥有「可安全退役」的最终判定，但不得写平台；`issue-sync` 拥有平台写；`platform-adapter` 拥有身份解析与逐平台读写。本轮把「平台取证的读」放 adapter、把「判定」放 wt-close、把「关闭对账」放 issue-sync——三者职责不重叠，也没有新增第二写通道。
- Q3 结构性冲突: 不会。取证是 `list -state all + title 过滤` 的一次读，不需要每文档一个工位，也不要求每次同步走 IBM。
- Q4 门禁失配: **是**。现有门禁测的是「本地字段值」，本轮要测的是「平台副本真实状态」。按 skill 要求先改判据模型（字段→平台事实），不是就地放宽或绕过。

## Input

- raw-20261125T071429Z（P0）：wt-close 能以本地 `platform_state: closed` 放行，而平台 I-* 仍 OPEN；当前平台有 17 个 OPEN `[I-*]`，仅 10 个 distinct local_id。
- 活体复现：`#4654` 收口时 `I-20261114T111702Z-A` 在平台上无任何副本，本地却写着 `platform_state: closed`，wt-close 打印「already closed … skipping issue-sync」后放行。

## Problem

三个缺陷叠加成自封闭环：
1. 门禁读缓存（`wt-close:1119-1126` 只读 frontmatter）；
2. 关闭通道只覆盖映射内副本（`close_linked` + `close_issue` 只用 `platform_ids`）；
3. 失败被吞（`cmd-batch.sh:118`、`pr-merge-guarded:573` 的 `|| true`）且 batch 用同一字段当跳过条件（`cmd-batch.sh:64`）。

于是同一个自述字段既是「已关闭」的写入证据，又是「可删除」的放行证据，平台真实状态无人校验；未映射副本与重复副本永久 OPEN，而工位已被不可逆删除。

## Brainstorm

### Option A: 只改门禁（wt-close 向平台取证）
- 优点：改动面最小，直接堵住不可逆删除的风险。
- 缺点：每次收口都靠门禁兜底，关闭通道仍在制造漂移；重复副本继续增长；`|| true` 仍会掩盖 partial。

### Option B: 只改关闭通道（按 local_id 对账关闭）
- 优点：治本，平台副本被真正关掉。
- 缺点：门禁仍信任本地字段；一旦关闭通道出错（网络/权限），工位照样被删，事后无法补救。

### Option C: 门禁取证 + 关闭对账 + fail-closed + 去重复创建（推荐）
- 门禁：`wt-close` 对每个 I-* 调 adapter 只读枚举，任一 OPEN 副本即拒绝，平台不可读也拒绝（fail-closed）。
- 关闭：`close_linked` 先按 local_id 在每个平台枚举副本，与 `platform_ids` 并集后关闭；任一平台失败即非零、不写 `platform_state`。
- 去吞错：`cmd-batch.sh:118` 去掉 `|| true` 并汇总退出码；`pr-merge-guarded:573` 捕获 rc，失败即中止合并。
- 去重复：`_already_on_platform` 增加平台侧存在性判定，避免 `platform_ids: {}` 时反复 create。
- 优点：写入侧治本、门禁侧兜底、失败可见，三者互为独立防线。
- 缺点：改动跨 4 个文件，需要新增只读 adapter 能力与 AT。

## Decision: Option C

- 理由：缺陷的本质是「判据真源错误」+「失败不可见」。只做其中一层都会留下另一个方向的漏洞；三层同时收紧后，任一层失效都不会导致「工位已删、issue 仍开」。
- 硬拦截（PATH wrapper 拦截直连 `gh issue close` / 内层 adapter）不并入本 PR：它是新的执行环境机制，需要独立 B1/B2 设计（进程树判定、bypass 环境变量、安装方式），并入会让本 PR 无法单独验证。

## Candidate

- candidate_id: C-20261125T071429Z-A
- status: promoted
- milestone: M-20261125T071429Z-A

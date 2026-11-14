---
schema_version: '1'
local_id: raw-20261114T101138Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T101138Z-A
platform_ids:
  github:
    issue_id: '4653'
    url: https://github.com/chatterzhao/freely/issues/4653
    synced_at: ''
  gitee:
    issue_id: IKVBNJ
    url: https://gitee.com/zhaoquan/freely/issues/IKVBNJ
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree/wt-close/raw-20261114T101138Z/issues/I-20261114T101138Z-A.md
last_synced_comment_at:
  github: '2026-11-14T12:08:54Z'
  gitee: '2026-11-14T12:08:54Z'
hash: ''
created_at: '2026-11-14T10:11:38Z'
updated_at: '2026-11-14T12:09:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T101138Z-A
source_candidate: ''
completed_at: '2026-11-14T12:08:53Z'
closeout_note: ''
severity: P1
---

# fix: dropped 收口应自动写关闭理由并防重新物化

workflow_kind: fix

## fix: dropped 收口应自动写关闭理由并防重新物化

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T101138Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T10:11:38Z |
| updated | 2026-11-14T10:11:38Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T101138Z`。实现前请用 `wt-create --raw-key 20261114T101138Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（raw-20261114T051655Z 真机 dropped 实测）

B1 P0 关键词广搜判定 dropped 后，当前收口路径是：
1. 手工把 `phase_state: proposed` 改成 `dropped`（**只改一个字段**，未写 `completed_at`/`closeout_note`）；
2. 手工 `freely comment --issue <raw> --file <research>` 写平台；
3. `wt-close --force --discard-unmerged --reason "..."` 关平台 + 抹除工位。

结果：#4574 / IKVA70 CLOSED、comments=1、但 **`stateReason=COMPLETED`**（dropped 被标成"完成"）；develop 无该 raw 文档（本地抹除符合预期）。

## 设计判断（经全局核实，采纳用户结论）

**dropped 不做 PR、本地抹除痕迹；关闭理由与研究过程留在平台 issue 时间线；靠 CLOSED 天然隔离，不加 dropped 标签。**

依据：
- 本地文档与平台 issue **1:1 镜像**；「为什么关闭」属于该 issue 的时间线，不是 develop 的生效治理资产。合进 develop 会把「不做的决定」混进「当前要做什么」。
- `freely-doc-B1_IBM-execution/SKILL.md:47`「标记 dropped……**直接终止 B1_IBM 流程**」；LAWS.md:304 的 skip-ibm 只针对「结构上不需要 IBM lifecycle 证据」的变更，不构成「dropped 必须 merge」。
- 历史 `raw-20260409T171500Z` 的「narrow followthrough owner + guarded merge」是**局部/过期做法**（当时只为绕过 protected push gate，其 `open_questions` 自己留了「Should future dropped research packets always materialize a narrow followthrough owner?」未定论）。按 B0 多文档分层属历史局部文档，不能当当前规范。
- `raw_metadata_contract.py` 契约层**本来就是对的**：`transition("dropped", reason=...)` 写 `phase_state` + `completed_at` + `closeout_note`（关闭理由落盘），`transition("platform_closed")` 单独关平台；`validate():194-196` 强制 dropped 必填 `completed_at` + `closeout_note`。**缺的是命令层串联。**

### 为什么不加 dropped 标签（用户提出的备选方案，经核实否决）

- `platform-adapter.py:1491` 明确：「platform `phase/*` label is a **CREATION-TIME snapshot**: the platforms never update it when the local raw is absorbed/closed」。让 `wt-close` 写 `phase/dropped` 会把平台标签从「只读快照」变成「本地决策镜像」，需新增同步逻辑（谁写/何时写/与 phase_state 冲突/双平台不一致），并破坏 `search_raw_issue`、`--reopen` 对「标签是快照」的前提 → **第二套真相源（L0 Q4）**。
- 已有机制足够：平台 `stateReason=NOT_PLANNED` 原生区分「完成/放弃」；关闭评论承载研究过程；`--state open` 过滤保证本地不拉回。三者组合即满足「本地不污染 + 有充足研究和关闭理由」。
- 「这个 CLOSED 是完成还是放弃」的答案应在**审计信息**（关闭评论 + `closeout_note`），不该编码进需同步的标签。

### 精确事实：本地拉取怎么过滤

- 主流物化入口**只取 open**：`platform-adapter.py:547`（GitHub `--state open`）、`:502`（Gitee `state=open`）。
- 两处刻意 `--state all`：`:365` / `:703` 的 `search_raw_issue`，属 **replica guard 副本发现**（按 raw-key 找有几份副本防重复建单），**只读身份、不物化**，看到 CLOSED 不污染本地。
- `wt-create:448-470` 另有本地保护：本地已存在 `phase_state ∈ {absorbed,completed,dropped}` 的 raw 拒绝隐式重开（除非 `--reopen`）。**但 dropped 后本地文档被抹除，此保护失效** → 真实缺口见 D。

## 实现缺口与 bug（逐条已核实）

| # | 问题 | 证据 |
|---|---|---|
| 1 | `wt-close --force --discard-unmerged` **不自动写关闭评论**：理由全靠人手工补，研究与关闭是两个可能半途失败的动作 | `wt-close` → `_close_issue_platforms_readonly` → adapter `close-multi` 不带 comment；`platform-adapter.py:329` GitHub `close_issue` 只 `gh issue close`（无 `--comment`），但 `add_comment` 存在；`gitee-issue.py:355` `close` 有 `--comment` 能力，adapter 未接 |
| 2 | **关闭语义错**：dropped 标 `stateReason=COMPLETED` | #4574 实测；GitHub 应 `gh issue close --reason "not planned"` |
| 3 | `wt-close:571` phase 检查只认 `completed`/`absorbed`，**漏 `dropped`** | 契约 `PHASE_STATES={"proposed","absorbed","dropped"}`、`platform_closed` 明确接受 dropped → 合法终态被逼用 `--force`（`--force` 语义是"彻底丢弃"），这是把执行者推进坑的实现 bug |
| 4 | **无 `drop` CLI**：`transition("dropped")` 能力存在但 `bin/issue-sync` dispatch 无此动作 | 执行者只能手工改 frontmatter；本次只改 phase_state，该文档 `validate()` 会红 |
| 5 | 两段 transition 未在命令层串联 | `raw_metadata_contract.py:258-272` |
| 6 | **dropped 后本地文档抹除 → 终态保护失效 → 显式 raw-key 可从 CLOSED 副本重新物化成 proposed** | `wt-create:448` 保护依赖 `[[ -f "$_issue_file" ]]`；`search_raw_issue` 用 `--state all` 能找到 CLOSED 副本 |

## 期望：完整技术方案

**A. 状态与理由落盘**
- 新增 `issue-sync drop <local_id> --reason <text>`，内部走 `transition("dropped", reason=...)`，原子写 `phase_state=dropped` + `completed_at` + `closeout_note`（=关闭理由），保证 `validate()` 通过。禁止手工改单字段。
- B1 阶段照做：`brainstorms.md` 记录 P0 研究；`candidates.md` 产出**一条 candidate，`status: dropped`**（`milestone-placement.md:45-47` 要求写清 dropped reason）。B2 及以后不做，不产生 develop 提交、不走 PR/review/merge。

**B. 平台关闭（修语义 + 理由同步）**
- `wt-close` 识别 `phase_state=dropped` 为**正常终态收口**，不再逼 `--force`（修 #3）。
- 关闭前**自动把 `closeout_note` + B1 研究结论作为关闭评论写到双平台**：GitHub `add_comment` + `gh issue close --reason "not planned"`（修 #1/#2）；Gitee 走 `cmd_close --comment`（能力已存在，adapter 接上）。
- 失败原子性：评论写失败 → 不关平台；平台关闭失败 → 不删工位。

**C. 本地抹除（不做 PR）**
- B1 研究与候选留在**平台时间线**（关闭评论），不进 develop。
- `--discard-unmerged` 语义收窄为「只删本地工位/分支痕迹」，不再是「丢弃研究成果」。

**D. 防重新物化（补 #6 缺口）**
- `wt-create --source platform --raw-key <key>` 与 `raw-issue-pull`：若按 raw-key 找到的平台副本**全为 CLOSED** → **fail-closed 拒绝物化**，报错带「已关闭、stateReason、关闭评论链接」；仅 `--reopen` 允许显式重开且必须写新理由。
- `search_raw_issue` 的 `--state all` 保持（副本发现需要），但**只返回身份给 replica guard，不得进入物化路径**；加 AT 钉住这条边界。

**E. 明确不做**
- 不加 `dropped` 标签；不改 `RAW_METADATA_FIELDS`、不改 `validate()` 的 dropped 必填规则；不改 GATE 1；不把 B1 研究合进 develop；不追溯重开历史 dropped（本次 #4574 的 `stateReason=COMPLETED` 作为已知偏差登记，不掩盖、不折腾）；不手工 `gh`/`gitee` 直连关单，仍走 adapter 唯一通道。

## 验收（AT，带基线红）

1. 构造 dropped raw（B1 研究 + 一条 `status: dropped` candidate），跑新收口路径后：双平台 CLOSED、各有一条含研究结论与理由的关闭评论、GitHub `stateReason=NOT_PLANNED`；
2. 抹除前的瞬时校验点：本地 `phase_state=dropped` 且 `completed_at`/`closeout_note` 齐全、`validate()` 通过；
3. develop 无该 raw 的新增文件（不产生 PR/merge）；工位与分支已清理；
4. 用相同 raw-key 再次 `wt-create --source platform` → fail-closed 拒绝，报错含关闭理由；`--reopen` 才允许；
5. `search_raw_issue` 仍能发现 CLOSED 副本（身份发现不被破坏），但不产生本地物化；
6. 评论写入失败时平台保持 OPEN 且工位保留（负向控制）；
7. 基线（develop）各条红。

## 自指防护（别懵圈）

本 raw 是**修复 dropped 收口命令的实现**，不是「被 P0 评审后要 dropped 的功能」。它自己的 B1 P0 必须判**继续**：缺口经源码核实（上表 1–6）、无既有 issue 覆盖（`065554Z` 只做未合并提交分诊、`031605Z` 只做 B0 审计、`#4652` 只做关键词广搜、历史 `20260409T171500Z` 是局部过期做法）。不得因「研究里看到很多 dropped 历史文档」而误判 dropped。

### comment-platform-1
- source: platform
- event: mirrored

## 方案修正（追加）：dropped 研究不提交 → 没有「未合并」，只有「丢工位」

用户指出：「本地研究 dropped，可能没有提交，也不用提交……也就没有不合并的说法，只是丢工位」。经核实成立，原方案里「`--discard-unmerged` 语义收窄」仍是错配，修正如下。

### 核实结论

`wt-close` 有两条**独立**门禁：

| 门禁 | 位置 | 检查对象 | 跳过 |
|---|---|---|---|
| dirty 检查 | `:1280-1300` | 工作区未提交文件（tracked dirty + untracked） | `--force` |
| unmerged 守卫 | `:782-880` | `rev-list develop..branch > 0`（**已 commit 未 merge**） | `--discard-unmerged` |

`--discard-unmerged` 只在 `FORCE==true && _ahead>0` 时触发。**B1 研究不提交 → `_ahead=0` → 该 flag 根本不参与**；且无新 commit 的分支 tip==develop tip，`git branch --merged develop` 会列出它 → 走 `-d` 正常删除，连 `-D` 都不需要。

`raw-20261114T051655Z` 那次是我**先 commit 了 B1 研究**（`b2af4e16d`）才凭空制造出「未合并提交」，进而被守卫拦、被迫 `--force --discard-unmerged`。即「未合并」不是 dropped 固有状态，是操作方式造成的。

### 真正的漏洞

dirty 检查的报错文案是「这些修改**没用** → 带 --force 直接丢弃」，把「不进 develop」等同于「没用」，因此**不会把研究结论留痕到平台**。命令缺的是「丢弃前自动把研究写成平台关闭理由」，不是 `--discard-unmerged`。

### 修正后的完整方案（替代原 C 段）

1. **B1 研究不 commit**：`brainstorms.md`（P0 研究）+ `candidates.md`（一条 `status: dropped`）留在工位工作区，untracked/dirty，不产生 commit、不进 develop、无 PR/review/merge。B2 及以后不做。
2. **`wt-close` 给 dropped 独立路径**，不再复用 `--force` / `--discard-unmerged` 的「丢弃提交」语义；`--discard-unmerged` 仅保留给「真有未合并提交」的场景。识别 `phase_state=dropped` 或新增 `--drop --reason <text>`，内部原子完成：
   - 读工位内**未提交**的研究 → 生成关闭理由；
   - 写本地**瞬时**合法终态：`transition("dropped", reason=...)` → `phase_state=dropped` + `completed_at` + `closeout_note`（**不 commit**，仅作理由单一来源 + 删除前 AT 校验点）；
   - **自动**把研究结论 + `closeout_note` 写入双平台关闭评论；GitHub `add_comment` + `gh issue close --reason "not planned"`，Gitee `cmd_close --comment`；
   - 失败原子：评论失败 → 不关平台；关平台失败 → 不删工位；
   - 删工位（`--force` 语义仅用于跳过 dirty 检查）+ `git branch -d`（无新 commit，无需 `-D`）。
3. **审计唯一持久载体 = 平台关闭评论**；本地零痕迹、develop 零污染、无 PR。`closeout_note` 的本地写入是瞬时的，随工位删除，不作为持久真相源。
4. `issue-sync drop --reason` 可作为 B1 阶段的显式标记动作存在，但 **wt-close 不得要求用户先手动执行、更不得要求先 commit**；wt-close 内部复用同一 `transition("dropped")` effect，保证理由只定义一次（回答「内部是否执行 issue-sync drop」：是「内部调用同一 drop 逻辑」，不是「用户先 drop 再 wt-close」）。

### 对验收的影响

- 新增：dropped 收口前 `git rev-list --count develop..<branch>` 必须为 **0**（研究未提交）；
- 新增：收口后分支以 `-d`（非 `-D`）删除，或至少不产生「丢弃未合并提交」日志；
- 保留：双平台 CLOSED + 关闭评论含研究 + `stateReason=NOT_PLANNED`、develop 无新增文件、工位清理、评论失败不关平台、再次 wt-create 对 CLOSED 副本 fail-closed。

### 边界不变

不加 dropped 标签、不改 `RAW_METADATA_FIELDS`、不改 GATE 1、不把研究合进 develop、不追溯重开 #4574（其 `stateReason=COMPLETED` 作为已知偏差登记）。自指防护不变：本 raw 自身 P0 判「继续」。

### comment-platform-2
- source: platform
- event: mirrored

## 方案收敛（最终）：复用 `--force --discard-unmerged` 骨架，内部接 drop

用户指出：「`wt-close --force --discard-unmerged` 本身就不检查提交不提交，反正就是丢。内部就是调用 drop 分支。不走正常 close 分支就对了。之前好像有些方面是满足的」。

经逐条核实 `wt-close` 的 FORCE 条件，**成立**。前两次修正里「研究不 commit」「新增 `--drop` flag」「走正常 close 分支」都是过度设计，作废。

### 已满足（无需改动，逐条证据）

| 行为 | 位置 | FORCE 时 |
|---|---|---|
| dirty 检查（工作区提交与否） | `:1279 if [[ "$FORCE" != true ]]` | 跳过 → **不检查提交没提交** |
| phase 检查 | `:569 if [[ "$FORCE" == false ... ]]` | 跳过 → dropped 的 phase 不会被拦 |
| unmerged 守卫 | `:797 if [[ "$FORCE" == true ]]` 才进 | `--discard-unmerged` 确认放行 |
| platform_state 未同步 | `:986 if [[ "$FORCE" != true ]]` | 跳过 → 直接关平台 |
| 关平台 | `:1008` `--force` 分支内 `_close_issue_platforms_readonly` | **已会关** |
| 删工位/删分支 | `:1338` `-D` | **已会删** |

即：`--force --discard-unmerged` 已经是「丢工位 + 关平台」的完整骨架，**不需要新 flag、不需要正常 close 分支、不需要约束提交状态**。

### 唯一要补的三件（都在 `--force` 路径内部，不改骨架）

1. **内部调用 drop 逻辑**：在 `--force` 分支关平台之前，调 `issue-sync drop` / 复用 `raw_metadata_contract.transition("dropped", reason=...)`，把 `--reason` 写成 `phase_state=dropped` + `completed_at` + `closeout_note`。产物是**瞬时本地状态**（工位随后被删），只用于：① 契约合法 ② 关闭理由的单一来源 ③ 删除前 AT 校验点。**不 commit、不要求用户先手动 drop、不进 develop**。
2. **自动写关闭理由到平台**：把 `closeout_note` + 工位内 B1 研究结论（未提交文件也读得到，工位此时还在）作为**关闭评论**写双平台；GitHub `add_comment` + `gh issue close --reason "not planned"`（修 `stateReason=COMPLETED`），Gitee `cmd_close --comment`。理由来自 `--reason`，不再靠人手工 `freely comment`。
3. **失败原子**：评论写失败 → 不关平台；关平台失败 → 不删工位。

### 明确作废（前两次修正里的过度设计）

- ❌ 「B1 研究必须不 commit」——`--force` 跳过 dirty 检查，提交与否都能丢；无需约束。
- ❌ 「新增 `--drop` / `--as-dropped` flag」——`--force --discard-unmerged` 就是入口。
- ❌ 「给 dropped 独立的正常收口路径、不复用 --force」——反了，正是要走 `--force` 丢弃分支。
- ❌ 「`--discard-unmerged` 语义收窄」——保留原语义即可（它同时服务「真有未合并提交」与「dropped 丢弃」）。
- ❌ 「分支必须 `-d` 而非 `-D`」——`-D` 是 `--discard-unmerged` 的既有行为，不动。

### 仍需修（与骨架无关的独立缺口，保留）

- `wt-close:571` phase 检查只认 completed/absorbed → **仅**在非 FORCE 的正常路径下才需要修正；dropped 走 FORCE 路径不受影响，故此项**降级为可选**（可在正常路径顺手补 `dropped` 以免未来误用，但非本轮必需）。
- `wt-create` / `raw-issue-pull` 对「按 raw-key 找到的平台副本全 CLOSED」应 fail-closed 拒绝重新物化（防污染），保留。
- `search_raw_issue` 的 `--state all` 保持不变（副本发现），加 AT 钉住「不进入物化路径」。

### 最终验收

1. `wt-close --force --discard-unmerged --reason <理由>` 对 dropped raw：双平台 CLOSED、各一条含研究+理由的关闭评论、`stateReason=NOT_PLANNED`；
2. 关平台前瞬时点：`phase_state=dropped` + `completed_at`/`closeout_note` 齐全、`validate()` 通过；
3. develop 无该 raw 新增文件（无 PR/merge）；工位/分支已清理；
4. **研究提交与否都能收口**（两个夹具分别覆盖）；
5. 评论失败 → 平台保持 OPEN、工位保留；
6. 同 raw-key 再次 `wt-create --source platform` → fail-closed；
7. 基线（develop）各条红。

### 边界

不加 dropped 平台标签、不改 `RAW_METADATA_FIELDS`、不改 GATE 1、不把研究合进 develop、不追溯重开 #4574。自指防护不变：本 raw 自身 P0 判「继续」。


### comment-20261114T120854Z
- source: system
- event: promote_finalized
- children: ["I-20261114T101138Z-A"]

拆解为以下任务:
1. [I-20261114T101138Z-A](will-be-updated)

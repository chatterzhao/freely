---
schema_version: '1'
local_id: raw-20261125T094413Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261125T094413Z-A
platform_ids:
  github:
    issue_id: '4703'
    url: https://github.com/chatterzhao/freely/issues/4703
    synced_at: ''
  gitee:
    issue_id: IKXYPB
    url: https://gitee.com/zhaoquan/freely/issues/IKXYPB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T09:44:13Z'
updated_at: '2026-11-26T04:58:57Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: 2026-11-26 04:58:47+00:00
closeout_note: ''
severity: P1
---

# feat: 元数据等价提交免重测，test-gate 证据沿袭机制

workflow_kind: feature

## feat: 元数据等价提交免重测，test-gate 证据沿袭机制

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T094413Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `none` |
| created | 2026-11-25T09:44:13Z |
| updated | 2026-11-26T04:58:57Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T094413Z`。实现前请用 `wt-create --raw-key 20261125T094413Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
封装命令在 dev 工位产生的可预测状态修改（issue-sync before merge 的 platform_ids、issue-sync close 的 platform_state、review verdict 文档、milestone 的 phase_state），同步到 test 工位后必须重跑全量 `test-all --ci`，否则证据 stale 被 wt-close 拦。这类修改不涉及任何功能/测试变更，重跑是纯浪费；本轮 #4699 收口就因 4 个纯文档提交重刷了 4 次全量测试。

## 根因（最小复现已证实）
`docs/system/workspace/scripts/quality/test-evidence.py:124-130` 的 validate() 强制 `LAST_TESTED_COMMIT == HEAD` 且 `EVIDENCE_HEAD == HEAD`。隔离复现：合法证据在 commit A 上 ok:true；仅改一个 frontmatter 字段 `phase_state: proposed→absorbed` 产生 commit B 后，validate 返回 `ok:false`，错误 `LAST_TESTED_COMMIT does not match worktree HEAD` / `EVIDENCE_HEAD does not match worktree HEAD`。判据是「HEAD 精确相等」，不区分变更性质，因此任何新 commit 都作废证据。

## 期望设计（安全优先，不能因放过可预测修改导致真修改不测）
1. **引入「元数据等价提交」分类**：仅当 commit 的全部改动落在严格白名单内才等价——
   - 允许路径：`docs/B1-docs/**/issue.md`、`docs/B2-docs/**/issues/I-*.md`、`docs/B2-docs/**/code-reviews/**`、`docs/milestones.md`；
   - 允许内容：仅 frontmatter 状态/同步字段的值变化（phase_state / platform_state / platform_ids / status / completed_at / synced_at / hash）与 review 文档正文；
   - **硬排除**（触碰即不等价，必须重测）：`**/verification/pre-tests.md`、`**/verification/tasks.md`、`bin/**`、`runtime/**`、`docs/system/**`、`tests/**`、`contracts/**`、`.githooks/**`、`projection.lock`、任何测试定义或可执行代码。
2. **证据沿袭而非清零**：新增 `freely test-gate attest-meta --worktree <test-wt> --through <commit>`（或等价封装），由可信调用方在合并等价 commit 后记录沿袭链。validate() 接受「LAST_TESTED_COMMIT 是 HEAD 的祖先，且 ancestor..HEAD 每个 commit 都通过白名单判定」；保留原 EVIDENCE_SHA256 绑定（不伪造新测试输出）。
3. **fail-closed + 写者可信**：沿袭链必须由封装命令写入并带机器校验（每个 commit 的 diff 分级结果 + hash）；手工 printf 的 env 不得被信任（沿用 test-evidence.py 头部威胁模型）。任一链上 commit 含非白名单改动 → 证据失效并给出可执行修复命令（重跑 test-gate run）。
4. **触发点**：`pr-merge-guarded` 的 issue-sync commit 与 `pr-review-guarded` 的 review commit 同步 test 工位后，自动判定是否等价并沿袭；等价则跳过重测，不等价则显式提示重测。
5. **可观测**：`test-gate validate` 回执区分 `current`（HEAD 相等）/ `equivalent`（沿袭有效）/ `stale`（必须重测）三态，理由可机读。

## 验收建议（TDD）
- AT 最小复现：commit A 上合法证据 → 改单个 frontmatter 字段生成 B → 原逻辑必须 RED（HEAD mismatch），修复后 `attest-meta` 沿袭 → validate ok 且 verdict=equivalent。
- 反向阻塞用例：构造含 `pre-tests.md` / `bin/**` / `runtime/**` 改动的 commit → 沿袭必须被拒、validate 必须 stale（证明未因放过元数据而漏测真修改）。
- 篡改用例：手工伪造沿袭链 env → validate 必须 fail（写者可信）。

## 非目标
- 不改变 test-gate run 的真实执行语义；不放宽任何代码/测试改动的强制重测；不改 pr-create/pr-merge 的门禁顺序；不夹带 #4702（push 吞错）、#4698、#4687。

## 与既有 raw 的关系
raw-20261125T094104Z（#4702）覆盖 pr-merge 源分支 push 回执；本条覆盖 test 工位证据 stale 判据，边界不重叠。

### comment-platform-1
- source: platform
- event: mirrored

## 设计修正（取代本 raw 初版 body 的「路径白名单一刀切」方案）

初版 body 用「路径 + 字段白名单一刀切放行」（issue 文档状态字段/review 文档/milestone 状态行 一律等价）是**错误设计**：它会在 Freely 自举场景放过真正该测的改动。用户澄清后修正如下，**以本评论为准**。

### 核心判据：语义影响，而非文件路径

重跑测试的充要条件是「**测试用例变了**」或「**被测对象变了**」；不是「某个文件被改了」，也不是「某个路径属于/不属于文档类」。

### 两类项目、两种测试对象（必须区分）

1. **用户项目**（Freely 作为工具被使用）：测试对象是用户自己的应用代码。封装命令（pr-create/pr-review/pr-merge/issue-sync）自动改的 issue 生命周期文档（B1/B2 issue、milestone、code-review 的 phase_state/platform_ids/platform_state 等）是**治理元数据/门禁依据**，不是用户应用的被测对象，用户也不会测试 Freely 本身。→ 这类变更**不重跑测试**，只 merge 证据沿袭。
2. **Freely 自举**：测试对象恰恰是 Freely 自身，AT 直接读取并断言 issue 字段（#4699 的 AT-001 断言 platform_state/platform_ids/phase_state；本轮 4 个纯文档 commit 改的正是被测字段）。→ 这类字段变更**就是被测行为，必须重跑**。

### 对「测试文档」的正确处理（修正初版的错误硬底线）

初版写「碰 `pre-tests.md` 一律 stale」是错的。正确区分：

- 改了 **测试用例定义**（`test_command`、`case_design`、`test_tasks`、`acceptance_target`、断言/期望值、新增或删除 AT）→ 测试内容变了，**必须重跑**。
- 只改了 **测试运行记录**（`red-green-status`、`status`、`actual_output`、`actual_RED_output`、`evidence_file` 等执行结果字段）→ 测试定义未变，**不重跑**（这些是证据留痕，不是用例）。

同理，任何文件（代码或文档）是否触发重测，取决于它是否属于「当前 lane 测试实际依赖的对象」，而非它在哪个目录。

### 落地设计

1. **每个 lane 显式声明测试依赖面**：pre-tests.md 新增 `evidence_sensitive_paths`（测试实际读取/断言的路径集合）+ `evidence_test_definition_fields` 标记哪些字段属于用例定义。未声明 → 保守视为全敏感（必须重测）。
   - 用户项目普通 lane：敏感面不含治理文档 → 元数据变更沿袭。
   - 自举 lane（#4699 类）：敏感面含被断言的 issue 字段 → 字段变更触发重测。
2. **等价判定 = 双重无交集**：
   - diff 路径 ∩ `evidence_sensitive_paths` = 空；
   - 且 diff 未触及任何 AT 的用例定义字段（测试定义指纹不变）。
   两者同时满足才等价。用「用例定义指纹」而非整个 `pre-tests.md` 文件哈希——否则运行记录字段变化会误触发。
3. **证据沿袭**：`freely test-gate attest-meta --worktree <test-wt> --through <commit>` 计算 LAST_TESTED_COMMIT..HEAD 每个 commit 的 diff，按上述判定；等价则沿袭原 EVIDENCE_SHA256（不伪造测试输出），写入可机读回执（commit hash + diff 路径 + 交集为空证据）。
4. **可信写入 + fail-closed**：沿袭链须由封装命令写入并机器校验；手工 printf 的 env 不被信任（沿用 test-evidence.py 威胁模型）。声明缺失、交集非空、用例定义变化、链不可验证 → 一律 stale + 可执行修复命令（重跑 test-gate run）。
5. **触发点**：pr-merge 的 issue-sync commit、pr-review 的 review commit 同步 test 工位后自动调用判定——等价免重测，不等价显式提示。
6. **三态回执**：validate 区分 current（HEAD 相等）/ equivalent（沿袭有效）/ stale（必须重测），理由可机读。

### 验收建议（TDD，语义正反用例）

- 用户项目场景：敏感面不含 issue 文档 → 改 platform_state → 沿袭成功、validate=equivalent。
- 自举场景（#4699 复刻）：敏感面含 issue 字段 → 改 platform_state → **必须** stale、拒绝沿袭。
- 用例定义变更：改 `test_command`/`case_design` → 必须 stale（即使没改任何代码）。
- 仅运行记录变更：改 `red-green-status`/`actual_output` → 必须 equivalent（不重跑）——修正初版误判。
- 篡改用例：手工伪造沿袭链 env → validate fail。
- 现有 test-evidence-chain AT 回归全绿。

### 非目标

不改变 test-gate run 真实执行语义；不放宽任何「被测对象/用例定义」变更的强制重测；不改 pr-create/pr-merge 门禁顺序；不夹带 #4702（push 吞错）、#4698、#4687。
#### resolution-20261126T053117Z
- status: adopted
- reason: 采纳平台设计修正评论——以语义影响而非路径白名单判据；实现 test-evidence.py attest-meta + 三态 validate + 测试定义指纹 fail-closed，AT 正反用例覆盖（13/0 GREEN、3/10 RED）。
- resolved_by: worker_01

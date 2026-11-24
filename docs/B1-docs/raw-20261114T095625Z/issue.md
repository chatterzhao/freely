---
schema_version: '1'
local_id: raw-20261114T095625Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T095625Z-A
platform_ids:
  github:
    issue_id: '4652'
    url: https://github.com/chatterzhao/freely/issues/4652
    synced_at: ''
  gitee:
    issue_id: IKVBLF
    url: https://gitee.com/zhaoquan/freely/issues/IKVBLF
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/issues/I-20261114T095625Z-A.md
last_synced_comment_at:
  github: '2026-11-24T12:30:12Z'
  gitee: '2026-11-24T12:30:12Z'
hash: ''
created_at: '2026-11-14T09:56:25Z'
updated_at: '2026-11-24T12:30:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T095625Z-A
source_candidate: ''
completed_at: '2026-11-24T12:30:11Z'
closeout_note: ''
severity: P1
---

# feat: B0 缺关键词广搜与多文档交叉，P0 可能误判方向

workflow_kind: feature

## feat: B0 缺关键词广搜与多文档交叉，P0 可能误判方向

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T095625Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T09:56:25Z |
| updated | 2026-11-14T09:56:25Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T095625Z`。实现前请用 `wt-create --raw-key 20261114T095625Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（本轮吃狗粮实测）

对 `raw-20261114T051655Z`（lane 模型 / 字段类判据）做 P0 时，用 **12 组关键词**广搜文档与实现，才发现这条 raw 的**前提不成立**，最终 B1 研究后 **dropped**：

- `governance-merge-gate:1108-1130`：skip 时在 GATE 1 之前 `return 0`，治理车道本就合法；
- `pr-create-guarded:133-144` 已接线 `FREELY_SKIP_IBM_GATE`；`config.toml allowed_paths` 已含 B1/B2-docs；
- 关键词 `字段类 / batch --all / chore\/sync / 第三类分支` **全项目只命中本会话刚写的 `replica-metadata-contract.md`**，证明这套术语是局部推论；
- 诉求已被 `031043Z` / `034750Z` / `#4435` 覆盖；继续实现会重复建设且引入第二套放行语义。

若只读 raw 自己列的「GATE 1 判路径」这一处，就会直接实现出一个基于局部、方向错误的方案——正是「实现后错误或不佳」。

## 现行 B0 的缺口（已读源码）

`freely-doc-B1_IBM-execution/SKILL.md` 的 B0（本会话刚落地）：

- 只要求「外部锚点（引用原文，至少两类）」——是**读列好的锚点**，没有要求**主动用关键词广搜**；
- step 0「审视 issue 价值与时效性」只问「是否值得做 / 是否已被覆盖」，没有要求**怀疑一个功能可能散落多份文档**；
- 没有要求区分「当前生效实现 / 历史 B1 局部文档 / 当前权威恢复点」；
- 没有要求交叉比对多份文档之间的**矛盾**（哪份已过期、哪份已废弃）；
- 没有把 P0 的结论显式写成 **「继续 or dropped」的二元决策**并留痕。

本轮命中 `governance-only lane` 的 40+ 份文档里，绝大多数是 2026-04~07 的历史 B1 `issue.md`/`brainstorms.md`，若只挑一份当依据必误判；`raw-20261103T091157Z` 的 IDN 描述也已部分过期；`goal-arch-debt.md` 大量历史恢复点只有「当前唯一权威」段有效。**文档没管理好，所以必须靠关键词广搜看全局**，这是用户明确指出的风险。

## 期望：B0 增加「关键词广搜 + 多文档交叉」层

1. **关键词族（至少覆盖 3 组）**：功能名 / 机制名 / 字段名 / 命令名 / 门禁名 / 相关 raw key；分别搜 `docs/**`、`bin/**`、`.freely/**`。
2. **怀疑多份文档**：明确写出「一个功能可能有多份文档，其中可能有局部、过期或废弃版本」，不得只读一份即下结论。
3. **三类分层**：把命中文件分成「当前生效实现」「历史局部文档」「当前权威恢复点」，并说明各自权重；历史文档只能作背景，不能当现状。
4. **交叉比对矛盾**：列出「哪两份文档说法冲突、哪份已过期/被后续实现取代」，作为 §0 的强制字段。
5. **二元决策**：P0 结论必须显式写「继续（附方向）/ dropped（附覆盖它的 issue 与证据）」；dropped 走 B1 step 0，不产出 B2/AT/实现。
6. **留痕**：dropped 的研究结论必须通过 `freely comment --issue <raw> --file ...` 留到双平台，避免工位删除后证据丢失（本轮已实践）。

## 验收（AT，带基线红）

1. skill 的 B0 含「关键词广搜」「多份文档/局部/过期/废弃」「三类分层」「交叉比对」「继续/dropped」等要求；
2. brainstorms 模板 §0 含关键词族记录表、三类分层表、矛盾清单、二元决策字段；
3. 完成自检加一项「§0 含关键词广搜记录且给出继续/dropped 结论」；
4. 静态断言「不做硬门禁」（防补字段就过）；
5. 基线（develop）红。

## 自指防护（本 raw 自己的 P0 必须判「继续」，不得 dropped）

用户明确提醒：「我们说的是未来用 freely 遇到一些评审要 dropped，但现在 p0 优化的这个 raw issue 自己用这个评审的时候，本来要推进，别看错，实现半天最后 dropped 了」。

因此本 raw 的 B1 P0 必须显式给出：

- **判定：继续**（不是 dropped）。
- 依据：B0 缺关键词广搜 / 多文档交叉 / 局部·过期文档辨识 / 显式二元决策，是**经读源码核实的真实缺口**；`freely-doc-B1_IBM-execution/SKILL.md` 的 B0 全文（第 47–77 行）逐条可证；**没有任何既有 issue 或实现覆盖它**（`raw-20261114T031605Z` 只做了锚点与四问，未做广搜；`raw-20261114T051655Z` 已 dropped 且是「被评审对象」而非规范增强）。
- **不得误判 dropped 的理由**：dropped 只适用于「前提被推翻 / 诉求已被其他 issue 覆盖」。本 raw 两者都不成立；研究过程中发现「很多历史文档过期」恰恰**证明**需要广搜层，而不是证明本 raw 无价值。
- 本条同时应写进 B0 增强内容：**dropped 判定必须给出「覆盖者」证据**，禁止以「研究耗时长 / 历史文档多 / 方向看起来复杂」为由 dropped。

> 这条自指防护本身就是「别懵圈」的落地：P0 是**方法**，dropped 是**方法作用于某个 raw 后的可能结论**；二者不在同一层。

## 边界

- 不改 review L0 五问与失败判据、不改 verdict 契约；
- 不新增硬门禁、不自动 dropped（dropped 必须由 B1 研究给出理由）；
- 不追溯校验历史 raw；不把关键词广搜做成自动脚本扫描（它是 B1 的研究动作，由 AT 钉住模板与自检）；
- 不夹带本轮 dropped 的 051655Z 结论（已单独留痕并关闭）。

## 证伪

- 「外部锚点已要求引用原文，等于搜过了」→ 否：列锚点是**读**，广搜是**找**；本轮正是靠 C 组关键词发现术语只在本会话文档里。
- 「这会把 B1 拖长」→ 否：关键词族与三类分层是结构化表格，纯文档 typo 类 raw 可写「不适用 + 理由」；价值在于防「实现后方向错误」。

### comment-20261124T123012Z
- source: system
- event: promote_finalized
- children: ["I-20261114T095625Z-A"]

拆解为以下任务:
1. [I-20261114T095625Z-A](will-be-updated)

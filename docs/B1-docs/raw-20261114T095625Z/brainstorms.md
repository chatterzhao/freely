---
b1_id: B1-20261114T095625Z
phase_state: completed
source_raw: raw-20261114T095625Z
produced_candidate: C-20261114T095625Z-A
created_at: 2026-11-24
---

# B1_IBM: B0 关键词广搜与多文档交叉

## 0. 设计意图审计（先于方案）

### 关键词广搜记录（本轮新增方法自举）
| 关键词族 | 命中文件（当前生效 / 历史局部 / 权威恢复点） |
|---|---|
| 功能名：B0 / 设计意图审计 | `skills/freely-doc-B1_IBM-execution/SKILL.md:49-77`（当前生效）；`docs/B1-docs/raw-20261114T031605Z/`（历史局部，仅做锚点四问） |
| 机制名：keyword / broad search / 广搜 | 本会话 raw body（当前需求）；无既有实现 |
| 门禁名：pretests-gate / b1-design-intent | `tests/test-b1-design-intent-audit.py`（当前生效，钉旧 B0） |
| 字段名：design_verdict / anchor_refs | `candidates.md` 模板（当前生效） |
| raw key：20261114T031605Z / 051655Z | 前者历史局部；后者已 dropped（被评审对象，非规范增强） |

### 三类分层
- 当前生效实现：SKILL.md B0 段（第 47–77 行）+ `test-b1-design-intent-audit.py`。
- 历史局部文档：`raw-20261114T031605Z/brainstorms.md`（只做锚点+四问，无广搜/分层/二元决策）。
- 当前权威恢复点：`.freely/goal-arch-debt.md` 顶部 v5 队列与恢复点；本轮队列确有 #4652 待推。

### 矛盾清单
- `raw-20261114T031605Z` 的 IDN 描述称"锚点即证据"，但本轮实证多个历史 B1 文档说法冲突（governance-only lane 40+ 份文档，多数 04–07 月过期）——说明"读列好的锚点"不足以判现状。

- 外部锚点（引用原文，至少两类）:
  - skill 源码 `SKILL.md:49-51`「外部锚点（引用原文，至少两类）…」——只要求读列好的锚点，无广搜。
  - 同文件 `:45-48` step 0「审视 issue 价值与时效性…是否已被其他 issue/candidate 覆盖」——无"怀疑功能散落多文档"。
  - 既有 AT `test-b1-design-intent-audit.py`——钉旧 B0，无广搜字段。
  - 本 raw body「文档没管理好，所以必须靠关键词广搜看全局」。
- 判定（五选一）: **设计不完整**。B0 的"读锚点+四问"设计方向正确，但缺"主动找（广搜）+ 多文档分层 + 交叉比对 + 显式二元决策"四层，导致已发生 P0 误判风险。
- 与既有断言的冲突: 无；扩展 B0 不删旧要求。
- 影响面: `freely-doc-B1_IBM-execution/SKILL.md` 的 B0 段与完成自检；新 AT；不改 review L0、不改 verdict 契约、不新增硬门禁。

## 0.1 全局适配反思（四问）
- Q1 类别: 流程能力（B1 预研质量）。
- Q2 职责边界: B0 是 B1 研究动作，由 skill 模板 + AT 钉住；不引入自动脚本扫描（那是另一层）。
- Q3 结构性冲突: 若把广搜做成硬门禁会要求"补字段就过"——反设计；保持"结构性表格 + 自检 + AT 静态断言"，不做硬门禁。
- Q4 门禁失配: 现有门禁不测 B0 文档质量；新增 AT 静态断言覆盖，不动 gate 判据。

## 自指防护（用户明确要求）
- **判定：继续**（不是 dropped）。
- 依据：缺广搜/分层/二元决策是经读源码核实的真实缺口（SKILL.md B0 全文逐条可证）；无既有 issue 覆盖（031605Z 只做锚点四问；051655Z 已 dropped 且是被评审对象）。
- 不得误判 dropped 的理由：dropped 仅适用于"前提被推翻/诉求已被覆盖"，本 raw 两者都不成立；发现历史文档过期恰恰证明需要广搜层。
- 本条同时写入 B0 增强：**dropped 判定必须给出"覆盖者"证据**，禁止以"研究耗时/历史文档多/方向复杂"为由 dropped。

## Decision
继续 B2：扩展 B0 段增加关键词族表、三类分层表、矛盾清单、继续/dropped 二元决策与留痕要求；新增 AT 静态断言；完成自检加一项。

## Candidate
- candidate_id: C-20261114T095625Z-A
- status: promoted
- milestone: M-20261114T095625Z-A

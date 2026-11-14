# B1 Brainstorm — raw-20261114T031605Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `skills/freely-doc-B1_IBM-execution/SKILL.md:45-51`「### B：Brainstorm — 发散→收敛→决策」，现有 step 0「审视 issue 价值与时效性」、step 2「读取边界文档：CONSTITUTION.md、LAWS.md、PROJECT_INTENT.md」；同文件 `:42`「Skill 是流程的唯一权威来源」。
  - 既有验收测试: `test-review-intent-anchor.py`（R33.14 的 L0 锚点 AT）、`test-review-guidance-l0.py`（R33.16 的评审引导 AT）、`test-verdict-contract`（verdict 唯一解析器）。
  - 门禁源码注释/理由: `skills/freely-tdd-review/SKILL.md` 的 L0 段「L0 先于四层。四层的『自洽』不能替代 L0 的『一致』」「L0 不通过直接 fail」；`governance-merge-gate:1500` 只校验 B1 产物**存在**（「此 merge 没有按 skill 治理产出的文档 (brainstorms.md + candidates.md)」），不校验其内容结构；`check-skill-frontmatter` 只校验 frontmatter 与 `skill-map.yaml`，不约束正文段落。
  - 既有同类实现: `freely-tdd-review` 的 L0（外部锚点 + Q1–Q5 + 四段举证 + 失败判据）——**合并前核对**；`issue-sync-scope.py`、`merge_issue_sync.py` 的「范围由调用方声明」分层。
  - 配置约束: `.freely/config.toml [skip_ibm_gate].allowed_paths` 不含 `skills/`（R33.14 已核实），故 skill 变更必须走完整 IBM 链路，不能走 doc-only。
- 判定（五分类）: **设计不完整** + **实现未完成**。B1 阶段缺一层「动手前的决策」（设计不完整），candidate 模板与完成自检缺相应可核对字段（实现未完成）。**不是**设计错误、**不是**实现偏差、**不是** bug：现有 B 阶段的行为与它的设计一致，只是设计本身少了一层。
- 与既有断言的冲突: 无。`governance-merge-gate` 只要求 brainstorms/candidates 存在，新增 §0 段落与两个 candidate 字段不违反任何现有校验；`check-skill-frontmatter` 不受正文段落影响；未改 L0 五问与失败判据。
- 影响面: `skills/freely-doc-B1_IBM-execution/SKILL.md`（B 阶段 / 两个模板 / 完成自检）、新增一条 AT、`bin/test-all` 接线；**不改** `governance-merge-gate`、不改 verdict 契约、不改 review L0。

### 0.1 全局适配反思（四问）

1. **类别**：这是**流程能力（B1 决策层）**，不是副本传播、不是治理元数据修复、不是实现 bug。
2. **职责边界**：`B1 §0` 是**决策**（动手前：这是哪类问题、该改设计还是改实现）；`review L0` 是**核对**（合并前：实现有没有偏离、降级、第二套语义）。两者引用同一套锚点，但**不能互相替代**——到了 review，返工成本已经付过。skill 是流程权威，AT 只防回退，**不做硬门禁**。
3. **结构性冲突**：若硬门禁只校验「§0 段落/字段存在」，会退化成「补一段空文本就过」（用户明确反对，L0 的教训）；若要求每个 raw 都写长篇审计，纯文档 typo 类会被拖慢。故要求「锚点原文 + 判定 + 冲突 + 影响面」四行实质内容，且允许纯文档修订写「不适用 + 理由」。
4. **门禁失配**：现有门禁测的是**产物存在性与治理链**，不是**决策质量**。本轮**不改门禁**、不新增跳过通道；只把决策写进 skill + 模板 + 自检。若若干轮后要升级为门禁，必须校验锚点能在被引用文件里**逐字命中**，而不是只查字段存在——这条写进边界，防止后人走捷径。

## 1. 问题（真实代价）

本轮之前连续三次「拿到 raw 就局部开干」：
1. 为让跨 raw 对齐通过 GATE 1，删掉 `wt-close` 的 `platform_state` 前置检查（把门禁冲突转嫁成实现退化）；
2. `git reset --hard` 回滚跨 raw 文档时把同分支已提交的 `cmd-create` 改动一起丢掉，review 却仍写 FR-1 已完成；
3. 见「batch 没关链接」就直接改 `cmd-batch`，事后才读 `ibm-framework.md` 确认「sync 由确定性生命周期事件驱动」。

共同点：**没有在动手前判定这是设计错 / 设计不完整 / 实现未完成 / 实现偏差 / bug**。到 review 才被 L0 兜住，返工成本已付。

## 2. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | B1 增 B0（锚点 + 五分类 + 四问 + 冲突 + 影响面）、candidate 带 `design_verdict`/`anchor_refs`、完成自检加两项、AT 防回退 | 决策前移、可核对、不做硬门禁 ✅ |
| B | 只在 review L0 加强 | 事后，返工成本已付；且与 L0 职责重复 ❌ |
| C | `pr-create-guarded` 新增硬门禁校验字段存在 | 补空文本即过，用户明确反对 ❌ |
| D | 要求每个 raw 写长篇审计 | 纯文档修订被拖慢，且与「不做补字段式门禁」精神冲突 ❌ |

采用 A。

## 3. 与 review L0 的分工

| 层 | 回答什么 | 时机 | 成本 |
|---|---|---|---|
| B1 §0 | 这个 raw 是哪类问题？该改设计还是改实现？ | 动手前 | 最低 |
| review L0 | 实现有没有偏离项目意图、降级、第二套语义？ | 合并前 | 兜底 |

B1 是**决策**，review 是**核对**；引用同一套锚点，不重复定义五问内容。

## 4. 证伪

- 「B 阶段 step 2 已读边界文档，等于做了审计」→ 否：step 2 是**读**，不产出判定；且漏了既有验收测试、门禁源码注释/理由、既有同类实现、配置约束。
- 「加字段就会被补空文本绕过，所以别加」→ 否：字段是**交接证据**（candidate 要带到 M/B2），不是门禁；AT 只断言 skill/模板/本轮产物的结构，不校验所有 raw。
- 「这属于 L0 的范围」→ 否：L0 在合并前，B1 在立项时；两者时机不同，B1 的结论正是 L0 的核对输入。

## 5. 边界

- 不改 `freely-tdd-review` L0 的五问与失败判据；不改 verdict 契约；不新增硬门禁/跳过通道；
- 不校验所有历史 raw 的 brainstorms（否则等于追溯性门禁）；
- 若未来升级为门禁，必须校验锚点逐字命中原文，不得只查字段存在。

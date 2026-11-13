---
name: freely-tdd-review
description: >-
  IBM 四节点链路（raw → candidate → milestone → I-* issue）逐级消化审查。
  按 raw issue → B1 brainstorms → candidate → milestone → B2 brainstorms →
  B2 物化（I-* issue + 设计文档）→ 实现 → 测试四层顺序，每级检查下游是否
  忠实消化了上游。不是门禁——查内容质量和 fidelity，不查文件存在。

  Use when: PR review 阶段，或 B1/B2/dev 任一阶段完成后需要独立验证
  消化质量。触发词："review"、"审查"、"消化"、"fidelity"、"评审"、
  "检查质量"、"逐级审查"。
loop: review
owner: reviewer
supersedes: []
---

# skill:freely-tdd-review

> 审查不是门禁。门禁问"文件在不在"，审查问"下一级有没有忠实消化上一级"。
>
> IBM 链路的本质：上层抽象 → 下层具体化。每一级都是上一级的细化展开。审查就是检查每个消化步骤的 fidelity。
>
> **但 fidelity 只回答「下层是否忠于上层」，不回答「上层是否忠于项目」。**
> 四层全绿仍可能整体漂移——因为 B1/B2 也是本轮的产物，不能用自己证明自己。
> 所以本 skill 在四层之前先跑一层 **L0：项目意图一致性**。L0 不通过直接 fail，不必逐层看完。

## L0：项目意图一致性（设计漂移检测）

> 锚点是**先于本轮存在**的项目资产，不是本轮的 B1/B2。
> 四层的「自洽」不能替代 L0 的「一致」。

### L0.1 必须引用的外部锚点

审查时必须打开并引用原文（引用不了 = 没做 L0）：

1. **设计文档**：`README.md`、`docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/PROJECT_INTENT.md`、`docs/system/workspace/scripts/README.md`、`contracts/**`。
2. **既有验收测试**：尤其是断言「必须拒绝 / 必须阻止 / 必须 fail-closed」的测试（例：`test-wt-close-protected-branch-guard` Test 1–3 断言 `main/develop/test-pre-merge-*` 一律 blocked）。
3. **既有门禁的源码注释与理由**（例：`check-bin-projection` 的 "no permanent exemptions"；`raw_reconciliation._body()` 的 "platform copies never inline them"）。
4. **既有同类实现**：是否已有同一能力？本轮是否在造第二套？
5. **配置对能力的约束**（例：`.freely/config.toml [skip_ibm_gate].allowed_paths` 是否允许把本改动当 doc-only）。

### L0.2 五个必答问题

| # | 问题 | 不通过的样子 |
|---|---|---|
| Q1 冲突 | 本轮实现是否与既有验收测试 / 契约 / README 的明确断言冲突？ | 有冲突却未解释；或直接改测试断言来适配实现 |
| Q2 门禁强度 | 是否放宽、绕过或删除任何门禁？改后强度是否 ≥ 改前？ | 把「必须拒绝」改成「条件放行」，却拿不出「当初设计错误」的证据 |
| Q3 能力降级 | 是否有能力被删除、强制执行变可选、fail-closed 变 fail-open、默认值变宽松？ | 为了让流程走通，把强校验降级为 WARN |
| Q4 第二套语义 | 同一概念是否出现第二个真源 / 第二套判断？ | 已有 `phase_state`/`platform_state` 判定，又写入 `status: closed` |
| Q5 设计漂移 | 本轮是否在「修实现」的名义下改变了设计意图？ | 注释说「never on develop」，实现却写 develop |

### L0.3 门禁改动的举证责任（四段证据，缺一不得 pass）

凡修改门禁 / 契约 / 安全边界，review 必须给出：

1. **当初为什么这样设计**：引用引入它的 commit / raw / 验收测试原文；
2. **现在为什么必须改**：是实现不达标、环境变化，还是设计本身错误；
3. **判定**：明确写「实现不达标（改实现）」还是「设计错误（改门禁）」；
4. **强度不降**：逐条说明改后仍满足原有断言；确需放宽时必须列出等价补偿。

### L0.4 失败判据（任一命中即 fail）

- 与既有验收测试/契约冲突，且 review 未解释；
- 为让本轮通过而修改/删除既有断言（而不是修实现）；
- 门禁被放宽且没有「当初设计错误」的证据；
- 出现第二套语义 / 真源；
- 用「本轮 B1/B2 已决定」回答 Q1–Q5（自证）；
- 用手工补数据 / 补字段让门禁通过，而不是修数据链路。

### L0.5 真实案例（这些实现四层全绿，但 L0 应判 fail）

- **R33.8**：新增 `close-linked` 只校验 kind + platform_ids 就关平台 → Q2（绕过 `phase_state` 与 `issue-sync batch` 状态驱动）、Q4（`status: closed` 第二套语义）、Q5（偏离 batch 单一路径）。
- **R33.8**：raw 副本判红时手工补 `### comment-` 块 → 「用补数据让门禁通过」，直接命中 L0.4。
- **R33.9 / R33.10**：为回收残留沙箱加 test-pre-merge 回退解析、放宽 `_is_protected_branch` → Q1（与 Test 1–3 冲突）、Q2（放宽 protected guard）、Q5（沙箱跑完整 raw 生命周期）。

## 核心方法

```
raw issue（问题）──→ B1 brainstorms（分析/决策）──→ candidate（结晶，C-{raw key}-A）
    ↓ 忠实消化？          ↓ 忠实消化？
    
candidate ──→ milestone（M-{raw key}-A，candidate_issues 入队）
    ↓ 忠实消化？
        ┌─ B2 I（Input）：读 candidate → 获取 I-* issue 元信息（key+suffix）
        │       ↓ 忠实消化？
milestone ──┤   B2 B（Brainstorm）：研究方案 → 物化 I-* issue → 产出全部设计文件
        │   （brainstorms/ + issues/ + prd.md + pre-tests.md + tasks.md + code-reviews/）
        │       ↓ 忠实消化？
        └─ B2 M（Map）：确认规范目录结构 → milestones.md committed_issues → 交付

B2 文档 ──→ 实现代码（TDD：测试驱动实现）
    ↓ 忠实消化？

pre-tests ──→ 测试执行（全 GREEN + 真实 evidence）
```

> 四节点链路（raw → C → M → I）：raw issue、candidate（C-{raw key}-{suffix}）、milestone（M-{raw key}-A）、I-* issue（I-{raw key}-{suffix}）共享同一时间戳 {raw key}。milestone 是 milestones.md 中的 `## M-{raw key}-A` 节点——candidate 通过 `candidate_issues` 入队，I-* issue 通过 `committed_issues` 出队。Milestone 始终使用 -A（一个 raw issue 一个 milestone 容器），candidate 和 I-* 的 suffix 可变（多个 candidate 时 -A、-B...）。
>
> `freely-doc-B2_IBM-execution` skill 的 I→B→M：**I** 读 B1 candidate（元信息）→ **B** 做全部产生工作（研究 + 物化 I-* issue + 产出 prd/pre-tests/tasks/IDN）→ **M** 确认路径 + 写 milestones。**I-* issue 是 B 阶段的产出，所有设计文件都在 B 阶段生成。** gate 校验四节点完整性，审查校验相邻节点间的消化 fidelity。

审查就是检查每个 "↓ 忠实消化？" 箭头。

**判断标准**：能从下层归纳回上层 → 消化到位。上层在下层中找不到对应 → 遗漏。下层出现了上层没有的东西 → 偏离。

## 输入

审查者从工位自行读取：
1. `docs/B1-docs/raw-{key}/issue.md`
2. `docs/B1-docs/{key}--{slug}/brainstorms.md` + `candidates.md`
3. `docs/milestones.md`（四节点链路：C-{key}-{suffix} → M-{key}-A → I-{key}-{suffix}）
4. `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md`（suffix 继承 candidate 的 suffix：C-{key}-{suffix} → I-{key}-{suffix}）
5. `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/brainstorms/b-I-{raw key}-{suffix}.md`
6. `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/prd.md`、`verification/pre-tests.md`、`verification/tasks.md`、`code-reviews/`
7. `git diff develop..HEAD`（实际代码变更）

> `{epic-name}` 和 `{story-name}` 由 `freely-doc-B2_IBM-execution` skill 在物化 I-* issue 时确定。epic 是能力域（如 `worktree-lifecycle`），story 是 epic 下的可交付切片（如 `creation-from-raw-issue`）。详见 `freely-doc-B2_IBM-execution` skill §M：Map。

## 四层逐级审查

### 第一层：Raw → B1 — 问题到决策的消化

> raw issue 描述问题 → brainstorms 分析问题并做出决策 → candidate 结晶决策为可执行候选

**核心问题**：candidate 能不能忠实归纳出 brainstorms 的结论？brainstorms 有没有遗漏 raw issue 的重要方面？

| 检查项 | 怎么审 |
|--------|--------|
| raw → brainstorms 覆盖 | raw issue 的每个问题点/模块，brainstorms 是否逐一分析？有没有 raw 提到了但 brainstorms 完全没涉及的？ |
| brainstorms 发散充分 | 是否探索了多个方案（Option）？每个方案的分析是否具体，不是走过场的"Option X 最好"？ |
| brainstorms → candidate 忠实 | candidate 的 acceptance_criteria 是否对应 brainstorms 的 Decision？brainstorms 的边界分析和依赖分析是否反映在 candidate 的 promotion_gate 中？ |
| scope 评估 | brainstorms 是否判断了 scope 大小？raw 覆盖多个独立模块时是否拆分为多个 candidate？一个 raw → 一个 candidate 是否合理？ |

**失败时必须给出**：
- brainstorms 遗漏了 raw 的哪个方面，应该怎么分析
- candidate 曲解了 brainstorms 的哪个决策，正确的 acceptance_criteria 应该是什么
- scope 为什么不合理，应该拆成几个 candidate、每个的边界是什么

### 第二层：B1 → B2 — candidate 经 milestone 到 B2 产出的消化

> candidate（C-{key}-{suffix}）→ milestone（M-{key}-A，candidate_issues 入队）→ `freely-doc-B2_IBM-execution` skill B 阶段（brainstorms 实现分析）→ M 阶段（物化 I-* issue + prd/pre-tests/tasks/code-review）

**核心问题**：candidate 是否正确进入了 milestone？B2 brainstorms 是否基于 candidate 做了充分的实现分析？B2 M 阶段物化的 I-* issue 是否忠实消化了 candidate？prd/pre-tests 等设计文档是否从 brainstorms 推导出来？

| 检查项 | 怎么审 |
|--------|--------|
| candidate → milestone 入队 | candidate 是否正确绑定到 milestone（M-{key}-A）？candidate 的 `milestone` 字段是否与 milestones.md 中的 M-{key}-A 一致？ |
| candidate → B2 brainstorms | b-I-*.md 是否分析了 candidate 的实现面？是否评估了替代实现方案？是否对齐了 candidate 的 acceptance_criteria？ |
| B2 brainstorms → I-* 忠实 | I-* 的 acceptance_criteria 和 promotion_gate 是否完整承载了 candidate？I-* 的 phase_state、字段是否齐全？是否在 milestones.md committed_issues 中有对应条目？ |
| B2 brainstorms → prd | prd 的模块划分是否从 b-I-*.md 的实现方案分析中自然推导出来？prd 的 Goal 是否对应 b-I-*.md 的设计决策？ |
| B2 brainstorms → pre-tests | pre-tests 的每条 acceptance 是否可追溯到 prd 的模块需求？test_command 是否针对改动面设计？覆盖层级（unit/integration/e2e）是否与改动范围匹配？覆盖率是否达标（改动面是否被充分测试，不是挂一漏万）？ |
| B2 brainstorms → tasks | tasks 的分解是否对应 prd 的模块？是否可从 tasks 回溯到 b-I-*.md 的实现顺序？ |
| B2 brainstorms → code-review | Implementation Decision Note 的 5 字段是否具体？是否反映了 b-I-*.md 的替代方案评估和残余风险？ |

**失败时必须给出**：
- 哪个 B2 产物缺失或与上级不对齐
- b-I-*.md 和 I-* 的对应关系是否正确
- pre-tests 遗漏了哪个改动面，应该增加什么测试，建议 test_command 示例

### 第三层：B2 → 实现 — TDD 测试驱动实现

> prd + pre-tests + tasks → 实际代码

**核心问题**：代码是否严格按照 pre-tests 的测试指导来驱动实现（TDD）？实现是否忠实于 prd 和 tasks 的设计？

| 检查项 | 怎么审 |
|--------|--------|
| pre-tests → 代码覆盖 | 每条 pre-tests acceptance 所描述的测试面，在 diff 中是否有对应的代码变更？反过来，diff 中的每个改动是否在 pre-tests 中有对应的验证项？覆盖率是否达标——不是"有一个测试就行"，而是改动面被充分覆盖？ |
| prd → 代码忠实 | prd 的每个模块是否在代码中有对应实现？代码是否实现了 prd 没有描述的功能（scope creep）？prd 描述的功能是否有遗漏？ |
| tasks → 代码完整 | tasks 的每个子任务是否在 diff 中有对应变更？未完成的 task 是否有明确标注？ |
| TDD 理念 | pre-tests 定义的 test_command 是否能够在实现代码上实际执行？测试是否真正驱动了实现（先写测试再写代码，或测试覆盖了全部实现面）？ |

**失败时必须给出**：
- 哪个改动面没有 pre-tests 覆盖，应该增加什么测试
- 哪些代码偏离了 prd 的设计，正确的实现方向是什么
- 哪个 task 没有对应的代码变更，是遗漏还是不需要

### 第四层：实现 → 测试 — 执行完成度

> pre-tests → 实际执行 → evidence → GREEN

**核心问题**：pre-tests 是否全部执行？执行结果是否真实？tasks 是否全部完成？

| 检查项 | 怎么审 |
|--------|--------|
| tasks 完成 | tasks.md 的每个子任务是否完成？未完成的阻塞在哪里？ |
| 测试全 GREEN | pre-tests 的每条 acceptance 的 status 是否为 passed（或有合理 not_applicable 理由）？有 failed 的必须指回第三层修实现 |
| evidence 真实 | 每条 passed 的 actual_output 是否真实执行结果（不是占位符）？evidence_file 指向的文件是否存在且内容合理？ |
| 不可逾越底线 | 全部 status=pending 或 actual_output="(执行后填写)" → 测试根本没跑。全部 not_applicable 且理由三个字"不适用" → 糊弄。status=pass 但 actual_output 为空 → ghost pass |

**失败时必须给出**：
- 哪个 test 未通过，失败原因是什么
- 哪个 task 未完成，阻塞在哪里
- 哪个 evidence 不真实，应该怎么补充

## 输出格式

```markdown
# PR Review: raw-{key}
- branch: {branch}
- reviewer: {reviewer}
- verdict: pass | fail

## L0：项目意图一致性（先于四层；失败则整体 fail）
- 外部锚点（引用原文）:
  - 设计文档: ...
  - 既有验收测试: ...
  - 门禁源码注释/理由: ...
  - 既有同类实现: ...
- Q1 冲突: pass | fail — ...
- Q2 门禁强度: pass | fail — ...
- Q3 能力降级: pass | fail — ...
- Q4 第二套语义: pass | fail — ...
- Q5 设计漂移: pass | fail — ...
- 门禁改动四段证据（若本轮改了门禁/契约/安全边界）:
  1. 当初为什么这样设计: ...
  2. 现在为什么必须改: ...
  3. 判定: 实现不达标 / 设计错误
  4. 强度不降: ...

## 第一层：Raw → B1（问题到决策）
- status: passed | fail
- 消化评估: brainstorms/candidate 是否忠实消化了 raw issue
- 具体发现: ...
- 问题与修复建议: ...

## 第二层：B1 → B2（candidate → milestone → B2 设计产出）
- status: passed | fail
- 消化评估: candidate 是否正确入队 milestone，B2 brainstorms 是否充分分析，I-* 是否忠实消化 candidate，B2 设计产物是否完整
- 具体发现: ...
- 问题与修复建议: ...

## 第三层：B2 → 实现（TDD 测试驱动）
- status: passed | fail
- 消化评估: 代码是否按 pre-tests 驱动、prd 设计实现
- 具体发现: ...
- 问题与修复建议: ...

## 第四层：实现 → 测试（执行完成度）
- status: passed | fail
- 消化评估: 测试是否全部执行、tasks 是否全部完成
- 具体发现: ...
- 问题与修复建议: ...

## Overall Verdict
- verdict: pass | fail
- summary: 综合评审意见
```

任一层 fail → overall verdict = fail。必须写清楚失败理由和修复建议，不能只说"不达标"。

完成后执行 `a2a-exit --state completed --summary '<verdict-json>' --role reviewer`，把 Overall Verdict 的 JSON 作为 summary。

## 与门禁的分工

| 门禁 | 本审查 |
|------|--------|
| 门禁是否被改动（diff 里有门禁/契约文件吗） | 改动是否正当、强度是否不降（L0.3 四段证据） |
| 既有验收测试是否全绿 | 本轮是否与既有断言的**语义**冲突（L0 Q1） |
| pre-tests.md 文件存在吗 | pre-tests 覆盖了改动面吗 |
| acceptance 字段齐全吗 | acceptance 的设计合理吗 |
| Implementation Decision Note 有 5 字段吗 | 5 字段的内容具体吗 |
| phase_state 合法吗 | phase_state 反映了实际进度吗 |

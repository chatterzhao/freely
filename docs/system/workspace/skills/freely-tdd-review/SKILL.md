---
name: freely-tdd-review
description: IBM 链路逐级审查。从 raw issue 自身质量开始，逐级检查：raw→B1→B2→实现→测试。每级有明确的评审面，不是门禁——查内容质量，不是查文件存在即可。
---

# skill:freely-tdd-review

> 审查不是门禁。门禁问"文件在不在"，审查问"做得好不好"——不是查文件存在即可。
>
> 按 IBM 链路逐级审查。每级有明确的评审面。下层是上层的具体化，可从下层归纳回上层。

## 核心方法

```
raw issue ──→ B1（brainstorms → candidate → I-*）──→ B2（prd/pre-tests/tasks/code-review）──→ 实现代码 ──→ 测试执行
```

审查就是逐级检查：上级在下一级中是否被忠实消化、充分展开、安全实现。

**判断标准**：能从下层归纳回上层 → 消化到位。上层在下层中找不到对应 → 遗漏。下层出现了上层没有的东西 → 偏离。

## 输入

审查者从工位自行读取全部 IBM 产物。

---

## 五层逐级审查

### 第一层：Raw Issue —— 评审面：问题质量

> 涉及文件：`docs/issues/raw-{key}/issue.md`
> 评审 raw issue 本身是否是一个好 issue。不是所有 issue 都值得做。

| 检查项 | 怎么审 |
|--------|--------|
| **fix 类**：问题真实性 | 是否真的有问题？是表面症状还是根因？有没有其他类似 raw issue 可以合并处理？有没有关联问题需要一起考虑？ |
| **feature/重构类**：价值与时机 | 当前阶段是否值得投入？是否有类似 raw issue 需要合并？是否需要延期到后续里程碑？是否缺少潜在需求支撑？ |
| 时效性 | 提出时间？是否已被其他 issue/candidate 覆盖？是否仍然相关？ |

**失败时必须给出**：
- 如果是 fix：问题不真实/是表面症状/应合并到哪个已有 issue
- 如果是 feature：现阶段价值不足/应延期/缺少的需求支撑是什么
- 建议：继续推进 / 合并到 X / 延期 / 补充需求后重新提交

### 第二层：Raw → B1 —— 评审面：质量 + 完整度 + 安全

> 链路：`raw issue` → `brainstorms.md` → `candidates.md` → milestones.md → `I-* issue`
> 涉及文件：`docs/issues/raw-{key}/issue.md`、`docs/pre-brainstorms/{key}--{slug}/brainstorms.md`、`docs/pre-brainstorms/{key}--{slug}/candidates.md`、`docs/milestones.md`、`docs/issues/I-{key}-A/issue.md`
> 这是最关键的预研层。brainstorms 必须真正理解问题并产出最佳方案。

#### 质量

| 检查项 | 怎么审 |
|--------|--------|
| 理解到位 | brainstorms 是否真正理解了 raw issue 的 fix 点或 feature 需求？不是在表面复述问题，而是深入分析根因和影响面？ |
| 方案最优 | 是否结合项目实际情况（CONSTITUTION、LAWS、现有架构）做了真正的头脑风暴？Option A/B/C 是实质不同的方案还是走过场？收敛理由是否充分？ |
| candidate 结晶 | candidate 的 acceptance_criteria 是否准确反映了 brainstorms 的决策？promotion_gate 是否可验证？ |

#### 完整度

| 检查项 | 怎么审 |
|--------|--------|
| 横向覆盖 | 为了解决这个问题，周边还有哪些必须一起解决的？brainstorms 是否识别了依赖和边界？ |
| scope 拆分 | raw 覆盖多个独立模块时，brainstorms 是否拆分为多个 candidate？一个 candidate 能否完整解决一个问题（不太大、不太细）？ |
| 不留尾巴 | 方案完成后是否还有遗留问题？遗留问题是否有明确的后续 candidate 或 revisit_trigger？ |

#### 安全

| 检查项 | 怎么审 |
|--------|--------|
| 安全隐患 | 从软件安全角度审视：brainstorms 提出的方案实现后是否会引入安全隐患？如权限旁路、数据泄露、注入风险、状态竞态？ |
| 架构风险 | 方案是否会破坏现有架构边界？是否引入了不可逆的耦合？是否绕过保护分支约束？ |

**失败时必须给出**：
- 质量：brainstorms 哪里是走过场、应该怎样深入分析；candidate 哪里曲解了决策
- 完整度：遗漏了哪些周边问题；scope 为什么不合理、应该拆成几个
- 安全：哪个方案引入了什么安全隐患、建议如何规避

### 第三层：B1 → B2 —— 评审面：设计质量

> 链路：`I-* issue` → `b-I-*.md` → `prd.md` / `pre-tests.md` / `tasks.md` / `code-reviews/` + milestones.md
> 涉及文件：`docs/issues/I-{key}-A/issue.md`、`docs/epics/{epic}/brainstorms/b-I-{key}-A.md`、`docs/epics/{epic}/prd.md`、`docs/epics/{epic}/verification/pre-tests.md`、`docs/epics/{epic}/tasks.md`、`docs/epics/{epic}/code-reviews/implementation-decision-note.md`、`docs/milestones.md`
> B2 将 B1 的决策展开为具体可执行的设计文档。

| 检查项 | 怎么审 |
|--------|--------|
| I-* 忠实 | I-* 是否完整承载了 candidate 的意图和验收标准？ |
| B2 brainstorms | 每个 I-* 是否有对应 b-I-*.md？是否分析了实现面？是否评估了替代实现方案？ |
| prd 可执行 | 从 prd 能否看出"具体要做什么"？模块划分是否从 b-I-*.md 自然推导？ |
| pre-tests 覆盖 | 每条 acceptance 是否可追溯到 prd 的模块？test_command 真实可执行？覆盖层级匹配改动范围？覆盖率达标？ |
| tasks 对齐 | 任务分解是否对应 prd 模块？是否可从 tasks 回溯到 b-I-*.md 的实现顺序？ |
| code-review | Implementation Decision Note 的 5 字段是否反映了真实的设计权衡？ |

**失败时必须给出**：哪个产物缺失/不对齐，应该怎么补，建议内容是什么。

### 第四层：B2 → 实现 —— 评审面：实现 fidelity + TDD 覆盖率

> 链路：`prd.md` / `pre-tests.md` / `tasks.md` → 实际代码（`git diff develop..HEAD`） + `docs/progress/{epic}/p-{issue}.md`
> 涉及文件：以上 B2 产物 + `git diff` + progress 文档

| 检查项 | 怎么审 |
|--------|--------|
| pre-tests ↔ 代码双向覆盖 | diff 的每个改动是否在 pre-tests 中有对应验证？每条 acceptance 是否在代码中有对应实现？覆盖率是否达标（不是"有一个测试"，而是改动面被充分覆盖）？ |
| prd → 代码忠实 | 实现了 prd 描述的每个模块吗？有没有 scope creep（实现了 prd 没写的功能）？有没有遗漏？ |
| tasks → 代码完整 | 每个 task 在 diff 中有对应变更吗？未完成的 task 有标注吗？ |

**失败时必须给出**：哪个改动面缺测试、哪个模块偏离设计、哪个 task 遗漏。

### 第五层：实现 → 测试 —— 评审面：执行完成度

> 链路：`pre-tests.md` → 实际执行 → `evidence_file` → GREEN + `tasks.md` 收尾
> 涉及文件：`docs/epics/{epic}/verification/pre-tests.md`、evidence 文件、`docs/epics/{epic}/tasks.md`

| 检查项 | 怎么审 |
|--------|--------|
| 测试全 GREEN | 每条 acceptance 的 status 是 passed（或合理 not_applicable）还是 pending/failed？ |
| evidence 真实 | actual_output 是真实执行结果还是占位符？evidence_file 指向的文件存在且内容可信？ |
| tasks 收尾 | tasks.md 的每个子任务都有对应产出吗？ |
| **不可逾越底线** | 全部 pending/green → 测试没跑。全部 not_applicable 且理由三字"不适用" → 糊弄。pass 但 actual_output 为空 → ghost pass |

**失败时必须给出**：哪个 test 未通过及原因、哪个 task 未完成及阻塞、哪个 evidence 不真实及怎么补。

---

## 输出格式

```markdown
# PR Review: raw-{key}
- branch: {branch}
- reviewer: {reviewer}
- verdict: pass | fail

## 第一层：Raw Issue（问题质量）
- status: pass | fail
- 评审面: 质量
- 具体发现: ...
- 问题与修复建议: ...

## 第二层：Raw → B1（质量 + 完整度 + 安全）
- status: pass | fail
- 质量: ...
- 完整度: ...
- 安全: ...
- 具体发现: ...
- 问题与修复建议: ...

## 第三层：B1 → B2（设计质量）
- status: pass | fail
- 具体发现: ...
- 问题与修复建议: ...

## 第四层：B2 → 实现（实现 fidelity + TDD 覆盖率）
- status: pass | fail
- 具体发现: ...
- 问题与修复建议: ...

## 第五层：实现 → 测试（执行完成度）
- status: pass | fail
- 具体发现: ...
- 问题与修复建议: ...

## Overall Verdict
- verdict: pass | fail
- summary: 综合评审意见
```

任一层 fail → overall verdict = fail。必须写清楚失败理由和修复建议，不能只说"不达标"。

---

## 与门禁的分工

| 门禁 | 本审查 |
|------|--------|
| pre-tests.md 文件存在吗 | pre-tests 覆盖了改动面吗 |
| acceptance 字段齐全吗 | acceptance 的设计合理吗 |
| Implementation Decision Note 有 5 字段吗 | 5 字段的内容具体吗 |
| phase_state 合法吗 | phase_state 反映了实际进度吗 |

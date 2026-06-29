---
name: freely-workflow-guarded-execution
description: bug 修复的完整开发流程——freely feedback → freely wt-create → freely-doc-B1_IBM-execution → freely-doc-B2_IBM-execution → freely-test-RED-execution → freely-dev-loop-execution → freely-test-execution → freely pr-create-guarded → freely pr-merge-guarded → freely wt-close。与 freely-workflow-guarded-execution 一致。
---

# skill:freely-workflow-guarded-execution

> 全链路: [cmd] freely feedback → [skill] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close

## 定位

**fix skill 是 bug 修复的完整开发流程抽象。** 与 `freely-workflow-guarded-execution`（新功能/大型改动）同级，流程顺序、B1/B2 深度、门禁要求完全一致。

fix 和 feature 的唯一差异：

| 维度 | fix | feature |
|------|-----|---------|
| 分支前缀 | `fix/*` / `hotfix/*` | `feature/*` |
| hotfix 路径 | 合并到 main + develop | 无 |

## 与 freely-workflow-guarded-execution 的分工

| | freely-workflow-guarded-execution | freely-workflow-guarded-execution |
|---|---|---|
| 适用 | bug fix、小改动 | 新功能、大型重构 |
| 流程 | feedback → wt-create → B1 → B2 → dev → test → pr | feedback → wt-create → B1 → B2 → dev → test → pr |
| IBM 顺序 | 治理后实现（Govern first, code later） | 治理后实现（Govern first, code later） |

## 核心原则

> **Govern first, code later.** 先想清楚再动手，与 feature 一致的治理标准。

- 不在 `main`/`develop` 上直接改代码（阻塞其他 AI 并发）
- B1 阶段分析根因、评估修复方案，不修表面症状
- B2 阶段写 pre-tests（复现+验证），让 TDD 驱动实现
- dev 阶段在 fix 工位实现，test-pre-merge 验证
- test-pre-merge 是纯验证沙箱，不参与合并链

---

## 分支规范速查（全部已有，不发明新名）

| 分支 | 可写 | 可提交 | 用途 |
|---|---|---|---|
| `main` | ❌ | ❌ | 发布目标 |
| `develop` | ❌ | ❌ | 集成目标 |
| `test-pre-merge-*` | ❌ | ❌ | 预集成验证批次 / 丢弃式测试沙箱 |
| `fix/*` | ✅ | ✅ | bug 修复专用 |
| `feature/*` | ✅ | ✅ | 功能开发 |
| `fix/premerge-*` | ✅ | ✅ | 冲突收敛 |
| `hotfix/*` | ✅ | ✅ | 紧急 fix，可直达 develop |

合并路径（来自 pr-merge-guarded）:
```
fix/*             → develop (pr-merge-guarded)
hotfix/*          → main + develop (pr-merge-guarded)
```

### 分支 base 差异

| 分支类型 | 默认 base | 说明 |
|---|---|---|
| `fix/*` | develop | bug 修复，从 develop 派生，通过 pr-merge-guarded 合并回 develop |
| `hotfix/*` | main | 紧急修复，从 main 的标签派生，通过 pr-merge-guarded 合并回 main 和 develop |

---

## 适用场景

### 先判：原 feature worktree 还在不在

| 原 feature 工位 | 做法 |
|---|---|
| **还在** | 直接在 feature 上做 B1→B2→dev→test。走 feature → pr-create → pr-review → pr-merge develop |
| **已退役（已合并/已删）** | wt-create 创建 fix 工位 + test-pre-merge → B1→B2→dev→test → pr |

### 再判严重程度

| 类型 | 分支 | 合并路径 |
|---|---|---|
| 普通 fix | `fix/raw-{raw-key}-{slug}` | fix → pr-create → pr-review → pr-merge develop |
| 紧急 hotfix | `hotfix/<desc>-<YYYYMMDD>` | hotfix → B1→B2→dev→test→pr → pr-merge-guarded main + develop |

---

## 工作流

### 前置：审视 issue 价值与时效性

进入任何场景前，先审视 raw issue 是否过时、是否仍有价值、是否已被其他变更覆盖。若已无价值，不执行 fix 流程，写交接回主管说明理由。

### 阶段 1：B1_IBM 预研（根因分析 + 修复方案）

```
1. skill:freely-doc-B1_IBM-execution
   → 读取 raw issue，分析根因
   → 评估修复方案，充分发散后收敛
   → 写 docs/pre-brainstorms/{key}--{slug}/brainstorms.md
   → 写 candidates.md，promote 或 absorb
   → 更新 milestones.md candidate_issues
2. candidate 决策：promote → 进入 B2_IBM
```

### 阶段 2：B2_IBM（修复设计 + pre-tests）

```
1. skill:freely-doc-B2_IBM-execution
   → materialize I-* issue
   → 写 pre-tests.md（覆盖全部改动面的测试方案，端到端优先）
     · 每条 acceptance item: red-green-status = pending
     · 写清楚 RED 阶段如何复现 bug（已有测试/新测试/手工端到端步骤）
   → 写 tasks.md
   → 写 code-reviews/implementation-decision-note.md
   → 更新 milestones.md committed_issues
2. issue phase_state = done_b2_ibm → 进入 RED（skill:freely-test-RED-execution）
```

### 阶段 3：RED — 确认 bug 可复现（写代码之前）

**不通过 RED，绝不允许写一行实现代码。**

```
1. 在 fix 工位逐条执行 pre-tests.md 的 test_command
2. fix 的 RED 含义: 确认 bug 真的可复现
   - 已有测试能捕获 bug → 直接跑，确认 FAIL
   - 需要新设计测试 → 先写好测试再跑，确认 FAIL
   - 手工端到端复现 → 记录复现步骤和结果到 actual_RED_output
3. 每条 acceptance item:
   - 真的 FAIL 了 → red-green-status = red，记录 actual_RED_output
   - 意外 PASS 了 → 测试本身有问题，回 B2 修 pre-tests
4. 全部 red（或合理 not_applicable）→ 进入 dev
```

### 阶段 4：Dev 实现（修复 bug）

```
1. skill:freely-dev-loop-execution
   → 在 fix 工位中实现修复
   → 不碰 pre-tests.md 的测试方案（测试先行，代码后行）
   → 更新 phase_state → in_dev
```

### 阶段 5：test-GREEN — 测试工位 GREEN 验证

```
1. skill:freely-test-execution
   → 在 test-pre-merge 工位执行
   → 运行前确认: test 工位包含全部 dev 最新提交（cherry-pick 同步，不能落后）

2. GREEN 判定（每条 acceptance item 必须同时满足）:
   - red-green-status = green（RED→dev→GREEN 循环完成）
   - status = passed（测试已执行）
   - actual_output 已填写且不是占位符
   - actual_output 与 expected_output 一致

3. 结果:
   - 全部 green → 开发与测试工位一致，进入 pr-create
   - 有任何不 green → 回阶段 4 修复 → git commit → cherry-pick 到 test 工位 → 重跑全量测试

4. 最终状态: 开发工位 ≡ 测试工位（commit 完全一致），全部 green
```

### 阶段 6：pr-create-guarded 提 PR

```
1. 在 fix worktree 中执行 ./bin/pr-create-guarded
2. 自动完成：pull develop → 冲突处理 → dry-run gate → push → platform-adapter
3. 禁止用 gh pr create 替代
```

### 阶段 7：pr-review-guarded 独立 review

```
1. ./bin/pr-review-guarded fix/<branch>
2. 6 维 review → verdict 文档
```

### 阶段 8：pr-merge-guarded 门禁合并

```
1. 切换到 develop 分支: git checkout develop
2. ./bin/pr-merge-guarded develop fix/<branch>
3. PR gate → promotion gate → merge → develop-push → platform-adapter close
```

### 阶段 9：wt-close 收口

```
1. ./bin/wt-close test-pre-merge-<key>-<slug>  # 先关测试工位
2. ./bin/wt-close fix/<branch>                  # 再关开发工位
```

---

## 硬性规则

- **流程顺序不可变**。B1 → B2 → dev → test → pr，与 feature 一致。
- **不发明新分支名**。只用 `fix/*`、`feature/*`、`hotfix/*`、`test-pre-merge-*`。
- **test-pre-merge-* 是纯验证沙箱**，禁止在上面直接开发。代码在 fix 工位写，cherry-pick 到 test 工位验证。
- **B1 必须有根因分析**，不修表面症状。
- **B2 必须有 pre-tests**，复现 bug 的 RED + 验证修复的 GREEN。
- **原 feature 还在就直接在上面修**，不新建工位。
- `freely pr-create-guarded` 和 `freely pr-merge-guarded` 是提 PR 和合并的唯一合法入口。
- `freely pr-merge-guarded` 必须在 develop 分支执行。
- **禁止用原子命令绕过**：gh pr create、gh pr merge --admin、git push --force、git merge。

## 门禁常见坑速查

> 本表为 fix-execution 特有场景。完整 IBM 治理坑速查见:
> - `skill:freely-doc-B1_IBM-execution` §门禁常见坑速查 (candidate/source_candidate/milestone)
> - `skill:freely-doc-B2_IBM-execution` §门禁常见坑速查 (I-* issue/verification/code-review)

| 失败 | 修复 |
|---|---|
| `decision` missing | 用 `## Implementation Decision Note` section |
| `promoted_issue_path` missing | candidate 显式声明 |
| `docs/epics/**/issues/I-*` missing | 创建 kind: linked 入口 |
| milestone 无条目 | 添加到 committed_issues |
| raw issue key 不匹配 | 目录名对齐 candidate date-time key |
| `owner issue 'missing'` | code-review 用 `issue_id` / `issue_path` |
| `verification_artifact_dir` missing | issue 添加此字段 |
| B1 brainstorms 缺失 | 必须写完整的根因分析和修复方案评估，与 feature 要求一致 |
| B2 pre-tests 缺失 | 必须有覆盖全部改动面的 pre-tests，与 feature 要求一致 |

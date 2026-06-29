---
name: freely-feature-execution
description: 新功能/大型改动的完整开发流程——feedback→wt-create→B1→B2→dev→test→pr-create→pr-merge→wt-close，与 freely-fix-execution 同级抽象。
---

# skill:freely-feature-execution

> 全链路: feedback → [命令] wt-create → [skill] skill:freely-doc-B1_IBM-execution → [skill] skill:freely-doc-B2_IBM-execution → skill:freely-test-RED-execution(确认功能未实现) → dev(实现) → GREEN(功能已实现) → [skill] skill:freely-test-execution(test-pre-merge) → [命令] pr-create-guarded → [命令] pr-review-guarded → [命令] pr-merge-guarded → [命令] wt-close
>                                                              [本 skill 自此开始 — B1→B2→dev→test→pr→merge→close 完整抽象]

## 定位

**feat skill 是新功能/大型改动的完整开发流程抽象。** 与 `freely-fix-execution`（快速修 bug）同级，覆盖从 raw issue 到 develop merge 的全链路。

## 与 freely-fix-execution 的分工

| | freely-fix-execution | freely-feature-execution |
|---|---|---|
| 适用 | bug fix、小改动 | 新功能、大型重构 |
| 流程 | feedback → wt-create → B1 → B2 → dev → test → pr-create → pr-review → pr-merge → wt-close | feedback → wt-create → B1 → B2 → dev → test → pr-create → pr-review → pr-merge → wt-close |
| IBM 顺序 | 治理后实现（Govern first, code later） | 治理后实现（Govern first, code later） |

## 下层 skill

freely-feature-execution 在不同阶段调用下层 skill：

1. `skill:freely-doc-B1_IBM-execution` — B1_IBM：raw issue → brainstorms.md → candidates.md
2. `skill:freely-doc-B2_IBM-execution` — B2_IBM：candidate → materialize I-* issue → milestone → ready for dev
3. `skill:freely-dev-loop-execution` — dev-loop：实现 + pre-tests + code-review + progress 回写

## 核心原则

- B1_IBM 预研阶段就写治理文档（brainstorms.md + candidates.md）
- B2_IBM materialize 后才能开始写代码
- dev-loop 产出 pre-tests + code-review 证据
- 合并走 feature → [skill] test-execution → [命令] pr-create → [命令] pr-review → [命令] pr-merge develop 完整链路
- 不跳过门禁

## 工作流

### 阶段 1：B1_IBM 预研
```
1. 创建工位:
   ./bin/wt-create --raw-key <key> --source <source> \
     --skill docs/system/workspace/skills/freely-feature-execution/SKILL.md \
     --slug <slug>

   自动创建:
   ├─ feature/raw-{raw-key}-{slug}     (基于 develop，永久开发工位)
   └─ test-pre-merge-{raw-key}-{slug}  (基于 feature，丢弃式测试沙箱)

2. skill:freely-doc-B1_IBM-execution
   → 写 docs/pre-brainstorms/{key}--{slug}/brainstorms.md
   → 写 candidates.md，每个 candidate 标注 promote/absorb/drop
   → 更新 INDEX.md
   → 更新 milestones.md candidate_issues
3. candidate 决策：promote → 进入 B2_IBM
```

### 阶段 2：B2_IBM
```
1. skill:freely-doc-B2_IBM-execution
   → materialize I-* issue
   → 写 docs/epics/{epic}/{story}/raw-{raw-key}/issues/I-{raw-key}-{suffix}.md
   → 写 prd.md / tasks.md / pre-tests.md
   → 更新 progress
   → 更新 milestones.md committed_issues
2. issue phase_state = done_b2_ibm → 进入 RED（skill:freely-test-RED-execution）
```

### 阶段 3：RED — 确认功能未实现（写代码之前）

**不通过 RED，绝不允许写一行实现代码。**

```
1. 在 feature 工位逐条执行 pre-tests.md 的 test_command
2. feature 的 RED 含义: 确认功能真的还未实现
   - 按重要度设计测试: 端到端（必须）→ 集成 → 单元
   - 每个测试在未实现时必须 FAIL
3. 每条 acceptance item:
   - 真的 FAIL 了 → red-green-status = red，记录 actual_RED_output
   - 意外 PASS 了 → 测试本身有问题（测的不是新功能/测试太弱），回 B2 修 pre-tests
4. 全部 red（或合理 not_applicable）→ 进入 dev
```

### 阶段 4：Dev 实现

```
1. skill:freely-dev-loop-execution
   → 在 feature worktree 实现
   → 不碰 pre-tests.md 的测试方案（测试先行，代码后行）
   → 写 code-review（含 Implementation Decision Note）
   → 更新 progress phase_state → in_dev
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
   - 全部 green → phase_state → in_verification，进入 pr-create
   - 有任何不 green → 回阶段 4 修复 → git commit → cherry-pick 到 test 工位 → 重跑全量测试

4. 最终状态: 开发工位 ≡ 测试工位（commit 完全一致），全部 green
```

### 阶段 6：pr-create-guarded 提 PR
阶段 6.5：pr-review-guarded 独立 review
```
1. 在 feature worktree 运行 dry-run 门禁检查
2. 运行 `freely pr-create-guarded` 命令
3. PR 审查通过后进入门禁合并
```

### 阶段 7：`freely pr-merge-guarded` 命令门禁合并
```
1. 切换到 develop 分支，运行 `freely pr-merge-guarded develop <pr-branch>` 命令（必须在 develop 分支执行）
2. PR gate 检查
3. promotion gate 检查
4. pr-merge-guarded develop <pr-branch> → develop-push
5. issue-sync close
```

### 阶段 8：`freely wt-close` 命令收口
```
1. 更新 issue phase_state → completed
2. 更新 milestones.md
3. raw issue → absorbed/dropped
4. freely wt-close <branch>
```

## Gate 处理

- 合并前必须运行 `./bin/governance-merge-gate --range "develop..HEAD"`
- `--range` 只检查本分支的变更，不受 develop 预存错误干扰
- 分支自己的 gate 错误：用对应 skill 修复
- 预存错误（非本分支引入）：报告但不阻塞
- gate 失败 ≥3 次：回传 `worker_blocked` + 具体的 gate 输出

## 硬性规则

- 不要跳过 feedback→wt-create→B1→B2→dev→test→pr-create→pr-review→pr-merge→wt-close 任一阶段
- 不要在 develop 上直接开发
- 分支名必须以 `feature/` 为前缀，工位名必须包含 `feature`
- feature worktree 必须用 ./bin/wt-create 创建
- 门禁必须过，不过就修，不绕过
- `freely pr-create-guarded` 命令和 `freely pr-merge-guarded` 命令是提 PR 和合并的唯一合法入口。禁止用 gh pr create、gh pr merge --admin、git push --force、git merge 等原子命令替代

---
name: freely-feat-execution
description: 新功能/大型改动的完整开发流程——feedback→wt-create→B1_IBM预研→B2_IBM→dev实现→test-pre-merge验证→pr-create-guarded→pr-merge-guarded门禁合并→wt-close，与 freely-fix-execution 同级抽象。
---

# skill:freely-feat-execution

> 全链路: feedback → [命令] wt-create → [skill] skill:freely-doc-B1_IBM-execution → [skill] skill:freely-doc-B2_IBM-execution → dev(RED-GREEN) → [skill] skill:freely-test-execution(全绿) → [命令] pr-create-guarded → [命令] pr-review-guarded → [命令] pr-merge-guarded → [命令] wt-close
>                                                              ↑ 本 skill 自此开始（提供 B1→B2→dev→test→pr→merge→close 完整抽象）

## 定位

**feat skill 是新功能/大型改动的完整开发流程抽象。** 与 `freely-fix-execution`（快速修 bug）同级，覆盖从 raw issue 到 develop merge 的全链路。

## 与 freely-fix-execution 的分工

| | freely-fix-execution | freely-feat-execution |
|---|---|---|
| 适用 | bug fix、小改动 | 新功能、大型重构 |
| 流程 | wt-create → 实现 → B1_IBM → B2_IBM → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close | wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close |
| IBM 顺序 | 实现后治理（Fix first, govern later） | 治理后实现（Govern first, code later） |

## 下层 skill

freely-feat-execution 在不同阶段调用下层 skill：

1. `skill:freely-doc-B1_IBM-execution` — B1_IBM：raw issue → brainstorms.md → candidates.md
2. `skill:freely-doc-B2_IBM-execution` — B2_IBM：candidate → materialize I-* issue → milestone → ready for dev
3. `skill:freely-dev-loop-execution` — dev-loop：实现 + pre-tests + code-review + progress 回写

## 核心原则

- B1_IBM 预研阶段就写治理文档（brainstorms.md + candidates.md）
- B2_IBM materialize 后才能开始写代码
- dev-loop 产出 pre-tests + code-review 证据
- 合并走 feature → test-pre-merge → pr-create-guarded → pr-review-guarded → pr-merge-guarded develop 完整链路
- 不跳过门禁

## 工作流

### 阶段 1：B1_IBM 预研
```
1. 创建工位:
   ./bin/wt-create --raw-key <key> --source <source> \
     --skill docs/system/workspace/skills/freely-feat-execution/SKILL.md \
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
   → 写 docs/epics/{epic}/issues/I-{key}.md
   → 写 prd.md / tasks.md / pre-tests.md
   → 更新 progress
   → 更新 milestones.md committed_issues
2. issue phase_state = done_b2_ibm → 进入 dev
```

### 阶段 3：Dev 实现
```
1. skill:freely-dev-loop-execution
   → 在 feature worktree 实现
   → 写 pre-tests 并运行
   → 写 code-review（含 Implementation Decision Note）
   → 更新 progress phase_state → in_dev → in_verification
```

### 阶段 4：test-pre-merge 验证
```
1. dev 合并到 test-pre-merge-{raw-key}-* → 在 test 工位启动项目测试
2. 有问题 → dev(fix|hotfix|feature) 修改 → 合并到 test → 重启测试（反复至达标）
3. phase_state → in_verification
```

### 阶段 5：pr-create-guarded 提 PR
阶段 5.5：pr-review-guarded 独立 review
```
1. 在 feature worktree 运行 dry-run 门禁检查
2. 运行 `freely pr-create-guarded` 命令
3. PR 审查通过后进入门禁合并
```

### 阶段 6：`freely pr-merge-guarded` 命令门禁合并
```
1. 切换到 develop 分支，运行 `freely pr-merge-guarded develop <pr-branch>` 命令（必须在 develop 分支执行）
2. PR gate 检查
3. promotion gate 检查
4. pr-merge-guarded develop <pr-branch> → develop-push
5. issue-sync close
```

### 阶段 7：`freely wt-close` 命令收口
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

- 不要跳过 B1_IBM→B2_IBM→dev→test-pre-merge→pr-create-guarded→pr-merge-guarded→wt-close 任一阶段
- 不要在 develop 上直接开发
- 分支名必须以 `feature/` 为前缀，工位名必须包含 `feature`
- feature worktree 必须用 ./bin/wt-create 创建
- 门禁必须过，不过就修，不绕过
- `freely pr-create-guarded` 命令和 `freely pr-merge-guarded` 命令是提 PR 和合并的唯一合法入口。禁止用 gh pr create、gh pr merge --admin、git push --force、git merge 等原子命令替代

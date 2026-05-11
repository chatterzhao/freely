---
name: feat-execution
description: 新功能/大型改动的完整开发流程——B1_IBM预研→B2_IBM→dev实现→门禁合并，与 fix-execution 同级抽象。
---

# skill:feat-execution

## 定位

**feat skill 是新功能/大型改动的完整开发流程抽象。** 与 `fix-execution`（快速修 bug）同级，覆盖从 raw issue 到 develop merge 的全链路。

## 与 fix-execution 的分工

| | fix-execution | feat-execution |
|---|---|---|
| 适用 | bug fix、小改动 | 新功能、大型重构 |
| 流程 | test-pre-merge 沙箱 → cp → commit | B1_IBM→B2_IBM→dev→merge 完整链路 |
| 治理 | 后置 | 前置（B1_IBM 即开始） |

## 下层 skill

feat-execution 在不同阶段调用下层 skill：

1. `skill:doc-B1_IBM-execution` — B1_IBM：raw issue → brainstorms.md → candidates.md
2. `skill:doc-B2_IBM-execution` — B2_IBM：candidate → materialize I-* issue → milestone → ready for dev
3. `skill:dev-loop-execution` — dev-loop：实现 + pre-tests + code-review + progress 回写

## 核心原则

- B1_IBM 预研阶段就写治理文档（brainstorms.md + candidates.md）
- B2_IBM materialize 后才能开始写代码
- dev-loop 产出 pre-tests + code-review 证据
- 合并走 feature → test-pre-merge → develop 完整链路
- 不跳过门禁

## 工作流

### 阶段 1：B1_IBM 预研
```
1. 创建工位:
   ./bin/wt-create --raw-key <key> --source <source> \
     --skill docs/system/workspace/skills/feat-execution/SKILL.md \
     --slug <slug>

   自动创建:
   ├─ fix/raw-{raw-key}-{slug}         (基于 develop，永久开发工位)
   └─ test-pre-merge-{raw-key}-{slug}  (基于 feature，临时测试工位)

2. skill:doc-B1_IBM-execution
   → 写 docs/pre-brainstorms/{key}--{slug}/brainstorms.md
   → 写 candidates.md，每个 candidate 标注 promote/absorb/drop
   → 更新 INDEX.md
   → 更新 milestones.md candidate_issues
3. candidate 决策：promote → 进入 B2_IBM
```

### 阶段 2：B2_IBM
```
1. skill:doc-B2_IBM-execution
   → materialize I-* issue
   → 写 docs/epics/{epic}/issues/I-{key}.md
   → 写 prd.md / tasks.md / pre-tests.md
   → 更新 progress
   → 更新 milestones.md committed_issues
2. issue phase_state = done_b2_ibm → 进入 dev
```

### 阶段 3：Dev 实现
```
1. skill:dev-loop-execution
   → 在 feature worktree 实现
   → 写 pre-tests 并运行
   → 写 code-review（含 Implementation Decision Note）
   → 更新 progress phase_state → in_dev → in_verification
```

### 阶段 4：门禁合并
```
1. 创建 test-pre-merge-{topic} 工位
2. merge feature → test-pre-merge
3. 运行 pre-tests + governance-merge-gate --range
4. gate 失败 → 修复分支自己的错误 → 重试
5. gate 通过 → merge test-pre-merge → develop (merge-guarded)
6. issue-sync close
```

### 阶段 5：收口
```
1. 更新 issue phase_state → completed
2. 更新 milestones.md
3. 清理 test-pre-merge 工位
4. raw issue → absorbed/dropped
```

## Gate 处理

- 合并前必须运行 `./bin/governance-merge-gate --range "develop..HEAD"`
- `--range` 只检查本分支的变更，不受 develop 预存错误干扰
- 分支自己的 gate 错误：用对应 skill 修复
- 预存错误（非本分支引入）：报告但不阻塞
- gate 失败 ≥3 次：回传 `worker_blocked` + 具体的 gate 输出

## 硬性规则

- 不要跳过 B1_IBM → B2_IBM → dev → merge 任一阶段
- 不要在 develop 上直接开发
- 分支名必须以 `feature/` 为前缀，工位名必须包含 `feature`
- feature worktree 必须用 ./bin/wt-create 创建
- 门禁必须过，不过就修，不绕过

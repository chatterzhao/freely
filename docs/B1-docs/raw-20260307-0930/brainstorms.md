# 研究：问题来源分层、milestone-owned issue 与派生 worktree 治理

## Context

- 日期：2026-03-07 09:30 UTC
- 触发：继续审查 Freely 自举流程时发现，当前文档虽然已经定义 `pre-brainstorm -> milestone -> IBM -> dev-loop` 主链，但“哪些地方会发现问题”“里程碑是否算来源”“progress 跟踪什么”“新 worktree 是否总从 develop 创建”仍不够收敛。
- 额外约束：Freely 自身是 AI 自治系统；如果不把这些判断写成技能步骤，AI 很容易只记住“有 worktree 规则”，却在需要时没有执行。

## 当前问题

1. 问题来源、编排来源、延续来源混在一起写，导致：
   - AI 容易把 `milestones.md` 误认为“原始发现源”
   - AI 容易把 `progress` 当成需求池而不是执行态跟踪
2. `IBM` 中的 `I` 边界不够硬，尚未明确“issue 应来自 milestone 已接纳条目”。
3. 执行环 skill 仍偏“职责说明”，对“遇到这种情况就这样做”的情景步骤不够明确。
4. 当前 worktree 规则默认把 `feature/*` 的创建基线表述为 `develop`，但多 agent 并行时会出现：
   - A worktree 尚未合并到 `develop`
   - A 中发现新的从属问题，需要新建 B worktree
   - 如果 B 仍从 `develop` 拉出，将看不到 A 的未合并上下文

## 分层判断

### 1. 三类来源

1. 原始发现源
   - `docs/PROJECT_INTENT.md`
   - chat / session evidence
   - test 结果
   - code review
   - github issue
   - 治理漂移
   - 运行时故障 / 恢复异常
   处理：先进入 `pre-brainstorm`，产出 candidate，再进入 milestone。

2. 编排来源
   - `docs/milestones.md`
   处理：它不是原始问题发现源，而是候选与 issue 队列的承接入口。
   - `candidate_issues`：不能默认直接执行；要判断是否仍需研究，或可进入 IBM
   - `committed_issues`：可以作为 IBM / dev-loop 的正式入口
   - `completed_issues`：不重复执行，只用于校验、追溯或回归判断

3. 延续来源
   - issue 文档
   - progress 文档
   - recovery 文档
   处理：不是发现新问题，而是恢复或继续已有执行链。

### 2. 环边界

- `pre-brainstorm`：负责把原始问题收敛成 candidate
- `milestone`：负责 candidate / issue 队列与优先级
- `IBM`：只处理 milestone 已接纳 issue 的文档成熟度
- `dev-loop`：只处理 ready issue 的实现与验证
- `progress`：只跟踪 dev-loop 的执行态

### 3. worktree 基线

需要区分两个概念：

- `integration_target`
  - 默认是 `develop`
  - 表示最终要合并/提升到哪里

- `execution_base`
  - 创建新 worktree 时真正使用的基线
  - 可以是 `develop`
  - 也可以是未合并的 `feature/<parent>`

判定：

1. 若新 issue 独立，不依赖未合并父分支改动：
   - `execution_base = develop`
2. 若新 issue 依赖未合并父分支改动：
   - `execution_base = feature/<parent>`
   - 仍保持 `integration_target = develop`
   - 必须显式记录依赖关系，并在提升前 restack / rebase / merge 上游
3. 若新发现的问题实际上仍属于当前 issue 验收范围：
   - 不新建派生 worktree，仍留在原分支处理

## 结论

1. `milestones.md` 应算“编排来源”，不算“原始发现源”。
2. `IBM` 的 `I` 应收紧为 milestone-owned issue。
3. `progress` 只跟踪 dev-loop 的 issue 执行，不承载候选收敛状态。
4. 路由 skill 应改成 scenario-driven：按“遇到什么情况 -> 做什么 -> 产出什么 -> 下一跳是什么”组织。
5. worktree 规则应从“feature 一律从 develop”升级为：
   - 默认从 `develop`
   - 依赖未合并父分支时，允许 derived worktree 从父 feature 创建
   - 必须记录 `execution_base / integration_target / depends_on`

## 推荐落地

1. 更新 `docs/PROJECT_INTENT.md`
   - 明确三类来源
   - 明确 milestone-owned issue 与 progress 边界
2. 更新 `docs/LAWS.md`
   - 把上述边界写成判定规则
3. 重写核心 skills
   - `context-source-skill`
   - `doc-pre-brainstorm-execution`
   - `doc-ibm-execution`
   - `dev-loop-execution`
   - `branch-management`
4. 更新 worktree 引导
   - 提供支持 `--base` 的标准创建入口
   - hook 文案不再把 `develop` 说成唯一合法 feature 基线

# 预研头脑风暴：protected-post-merge-acceptance-route-governance

## 背景

- 本预研保留历史阶段形成的 `pre-test-merge` 表述。
- 当前 canonical 语义一律按 `test-pre-merge-*` 临时测试批次前缀族解释；下文出现的 `pre-test-merge` 不再表示可长期保留的单例分支。

Freely 已经正式允许某些 issue 声明 `post-merge acceptance`，并且刚刚把环境规则收紧为：

- `develop` / `test-pre-merge-*` 都可以作为 protected verification environment
- 验收直接在目标 protected branch 的 canonical worktree 中执行
- 若验收暴露问题，必须回到 feature worktree 或新 feature worktree 修复

但当前治理链还有一个明显缺口：

- hook 能阻止在 `test-pre-merge-*` 上 `commit`
- `wt-add` helper 能阻止在 `test-pre-merge-*` 上 `add`
- 但 Git 没有原生 pre-add hook，raw `git add` 无法被同级拦截
- 旧规则曾允许 `pre-test-merge -> develop`
- 现在已经冻结新规则：`test-pre-merge-*` 只是受保护验证环境 / shadow batch，不应携带需要直接 promote 的独有实现差异

这会让使用者很容易忘记：

1. 在 `test-pre-merge-*` / `develop` 环境里只是测试，不是继续修
2. 测试时若顺手改了东西，即使 commit 被拦，dirty 仍会残留
3. 后续如果 promotion gate 不够硬，仍可能把 protected environment 上的脏状态带进 `develop`

## 为什么现在必须研究

这不是抽象担忧，而是 Freely 自己已经处在这种主环境验收场景里：

- `test-pre-merge-*` 主管位被用来做真实 post-merge acceptance
- `develop` 主管位本身也是真实运行环境
- 某些能力只有在“真实主管环境”里才能验证，例如 manager patrol / handoff / worker launch / recovery

也就是说：

- 不能简单说“都在 feature worktree 里测”
- 也不能因为 protected env 需要测试，就默认允许它成为新的开发工位

## 当前事实

### 已有约束

1. `docs/system/workspace/hooks/pre-commit.sh`
- 明确阻止 `main` / `develop` / `test-pre-merge-*` 上的 commit

2. `docs/system/workspace/scripts/worktree/wt-add`
- 若通过 helper 进入 add 流程，会阻止 `main` / `develop` / `test-pre-merge-*`
- 但这不是 Git 原生 hook，只是“走规范入口时的保护”

3. `docs/system/workspace/scripts/worktree/merge-guarded`
- 现在允许：
  - `feature/* -> test-pre-merge-*`
  - `feature/* -> develop`
- 不允许：
  - `test-pre-merge-* -> develop`
- 但没有额外校验：
  - replay 用 batch manifest 的最小字段
  - 当前批次是否只包含来源 feature 的可追溯合入
  - 是否存在 protected env 上未回流到来源 worktree 的差异

### 已有相邻研究，但不覆盖本题

`20260322-0715--pre-test-merge-post-merge-acceptance-stall`

- 研究的是：主管在 `test-pre-merge-*` 中收到 delegated continuation 后为什么卡住
- 不研究：`post-merge acceptance` 的 hook / promotion / replay / cleanup 路由

## 问题定义

需要一条更完整的治理路线，回答：

> 当某个 issue 必须在 `develop` 或 `test-pre-merge-*` 的真实环境里做 post-merge acceptance 时，如何既允许真实验收，又确保任何修复都回到来源 feature worktree，并且不会让 protected verification environment 本身成为新的实现来源？

## 关键张力

1. `test-pre-merge-*` 是临时集成验证分支
- 现在已确定它是 batch shadow，不承载“只能从它 promote 的独有实现”
- 剩下的问题不是要不要保留 `test-pre-merge-* -> develop`，而是如何定义 replay 批次的可追溯证据

2. `develop` 是真实长期运行环境
- 某些主管位验收只能在 `develop` 里看见
- 但也不能因此允许人在 `develop` 里边测边修

3. Git hook 能力本身有限
- 可以可靠拦 commit
- 不能可靠拦 raw `git add`
- 所以“只靠 add/commit hook”不是完整方案，promotion gate 必须兜底

## 候选设计方向

### 方向 A：保持 `test-pre-merge-* -> develop`，但把 promotion gate 收紧

- `test-pre-merge-*` 允许继续作为临时验证批次入口
- 但在 promote 到 `develop` 之前，必须额外证明：
  - `test-pre-merge-*` worktree clean
  - 没有未回流到来源 feature worktree 的 protected-env dirty residue
  - 当前批次可被解释为“来源 feature 集合 + merge order + acceptance evidence”
- 若不满足，上游不得 promote

说明：该方向已不再采用，保留仅作决策追溯。

### 方向 B：把 `test-pre-merge-*` 定义为纯 shadow batch，不再直接 promote

- `test-pre-merge-*` 只负责组合验证
- 验证通过后，删除当前 `test-pre-merge-*` 批次
- 再按已验证顺序把来源 feature 逐条 replay/merge 到 `develop`
- 优点：更强地保证“实现来源永远是 feature”
- 风险：需要一个可重放、可追溯的 batch manifest，否则容易与真实已验批次漂移

### 当前决议

- 采用方向 B。
- `test-pre-merge-*` 的角色固定为 shadow batch / test-merge 环境。
- 它不会被直接用来合并到 `develop`。
- 若某条线需要先经过 `test-pre-merge-*`，进入 `develop` 的动作必须是 replay 已验证的来源 feature，而不是提升测试批次本身。

### 方向 C：按目标环境区分两类 post-merge acceptance

- `develop-only acceptance`
  - 适合像 Freely 主管位这类只有长期主环境才能看见的行为
  - 更像“feature merge 到 develop 后的 completion verification”
- `test-pre-merge-* batch acceptance`
  - 适合多 feature 组合验证
  - 更像“临时批次集成 gate”
- 两类 acceptance 需要不同的 promote / cleanup policy，而不应共用一句泛化的 `post-merge acceptance`

## 更可能的落点

- `docs/system/workspace/scripts/worktree/merge-guarded`
- `docs/system/workspace/scripts/tests/test-merge-guarded`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/worktree/wt-add`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## 需要冻结的开放问题

1. replay 来源 feature 的 batch manifest 与验证重放证据最小字段是什么？
2. 对 `develop` 上的主环境验收，是否应明确归类为：
- `completion_verification on protected environment`
而不是泛化 `post-merge acceptance`
3. 如果 raw `git add` 无法 hook，最小可靠兜底应该放在哪里：
- merge guard
- cleanup guard
- runtime fleet patrol
- status surface alert
4. 对 Freely 主管位这类主环境验收，最小 machine-readable evidence 应该是什么，才能说明：
- “现在只是验证”
- “发现问题已回流到来源 worktree”
- “protected env 没有残留未归属修改”

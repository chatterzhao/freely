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
- 旧讨论里曾把 `pre-test-merge` 视为只做 shadow/replay 的临时批次
- 但当前 canonical 宪法/法律已经冻结：`develop` 的正常 promote source 就是 `test-pre-merge-*` family，而不是重新回放来源 feature
- 真正仍未冻结的是：当 protected env 测出问题时，如何证明修复已回流到 dedicated feature worktree，且 `test-pre-merge-*` / `develop` 没有留下未归属的实现差异

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

3. `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- 当前 canonical 方向已经收紧为：
  - `feature/* -> test-pre-merge-*`
  - `test-pre-merge-* -> develop`
- `feature/* -> develop` 已不是正常路径
- 但仍没有把下列 acceptance / closeout 语义完整 machine-enforce：
  - 当前批次是否仍是权威 batch，而不是应该 retire/rebuild 的 stale batch
  - protected env 上发现的问题是否已经明确回流到 dedicated feature worktree
  - 当前批次是否还残留未回流、未归属、因此不应继续 promote 的 protected-env 差异

### 已有相邻研究，但不覆盖本题

`20260322-0715--pre-test-merge-post-merge-acceptance-stall`

- 研究的是：主管在 `test-pre-merge-*` 中收到 delegated continuation 后为什么卡住
- 不研究：`post-merge acceptance` 的 hook / promotion / replay / cleanup 路由

## 问题定义

需要一条更完整的治理路线，回答：

> 当某个 issue 必须在 `develop` 或 `test-pre-merge-*` 的真实环境里做 post-merge acceptance 时，如何既允许真实验收，又确保任何修复都回到来源 feature worktree，并且不会让 protected verification environment 本身成为新的实现来源？

## 关键张力

1. `test-pre-merge-*` 是临时集成验证分支
- 现在已确定它是 `develop` 前的 canonical 预集成批次，而不是长期开发父分支
- 剩下的问题不是“要不要允许 `test-pre-merge-* -> develop`”，而是：什么证据能证明这次 promote 仍然只是已验证来源的合法集成结果，而不是 protected env 上新写出来的实现

2. `develop` 是真实长期运行环境
- 某些主管位验收只能在 `develop` 里看见
- 但也不能因此允许人在 `develop` 里边测边修

3. Git hook 能力本身有限
- 可以可靠拦 commit
- 不能可靠拦 raw `git add`
- 所以“只靠 add/commit hook”不是完整方案，promotion gate 必须兜底

## 候选设计方向

### 方向 A：保持 `test-pre-merge-* -> develop`，并把 promotion / cleanup gate 收紧

- `test-pre-merge-*` 允许继续作为临时验证批次入口
- 但在 promote 到 `develop` 之前，必须额外证明：
  - `test-pre-merge-*` worktree clean
  - 没有未回流到来源 feature worktree 的 protected-env dirty residue
  - 当前批次可被解释为“来源 feature 集合 + merge order + acceptance evidence”
- 若不满足，上游不得 promote

### 当前决议

- 当前 canonical 真相采用方向 A，而不是旧的 replay-only 假设。
- `test-pre-merge-*` 是进入 `develop` 的正常 promote family，但它依然只承担临时预集成验证职责。
- 因此本预研的剩余问题不再是“禁止 `test-pre-merge-* -> develop`”，而是补齐：
  - protected acceptance 期间 dirty residue 的发现与阻断
  - 问题回流到 dedicated feature worktree 的 machine-readable evidence
  - stale batch / post-merge followthrough / cleanup closeout 的明确分流

### 方向 C：按目标环境区分两类 post-merge acceptance

- `develop-only acceptance`
  - 适合像 Freely 主管位这类只有长期主环境才能看见的行为
  - 更像“feature merge 到 develop 后的 completion verification”
- `test-pre-merge-* batch acceptance`
  - 适合多 feature 组合验证
  - 更像“临时批次集成 gate”
- 两类 acceptance 需要不同的 promote / cleanup policy，而不应共用一句泛化的 `post-merge acceptance`

## 更可能的落点

- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/worktree/wt-add`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## 需要冻结的开放问题

1. 对 `test-pre-merge-* -> develop` promote，最小 source/acceptance/cleanup evidence 组合是什么，才能证明 protected env 没有偷偷变成新的实现来源？
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

# 预研头脑风暴：develop-push-pending-guard-governance

## 背景

当前仓库已经把 protected branch 的 add/commit/push 边界、`test-pre-merge-*` 的 local-only 语义、以及 `develop` push 前的 merge governance gate 都写成了 canonical rule：

- `docs/CONSTITUTION.md` 明确 `develop` 允许 push，但不允许直接 add/commit
- `docs/system/workspace/hooks/pre-push.sh` 已经拦截 `test-pre-merge-*` push，并在 `develop` push 前执行 `governance-merge-gate`
- `branch-management` skill 已经要求 `post-merge acceptance` 在目标 protected branch 的 canonical worktree 中执行

但当前还缺一条关键治理：

- merge 到 `develop` 之后，如果本地 `develop` 仍然 ahead of `origin/develop`
- 且没有显式记录“为什么暂缓 push”
- Freely 仍可能继续开新 lane、继续做下一个 merge、甚至先 cleanup

这会造成一种新的“假完成”：

- 本地已经 merge
- 生命周期文档可能也被写成 completed
- 但远端 canonical shared truth 还没有吸收

## 已确认事实

### 1. 现有 hook 不会自动 push，也不应该自动 push

`pre-push` hook 只负责阻断非法 push，不负责代替操作者执行 push。

这条边界是合理的：

- push 有网络和远端副作用
- 某些 owner 明确需要 `post-merge acceptance`
- 在 acceptance 还没完成前，不应静默自动把本地 `develop` 推上去

因此，“merge 后自动 push”不该设计成 hook 自动动作。

### 2. 现有治理缺少 `push_pending` 这条显式状态

当前规则强调：

- merge 前测试、评审、progress/recovery、cleanup 留痕
- protected branch canonical worktree 只承担集成与验收

但没有明确机器可判定的状态去表达：

- `develop` 当前 ahead
- 这是正常的 post-merge acceptance 窗口，还是不该继续拖延的 push debt

结果就是：

- 系统能看见 ahead
- 但不能明确判定“现在是否允许继续下一个治理动作”

### 3. “提醒 agent 记得 push”不够，必须有阻断面

如果只把这件事写进 skill 或 agent 提示：

- 对执行者有帮助
- 但不能防止真实遗漏

这次历史悬挂 owner 的问题说明：

- 没有硬状态和主动巡检时，任务很容易在“看起来差不多完成”时被继续向前推进

因此这里需要的不是纯提示，而是：

- 明确 `push_pending` / `push_deferred`
- status/fleet patrol 能主动发现
- promotion/cleanup/new-merge 在无合理 defer 原因时被阻断

## 设计判断

### A. 不做 `post-merge auto push`

原因：

- 它会越过 `post-merge acceptance`
- 它会把网络与远端副作用藏进 hook
- 它不利于显式记录“本轮 merge 后仍需观察”的治理意图

### B. 把“merge 已发生但 push 未发生”建模成治理状态

最小需要区分：

1. `push_pending`
- 本地 `develop` ahead of remote
- 若没有显式 defer reason，就应被视为 standing-source followthrough drift

2. `push_deferred`
- 允许暂缓 push
- 但必须有结构化原因，例如：
  - `post_merge_acceptance`
  - `cleanup_followthrough`
  - `remote_delivery_hold`

### C. 阻断面应先落在主动检查和巡检，而不是先扩 hook

更合理的第一刀：

- status-family 输出显式暴露 `develop ahead`
- manager / fleet patrol 在循环找新任务前扫描：
  - 当前 milestone 阶段任务
  - worktree 脏树
  - progress / recovery
  - protected branch ahead/deferred truth
- 若 `push_pending`，先解释它属于合法 defer window 还是悬空的 followthrough drift，再做下一轮 merge / cleanup / 新 lane

hook 仍然可以补，但第一刀更应该是：

- 把 `push pending` 变成 machine-readable truth
- 让 status / patrol 都能看见

## 候选实现层

### 方案 1：只改 skill / agent 提示

优点：

- 成本低

缺点：

- 不可执行
- 不能防止遗漏

结论：

- 只能作为辅助手段，不能单独承担治理

### 方案 2：只改 hook

优点：

- 本地动作阻断强

缺点：

- hook 只在特定 git 动作发生时触发
- 不能主动发现“merge 后长期未 push”
- 不适合静默自动 push

结论：

- 适合补强，不适合单独承担

### 方案 3：状态真相 + patrol/check + skill/agent 提示

优点：

- 有 machine-readable truth
- 有主动扫描
- 有执行提示
- 不会把 push 副作用自动化

缺点：

- 要同时改 status-family、manager patrol、技能合同

结论：

- 这是最稳的 canonical 方向

## 初步结论

这条能力的正确目标不是“merge 后自动 push”，而是：

- freeze a canonical `develop push pending` governance state
- require explicit defer reason when push is intentionally delayed
- make status / fleet patrol surface the state
- block further promotion / cleanup / new merge when `develop` is ahead without a valid defer reason

## 关联真源

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/hooks/pre-push.sh`
- `docs/system/workspace/skills/branch-management/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/`
- `freely status`
- `freely fleet-status`

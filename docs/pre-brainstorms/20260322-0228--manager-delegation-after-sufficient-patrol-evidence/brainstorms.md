# 头脑风暴：manager-delegation-after-sufficient-patrol-evidence

## 背景

这轮不是静态阅读发现的问题，而是一次真实的 Freely 集成测试：

- 在 `develop` 主管工位启动 `freely start`
- 通过 `freely chat` 给主管下达“检查剩余 feature worktree，按三层 loop 与 worktree 治理继续推进并收口”的任务
- 主管已经成功做到：
  - 接住 chat signal
  - 正确 triage 到 `manager continuation`
  - 形成项目级 patrol judgment
  - 并行委派 subagent 审计不同 worktree
  - 写出新的 manager continuity

但随后又暴露出新的断点：

- 在证据已经足够支持具体执行顺序时，主管没有及时进入明确的 worker delegation / cleanup execution
- 而是继续停留在更多只读核对、继续 patrol、继续补充证据
- 结果是：
  - `cli-first` 明明已经 `retire-only`
  - `manager-handoff-consumption-reentry` 明明已经 `retire-now`
  - `three-loop` 明明已经 `continue-dev`
  - 主管仍未把这些判断转成真正的下一跳 worker handoff

## 观察到的真实症状

### 1. 主管 patrol 能力已经显著进步

真实运行中已经出现：

- `manager-continuity-20260322-015940.md`
- `feature/cli-first-observability-surfaces-20260322 -> retire-only`
- `feature/three-loop-dev-loop-ai-native-definition-20260321 -> continue-dev`
- `feature/manager-handoff-consumption-reentry-20260322 -> retire-now`

而且这一轮不是单线程拍脑袋：

- 主管读了 `worktree-maintenance-governance`
- 并行拉起 subagent 审计两个 feature worktree
- 发现并纠正了 `fleet-status` 少报 worktree 的 control-plane 漂移

说明：

- `auto-loop` 的 `patrol-driven` 能力已基本成立
- `manager` 的 worktree disposition 判断能力已具备

### 2. 主管没有及时切换到“执行排班”

在以下条件都已经成立后：

- `cli-first` 的 issue / progress / verification 已是 `completed`
- `cli-first` 分支已被 `develop` 吸收
- `manager-handoff-consumption-reentry` 分支相对 `develop` 为 `0/0`
- `three-loop` 的继续方向也已足够明确：`verification -> dev continuation`

主管仍然：

- 继续读取更多 issue / progress / review 文件
- 继续补更多佐证
- 继续生成新的 investigation text

而不是尽快转成：

1. cleanup worker for `cli-first`
2. cleanup/control follow-up for `manager-handoff-consumption-reentry`
3. continue-dev worker for `three-loop`

## 本质问题

问题不是“主管不会巡检”，而是：

**主管缺少一个明确的 `sufficient evidence -> stop patrolling -> delegate execution` gate。**

也就是说，当前 truth sources 已经定义了：

- 如何巡检
- 如何判断 disposition
- 如何输出 `ownership + restart_point + next_action`

但还没有把下面这件事收成硬规则：

> 当 disposition 已稳定、验收/治理证据已满足下一跳阈值时，主管必须停止继续补充只读证据，转而产出具体 worker handoff，并优先推动 cleanup / continue-dev 真正开始执行。

## 为什么这是 Freely 能力缺口

如果这条能力缺失，Freely 会出现一种典型退化：

- 能分析
- 能解释
- 能 patrol
- 甚至能写 continuity
- 但始终不切换到具体执行

这会让整个系统停在：

- “不断监督”
- “不断补证据”
- “不断重述判断”

而不是：

- 真正推进生命周期
- 真正收口 worktree
- 真正让 worker 开工

对用户项目来说，这同样是致命问题：

- 主管会越来越像“高质量状态面板”
- 而不是“自治编排器”

## 与已有能力的边界

这条线不应重复这些已完成能力：

- `manager-chat-reentry-and-cleanup-misrouting`
  - 解决的是新 signal 不要误吸到旧 cleanup continuity
- `manager-continuation-handoff-consumption`
  - 解决的是 continuation handoff 的 generated / consumed evidence
- `manager-watchdog-trigger-and-drift-reconcile`
  - 解决的是 patrol-driven + event-driven 监督语义

这次新增的是更后面的门槛：

- 主管已经 patrol 完并拿到了足够证据之后
- 什么时候必须停止只读巡检
- 并开始真正的 worker delegation / cleanup execution

## 应该收敛到哪里

不应新造平行大 skill。

更合理的落点：

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- 必要时补 `multi-worktree-supervision` reference

也就是把这条能力收敛成：

- manager patrol completion gate
- manager delegation threshold
- manager must transition from supervision to concrete worker routing when evidence is sufficient

## 预期结果

当主管完成一次项目级 patrol 后：

- 若仍缺关键事实，继续 patrol 是对的
- 但若 disposition 已足够明确，则必须立即：
  - 形成 worker-specific handoff
  - 指定 `ownership`
  - 指定 `restart_point`
  - 指定 `worktree`
  - 指定 `selected_tool`
  - 指定 `next_action`

并把它推进到真实 worker 执行，而不是继续停留在 manager-only continuity。

## 候选方向

1. 为 manager 增加 `patrol completion gate`
2. 明确定义 `sufficient evidence for delegation`
3. 对 `retire-only / retire-now / continue-dev` 三类 disposition 增加最小 required handoff schema
4. 在真实集成测试中要求：
   - 主管 patrol 完后
   - 必须出现 worker launch intent 或 cleanup followthrough intent
   - 否则视为未完成

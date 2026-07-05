# 预研头脑风暴：插话拓扑、主管路由与三层循环融合

## 背景

- Freely 不是“等人发工单再处理”的系统，而是一个会自己发现需求、问题、异常、缺口，并在三层循环中持续推进的自治系统。
- `human interruption` 只是输入来源之一，不是独立于 Freely 主链之外的特例系统。
- 除了人类插话之外，Freely 还会从测试、review、runtime、里程碑、progress、当前 issue 文档、以及 `PROJECT_INTENT` 本身持续发现问题。
- 当前围绕 interruption 已经落下了若干局部能力：
  - durable intake
  - interruption dispatcher
  - manager-triage handler
  - `chat/tui` 自动 bootstrap
- 但这些能力还没有和 Freely 的完整工作拓扑真正打通，尤其是：
  - 新问题出现后应从哪一层开始
  - 主管何时自己澄清，何时委派
  - doc-loop / dev-loop / verification / review / recovery 之间如何继续流转
  - 工作进行到一半再出现新问题时，应回到哪里重新开始

## 主问题

需要回答的不是“插话如何被存下来”，而是：

1. Freely 的“问题发现”有哪些来源，它们在三层循环中的首跳是什么。
2. 主管在顶层到底管理什么，它做判断时依赖什么。
3. 一个新问题或新缺口出现后，应该从 `pre-brainstorm / candidate / milestone / IBM / progress / review / recovery` 的哪一层重新接入。
4. interruption 如何和测试发现、review 发现、runtime 异常、开发中边界外发现统一到同一个拓扑里。

更上位地说，需要回答：

5. Freely 的问题来源是否应拆成 `event source` 与 `standing source`。
6. 主管是否应成为所有 source 的统一顶层路由者，而不是 interruption 专属路由者。

## 现状判断

### 1. interruption 只是 `source`，不是单独生命周期

`three-loop-capability-lifecycle` 已经给出了对的骨架：

- `human chat intake` 属于 `auto-loop`
- 它的 canonical output 不是“新系统”，而是：
  - intake record
  - reaction decision
  - resolution artifact
  - delegated handoff

也就是说，interruption 的第一层职责是把外部输入变成可恢复、可监督的 source record。

它不应自己决定后面一定进入哪一个固定 loop。

### 2. 真正需要统一的是“问题进入主链的首跳路由”

Freely 当前会自己遇到很多类型的问题：

- 人类插话
- 测试失败
- review 发现
- runtime 异常
- worker 在实现中发现 IBM 文档不足
- worker 在 doc-loop 中发现 milestone / candidate 不足
- verification 中发现需要回退到 dev-loop 或 doc-loop

这些来源看上去不同，但本质上都应回答同一个问题：

> 这件事现在应该从哪里开始重新接入三层循环？

### 3. “从哪里开始”不能被写死成 interruption 规则表

一个新问题的最佳首跳，取决于它当前所处的治理位置，而不是取决于它来自哪一个 channel。

例如：

- 人类插话提出一个全新方向 -> 可能回到 `pre-brainstorm`
- 人类插话要求澄清当前某个进行中的 issue 边界 -> 可能进入当前 `issue/progress/recovery`
- review 发现代码行为错误但 issue 边界没错 -> 可能直接回到 `dev-loop`
- worker 在 dev-loop 中发现缺失验收标准 -> 应回退到 `IBM`
- verification 发现实现其实建立在错误前提上 -> 可能直接回到 `pre-brainstorm` 或 `candidate`

因此，真正该做的不是给 interruption 发明特殊类型，而是让主管掌握“从哪里重新开始”的顶层路由职责。

### 4. source 应拆成 `event` 与 `standing`

这一层是当前 interruption 讨论之上更重要的抽象。

#### `event source`

特点：

- 有明确发生时刻
- 会触发主管及时注意
- 更像“刚刚发生了一件新事”

典型例子：

- human interruption
- test failure
- review finding
- runtime anomaly
- worker 在当前执行中发现边界外问题
- verification failure
- 用户通过 CLI `auto` 参数、TUI、GUI 发出的明确指令

#### `standing source`

特点：

- 不是一次性发生，而是长期存在的事实源
- 需要主管周期性扫描
- Freely 会从中主动发现“现在也该处理的事”

典型例子：

- `PROJECT_INTENT`
- `docs/milestones.md`
- candidates / issue / IBM / progress / recovery
- worktree fleet / branch / runtime state
- 当前 review / verification backlog

#### `standing source` 会派生新的 event-like problem signals

例如：

- 某 milestone candidate 长期未收口
- 某 committed issue 长时间无 progress
- 某 completed issue 对应 worktree 尚未 cleanup
- 某 runtime 长时间不符合期望状态

这说明：

- `milestone` 本身不是 event
- 但对 milestone 的扫描可以产生新事件

因此，Freely 的问题发现主链更像：

```text
event source
or
standing source -> scan -> derived problem signal
-> manager routing
-> restart point
-> delegated loop
```

## Source 生命周期矩阵

### 1. `event source`

#### `human interruption`

- canonical source record:
  - `.freely/intake/**`
- manager activation:
  - 立即，由 interruption dispatcher / manager 看到
- manager first job:
  - notice
  - claim
  - 判断当前上下文与 restart point
- possible restart points:
  - `pre-brainstorm`
  - 当前 `issue/progress/recovery`
  - `IBM`
  - `dev`
  - `review/verification`
  - `runtime supervision/cleanup`
- expected artifact:
  - resolution / handoff
  - 以及后续 canonical artifact

#### `test signal`

- canonical source record:
  - test log / test artifact / verification evidence
- manager activation:
  - test 失败时触发，或 verification scan 时发现
- manager first job:
  - 判断是实现缺陷、验收不足、还是 issue/IBM 边界错误
- possible restart points:
  - `dev`
  - `verification`
  - `IBM`
  - `pre-brainstorm`
- expected artifact:
  - review / verification continuation
  - progress / issue writeback

#### `review finding`

- canonical source record:
  - `docs/epics/**/code-reviews/*.md`
- manager activation:
  - review 完成后或主管扫描 review backlog 时
- manager first job:
  - 判断是局部代码修正、还是文档边界错误、还是上游问题
- possible restart points:
  - `dev`
  - `IBM`
  - `pre-brainstorm`
- expected artifact:
  - code review finding handoff
  - progress / issue / IBM continuation

#### `runtime anomaly`

- canonical source record:
  - `.freely/run/**`
  - continuity / recovery artifacts
- manager activation:
  - runtime signal / watchdog / status drift
- manager first job:
  - 判断 owner：runtime-owned 还是 manager-owned
- possible restart points:
  - `runtime supervision/recovery`
  - `cleanup`
  - 必要时 reroute 到 doc/dev
- expected artifact:
  - recovery target
  - continuity
  - cleanup evidence

#### `worker-discovered gap`

- canonical source record:
  - 当前 issue / progress / recovery continuity
- manager activation:
  - worker handoff / continuation 中显式提出
- manager first job:
  - 判断当前 loop 是否还能继续，还是必须回退
- possible restart points:
  - `IBM`
  - `pre-brainstorm`
  - `candidate/milestone`
  - `dev continuation`
- expected artifact:
  - continuation handoff
  - issue/progress/brainstorm writeback

### 2. `standing source`

#### `PROJECT_INTENT`

- canonical source record:
  - `docs/PROJECT_INTENT.md`
- scan mode:
  - 主管周期扫描
- derived signal examples:
  - 长期能力缺口
  - 明显与 intent 不一致的当前工作
- common restart points:
  - `pre-brainstorm`
  - `candidate/milestone`

#### `milestones / candidate / issue / progress / recovery`

- canonical source record:
  - `docs/milestones.md`
  - `docs/epics/**`
  - `docs/progress/**`
  - `docs/recovery/**`
- scan mode:
  - 主管周期扫描
- derived signal examples:
  - candidate 长期未收口
  - committed issue 长期无进展
  - progress / phase 状态漂移
  - completed issue 未 cleanup
- common restart points:
  - `candidate/milestone`
  - `IBM`
  - `dev`
  - `verification`
  - `cleanup`

#### `fleet / branch / worktree / runtime state`

- canonical source record:
  - worktree snapshot
  - branch/runtime state
  - `.freely/run/**`
- scan mode:
  - 主管周期扫描
- derived signal examples:
  - merged worktree 未清理
  - expected running but down
  - dirty/checkpoint drift
- common restart points:
  - `runtime supervision`
  - `cleanup`
  - `recovery`

## 三层循环中的统一问题拓扑

### A. 发现层：任何来源都先成为 `problem signal`

来源包括：

- `human interruption`
- `test signal`
- `review finding`
- `runtime anomaly`
- `worker-discovered gap`
- `verification failure`
- `PROJECT_INTENT` 推导出的潜在需求
- milestone / progress / recovery / cleanup drift

这一步的目标只有一个：

- 把 signal durable 化，并附着最小上下文

interruption 在这里的特殊性仅仅是：

- 它需要被第一时间 noticed
- 但 noticed 之后，仍然要进入同一套问题路由体系

standing source 在这里的特殊性仅仅是：

- 它不靠外部显式触发
- 而是由主管周期性扫描后自己派生出新的 `problem signal`

### B. 主管层：判断“这件事从哪里重新接入”

主管的顶层职责不是“解释插话”本身，而是：

1. 判断 ownership
2. 判断当前工作上下文
3. 判断这件事应该从哪个治理层重新开始

也就是至少判断：

- 这是 `auto-loop` 的监督/恢复问题？
- 还是 `doc-loop` 的边界/候选/里程碑/IBM 问题？
- 还是 `dev-loop` 的实现/测试/review/verification 问题？

更细一点地说，主管真正应掌握的是下面这些 restart points：

- `pre-brainstorm`
- `candidate / milestone intake`
- `IBM`
- `dev execution`
- `review`
- `verification`
- `progress / recovery continuation`
- `runtime supervision / cleanup`

并且主管还应统一判断：

- 这是 `event source` 直接触发，还是 `standing source` 扫描出来的派生问题
- 这是高优先级抢占问题，还是正常排班问题
- 是否需要先做一段主管自己的澄清
- 还是应立即委派给 specialized analysis / worker

### C. 执行层：委派给对应专门 AI / skill

主管做的是顶层路由和委派，不是所有问题都亲自展开。

一旦首跳确定，后面应进入对应 worker/skill：

- `pre-brainstorm` -> `doc-pre-brainstorm-execution`
- `IBM` -> `doc-ibm-execution`
- `dev execution` -> `dev-loop-execution`
- `review / verification` -> 对应 worker/verification 路径
- `runtime supervision` -> runtime/scripts 或 supervision skills

这里的关键不是“所有事都立刻开 worker”，而是：

- 有些事先进入主管澄清
- 有些事先进入 specialized analysis skill
- 有些事直接进入 doc-loop / dev-loop / verification / recovery worker

但无论哪种，主管都应是统一顶层路由者。

## 当前实现盘点

### 已实现

1. `human interruption` 的最小 event ingestion
- 已实现：
  - durable intake
  - dispatcher
  - triage handler
  - abstract routing contract:
    - `DECISION`
    - `RESTART_POINT`
    - `OWNERSHIP`
    - `WHY/HANDOFF/ANSWER`
  - `chat/tui` auto bootstrap
- 已测：
  - [test-freely-human-chat-intake](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260320-0248-feature-interruption-topology-prebrainstorm/docs/system/workspace/scripts/tests/test-freely-human-chat-intake)
  - [test-freely-chat-and-tui](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260320-0248-feature-interruption-topology-prebrainstorm/docs/system/workspace/scripts/tests/test-freely-chat-and-tui)
  - [test-freely-interruption-direct-answer](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260320-0248-feature-interruption-topology-prebrainstorm/docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer)

2. 第一条完整 event 链：`human interruption -> manager triage -> cleanup followthrough -> writeback`
- 已实现：
  - manager triage 不再输出 `manager_answer_*` 这类硬编码问题类型
  - cleanup 类 signal 可被路由到 `restart_point=cleanup`
  - worker followthrough 会检查 merged feature worktree 是否可安全删除
  - followthrough 会写回 cleanup resolution artifact 与 intake absorption
- 已测：
  - [test-freely-interruption-direct-answer](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260320-0248-feature-interruption-topology-prebrainstorm/docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer)

3. `runtime` / `fleet` / supervision signal 的部分 standing scan
- 已实现：
  - status / PID / hygiene / manager supervision alert 的部分扫描
- 已测：
  - 若干 `test-freely-*manager*`, `test-freely-*hygiene*`, `test-freely-*status*`

4. `doc-loop` / `dev-loop` 的 canonical artifact 主链
- 已实现：
  - `pre-brainstorm`
  - `IBM`
  - `dev-loop`
  - `review`
  - `verification`
  - progress/recovery 写回
- 已测：
  - routing foundation 相关测试和各 runtime/doc/dev 测试

### 未实现或未统一

1. `event source` / `standing source` 的统一 taxonomy
- 当前只是在预研里提出，真源尚未统一改写。

2. `restart point routing` 的统一主管模型
- 当前 interruption 有局部 triage，但 review/test/runtime/intent 还没统一到同一框架。

3. `standing source -> derived signal` 的主动扫描闭环
- 当前只有零散 alert / scan，不是统一问题发现模型。

4. generic delegated followthrough 仍未统一
- 当前已打通：
  - `restart_point=cleanup`
- 仍未统一：
  - `pre-brainstorm / IBM / dev / review / verification / continuation`

## 阶段性里程碑建议

### M1: 真源对齐

- 把 `three-loop-capability-lifecycle`
- `manager-agent`
- `auto-loop-orchestrator`

先统一改成：

- source 分为 `event` / `standing`
- 主管顶层职责是 `restart-point routing`
- 不再把 interruption 写成单独局部协议中心

当前状态：
- 已完成最小真源对齐

### M2: 统一 signal record 与 routing contract

- 定义各类 signal 的 source record
- 定义主管输出结构：
  - `problem_kind`
  - `current_context`
  - `restart_point`
  - `suggested_owner`
  - `handoff_note`

当前状态：
- interruption slice 已完成最小 contract
- 其他 signal source 尚未全部接入

### M3: 先打通一条完整 event 链

- 从 `human interruption`
- 到 `restart point`
- 到真实 delegated loop
- 到 canonical artifact writeback

当前状态：
- 已完成第一条最小链：
  - `human interruption -> cleanup followthrough`

### M4: 打通 standing scan

- `PROJECT_INTENT`
- milestone/progress/recovery/fleet

周期扫描后生成 derived signal，并进入同一 routing contract

## 对 interruption 的重新定位

### 1. interruption 不是“主管直答系统”

主管当然可以根据自身职责选择自己先做澄清或回答。

但那应该来自 AI 的职责判断，而不是 runtime 里的硬编码类型。

因此：

- 可以在 skill / 职责文档里给少量示例
- 不能在 runtime 里做大量 `manager_answer_*` 枚举

更进一步地说：

- 不只是 interruption 不该写死规则表
- 所有 source 都不该在 runtime 层被写死成大量问题类型枚举

### 2. interruption 的核心不在“自己答还是委派”

更核心的是：

- 这条事应从哪里重新开始
- 是否需要 worker
- 需要哪类 worker
- 需要什么 handoff
- 最后回写到哪类 canonical artifact

换句话说，interruption 更像“高优先级外部 source”，而不是“答疑系统”。

而整个 Freely 的更大模型应是：

- `interruption` 只是 `event source` 的一个子类
- 它和 test/review/runtime/worker-gap 一起共享上位问题拓扑

### 3. interrupted work 的处境必须进入判断

插话发生时，系统可能正处于：

- 无 active issue
- `pre-brainstorm`
- `candidate`
- `IBM`
- `in_dev`
- `review`
- `in_verification`
- `runtime recovery`

同一句插话，在不同上下文里，首跳可能不同。

例如“这里文档不够”：

- 若当前在 `IBM`，可能是当前 issue 的 IBM continuation
- 若当前在 `in_dev`，可能需要回退到 IBM
- 若当前根本没有稳定 issue，可能需要新开 pre-brainstorm

所以 interruption triage 不能脱离当前 phase / issue / milestone 状态。

同理：

- test triage 也不能脱离当前 issue / verification 状态
- review triage 也不能脱离当前 dev/review 状态
- runtime triage 也不能脱离当前 expected runtime / manager plan

## 当前文档里的结构性冲突

### 1. manager-agent 仍把 interruption 过多描述成单独固定顺序

现在的 `manager-agent.md` 更像在描述一个局部 interruption protocol，而不是把它纳入主管的总路由职责。

需要改成：

- interruption 只是 signal source
- 主管负责判断 restart point 和 downstream owner
- `human-interruption-handling` 是 specialized analysis skill，而不是 interruption 专属世界

而且 manager-agent 还应显式纳入：

- standing source scanning
- derived signal creation
- signal priority arbitration

### 2. auto-loop-orchestrator 对 interruption 作为局部特殊协议写得过重

这里容易把“示例”误写成“固定运行时分支”。

正确写法应是：

- 允许主管根据职责做必要澄清
- 但不把 interruption 写成独立于其他 signal 的局部硬编码协议

### 3. 当前 interruption 讨论还没和 `PROJECT_INTENT` 主动发现链真正接上

Freely 作为自治开发应用，不仅要响应 signal，还应主动看：

- `PROJECT_INTENT`
- 当前 milestone 空洞
- 长期缺失的 capability
- 当前 loop 中被忽略的问题

这条“standing source -> self-proposed problem”链目前还没有被 interruption 讨论吸收进统一模型。

### 4. 当前 interruption followthrough 还没接到完整后续拓扑

现在最明显的断点是：

- claim/triage 已有
- 但 triage 之后，如何继续 materialize 为
  - pre-brainstorm
  - candidate
  - milestone
  - IBM continuation
  - dev continuation
  - review/verification continuation
  - runtime cleanup/recovery

还没有统一模型。

## 一个更符合 Freely 的上位设计

### 主管的上位职责

主管对任意 signal 都做同一套顶层判断：

1. 这是什么类型的问题。
2. 它当前属于哪一层 loop。
3. 它应该从哪个 restart point 重新进入。
4. 由谁继续处理。
5. 需要什么 handoff 与回写。

主管的两个并行工作面应明确区分：

1. `consume events`
- 及时处理新来的 interruption/test/review/runtime 等事件

2. `scan standing sources`
- 周期性扫描 `PROJECT_INTENT / milestones / progress / recovery / fleet`
- 主动发现尚未被显式提出来的问题

### interruption handler 的职责

它不应只是“判断是否直答”。

更合理的是：

- 读取 raw interruption + 当前项目状态
- 形成一个结构化问题判断：
  - `problem_kind`
  - `current_context`
  - `restart_point`
  - `suggested_owner`
  - `handoff_note`

然后交给主管做最终 accept / schedule。

如果未来扩展到统一 signal handling，则对应也可以有：

- test/review/runtime/standing-scan 的 specialized analysis skill

但这些都应服务同一个上位框架，而不是各自长成一套系统。

### canonical artifacts 的映射

问题一旦确定 restart point，就应进入对应 canonical pool：

- 新模糊问题 -> `docs/B1-docs/raw-**`
- 已有候选提升 -> `docs/milestones.md`
- issue 边界不足 -> `docs/epics/**`
- dev continuation -> `progress` / code / tests
- verification/review -> review / verification artifacts
- runtime supervision -> `.freely/run/**` / continuity / cleanup evidence

对于 standing source 扫描派生出来的问题，也应回写：

- 它来自哪个 standing source
- 为什么现在被提升成 active problem
- 为什么被路由到这个 restart point

## 这份预研的阶段结论

1. interruption 不能单独设计，必须纳入 Freely 的统一问题拓扑。
2. Freely 的问题来源应明确拆成 `event source` 和 `standing source`。
3. 每种 source 都应补齐 source record、manager activation、restart points、expected artifacts 的生命链路描述。
4. standing source 应通过周期性扫描生成新的 problem signal，而不是永远只做静态背景。
5. 主管真正管理的是“问题从哪里重新开始”，而不是只管理“插话怎么分流”。
6. `manager direct answer` 可以作为 AI 的一种判断结果存在，但不能被写成 runtime 硬编码类型。
7. 下一阶段真正需要 materialize 的，不是再补一个 interruption 小能力，而是：
   - `problem restart-point routing`
   - 或更准确地说：
   - `signal -> restart point -> delegated loop` 的统一模型。

## 下一步建议

- 先基于这份预研，单独收敛一个 candidate：
  - 主管对任意 signal 的 `restart point routing`
- 再单独收敛：
  - `event source` / `standing source` taxonomy
  - standing scan 的优先级模型
  - derived signal 的 canonical record
- 再决定 interruption、review、test、runtime anomaly 是否统一接到同一个 specialized analysis skill
- 在这之前，不应继续扩 interruption runtime 的局部规则表

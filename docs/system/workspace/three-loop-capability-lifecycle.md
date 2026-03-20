# Three-Loop Capability Lifecycle

本文件是 Freely 三层循环能力映射与生命周期的唯一细节真源。

作用：
- 统一定义 `auto-loop / doc-loop / dev-loop` 下的能力归宿
- 统一定义能力 owner 边界
- 统一定义从发现到 cleanup 的生命周期与回写落点

不负责：
- 不替代 `CONSTITUTION.md` 的边界原则
- 不替代 `LAWS.md` 的验收与状态词典
- 不替代各个 `SKILL.md` 的执行步骤

使用规则：
- 高层文档只保留摘要并引用本文件
- 具体执行步骤仍回到对应 `skill`
- 若本文件与 `CONSTITUTION.md` / `LAWS.md` 冲突，以后两者为准，并应尽快修正本文件

## 1. Core Model

Freely 的自治开发不是单一 agent，也不是单纯脚本自动化，而是两层自治叠加在三层循环之上：

- `runtime autonomy`
  - 由 `scripts/runtime` 和相关 supervisor/watchdog 实现
  - 负责保活、恢复、切号、等待、重启、会话轮换
- `agent autonomy`
  - 由 `lead-agent`、`manager-agent`、`worker-agent` 和 skills 实现
  - 负责判断、路由、委派、执行、验证、回写

两层自治共同服务三层循环：

```text
auto-loop -> doc-loop -> dev-loop -> verification/completion -> cleanup -> auto-loop
```

## 2. Loop Boundaries

### 2.1 auto-loop

目标：
- 维持项目级自治运行
- 判断当前应该推进什么
- 在中断后恢复到正确上下文

负责：
- 来源扫描与路由
- 多 worktree 监督与排班
- runtime continuity / recovery
- availability / account switching
- watchdog / supervision control plane
- manager/worker handoff
- completion verification routing
- freeze / merge / cleanup decision

不负责：
- 不直接替代 `doc-loop` 做 issue 文档收敛
- 不直接替代 `dev-loop` 做实现和测试
- 不在 protected branch 上写 worker 级产物

### 2.2 doc-loop

目标：
- 把模糊问题收敛成可执行 issue
- 确保文档边界先于实现

负责：
- `pre-brainstorm`
- candidate recording
- milestone intake
- issue materialization
- `IBM + G`
- doc continuity
- 新边界外问题回流到 pre-brainstorm

不负责：
- 不承担 runtime 保活
- 不直接承担代码实现、测试和 promotion

说明：
- `doc-loop` 中的 `IBM + G` 表示 issue-bound 文档收敛与治理资产一致性维护共属同一层，不新增第四层循环。

### 2.3 dev-loop

目标：
- 在已收敛的 issue 边界内完成实现、验证与交付

负责：
- 代码实现
- 测试
- code review
- verification
- progress writeback
- checkpoint / hygiene 收口
- promotion / cleanup readiness

不负责：
- 不重新定义 issue 边界
- 不把边界外问题直接吞进当前实现
- 不承担进程退出后的恢复动作

## 3. Owner Layers

Freely 的能力必须同时标注 loop 和 owner，避免“能力有了，但不知道谁负责”。

### 3.1 runtime/scripts

适用原则：
- AI 不在线也必须发生的动作
- 需要 shell、PID、sleep、重启、切号、进程探活的动作

典型职责：
- start / stop / status
- PID / session 监控
- 崩溃后重启
- availability probing
- account cooldown / switch / sleep-until-reset
- `resume` / `fresh` / `fresh_with_handoff`
- fleet runtime status

### 3.2 manager-agent

适用原则：
- 项目级监督、委派、合并节奏、cleanup 判断

典型职责：
- 读取项目级 worktree 快照
- 判断 `runtime-owned` / `worker-owned` / `manager-owned`
- 决定 delegate / freeze / merge / cleanup
- 在轮换前写项目级 continuity

### 3.3 worker-agent

适用原则：
- 某个 feature worktree 内的 doc-loop / dev-loop / verification 执行

典型职责：
- 执行 pre-brainstorm / IBM / dev-loop
- 回写 issue / milestone / progress / continuity
- 在 checkpoint 边界先收口再继续扩写

### 3.4 skills

适用原则：
- 可复用、可组合、可被 agent 调用的执行能力

典型职责：
- 路由
- pre-brainstorm 执行
- IBM 执行
- dev-loop 执行
- recovery / supervision / hygiene

### 3.5 state artifacts

适用原则：
- 需要长期留痕、被下一轮继续消费的事实状态

典型职责：
- `milestones.md`
- `pre-brainstorms/**`
- `docs/epics/**`
- `docs/progress/**`
- `docs/recovery/**`
- `.freely/intake/**`

## 4. Capability Placement Map

| Capability | Primary loop | Primary owner | Trigger | Main outputs | Canonical artifacts |
| --- | --- | --- | --- | --- | --- |
| source classification | auto-loop | `context-source-skill` | new input / next cycle | `source_class`, `route_kind` | `docs/system/workspace/skills/context-source-skill/**` |
| human chat intake | auto-loop | runtime/scripts + `manager-agent` + `skill:human-interruption-handling` | user interruption / explicit chat intake | intake record, reaction decision, resolution artifact, completion signal | `.freely/intake/**`, `.freely/run/interruption-resolution/**`, manager continuity, delegated worker handoff |
| worktree preparation | auto-loop | `branch-management` + runtime | before write | branch/worktree decision | `docs/system/workspace/skills/branch-management/**` |
| project supervision | auto-loop | `manager-agent` | manager cycle | delegate/freeze/merge/cleanup decision | `docs/system/workspace/agents/manager-agent.md` |
| watchdog / supervision control plane | auto-loop | runtime + manager-agent | expected running but down / hygiene drift / availability loss | recovery or supervision action | `docs/system/workspace/scripts/runtime/**`, relevant supervision skills |
| availability / account switching | auto-loop | runtime/scripts | auth failure / usage limit / probe failure | switch, cooldown, wait, restart | runtime + watchdog availability module |
| runtime continuity | auto-loop | runtime/scripts | session nearing limit / crash / compacted context | `resume` or `fresh_with_handoff` | runtime scripts + handoff artifacts |
| recovery routing | auto-loop | `recovery-subagent-governance` + runtime | unavailable runtime / stale `in_*` state | recovery path and continuity | recovery artifacts |
| pre-brainstorm | doc-loop | `doc-pre-brainstorm-execution` | discovery source or unstable boundary | `brainstorms.md`, `candidates.md` | `docs/pre-brainstorms/**` |
| candidate acceptance review | doc-loop | worker-agent + `skill:candidate-acceptance-review` | candidate preparing promotion or high-risk boundary | independent acceptance review verdict, updated `acceptance_reviews` | `docs/pre-brainstorms/**/candidates.md` |
| milestone intake | doc-loop | `doc-pre-brainstorm-execution` or `doc-ibm-execution` | candidate accepted into active scope | milestone queue update | `docs/milestones.md` |
| IBM + G | doc-loop | `doc-ibm-execution` | milestone-owned issue needs docs | `issue`, `brainstorm`, `prd`, `pre-tests`, `tasks` | `docs/epics/**` |
| doc continuity | doc-loop | worker-agent + current doc skill | warn/rotate/recovery inside doc work | updated issue/brainstorm continuity | current doc artifacts |
| implementation | dev-loop | `dev-loop-execution` | ready issue | code/test changes | `src/**`, tests, issue docs |
| code review | dev-loop | worker-agent | after implementation batch | review findings or pass | `docs/epics/**/code-reviews/*.md` |
| verification | dev-loop | worker-agent + manager decision | after implementation and tests | completion evidence / blockers | issue + milestone + progress/recovery |
| checkpoint / hygiene | dev-loop | worker-agent + hygiene supervision | dirty budget / checkpoint drift | checkpoint commit or hygiene intervention | progress/equivalent continuity |
| promote / cleanup readiness | dev-loop -> auto-loop | manager-agent | verified-retirable state | merge/cleanup decision | milestone + continuity + cleanup evidence |

## 5. Lifecycle Truth

### 5.1 Signal model before routing

Freely 的来源先分成两类：

- `event source`
  - human interruption
  - test failure
  - review finding
  - runtime anomaly
  - worker-discovered gap
- `standing source`
  - `PROJECT_INTENT`
  - milestones / candidates / issue / progress / recovery
  - fleet / branch / worktree / runtime state

standing source 经周期扫描后，会派生新的 `problem signal`。

所有 source 最终都应汇聚成：

```text
source record
-> problem signal
-> manager restart-point routing
-> delegated loop
```

### 5.2 Discovery to candidate

```text
PROJECT_INTENT / chat / review / test / runtime anomaly
-> doc-loop(pre-brainstorm)
-> candidates.md
-> milestones.md.candidate_issues
```

约束：
- `chat` 在进入 `doc-loop(pre-brainstorm)` 前，可先经过 `auto-loop` 的 durable intake / classification / delegation；该 intake 层不改变“原始发现源不得伪装成 ready issue”的规则，只负责把外部输入变成可恢复、可监督的 source record
- 并非所有 source 都必须先进入 `pre-brainstorm`；主管需要先判断正确 restart point。这里描述的是“当新 signal 被判定为 discovery source 时”的典型链路。
- 原始发现源不得直接伪装成 ready issue
- candidate 在未进入 milestone-owned issue 前，不得跳过 IBM 直接进入 dev-loop
- future candidate 默认使用 `candidate_format_version: v2`，并包含 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`

### 5.2 Candidate to milestone-owned issue

```text
candidate_issues
-> doc-loop(IBM materialization)
-> issue_path established
-> milestones.md.committed_issues
-> phase_state=in_ibm
```

约束：
- `milestones.md` 是编排入口，不是原始发现源
- issue 的正式边界在 `docs/epics/**`
- `candidate_format_version: v2` 的 candidate 在 promotion 前，应有独立 acceptance review 记录
- IBM 不是复制 candidate acceptance；它必须把 candidate boundary 深化成 issue-level acceptance

### 5.3 Issue docs to ready implementation

```text
in_ibm
-> IBM + G completed
-> done_ibm
-> next route: dev-loop
```

约束：
- doc-loop 必须先把 issue 边界、产物和治理口径收齐
- 不允许用 `progress` 代替 IBM 产物

### 5.4 Implementation to verification

```text
done_ibm
-> in_dev
-> code / tests / progress
-> in_verification
```

约束：
- `progress` 只跟踪 dev-loop
- 边界外新问题必须 reroute 到 pre-brainstorm

### 5.5 Verification to completion

```text
in_verification
-> completed
-> milestones.md.completed_issues
```

约束：
- completion 前必须完成要求的 review、tests、evidence writeback
- completion 不等于 cleanup 已完成

### 5.6 Completion to cleanup

```text
completed
-> verified-retirable
-> merge / branch delete / worktree delete
-> cleanup evidence
-> next auto-loop scan
```

约束：
- cleanup 属于 `auto-loop` 的项目级治理决策
- 具体条件仍以 `LAWS.md` 的 worktree hygiene / promotion discipline 为准

## 6. Where Common Capabilities Belong

### 6.1 切号

- 所属 loop: `auto-loop`
- owner: `runtime/scripts`
- 本质：availability recovery，不是业务功能
- 目标：让循环继续活着，而不是决定做什么 issue

### 6.2 上下文管理

- `runtime continuity`
  - 所属 loop: `auto-loop`
  - owner: `runtime/scripts`
  - 内容：warn / rotate / `fresh_with_handoff` / session restart
- `doc continuity`
  - 所属 loop: `doc-loop`
  - owner: 当前 doc worker
  - 内容：在 `brainstorm/issue/recovery` 中写可续接证据
- `dev continuity`
  - 所属 loop: `dev-loop`
  - owner: 当前 dev worker
  - 内容：在 `progress/recovery` 中写实现态 continuity

### 6.3 watchdog

- 所属 loop: `auto-loop`
- owner: runtime + manager supervision
- 本质：监督控制面 umbrella
- 子模块可包括：
  - availability watchdog
  - runtime watchdog
  - continuity watchdog
  - worktree hygiene watchdog

### 6.4 milestone

- 所属 loop: `doc-loop` 与 `auto-loop` 交界
- owner: doc skills 写入，auto-loop 扫描
- 本质：编排中心 / board index
- 不是原始发现真源
- 不是详细执行真源

## 7. Single-Source Maintenance Rules

为避免继续产生平行口径，后续维护遵循：

1. `CONSTITUTION.md`
- 只保留三层循环边界与不可越界原则

2. `PROJECT_INTENT.md`
- 只保留产品方向、高层结构和为什么需要三层循环

3. `LAWS.md`
- 只保留状态词典、验收门和路由判定

4. `docs/system/workspace/three-loop-capability-lifecycle.md`
- 保留能力映射、owner 边界、生命周期流转的细节真源

5. `SKILL.md`
- 只保留该 skill 的职责、边界、输入输出和执行步骤
- 不重复发明完整三层循环定义

## 8. Current Consolidation Notes

- `doc-loop(IBM + G)` 的治理结论已被吸收到本文件，旧 pre-brainstorm 仅保留研究追溯价值。
- `milestones.md` 继续作为项目级编排中心，但其字段含义仍以 `LAWS.md` 为准。
- 新能力在落地前，应先回答四个问题：
  - 它属于哪个 loop
  - 它的 primary owner 是谁
  - 它的主回写产物是什么
  - 它在生命周期中从哪里触发、回到哪里

## 9. Current Capability Inventory

本节列出现有系统能力已经落在哪一层，避免再靠分散的 skill 名称猜测。

### 9.1 auto-loop capability inventory

| Capability | Main implementation | Primary owner |
| --- | --- | --- |
| outer-loop orchestration | `skill:auto-loop-orchestrator` | `lead-agent` / `manager-agent` |
| source classification and routing | `skill:context-source-skill` | `lead-agent` |
| branch/worktree lifecycle | `skill:branch-management`, `scripts/worktree/*` | runtime + manager |
| protected-branch constitutional gating | `skill:constitution-guard`, `skill:laws-enforcer` | agent preflight |
| multi-worktree supervision | `skill:multi-worktree-supervision`, `wt-fleet-status` | `manager-agent` |
| worktree hygiene supervision | `skill:worktree-hygiene-supervision`, `checkpoint-guard` | manager + worker |
| runtime recovery and continuity | `skill:recovery-subagent-governance`, `runtime/freely`, `monitor-ai-cli.sh` | runtime |
| AI CLI availability / account switching | `skill:ai-cli-availability-manager`, `runtime/ai-cli`, watchdog modules | runtime |
| manager bootstrap and watchdog restart | `freely ensure-manager`, `manager-watchdog.sh` | runtime |
| premerge conflict convergence | `skill:premerge-reconcile` | manager + dedicated worker |

说明：
- 这些能力的共同点是服务“项目继续活着并保持可编排”。
- 它们即使影响 doc/dev 执行，也不属于 issue 本地业务实现。

### 9.2 doc-loop capability inventory

| Capability | Main implementation | Primary owner |
| --- | --- | --- |
| raw discovery convergence | `skill:doc-pre-brainstorm-execution` | worker |
| candidate recording and milestone intake | `skill:doc-pre-brainstorm-execution`, `docs/milestones.md` | worker |
| milestone-owned issue materialization | `skill:doc-ibm-execution` | worker |
| governance maintenance within issue docs | `IBM + G` semantics in `skill:doc-ibm-execution` | worker |
| doc continuity writeback | current brainstorm / issue / recovery artifacts | worker |
| skill governance as documentation system maintenance | `skill:workspace-skill-governance` | worker |
| module/interface contract shaping | `skill:module-interface-governance` | worker |

说明：
- `doc-loop` 是“问题定义层”，核心职责是把问题收稳，而不是写实现。
- 任何还没有稳定 issue 边界的东西，都应该先回这里。

### 9.3 dev-loop capability inventory

| Capability | Main implementation | Primary owner |
| --- | --- | --- |
| ready issue implementation | `skill:dev-loop-execution` | worker |
| test execution and proof | `tests/**`, issue verification sections | worker |
| review evidence | `docs/epics/**/code-reviews/*.md`, `new-review` | worker |
| checkpoint and batch hygiene | `checkpoint-guard`, `worktree-hygiene-supervision` | worker |
| progress writeback | `docs/progress/**` or current equivalent continuity path | worker |
| promote/cleanup readiness handoff | issue + milestone + continuity evidence | worker -> manager |
| user-facing or project-facing feature skills | `url-content-intake`, future product skills | worker in issue scope |
| environment bootstrap in support of implementation | `rust-tauri-toolchain-bootstrap`, `config-backup-guard` | worker |

说明：
- 某些能力如 `checkpoint-guard` 横跨 auto/dev，但在“当前 issue 是否该先收口再继续实现”这一层，它主要服务 dev-loop。

## 10. Cross-Loop Capability Rules

有些能力天然跨层，不能被粗暴塞成“只属于一个 loop”。处理规则如下：

### 10.1 continuity

- `auto-loop continuity`
  - owner: runtime
  - 目标：让会话在崩溃、compact、轮换后可继续
- `doc-loop continuity`
  - owner: 当前 doc worker
  - 目标：让 brainstorm / issue / recovery 继续可读可接
- `dev-loop continuity`
  - owner: 当前 dev worker
  - 目标：让实现、测试、blocker、next step 可续接

### 10.2 checkpoint and hygiene

- checkpoint budget 计算与 runtime/manager 告警属于 `auto-loop`
- 当前工位收口、原子提交、拆 scope 属于 `dev-loop`

### 10.3 milestone

- 作为编排入口时属于 `auto-loop` 扫描面
- 作为 candidate/issue intake 落点时属于 `doc-loop`
- milestone 本身不承担实现态细节

### 10.4 verification and cleanup

- verification 证据生产主要属于 `dev-loop`
- 是否允许 merge / retire / cleanup 的项目级判断属于 `auto-loop`

## 11. Unresolved or Guarded Boundaries

以下边界已经有方向，但仍应作为后续检查面，避免再次漂移：

1. `ai-cli-availability-manager`
- 现在实质上是 watchdog availability 子模块
- 后续应继续避免与更广义 `watchdog-control-plane` 平行长大

2. `workspace-skill-governance`
- 当前属于 doc-loop 的治理维护能力
- 但若未来出现独立 skill registry / installer 生命周期，可能需要补充更明确的 auto-loop intake 边界

3. `config-backup-guard` 与 `rust-tauri-toolchain-bootstrap`
- 现在作为实现支持能力挂在 dev-loop
- 若未来这些动作被 runtime 预热自动执行，需要重新确认 owner 不要混乱

4. `verification/completion/cleanup`
- 当前已有 `phase_state` 语义和 manager cleanup discipline
- 但仍缺一个专门的 completion-verification 细节真源；当前先由 `LAWS.md` + issue verification sections + 本文件共同约束

## 12. Maintenance Checklist For New Capabilities

新增能力前，先检查：

1. 它的 primary loop 是什么。
2. 它的 primary owner 是 runtime、manager、worker、还是某个 skill。
3. 它的 canonical artifact 是什么。
4. 它是 discovery、continuation、verification 还是 cleanup 中的哪个触发点。
5. 它是否跨 loop；若跨 loop，是否已明确“主 owner”和“次 owner”。
6. 它是否会让 `CONSTITUTION`、`PROJECT_INTENT`、`LAWS` 与本文件出现重复定义；若会，应把细节只留在一个地方。

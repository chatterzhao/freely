# Three-Loop Capability Lifecycle

Freely 三个 loop 的应用级事件地图真源。

核心关系：
- `auto-loop` 是 outer orchestration / governance loop
- `doc-loop` 与 `dev-loop` 是 sibling execution loops
- `verification`、`recovery`、`cleanup governance` 是 route / phase / governance path，不是新增 loop

边界：
- `CONSTITUTION.md`: 边界与硬约束
- `LAWS.md`: 状态词典、判定门、验收
- `SKILL.md`: 执行步骤

本文件只保留：
- 全应用流向图
- `signal -> lifecycle record -> worktree execution cell` 联动
- owner / artifact / route 决策表
- worktree 生命周期与 completion / cleanup 回路
- 省周期关键点

## 1. Whole-System Flow

```mermaid
flowchart TD
    A[front-door command or standing source] --> B[signal record]
    B --> C[sync execution triad]
    C --> C1[lifecycle record]
    C --> C2[worktree execution cell]
    C --> D[manager routing]

    D --> E{route_kind}
    E -->|pre_brainstorm| F[doc-loop: pre-brainstorm]
    E -->|ibm| G[doc-loop: IBM]
    E -->|dev_loop| H[dev-loop]
    E -->|completion_verification| I[completion verification]
    E -->|recovery| J[runtime or session recovery]
    E -->|cleanup_governance| K[cleanup governance]

    D --> L{worktree action}
    L -->|reuse_existing_worktree| M[worker re-entry]
    L -->|create_feature_worktree| N[new execution cell]
    L -->|freeze_current_worktree| O[frozen / waiting]
    L -->|retire_worktree| P[retirement handoff]
    L -->|manager_only_no_worker| Q[manager-only patrol]

    F --> R[canonical writeback]
    G --> R
    H --> R
    I --> R
    J --> R
    K --> R

    I -->|verification failed| H
    I -->|new boundary exposed| F
    I -->|verification passed| K
    J -->|runtime recovered| D
    K -->|cleanup finished| S[next patrol sees closed lifecycle]
    O --> S
    P --> S
    Q --> S
    R --> S
    S --> D
```

说明：
- 任何一轮都先同步三元组，而不是只看 issue 或只看 worktree。
- `auto-loop` 负责 route 与 outer governance，不包含 `doc-loop` / `dev-loop` 的实现细节。
- `doc-loop` 与 `dev-loop` 是 sibling execution loops；它们都可能把结果回流给 `auto-loop`。
- `completion verification` 不是 cleanup，也不是第四个 loop；它是 promote 前后的验收路径。
- cleanup 完成后才算 lifecycle 真正闭环，不允许停在 `merged-not-cleaned`。
- `route_kind` 与 `worktree action` 是两个并列判断，不允许只判 loop 不判执行容器。
- 新 discovery 可以先被 intake 接住，但若存在唯一 canonical retained tree 仍未收口，manager 可以先延后 create，直到旧树 closeout 完成。

## 2. Execution Triad Map

```mermaid
flowchart LR
    A[signal] --> D[manager routing]
    B[lifecycle record] --> D
    C[worktree execution cell] --> D

    A1[why this cycle woke up] --> A
    B1[current phase and canonical truth] --> B
    C1[where execution can safely happen] --> C
```

三元组定义：
- `signal`: 这轮为什么被唤醒，例如 human interruption、patrol、test failure、review finding、runtime anomaly。
- `lifecycle record`: 当前 canonical 文档真相，例如 candidate、issue、progress、recovery、milestone。
- `worktree execution cell`: 当前真实执行容器，即 `branch + worktree + runtime/session + ownership`。

判定原则：
- 只看 `signal` 会丢掉当前做到哪一步。
- 只看 `lifecycle record` 会丢掉“该在哪棵树执行”。
- 只看 `worktree execution cell` 会把 dirty/clean 误判成业务完成度。

## 3. Front-Door Flow

```mermaid
flowchart LR
    A[freely init] --> A1[baseline ready]
    B[freely start] --> B1[runtime boot]
    B1 --> B2[manager patrol]

    C[freely chat]
    D[test or review finding]
    E[runtime anomaly]
    F[milestones / progress / recovery / fleet]

    C --> G[durable intake or source record]
    D --> G
    E --> G
    F --> G

    G --> H[manager notice]
    H --> I[classify source]
    I --> J[load lifecycle record]
    J --> K[load worktree cell]
    K --> L[choose route and worktree action]
```

## 4. Runtime Artifact Chain

```mermaid
flowchart LR
    A[signal or patrol wakeup] --> B[durable intake or source record]
    B --> C[interruption resolution]
    C --> D[manager continuity]
    D --> E[worker prompt]
    E --> F[worker runtime / prompt]
    F --> G[canonical writeback]
    G --> H[verification or cleanup evidence]
    H --> I[next patrol / next task scan]
```

说明：
- 运行时真正消费的是 artifact 链，而不是聊天里的自然语言。
- `intake -> resolution -> continuity -> worker prompt` 任何一环缺失，都会造成“看起来路由过了，实际上下游无从续跑”。
- 文档真相写回后，还要再经过 `verification / cleanup evidence` 才算真正回到下一轮 patrol。
- `worker prompt set` 不是无序列表；每条 worker handoff 至少要带 `dispatch_priority`、`parallel_safe`、`write_scope`，供 runtime 做 capacity-aware 排班与 queueing。

## 5. Manager Routing Map

```mermaid
flowchart TD
    A[signal] --> B[classify source_class]
    B --> C[read phase_state and runtime_state]
    C --> D[read worktree state and ownership]
    D --> E{retained canonical owner still open?}
    E -->|yes| F[finish retained tree first]
    E -->|no| G[allow new create or reuse]

    F --> H{retained tree state}
    H -->|dirty merged tree| I[continuation / cleanup followthrough]
    H -->|operator stopped or rate-limited| J[manager-only hold or recovery]
    H -->|already retire-ready| K[retire_worktree]

    G --> L{worktree action}
    L -->|reuse_existing_worktree| M[worker re-entry]
    L -->|create_feature_worktree| N[branch-management]
    L -->|freeze_current_worktree| O[frozen worktree]
    L -->|retire_worktree| P[cleanup handoff]
    L -->|manager_only_no_worker| Q[manager-only governance]

    I --> R{route_kind}
    J --> R
    M --> R
    N --> R

    R -->|pre_brainstorm| S[worker doc-loop: pre-brainstorm]
    R -->|ibm| T[worker doc-loop: IBM]
    R -->|dev_loop| U[worker dev-loop]
    R -->|completion_verification| V[manager or worker verification path]
    R -->|recovery| W[runtime/session recovery]

    K --> X[next patrol]
    O --> X
    P --> X
    Q --> X
    S --> X
    T --> X
    U --> X
    V --> X
    W --> X
```

## 6. Worktree Lifecycle Map

```mermaid
stateDiagram-v2
    [*] --> planned
    planned --> provisioning
    provisioning --> active

    active --> frozen
    frozen --> active

    active --> verification_ready
    verification_ready --> active: verification failed / more implementation
    verification_ready --> promotion_in_flight

    promotion_in_flight --> active: replay conflict / protected verification failed
    promotion_in_flight --> merged_not_cleaned

    merged_not_cleaned --> retained_dirty: canonical writeback still open
    retained_dirty --> active: followthrough resumed
    retained_dirty --> frozen: operator stop / runtime hold / account unavailable
    merged_not_cleaned --> retire_ready
    retire_ready --> retired
    retired --> [*]
```

约束：
- `completed` 属于 issue 生命周期，不等于 worktree 已退休。
- `merged-not-cleaned` 不是 terminal。
- `retire-ready` 只表示 cleanup gate 已过，还差正式删除与留痕。
- `retained_dirty` 表示“树已经被目标分支吸收，但该树仍持有 canonical writeback 或 closeout 责任”。
- `operator stop`、`usage limit`、AI 崩溃这类运行时异常不会直接改写 lifecycle；它们只会让 worktree 暂停在当前状态，等待 manager recovery judgement。

## 7. Completion And Cleanup Flow

```mermaid
flowchart LR
    A[worker verification evidence] --> B[manager completion verification]
    B --> C{result}
    C -->|pass| D[promotion in flight]
    C -->|same issue needs more work| E[back to active dev-loop]
    C -->|new boundary exposed| F[back to pre-brainstorm]

    D --> G[merged-not-cleaned]
    G --> H[cleanup gate check]
    H -->|pass| I[retire-ready]
    H -->|hold with reason| J[merged-not-cleaned visible in patrol]
    I --> K[branch delete / worktree delete / remote disposition]
    K --> L[cleanup evidence]
    L --> M[next patrol sees lifecycle closed]
```

## 8. Ownership And Boundary Map

```mermaid
flowchart LR
    A[runtime-owned] --> A1[intake durability]
    A --> A2[watchdog and pid recovery]
    A --> A3[continuity / prompt materialization]

    B[manager-owned] --> B1[route_kind]
    B --> B2[worktree action]
    B --> B3[fleet priority order]

    C[worker-owned] --> C1[doc-loop writeback]
    C --> C2[dev-loop writeback]
    C --> C3[verification evidence]

    D[cleanup-owned] --> D1[retirement decision]
    D --> D2[branch/worktree deletion]
    D --> D3[cleanup evidence]
```

关键边界：
- runtime 只负责托管、恢复、handoff artifact 与进程态，不替 worker 做语义 closeout。
- manager 负责决定“先收哪棵树、何时新建树、何时只冻结/等待”，不直接在 protected branch 上实现。
- worker 负责 canonical 文档或代码写回，不负责自己决定 retirement。
- queue / capacity 判断属于 `manager decision + runtime enforcement` 联动：manager 写 lane metadata，runtime 按 worker capacity 与 active lane 实际执行。

## 8A. Dispatch Scheduling Map

```mermaid
flowchart TD
    A[manager continuity with worker prompt set] --> B[rank by dispatch_priority]
    B --> C{worker capacity available?}
    C -->|yes| D{parallel_safe and write_scope conflict-free?}
    C -->|no| E[queue remaining prompts]
    D -->|yes| F[launch worker runtime]
    D -->|no| E
    F --> G[active running worker lane]
    E --> H[queued worker list in continuity / launch state]
    G --> I[next manager patrol]
    H --> I
```

调度约束：
- `dispatch_priority` 决定先派谁，不决定 route_kind 本身。
- `parallel_safe=false` 的 lane 默认单独占一个 dispatch wave。
- `write_scope` 冲突的 lane 不应同 wave 并发。
- 没有空余 worker capacity 时，未派发 lane 必须保留在 queue，而不是静默丢失或被挤回单一 continuation。

## 9. Loop Ownership Table

| Node | Primary owner | Main modules | Canonical artifacts |
| --- | --- | --- | --- |
| front-door intake | runtime | `freely init/start/chat`, runtime scripts | `.freely/intake/**`, runtime state |
| manager routing | manager-agent | `auto-loop-orchestrator`, `context-source-skill` | routing output, continuity |
| pre-brainstorm | worker | `doc-pre-brainstorm-execution` | `docs/pre-brainstorms/**` |
| IBM | worker | `doc-ibm-execution` | `docs/epics/**` |
| dev-loop | worker | `dev-loop-execution` | code, tests, reviews, progress |
| completion verification | manager -> worker | issue verification sections, review artifacts, protected acceptance evidence | issue, progress, milestone, cleanup pending truth |
| recovery | runtime + manager | runtime scripts, `recovery-subagent-governance` | `docs/recovery/**`, continuity |
| worktree action | manager + runtime | `branch-management`, worktree scripts | branch/worktree state |
| fleet supervision | manager | `multi-worktree-supervision`, `worktree-maintenance-governance` | fleet snapshot, disposition |
| cleanup governance | manager -> worker | `worktree-maintenance-governance`, `branch-management` | cleanup evidence |

## 10. Route Decision Table

| Condition | Route | Worktree default | Why |
| --- | --- | --- | --- |
| no stable issue boundary | `pre_brainstorm` | create | 先收敛边界，不提前写实现 |
| milestone-owned issue but IBM incomplete | `ibm` | reuse/create | 先补 issue 文档，不跳过文档层 |
| ready issue or explicit continuation | `dev_loop` | reuse | 默认回现有 active tree，减少新树与上下文切换 |
| `phase_state=in_verification` or milestone completed but cleanup open | `completion_verification` | reuse/manager-only | 不重复开发，直接处理 promote/cleanup |
| runtime/session unavailable or stale `in_*` | `recovery` | freeze/reuse | 先恢复 continuity，再决定是否继续 |
| cleanup gate already passed | cleanup governance | retire | 直接删树留痕，不让旧树继续占位 |
| new discovery admitted but retained dirty owner still open | `pre_brainstorm` deferred | manager-only first | 先收 canonical owner，避免同时制造第二个 competing tree |
| operator-stopped worker with unresolved lifecycle | `recovery` or manager-only hold | freeze | 不擅自自动复活，要先重新判定 ownership |
| AI tool usage limit / auth unavailable | `recovery` | freeze/manager-only | 这是 runtime-owned 暂停，不是业务状态改变 |

## 11. Worktree Action Table

| Action | Chosen by | Meaning | Next hop |
| --- | --- | --- | --- |
| `reuse_existing_worktree` | manager | current signal continues in an existing active tree | worker re-entry |
| `create_feature_worktree` | manager | current signal needs a new dedicated execution cell | `branch-management` |
| `freeze_current_worktree` | manager | tree remains visible but cannot continue now | next patrol / recovery |
| `retire_worktree` | manager | tree passed cleanup gate and should be removed | cleanup handoff |
| `manager_only_no_worker` | manager | this hop is governance-only and does not need worker execution | next patrol |

复用优先规则：
- 现有 issue continuation 默认复用当前 active worktree。
- 只有边界变化、树已退休、树不可安全继续、或需要独立 repair/research cell 时才新开树。
- 若唯一 retained dirty tree 仍持有 canonical closeout，默认先完成它，再决定是否新开 discovery worktree。

## 12. Worktree State Table

| Worktree state | Meaning | Usual owner |
| --- | --- | --- |
| `planned` | dedicated tree required but not created yet | manager |
| `provisioning` | branch/worktree creation or enter in progress | runtime + manager |
| `active` | tree is executing doc-loop or dev-loop | worker |
| `frozen` | tree is intentionally paused by dependency/runtime/hygiene reason | manager |
| `verification-ready` | worker finished current batch and is waiting for completion routing | manager + worker |
| `promotion-in-flight` | merge-up, merge-prep, replay, or protected acceptance is running | manager |
| `merged-not-cleaned` | target absorbed changes but branch/worktree disposition still open | manager |
| `retained-dirty` | merged tree still carries canonical writeback / closeout duty | manager + worker |
| `retire-ready` | cleanup gate passed; delete/retain disposition remains to execute | manager |
| `retired` | local tree and branch removed; remote handled or retained-with-reason | manager |

## 13. Lifecycle Record Map

| Record | Main loop | Purpose |
| --- | --- | --- |
| `pre-brainstorm candidate` | doc-loop | discovery boundary |
| `issue` | doc-loop | issue boundary |
| `progress` | dev-loop | implementation continuity |
| `recovery` | auto-loop / recovery | recovery continuity |
| `milestones.md` | auto-loop + doc-loop | queue, index, orchestration |
| cleanup evidence | auto-loop | closure proof |

## 14. Event Matrix

| Event | Source | First owner | Loop entry | Lifecycle record update | Worktree action | Next hop |
| --- | --- | --- | --- | --- | --- | --- |
| `project_initialized` | `freely init` | runtime | auto-loop | baseline/bootstrap truth | none | wait/start |
| `manager_started` | `freely start` | runtime | auto-loop | runtime continuity updated | none | patrol |
| `human_chat_received` | `freely chat` | runtime -> manager | auto-loop | intake refs, issue refs, recovery refs | reuse/create/none | route |
| `standing_source_patrol` | milestones/progress/recovery/fleet | manager | auto-loop | continuity snapshot | reuse/create/freeze/retire/none | route |
| `new_discovery_confirmed` | manager routing | manager | doc-loop | pre-brainstorm + candidate | create | worker pre-brainstorm |
| `new_discovery_admitted_but_deferred` | manager routing | manager | auto-loop | intake + candidate stay visible | manager-only | finish retained owner first |
| `candidate_promoted_to_issue` | doc-loop | worker | doc-loop | issue + milestone | reuse/create | IBM |
| `issue_docs_ready` | IBM | worker | dev-loop | issue + milestone | reuse | dev-loop |
| `issue_continuation_confirmed` | manager routing | manager | doc-loop or dev-loop | issue/progress/recovery continuity | reuse | worker re-entry |
| `runtime_recovery_required` | runtime/session failure | runtime -> manager | recovery | recovery continuity | freeze/reuse/none | recovery |
| `runtime_limit_hit` | AI tool / account | runtime | recovery | runtime continuity only | freeze/manager-only | wait or re-entry |
| `operator_stopped_worker` | human or runtime stop | runtime -> manager | recovery | workcell state only | freeze | manager re-judge before resume |
| `checkpoint_or_hygiene_triggered` | worker or patrol | manager + worker | dev-loop | progress continuity | freeze/reuse | hygiene / continue |
| `verification_passed` | worker | manager | completion verification | issue/progress/milestone evidence | none | promote decision |
| `verification_failed_same_issue` | worker/protected verification | manager | dev-loop | blocker / next-step continuity | reuse | repair same tree |
| `verification_failed_new_boundary` | worker/protected verification | manager | doc-loop | candidate / issue reroute | create/reuse | pre-brainstorm |
| `promotion_started` | manager | manager | completion verification | verification continuity | none | merge-up / merge-prep / replay |
| `promotion_completed` | manager | manager | cleanup governance | cleanup pending truth | none | cleanup decision |
| `cleanup_gate_passed` | manager | manager | cleanup governance | cleanup readiness evidence | retire | branch-management cleanup |
| `cleanup_completed` | cleanup worker | manager | auto-loop governance | cleanup evidence | retired | patrol |
| `post_merge_new_finding` | review/test/patrol after promote | manager | discovery or dev-loop | new candidate / issue / blocker continuity | create/reuse | new repair route |

## 15. Standard Chains

### 15.1 Chat To Worker Execution

```mermaid
flowchart LR
    A[freely chat] --> B[durable intake]
    B --> C[manager notice]
    C --> D[classify source]
    D --> E[load issue/progress/recovery]
    E --> F[load worktree cell]
    F --> G{reuse or create}
    G -->|reuse| H[existing worktree]
    G -->|create| I[new feature worktree]
    H --> J[worker handoff]
    I --> J
    J --> K[doc-loop or dev-loop]
    K --> L[writeback]
    L --> M[next patrol]
```

### 15.2 Verification To Retirement

```mermaid
flowchart LR
    A[worker verification-ready] --> B[manager completion verification]
    B -->|pass| C[promotion in flight]
    B -->|fail same issue| D[back to active]
    B -->|new boundary| E[back to pre-brainstorm]
    C --> F[merged-not-cleaned]
    F --> G[cleanup gate]
    G -->|pass| H[retire-ready]
    G -->|partial / retained| G2[continuation handoff]
    G2 --> F
    H --> I[delete branch/worktree]
    I --> J[cleanup evidence]
    J --> K[closed lifecycle visible to patrol]
```

### 15.3 Retained Dirty Tree Before New Discovery

```mermaid
flowchart LR
    A[new chat discovery admitted] --> B[intake delegated to pre_brainstorm]
    B --> C[manager patrol sees retained dirty merged tree]
    C --> D{canonical owner still open?}
    D -->|yes| E[defer create_feature_worktree]
    E --> F[route retained tree to continuation or cleanup]
    F --> G[closeout or freeze with reason]
    G --> H[next patrol]
    H --> I[new discovery becomes creatable]
    D -->|no| J[create dedicated worktree now]
```

### 15.4 Runtime Pause Without Lifecycle Rewrite

```mermaid
flowchart LR
    A[worker or manager active] --> B[runtime anomaly: limit/auth/crash/operator stop]
    B --> C[runtime-owned hold]
    C --> D[workcell state updated]
    D --> E[manager recovery judgement]
    E -->|resume same tree| F[re-entry]
    E -->|freeze| G[next patrol]
    E -->|retire| H[cleanup]
```

## 16. Cycle-Saving Gates

| Gate | Default decision | Cycle saved |
| --- | --- | --- |
| issue continuation already has active tree | reuse existing worktree | 避免无意义新开 sibling tree |
| docs already sufficient for implementation | skip back to IBM and enter `dev_loop` | 避免重复文档收敛 |
| current batch only needs promote/cleanup | enter `completion_verification` instead of `dev_loop` | 避免重复开发和重复测试 |
| verification failed but boundary unchanged | return to same active tree | 避免把实现问题误升级成新 discovery |
| verification exposed a new boundary | reroute to `pre_brainstorm` | 避免把边界问题硬塞进当前 issue |
| retained dirty canonical owner still open | defer new worktree creation | 避免新旧两棵树同时争夺同一 closeout 真相 |
| cleanup gate passed | retire immediately | 避免停留在 `merged-not-cleaned` 占住树和注意力 |
| operator stop or usage limit only changed runtime state | keep lifecycle truth unchanged | 避免把运行时暂停误写成业务完成或失败 |
| runtime broken but canonical truth intact | recovery before new work | 避免重做已经完成的 doc/dev 写回 |

## 17. Minimal Maintenance Rule

新增能力时只补对应真源：
- 新入口事件：补 `Whole-System Flow`、`Front-Door Flow` 或 `Event Matrix`
- 新 artifact 交接层：补 `Runtime Artifact Chain`
- 新 manager 判断：补 `Manager Routing Map` 或 `Route Decision Table`
- 新 worktree 状态：补 `Worktree Lifecycle Map` 和 `Worktree State Table`
- 新 promote / cleanup 分支：补 `Completion And Cleanup Flow`
- 新 owner 边界：补 `Ownership And Boundary Map`

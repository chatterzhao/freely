# 预研头脑风暴：verification-contract-and-premerge-adequacy

## 问题陈述

Freely 已经有三层与测试相关的真源：

1. IBM / `pre-tests.md` 负责定义 acceptance contract
2. `test-lane` / branch laws 负责 lane 与工位匹配
3. `pretests-gate` / merge gate 负责在 completion / merge 出口做最低 enforcement

但用户暴露的是更前置的 adequacy 问题：

- `test-pre-merge-*` 阶段到底该跑什么，是否只是在“有跑测试”而不是“跑够了 issue 真正需要的测试”
- 为什么很多 bug 仍然要到真实 dogfooding 才暴露
- manager/worker handoff 是否没有把测试契约、lane、exit criteria 明确写给执行者
- skill 虽然写了质量线，但是否没有被 prompt/runtime 强消费，导致实际执行继续偷懒

这说明当前缺口不是“完全没有测试规则”，而是：

1. `pre-tests.md` 与 worker handoff 之间仍有恢复断层
2. `test-pre-merge-*` 的 adequacy 还没有从 issue acceptance contract 反推成必跑集合
3. merge adequacy 主要靠后置 gate 拦截，前置 manager/worker contract 偏弱

## 现状真源

### 0. 当前项目里的测试设计其实已经是五层，不是单点缺失

把当前项目所有测试相关设计拉平后，至少有这五层：

1. 宪法/法律层
   - 定义 `test-pre-merge-* -> develop` 的合法路径
   - 定义 `feature-local` / `premerge-integration` / `post-merge-followthrough`
   - 定义 `pre-tests.md` 的最低质量线与 `develop` merge 前必须优先看的 integration / acceptance evidence
2. IBM / `pre-tests.md` / `prd.md` 层
   - 定义 issue-level acceptance contract
   - 默认要求 pre-merge focused regression 与 post-merge integration / real-environment / dogfood
3. wrapper / lane enforcement 层
   - `./bin/test-lane` 只解决“在哪条 lane 上跑才合法”
4. completion / merge gate 层
   - `pretests-gate` 只卡 issue 进入 `completed`
   - `governance-merge-gate` 只卡 develop-bound lifecycle / owner / review note
5. manager/worker handoff 层
   - 只强制写调度/写域/所有权 metadata
   - 还没有强制带测试义务摘要

所以当前项目不是“没有测试设计”，而是设计已经分层存在，但没有在 `test-pre-merge-* -> develop` promote 与 worker handoff 这两处形成闭环。

### 1. 已有能力

- `doc-ibm-execution` 已要求 `pre-tests.md` 成为 issue-level acceptance 主控制面，默认覆盖 focused regression、integration、real-environment、dogfood。
- `test-lane-routing-and-enforcement-governance` 已完成，冻结了 `feature-local`、`premerge-integration`、`post-merge-followthrough`。
- `pre-tests-evidence-binding-and-completion-gate-governance` 已完成，把 issue-bound `pre-tests.md` 接到 completion gate。
- `test-pre-merge-*` 的职责已清晰：只做主线前集成 smoke / regression / acceptance，不做继续实现。

### 2. 当前缺口

- manager continuity / worker prompt 目前只强制 `Worktree`、`Branch`、`dispatch_priority`、`parallel_safe`、`write_scope`、`intent_kind`、`intent_target`，没有要求携带：
  - `pre_tests_path`
  - required lane
  - required acceptance items
  - verification exit criteria
- worker/manager prompt 真源更多要求“带回 evidence”，但没有冻结“必须先从 issue/pre-tests 恢复本轮最小必跑测试集”。
- `test-lane` 解决的是 lane misuse，不解决“在正确 lane 里是否跑够了 issue 所需 acceptance”。
- `governance-merge-gate` 当前不解析 `pre_tests_path`，`pre-merge-commit` 在 develop guarded merge 路径里也不会调用 `pretests-gate`；因此 `test-pre-merge-* -> develop` 仍未真正检查 testing adequacy。
- `pretests-gate` 目前只检查 `Acceptance Items` 的最小五字段、`status=pass|not_applicable`、`artifact_ref` 非 pending 且存在；它不检查“是否与本次修改相关”“是否属于真实环境/端到端层”“是否对应 promote 必需项”。
- 很多 issue 的 prose 章节已经写出了 `real-environment` / `dogfood` / `failure signal` / `failure handling`，但 machine-readable item 仍不足以让 gate 消费这些语义。

## 为什么它属于 Freely 自身能力

这不是“当前仓库测试写得不认真”的一次性问题，而是 Freely 自举和未来托管项目都需要的能力：

- manager 必须能稳定把 issue acceptance contract 委派给 worker
- worker 必须能在 continuation 恢复中明确知道本轮测试义务，而不是仅凭自由裁量
- `test-pre-merge-*` 必须成为可判定的主线前 adequacy surface，而不是形式上的“跑过点东西”

因此它属于 Freely 的 verification governance / execution contract 能力。

## 关键判断

### 1. `test-pre-merge-*` 的职责已经清楚，但 adequacy 仍未冻结

现行真源已经说明：

- 该工位只做 premerge integration / acceptance，不做继续开发
- 需要使用 `premerge-integration` lane
- 具体跑哪些命令应由 issue 的 `pre-tests.md` 决定

缺的不是 lane 定义，而是“如何从 issue 的 acceptance contract 推导出 test-pre-merge 的必跑集合，并在 handoff 中强制带上去”。

### 2. bug 经常到 dogfood 才暴露，不等于 dogfood 不该存在

对 Freely 自治能力，真源本来就要求 post-merge real-environment 与 dogfood acceptance。问题不在“为什么还有 dogfood”，而在：

- 某些本应在 premerge integration 暴露的缺口没有提前暴露
- 某些 issue 虽写了 dogfood / real-env，但 manager/worker 并未把这些面当成明确 contract 去排班和执行

所以目标不是拿 dogfood 替代 premerge，也不是幻想 premerge 覆盖一切，而是让各测试面的责任边界和前置派生更清楚。

### 3. 更像统一治理问题，下游可拆多个 owner

最合理的形态不是把所有问题粗暴挂给一个现有 owner，而是先形成一个 umbrella pre-brainstorm，再视 materialization 拆成多个 owner：

1. `verification-handoff-contract-governance`
   - manager continuity / worker prompt 必须携带测试契约元数据
2. `premerge-adequacy-derivation-governance`
   - 从 issue / `pre-tests.md` 推导 `test-pre-merge-*` 的必跑 acceptance 集合
3. `test-wrapper-adoption-and-adequacy-enforcement-governance`
   - 把必跑 contract 接到 wrapper / gate / maybe runtime checks，减少 raw command 绕过

## 全仓审计结论

### 1. 当前项目里“测试相关的所有设计面”已经具备，但割裂

综合 laws、skills、hooks、scripts、issues、pre-tests 样例、verification artifacts，可归纳为：

- `LAWS.md` 已要求：
  - `develop` merge 前优先看 issue-bound `pre-tests.md` 的 integration / acceptance evidence
  - `test-pre-merge-*` 只做主线前集成 smoke/regression/acceptance
  - `pre-tests.md` 必须至少能恢复 acceptance target、testing layer、target environment、required evidence、blocker taxonomy
- `doc-ibm-execution` / `prd-quality-bar` / `ibm-completion-gate` 已要求：
  - `pre-tests.md` 默认覆盖 post-merge integration / application-native real-environment / end-to-end dogfood
  - `pre-tests.md` 应写 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
  - `Acceptance Items` 需具备 machine-readable 字段
- `test-lane` 已把 lane 语义 machine-enforce
- `pretests-gate` 已把 issue `completed` 的 acceptance item 最小结构 machine-enforce
- `governance-merge-gate` 已把 develop-bound owner lifecycle、progress/review、implementation decision note machine-enforce

缺的是把这些层串起来：

- `test-pre-merge-* -> develop` merge gate 还没真正读 issue-bound `pre-tests.md`
- handoff 还没把测试义务压成 worker 必执行摘要
- acceptance prose 与 acceptance items 之间还存在信息损失

### 2. 上乘设计的核心不是“更多测试”，而是“单一真源、两处强消费”

上乘设计不该做三件错事：

- 不该扫全仓 `pre-tests.md`
- 不该靠关键词或 changed paths 猜哪些测试与本次修改相关
- 不该把完整 `pre-tests.md` 复制进 prompt/header 形成平行真相

上乘设计应该做的，是把单一 issue-bound 测试真源在两处强消费：

1. `test-pre-merge-* -> develop` guarded merge
   - 卡 promote adequacy
2. manager -> worker handoff
   - 卡执行 adequacy

issue / `pre-tests.md` 仍是主真源；merge gate 与 handoff 只消费它的 machine-readable 摘要，而不是各自发明新标准。

## 上乘设计

### A. merge gate 负责卡 `test-pre-merge-* -> develop` 的测试充分性

这层应成为第一道硬门，而不是等到 dogfood 再发现。

最小正确设计：

1. 触发点放在 `test-pre-merge-* -> develop` 的 guarded merge 路径，不另开平行 gate。
2. 复用现有 owner issue 解析结果，只检查本次 merge 已绑定出来的 owner issue。
3. 对每个 owner issue：
   - 若声明了 `pre_tests_path`，就读取该 issue 绑定的 `pre-tests.md`
   - 校验最低 contract 是否存在：
     - acceptance target
     - testing layer
     - target environment
     - required evidence
     - blocker taxonomy
4. gate 不要求所有 acceptance items 全部通过，只要求“本次 promote 必需项”达到：
   - `status=pass|not_applicable`
   - 非 `pending://`
   - artifact 可解析
5. gate 至少要求一个 promote 必需项属于真实的集成/真实环境/端到端层，不能只靠 docs/mock/wording 项过门。

这意味着：

- `pretests-gate` 需要从“completed gate”扩成“可被 develop merge path 复用的 adequacy gate”
- `governance-merge-gate` 继续管 owner / lifecycle / review artifact
- 两者共享同一 owner set，不各自重新猜 issue

### A1. gate 不是主执行者，而是最后兜底并给出可操作诊断

更好的设计不是 gate 代替人设计测试，而是：

1. manager / worker handoff 先把 issue-bound 测试义务讲清楚
2. `pre-tests.md` 继续做唯一 acceptance 真源
3. merge gate 只在 promote 出口兜底，并明确告诉执行者到底卡在哪一层

最小诊断面应至少区分四类：

1. `pre_tests_missing`
   - `pre-tests.md` 没写，或未写出当前 issue 所需的测试任务 / acceptance items
2. `testcase_derivation_missing`
   - `tasks.md` / acceptance target 已写，但没有把它们派生成可执行、可 machine-read 的测试项
3. `execution_missing`
   - 测试项已定义，但没有实际执行；仍停留在 `pending://`、空 artifact 或未跑状态
4. `verification_state_missing`
   - 测过了，但 `pre-tests.md` 没有正确标记 `status`、不适用理由、替代证据或完成情况

这样 gate 的价值才是“兜底并提示下一步补什么”，而不是只报一个抽象的 “testing inadequate”。

### B. `pre-tests.md` 继续做主真源，但要把关键测试语义下沉到 item 级

同时，`pre-tests.md` 不能只靠零散 item；它还需要固定章节骨架，便于评审快速判断有没有偷掉某个测试面。

建议最小强制章节：

1. `Unit`
2. `Integration`
3. `End-to-End`
4. `Real-Environment`

每个章节都必须出现：

- 若当前修改需要该层测试，就写具体测试任务、测试用例与通过标准
- 若当前修改不需要该层测试，也不能省略；必须写 `not_applicable_reason`

`not_applicable_reason` 不应是自由发挥长文，而应先落有限枚举，再补一句解释。建议第一版白名单：

- `change_not_touching_this_layer`
- `no_executable_boundary_at_this_layer`
- `protected_environment_only`
- `human_observation_only`
- `covered_by_more_realistic_required_surface`

最稳设计不是再造一套平行 `testing section`，而是：

1. 保留现有 `Acceptance Structure`
   - 继续承载 prose 级的 `environment`、`evidence`、`failure signal`、`failure handling`
2. 强化现有 `Acceptance Items`
   - 把 gate 需要消费的关键字段下沉到 item 级

建议至少新增/强制：

- `surface_kind`
  - `premerge_regression`
  - `postmerge_integration`
  - `real_env`
  - `dogfood`
- `target_environment`
  - `feature_worktree`
  - `test-pre-merge-*`
  - `develop`
- `target_lane`
  - `feature-local`
  - `premerge-integration`
  - `post-merge-followthrough`
- `promotion_gate`
  - `required`
  - `deferred_to_post_merge`
  - `not_applicable`
- `blocker`
  - 复用现有 blocker taxonomy
- `why_not_applicable`
- `replacement_evidence`
- `task_refs`
  - 当前测试项来自哪些 `tasks.md` / acceptance target
- `case_design`
  - 最小测试用例摘要，避免只写“跑点测试”
- `not_applicable_reason`
  - 若当前 item 或整章不适用，必须使用白名单 reason，而不是自由发挥

这样才能让系统 machine-readably 判断：

- 这条 item 属于哪类测试面
- 该在哪个环境/lane 跑
- 它是不是这次 `test-pre-merge-* -> develop` promote 的必需项
- 若标 `not_applicable`，是否有合法理由和替代证据
- 是否真的从任务设计出了测试用例，而不是跳过设计直接宣称“已测”

### C. manager/worker handoff 负责卡“不能只跑象征性 smoke”

这层不该复制全部 `pre-tests.md`，但必须携带最小测试义务摘要。

worker prompt header / continuity 至少应新增：

- `Owner-Issue`
- `Pre-Tests-Path`
- `Verification-Artifact-Dir`
- `Required-Test-Lanes`
- `Required-Acceptance-Surfaces`
- `Required-Acceptance-Item-Ids`
- `Minimum-Evidence-Level`
- `Exit-Criteria`
- `NA-Policy`

分层建议：

- issue / `pre-tests.md`
  - 长期 canonical truth
- worker prompt header
  - 最小 machine-readable 执行索引
- manager continuity
  - queue/freeze/supervision 视角下的测试债务摘要

不要把完整 acceptance prose 镜像进 prompt；否则会制造第二套真相。

## 为什么这才是上乘设计

因为它同时满足四点：

1. 单一真源
   - 仍由 issue-bound `pre-tests.md` 定义测试义务
2. 强消费
   - merge gate 和 handoff 都真正消费这份义务
3. 不过度自动化
   - 不靠路径猜测、关键词猜测、全仓扫描
4. 区分测试层次
   - 不把 premerge integration、post-merge real-env、dogfood 混成一个“都测了”

## 推荐 owner 切分

按实现边界，最自然的 materialization 可能是两条：

1. `issue-bound-verification-contract-materialization-governance`
   - 负责 `pre-tests.md` item schema、h andoff metadata、NA policy、acceptance surface machine readability
2. `premerge-adequacy-gate-governance`
   - 负责把 `test-pre-merge-* -> develop` merge gate 接到 issue-bound required acceptance items

如果第一阶段想更稳，也可以先出一个 owner：

- 先冻结 contract 与 merge semantics
- 第二阶段再把更多 wrapper/runtime enforcement 接上

## 建议方向

### A. 给 manager/worker handoff 增加 machine-readable verification contract

至少考虑新增：

- `Pre-Tests:`
- `Required-Test-Lane:`
- `Required-Acceptance-Items:`
- `Verification-Exit-Criteria:`
- `Post-Merge-Followthrough:`

目标不是把全部 `pre-tests.md` 复制进 prompt，而是让 worker continuation 不再需要自己猜测“本轮到底要跑什么才算足够”。

### B. 定义 `test-pre-merge-*` 的 adequacy derivation

需要回答：

1. issue 的哪些 acceptance item 必须在 `feature-local` 解决。
2. 哪些 acceptance item 必须在 `premerge-integration` 复跑。
3. 哪些 acceptance item只能在 `develop` 的 `post-merge-followthrough` 或真实 dogfood 中完成。

如果这层不冻结，`test-pre-merge-*` 仍可能沦为只做“象征性 smoke”。

### C. 减少 raw test command 绕过

当前 `test-lane` owner 已承认：只要团队继续直接调用原始测试命令，就可能绕过显式 lane contract。下一阶段应至少回答：

- 哪些变更必须通过 wrapper 入口留痕
- merge / verification evidence 是否需要声明 lane-bound command
- hooks/runtime 是否要对“完全未经过 wrapper 的关键验证”增加更强提示或 gate

## 与现有 owner 的关系

### 不应 reopen 的 completed owner

- `I-20260405-1914-A` 只冻结 lane 路由与 wrapper correctness，不负责 adequacy 推导
- `I-20260327-0701` 只冻结 completed gate，不负责 manager/worker 前置 handoff contract

### 更像 follow-on 的 owner 面

- IBM 定义层已存在，但要继续被 handoff/runtime 消费
- lane enforcement 已存在，但要继续接 adequacy contract
- completion gate 已存在，但要继续前移到 manager/worker dispatch 与 premerge verification

## Promotion Gate

- 证明这不是在重复“已经有 `pre-tests.md` 和 test-lane”这层已完成 owner
- 证明当前主要缺口是 adequacy derivation 与 handoff enforcement，而不是继续写更多测试建议文档
- 证明第一阶段可先落治理 contract 与最小 machine-readable metadata，而不必一次性做全自动 test orchestration

## Open Questions

1. verification contract 元数据应放在 worker prompt header、manager continuity、还是 issue/progress sidecar 中。
2. adequacy derivation 是仅写入 docs truth，还是第一阶段就接到脚本校验。
3. 对已存在 `pre-tests.md` 但质量仍偏弱的 issue，是增量升级还是只从新 owner 开始强制。
4. dogfood 暴露的新 bug 应如何区分“预期的 post-merge surface”与“本应在 premerge 就抓到的 adequacy miss”。

## Status Reconcile

- reconcile_status: `stale_with_follow_on`
- why: `这里把“当前 develop 尚未 adequacy enforce”与“应如何 materialize follow-on owner”混在了一起。后续 canonical truth 已经把 adequacy 问题收束到独立 owner，但该 owner 的更强 gate 并不等于已经全部合回当前 develop 基线。`
- canonical_truth:
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/pre-tests.md`
  - `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/code-reviews/20260408-verification-contract-and-premerge-adequacy-verification.md`
- stale_statement:
  - `governance-merge-gate 当前不解析 pre_tests_path，pre-merge-commit 在 develop guarded merge 路径里也不会调用 pretests-gate；因此 test-pre-merge-* -> develop 仍未真正检查 testing adequacy。`
- follow_on_note: `不要再把这句旧判断当作 owner 归因入口；当前应直接看 adequacy owner 的 issue / pre-tests / verification receipt，并区分“已在 owner 中冻结”“已在某条 feature lane materialize”“已合回 develop”这三个阶段。`
- reconcile_note: `保留本预研作为 adequacy gap 的发现来源，但它不再是当前实现状态的权威描述。`

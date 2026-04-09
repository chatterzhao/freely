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

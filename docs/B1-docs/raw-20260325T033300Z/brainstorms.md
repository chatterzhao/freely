# 预研头脑风暴：testing-evidence-ladder-and-real-environment-gates

## 背景

Freely 正在用 Freely 开发 Freely。最近这一轮同 family runtime/parser 回归再次暴露出一个比单点 bug 更上层的问题：

- 当前多数测试仍偏脚本级回归
- 真实 `develop` / manager runtime / interruption intake / worker launch 这种 application-native 行为，更多靠事后 dogfood 才暴露
- `pre-tests.md` 已经承担 issue-level acceptance 控制面，但“什么测试证据足以通过 gate”仍然没有形成统一、可执行、可恢复的能力 contract

这会带来两个直接后果：

1. 同类问题会不断以“本地测试都过了，但真实环境又炸了”的形式重复出现。
2. Freely 还没有把“测试质量是硬门禁” materialize 成产品能力，而只是停留在局部 issue 的经验写法。

## 为什么现在必须研究

这不是抽象质量口号，而是 Freely 自举中已经反复出现的真缺口：

- parser drift、launch-state consumed truth、runtime churn、账号恢复、slot 语义这几类问题，都不是纯 unit-level 失误
- 它们往往需要 integration / end-to-end / application-native real-environment 才能稳定看见
- 当前多个 candidate 已经分别提到 `testing closeout evidence bar`、`post-merge acceptance`、`protected verification environment`，但还没有一条更上层的测试能力 candidate 把这些边界统一起来

如果不先把这条能力独立化，Freely 就会继续：

- 一边要求测试作为 completion / retirement gate
- 一边又让每个 issue 自己临时发明“这次够不够测完”

## 当前事实

### 已经存在但不够的真源

1. `integration-acceptance-first` 已经把 `pre-tests.md` 固定成 issue-level acceptance 控制面。
2. `protected post-merge acceptance route` 已经在研究 protected env 里的验证与 promote guard。
3. `pre-test-merge lifecycle management` 已经开始写 `testing closeout evidence bar`。
4. 个别 issue 已经补了 live integration test 或 develop-side acceptance。

### absorbed inventory 已落盘

为避免继续把测试能力写成“大家都知道但没人冻结”的经验规则，当前 candidate 的已吸收真源、缺口与最小 materialization 顺序已写入：

- `./inventory.md`

这份 inventory 不是附录，而是下一跳 issue materialization 的直接输入。

### 已有真源吸收清单

当前至少已有三组真源必须被本 candidate 继承，而不是重写：

1. `I-20260322T013500Z integration-acceptance-first-verification-governance`
- 已冻结：`pre-tests.md` 是 issue-level acceptance 控制面
- 已冻结：verification 默认先看 integration / acceptance evidence，再做定向代码评审
- 仍未冻结：story-level `pre-tests.md` 最低质量线，以及测试分层的统一 ladder

2. `I-20260318T163000Z global-ai-account-watchdog-and-manager-bootstrap`
- 已证明：某些能力必须要求 live integration test，不能只靠脚本单测
- 已证明：真实链路验证可以进入 story acceptance，而不是只能停在人工 dogfood
- 仍未冻结：哪些类型的问题默认必须提升到 live integration / real-environment

3. `I-20260324T041500Z application-native-runtime-observation-contract-and-observability-planes`
- 已冻结：artifact plane 是 acceptance evidence 的 canonical truth surface
- 已冻结：current-state / fleet 只镜像最小 acceptance 摘要与 `acceptance_ref`
- 仍未冻结：testing closeout 的 machine-readable 状态该如何映射到 acceptance evidence schema

### 仍然缺失的能力边界

1. 缺少统一的 testing evidence ladder：
- smoke / script regression
- integration
- end-to-end
- application-native real-environment
- protected-env post-merge acceptance

2. 缺少统一的 gate contract：
- 什么时候 script 级测试足够
- 什么时候必须跑 integration
- 什么时候必须跑真实 runtime / develop / manager dogfood
- 什么时候没有这些证据就不得宣称 completion verification / worktree retirement

3. 缺少统一的 capability 落点：
- 哪些测试应该进入 `docs/system/workspace/scripts/tests/**`
- 哪些应该成为 application-native harness / scenario runner
- 哪些应在 runtime/manager continuity 中被 machine-readably 标记为“已执行/未执行/被阻塞”

### 必须再明确的一条硬规则

每个 story 下的 `pre-tests.md` 质量本身就是头等门禁，不是后置附件：

- `pre-tests.md` 不能只列脚本名，它必须能恢复 story 的 acceptance contract
- 若 `pre-tests.md` 质量不足，后续 integration / end-to-end / real-environment 再多，也只是“在不稳定目标上做更多测试”
- 因此测试能力研究不能只讨论“补多少测试”，还必须讨论“story-level `pre-tests.md` 何时才算合格”

## 为什么不直接吸收到现有 candidate

### 不直接吸收到 `C-20260322T180100Z-B`

`C-20260322T180100Z-B` 的中心是 stale `pre-test-merge` lifecycle transaction。它只在 scope 里引用了 testing closeout evidence bar，但不是测试能力体系本身。

### 不直接吸收到 `C-20260322T161500Z-A`

`C-20260322T161500Z-A` 的中心是 protected verification environment 的 route / promote / replay guard。它研究“在哪里测、怎么防止 protected env 变成实现来源”，不是研究“测试能力矩阵和证据阶梯本身”。

因此这里更像一条新的上层能力候选：

> Freely 需要一套可执行、可恢复、可被 manager/runtime/gates 消费的测试证据阶梯与真实环境门禁能力。

## 问题定义

需要回答：

> 对于一个用 AI 自己开发项目的系统，Freely 应该如何定义测试分层、证据阶梯、真实环境验证义务与门禁规则，才能让 completion / promote / retirement 都建立在统一而足够强的测试 contract 上，而不是靠每个 issue 临时解释？

## 关键张力

1. 不能把所有问题都升级成真实环境测试，否则迭代成本会失控。
2. 也不能只靠脚本回归，因为 Freely 的许多缺陷只在真实 runtime / dogfood 中出现。
3. `pre-tests.md` 负责 acceptance contract，但测试执行与证据留痕还需要更强的能力化承载。
4. 测试作为硬门禁，必须可 machine-readably 拒绝“没测完却宣称完成”的情况。

## 初始收敛方向

### 方向 A：定义 testing evidence ladder

至少明确这些层级及默认用途：

- script regression
- integration test
- end-to-end scenario
- application-native real-environment test
- protected-env post-merge acceptance

### 方向 B：定义 gate mapping

至少明确：

- 哪些 issue 默认只需要到 integration
- 哪些类型的问题必须提升到 end-to-end 或 application-native
- completion verification / retirement 各自最低需要哪一级证据
- 每个 story 的 `pre-tests.md` 必须先达到最低质量线，才能谈后续测试执行是否足够

### 方向 B.1：定义 `pre-tests.md` 质量线

至少明确每个 story 下的 `pre-tests.md` 必须回答：

- 测的是什么 acceptance，而不只是“运行哪些命令”
- 这些测试分别属于 script regression、integration、end-to-end，还是 application-native real-environment
- 目标验证环境是什么
- 哪些证据缺失时不得判 completion verification / retirement
- 哪些 blocker 属于“测试还没跑”，哪些属于“`pre-tests.md` 自己还没定义清楚”

### 方向 C：定义 capability 落点

至少明确：

- 脚本测试、场景测试、真实环境 harness 各自落在哪里
- manager/runtime 应如何承载 `testing_closeout_state` 或等价 machine-readable truth
- `live-status` / artifact plane 是否需要只镜像最小测试完成摘要与 `acceptance_ref`

### 方向 D：先做 capability inventory，再做 materialization

为了按 Freely 规范做到真正完成，这条线不能直接从 candidate 跳实现；它必须先补一份清晰 inventory：

- 哪些真源已经规范了 testing acceptance
- 哪些真源已经要求 live / protected / real-environment evidence
- 哪些仍然只是 issue 局部经验，没有升格成 Freely capability
- 最小 follow-on issue 应该承接哪一块，而不是把 ladder / gate / harness / status 全部压成一个大 issue

当前 inventory 结论已经足够明确：

- 第一个最小切口应是 `story-level pre-tests quality gate`
- testing evidence ladder / gate mapping / real-environment harness 作为后续切口继续承接

## 预期落点

- `docs/B1-docs/raw-20260325-0333/`
- `docs/milestones.md`
- 后续若 materialize，再落到：
  - `docs/system/workspace/scripts/tests/**`
  - `docs/system/workspace/testing/**` 或等价能力目录
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - 相关 manager/runtime/status surface 真源

## 当前结论

- 这是新的上层能力候选，不是旧 `pre-test-merge` candidate 的局部修补。
- 当前先停在 pre-brainstorm，优先冻结 testing evidence ladder、gate mapping、以及 application-native real-environment 的最低证据 bar。
- 同时把“每个 story 下的 `pre-tests.md` 质量是头等门禁”冻结成单独 contract，而不是混在一般 testing advice 里。
- absorbed capability inventory / gap map 已产出在 `./inventory.md`。
- 下一跳不是直接写实现，而是先把 inventory 里最小切口 `story-level pre-tests quality gate` materialize 成独立 issue，再判断 follow-on ladder / harness issue。
- 在这些边界冻结前，不直接开实现 issue，也不把“测试天花板”写成泛化口号。

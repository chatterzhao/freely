# Brainstorm: ibm-pretests-real-environment-acceptance-quality

- brainstorm_id: `20260326-1733--ibm-pretests-real-environment-acceptance-quality`
- created_at: `2026-03-26`
- status: `active`
- related_signals:
  - 当前 `doc-ibm-execution` 已要求 `pre-tests.md` 以 integration / acceptance 为主，但新 issue 仍容易把 pre-tests 写成 truth-source reading checklist。
  - Freely 是自治 AI 开发工具，很多真实缺口只有在 `freely start`、`freely chat`、manager patrol、worker delegation、runtime recovery 的真环境链路里才会暴露。
  - 若 governance / capability issue 的 `pre-tests.md` 仍停在“读文档能否读出语义”，后续 dev-loop、verification 与 closeout 会缺少可执行的端到端验收 contract。

## Problem

`integration-acceptance-first-verification-governance` 已经把方向写对了，但 enforcement 还不够强：

- `prd.md` 的 `Eval Plan` 仍可能先收缩成 truth-source review
- `pre-tests.md` 仍可能退化成文档语义检查，而不是 issue-level executable acceptance contract
- governance / agent / skill 改造型 issue 尤其容易被误判为“没有真环境测试面”

结果是 Freely 会在最需要自治验收的地方，丢失：

- 集成测试面
- application-native real-environment testing 面
- 端到端狗粮验收面
- 失败判据、证据面与 post-merge replay 语义

## Desired Outcome

冻结一条更强的 IBM 质量门槛：

1. `pre-tests.md` 默认必须给出可执行的 acceptance contract，而不只是阅读检查。
2. 对 Freely 自治能力，集成测试、真环境测试、端到端狗粮测试应成为必答面；若某项暂不适用，必须写出为什么不适用，而不是省略。
3. `prd.md` 的 `Eval Plan` 必须先定义行为验收、证据、失败判据，再允许补 truth-source review。
4. verification / closeout / replay 能从 `pre-tests.md` 恢复出应跑什么、在哪个环境跑、哪些证据算通过。

## Tensions

- 不能把“真环境测试必做”误写成“每条 issue 都必须发明新的脚本测试”；有些应是 runtime dogfood scenario，而不是单元脚本。
- 不能只强化 wording；必须让 IBM artifact 本身更难写出弱验收。
- 不能把已有 `integration-acceptance-first` 规则推翻重写；这条更像是 enforcement / executable acceptance contract 的下一层。

## Likely Landing Zones

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- 视需要补 `three-loop-capability-lifecycle.md` 或 verification truth source

## Working Hypothesis

下一条能力不该只是“提醒写更好的 pre-tests”，而应把下面这些 contract 写死：

- `pre-tests.md` 至少显式覆盖：
  - pre-merge focused regression / smoke
  - post-merge integration / real-environment / end-to-end acceptance
  - non-goals / out-of-scope
  - 失败判据与所需证据
- 对 governance / agent / skill issue，也必须回答：
  - 在真 runtime 中如何观察 manager / worker / patrol 行为变化
  - 用什么 interruption / patrol / replay 场景证明 contract 生效
  - 如果只能 merge 后验证，目标环境是 `develop` 还是 `pre-test-merge`

## Open Questions

1. 是否需要给 `pre-tests.md` 增加更 machine-readable 的固定段，如 `environment`, `evidence`, `failure_signal`, `replay_expectation`？
2. 是否需要把 “application-native real-environment testing” 与 “integration testing” 分成两个显式栏位，避免被一个笼统的 `post-merge acceptance` 淹掉？
3. 这条能力应先收敛到 IBM truth source，还是需要同步改 verification review 模板，防止下游继续按弱验收 closeout？

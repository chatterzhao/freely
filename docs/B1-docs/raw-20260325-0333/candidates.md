# Candidates - 20260325-0333--testing-evidence-ladder-and-real-environment-gates

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260325-0333-A: legacy issue
- candidate_format_version: v2
- title: Testing evidence ladder and real-environment gates for Freely
- problem: Freely 已经把 `pre-tests.md` 固定成 issue-level acceptance 控制面，但仍缺少一套统一、可执行、可恢复的测试能力 contract，去定义 script regression、integration、end-to-end、application-native real-environment 与 protected-env acceptance 各自的职责、最低证据 bar，以及它们如何进入 completion / promote / retirement gate。结果就是：本地测试可能都过了，但真实 runtime/dogfood 仍会暴露关键缺口；而这些缺口当前只能事后通过新 issue 回补。
- why_now: 近期连续暴露的 parser drift、runtime churn、launch-state truth、账号恢复与 slot 语义问题，都说明 Freely 的关键风险并不只存在于脚本级测试。Freely 是 AI 自己开发项目的工具，测试作为硬门禁不能只停留在 issue 局部经验；它必须上升成 Freely 可复用的能力。
- acceptance_criteria:
  - 明确“每个 story 下的 `pre-tests.md` 质量”本身就是第一层 gate；若它不足以恢复 acceptance contract，则后续测试执行不得被计作完成 closeout
  - 先产出一份 absorbed capability inventory，明确当前仓库里哪些 issue/skill/runtime truth 已经分别规范了 `pre-tests.md`、integration acceptance、live integration、artifact-plane acceptance evidence 与 protected-env acceptance
  - 冻结一份 testing evidence ladder，至少覆盖 `script regression`、`integration`、`end-to-end`、`application-native real-environment`、`protected-env post-merge acceptance`
  - 为每一级测试定义默认用途、升级触发条件与不能替代的边界，而不是允许 issue 自由发挥
  - 明确 completion verification 与 worktree retirement 各自最低需要哪一级测试证据，且缺证据时必须能 machine-readably 阻断“已完成”判断
  - 冻结每个 story 下 `pre-tests.md` 的最低质量线，至少要能表达 acceptance target、测试层级、目标环境、必需证据与 blocker 分类，而不是只给命令清单
  - 明确哪些问题类别默认必须提升到 application-native real-environment，至少包括 manager/runtime/interruption/worker orchestration 这类只有真实运行态才能稳定暴露的问题
  - 明确测试能力真源的最小落点：脚本测试、scenario/e2e harness、真实环境验收留痕、以及 runtime/status surface 只镜像最小摘要与 `acceptance_ref`
  - 明确 `pre-tests.md`、code-review、progress、artifact plane 与 runtime/status surface 之间的分工，不新增平行真相系统
  - 形成一条可 materialize 的 follow-on 路线，而不是把“测试要更强”停在口号层
- promotion_gate:
  - `./inventory.md` 已吸收现有真源，并把 follow-on materialization 顺序收敛到最小切口，而不是继续停在笼统目标
  - 冻结 testing evidence ladder 的分层与命名，不与旧 issue 的局部表述冲突
  - 冻结 story-level `pre-tests.md` 质量线，避免后续 issue 把它退化成“命令列表”或“测试 TODO”
  - 冻结 completion / promote / retirement 与测试证据的映射规则
  - 冻结 application-native real-environment 的最小定义，避免把“人工随便 dogfood 一下”误记为同等级证据
  - 冻结哪些能力目录将承载脚本测试、scenario/e2e harness 与真实环境留痕
  - 冻结与现有 `pre-tests.md` / protected acceptance / artifact plane 的衔接点
- open_questions:
  - 是否需要独立的 `testing capability` 目录，还是继续先收在 `docs/system/workspace/scripts/tests/**` 与引用文档中
  - end-to-end 与 application-native real-environment 之间的边界如何稳定表达
  - manager/runtime 是否需要新增最小 machine-readable `testing_closeout_state`，还是只镜像 artifact plane 摘要即可
  - 哪些 issue family 可以在没有真实环境测试的情况下仍然完成，判据应该如何枚举
  - 测试门禁是只在 completion / retirement 生效，还是也要更早进入 materialization / promote guard
- acceptance_reviews:
  - reviewer: `codex`
    mode: `initial candidate acceptance review`
    summary: `This is broader than stale pre-test-merge governance and protected acceptance routing. It needs its own candidate so Freely can turn dogfood-exposed test gaps into a reusable capability contract.`
    verdict: `ready_for_pre_brainstorm`
- priority: P0
- status: promoted
- decision_reason: Slice 1 (C-20260325-0333-B) 已完成并验证通过。Slice 2 (I-20260519-0333-C, testing evidence ladder and gate mapping) 已完成 dev-loop 实现，B2_IBM 产物已验证验收，slice 通过全部验收标准。
- promoted_issue_path: `docs/issues/I-20260519-0333-C/issue.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: Slice 2 (I-20260519-0333-C) 已完成 dev-loop 实现并 closed。剩余切口的 Slice 3（real-environment harness contract）和 runtime mirror 推迟到后续 umbrella 决策。
- revisit_trigger: 当 I-20260519-0333-C dev-loop 完成后，评估是否需要继续 Slice 3（real-environment harness contract），或将 umbrella candidate 标记为 partially_absorbed。
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

### C-20260325-0333-A: legacy issue
- candidate_format_version: v2
- title: Story-level pre-tests quality gate governance
- problem: Freely 已明确 `pre-tests.md` 是 issue-level acceptance 控制面，但还没有冻结 story-level 最低质量线，导致 commands-only 或 acceptance-target 缺失的 `pre-tests.md` 仍可能形式上“存在”，却无法真正定义测试与验收边界。
- why_now: 若不先冻结 story-level `pre-tests.md` 质量 gate，后续 testing evidence ladder、gate mapping、real-environment harness 都会建立在不稳定的 acceptance 定义上。这个切口是当前 umbrella candidate 中最小、最先必须落地的 slice。
- acceptance_criteria:
  - Freely 真源明确每个 story 下的 `pre-tests.md` 若不能恢复 acceptance contract，则不得视为合格的 acceptance 控制面
  - 真源明确 story-level `pre-tests.md` 至少要覆盖 acceptance target、testing layer、target environment、required evidence、blocker taxonomy
  - 真源明确 commands-only `pre-tests.md` 不合格
  - 真源明确区分 `pre-tests.md` 质量失败 与 测试执行失败/未执行
  - 这条质量线与既有 integration-acceptance-first、artifact-plane acceptance evidence、protected/post-merge verification contract 对齐
- promotion_gate:
  - 最低字段与退化判据被冻结成稳定口径
  - 质量失败与执行失败的 blocker 区分被冻结成稳定口径
  - 与既有 truth sources 的衔接点被冻结，不另造平行 truth
- open_questions:
  - 质量 gate 是主要落在 IBM references，还是还需要同步进入 three-loop capability lifecycle
  - 是否需要在后续 follow-on 中再增加 machine-readable testing closeout summary
- acceptance_reviews:
  - reviewer: `codex`
    mode: `materialization review`
    summary: `This is the narrowest first slice from the umbrella testing candidate and is ready to become a milestone-owned issue.`
    verdict: `ready_for_issue_materialization`
- priority: P0
- status: completed
- decision_reason: 这条 slice 足够小，已经可以从 umbrella candidate 中独立 materialize，先把 `pre-tests.md` 质量 gate 固定成硬门禁，再继续后续 ladder / harness 切口。
- promoted_issue_path: `docs/B2-docs/ibm/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- completion_note: Story-level `pre-tests.md` 质量 gate 已进入 capability truth，blocker taxonomy 已冻结，verification 已 pass
- next_action: 本 slice 已完成；后续 testing ladder / real-environment harness 切口由 umbrella candidate `C-20260325-0333-A` 继续承接
- revisit_trigger: 当 issue dev-loop 需要继续扩到 testing ladder / real-environment harness 时，停止在本 slice 内扩 scope，回到 umbrella candidate 判断后续切口
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

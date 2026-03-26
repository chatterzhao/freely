# Candidates - 20260322-1801--pre-test-merge-governance-lifecycle

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260322-1801-A
- title: pre-test-merge responsibility, usage, and lifecycle governance
- problem: `pre-test-merge` 现在同时被用作临时预集成验证批次、真实验收环境的比较基线，以及旧实现回收的中间站，但职责边界、允许操作、失效条件和退休条件都没有被明确收束。
- why_now: 这次分叉直接暴露出 `pre-test-merge` 的生命周期管理不足。如果不先收口，它会继续把“验证批次”和“事实主线”混在一起，造成有效实现难以判断该保留还是该回收。
- acceptance_hint:
  - 明确 `pre-test-merge` 只是临时预集成验证批次，而不是长期开发父分支
  - 明确哪些动作允许、哪些动作禁止、哪些情况必须退役当前批次
  - 明确 stale batch 的判定信号，以及 `develop` 前进后是否需要重建批次
  - 明确 promote 语义是保留批次快照，还是 replay 来源 feature
  - 明确这套判断能被 Freely 自己消费，而不是只靠人工记忆
- priority: P0
- status: promoted
- decision_reason: 这是治理定义问题，不是 runtime 修补问题。它决定 Freely 后续如何使用 `pre-test-merge`，而不是单次如何合并。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

### C-20260322-1801-B
- candidate_format_version: v2
- title: pre-test-merge lifecycle management capability for Freely
- problem: 即使治理规则写清了，Freely 仍缺少把 stale `pre-test-merge` 收口成治理事务的能力：它需要 machine-readable stale state、manager lifecycle transaction、runtime gate，以及可追溯的 replay/retire evidence，而不是继续靠人工判断。
- why_now: 这次问题已经证明“只靠人记住规则”不够。Freely 作为未来的开发工具，需要把这套判断 materialize 成可执行能力，才能避免下一次再次手工误用。
- acceptance_criteria:
  - manager 在 stale `pre-test-merge` 上写出唯一 machine-readable stale state，且真相面可被 continuity / status surface / runtime gate 一致消费
  - 一旦 batch 被判 stale，它就不再是 active verification truth surface；后续只允许 read-only cleanup / retire / rebuild planning
  - stale 后 manager 继续使用既有 `ownership / restart_point / next_action` 词典，但必须补齐 `replay source manifest`、`replay order`、`retire evidence`、`remaining cleanup requirement`
  - manager patrol 在 stale batch 上必须显式给出 `stale_batch -> retire/rebuild` 或更细的过渡治理事务，不能静默继续普通 verification
  - runtime 对 stale batch 只允许 read-only patrol、cleanup handoff、rebuild/replay handoff，不再把它恢复成普通 verification 会话
  - watchdog 仍只负责 runtime recovery，不负责决定 validation batch legitimacy；batch legitimacy 只能消费 manager 已写出的治理真相
  - 所有指向 stale batch 的旧 queued worker prompts / delegated launches 都会被 supersede 或失效，不再继续消费旧 prompt 池
  - 若同一能力仍需继续验证，必须 replay 来源 feature 集合到 fresh `pre-test-merge` batch，而不是复用旧 stale batch 继续跑
  - 反滥用默认值必须固定：默认提升路径仍是 `feature/* -> develop`；只有当 `pre-tests.md` 显式声明 `integration_target=pre-test-merge` 或当前问题确属主线前组合验证时，manager 才可把 lane 路由到 `pre-test-merge`
  - 只能使用现有状态与 gate 组合判断是否继续推进或删树：`done_ibm`、`completed`、cleanup gate、`verified-retirable`、`retired`；其中 `completed` 只代表 issue completion，不代表 delete-eligible，stale retire/rebuild 不得只依据 issue `completed` 或局部 loop 收口
  - 上述 contract 优先落在现有真源：manager continuity 为唯一治理真相面，`manager-worker-launch-state.env` 与 `live-status` 仅做消费镜像，不新增平行状态文件
  - manager continuity 必须带批次身份锚点与固定承载语法，至少包括 `validation_batch_id`、`integration_target`、`source_batch_base`，并以固定可解析块承载，而不是自由文本
  - 当前固定承载语法先冻结为 manager continuity 中连续的 `Validation batch governance:` `v1` 块，标题下每行固定为 `- key: value`，并保持固定 key 顺序
  - manager continuity 还必须固定承载 `acceptance_contract_state`、`acceptance_contract_source`、`acceptance_contract_blocker`，把 IBM acceptance 完整性桥接成 runtime 可消费字段，而不是让 runtime 读取 issue/brainstorm/prd 自行推理
  - runtime 在应用旧 prompt supersede 后，必须留下 machine-readable `superseded_worker_prompts_applied_at` 或等价信号，证明旧 prompt 已停止被消费
  - 当 issue 的 `I + B + PRD -> pre-tests.md` 派生链不足以恢复 issue-level acceptance、显式声明的 `post-merge acceptance`，或目标验证环境时，manager 必须写出 `acceptance_contract_state=incomplete` 与 blocker，而不是让 stale/retire 流程伪装成“只剩执行”
  - `pre-tests.md` 质量检查与 testing closeout 必须分开建模：前者确认 acceptance contract 是否完整，后者确认 acceptance 是否已真实执行并留痕
  - testing closeout 默认优先 integration / end-to-end 与 application-native real-environment testing evidence；若缺少这些证据，不得把 lane 判成 `completion_verification done` 或允许 worktree retirement
  - 必须固定一条最终完成检查顺序：`done_ibm` 之后先过 `pre-tests.md` 质量 gate，再做 dev / verification / testing closeout，逐项完成 `pre-tests.md` 后 issue 才可 `completed`；此后仍需继续经过 merge / cleanup evidence / `verified-retirable`，并且仅当 `pre-tests.md` 显式声明时才追加 `post-merge acceptance`，最后才允许 delete worktree / branch
  - 必须把三层 loop 的跳出语义固定下来：doc-loop 只负责把 candidate/IBM 推到可交给下一层；dev-loop 只负责把 issue 推到 `completed` 或回流新边界；cleanup/auto-loop governance 才负责把 worktree/branch 推到 `retired`，任何局部 loop 收口都不得冒充主题最终完成
  - `can merge to develop` 必须与 `issue completed` / `worktree retired` 分离：merge gate 只回答“当前 feature 是否可提升”，不能被误读成“任务已完成”
  - 若 merge 已发生但 delete eligibility chain 尚未闭合，manager 必须显式把后续 closeout materialize 为 delegated continuation / cleanup lane，或把 issue 挂回 milestone/owner queue 并写清 `next_action` / `revisit_trigger`；不得在 merge 后静默消失
  - 若 merge / cleanup / `verified-retirable` / `retired` 链条尚未闭合，即使 issue 已 `completed`，也不得删除最后一个 owner worktree
  - 最终 delete worktree / branch 必须有单独删除门；若未来以 hook / guard 投影执行，该门只能消费已有状态与 evidence 组合，不得重造一套平行 completion 状态
  - 当前字段级冻结草案以 `combined minimal contract v0` 为准：manager continuity 最少承载 `validation_batch_id`、`validation_batch_state`、`validation_batch_mode`、`stale_reason`、`lifecycle_decision`、`integration_target`、`source_batch_base`、`replay_source_manifest`、`replay_order`、`retire_evidence_ref`、`remaining_cleanup_requirement`、`acceptance_contract_state/source/blocker`、`superseded_worker_prompts`、`superseded_worker_prompts_applied_at`
  - 当前 fresh-batch followthrough 的 machine-readable absorption contract 明确冻结为：`retire_evidence_ref + remaining_cleanup_requirement is the canonical machine-readable absorption pointer for fresh-batch followthrough, and no extra machine-readable pointer is required.`
- promotion_gate:
  - 冻结 stale 判定的最低 machine-readable 字段、真相面和消费路径
  - 冻结 manager lifecycle transaction 与现有 patrol 词典的映射，不新增平行状态系统
  - 冻结 replay source manifest / replay order / retire evidence 的最小 schema
  - 冻结 `pre-test-merge` 的反滥用默认路由：未命中显式 `integration_target=pre-test-merge` 或主线前组合验证需求时，不得把它当默认验证面
  - 冻结 `superseded_worker_prompts` 与 stale batch gate 的联动，保证旧 queued prompt 不会继续被 runtime 消费
  - 冻结 `validation_batch_mode=read_only_cleanup|rebuild_planning`，确保 `collect_cleanup_evidence` 不会被误读成恢复普通 verification
  - 冻结 `Validation batch governance:` `v1` 固定块、必留 key 与 key 顺序，并证明 runtime / cleanup skill 只靠该块就能稳定读到最小治理字段
  - 明确 `Issue + Brainstorm + PRD -> pre-tests.md` 派生链与 stale governance 的连接点，避免把 acceptance contract 缺失误修成纯 runtime stale 判定
  - 冻结 issue completion chain 与 delete eligibility chain 的分段语义，证明 `completed` 只表示 issue 完成，不表示 worktree / branch 已可删除
  - 冻结三层 loop 的进入/跳出/最外层结束条件，证明只有 cleanup/auto-loop governance 闭合并到 `retired`，当前主题才从 active lifecycle 中退出
  - 冻结 testing closeout 的最低 evidence bar，明确 application-native real-environment testing 属于主验证面；Freely self-host 时其当前实例才是 `freely chat`
  - 冻结最终 delete worktree / branch 门禁的最小输入组合与拒绝语义，并判断它是否应由现有 hook / guard 投影兜住
  - 用 `specimen-S1/S2/S3` 的 field audit/evidence 证明 delete gate 会拦住至少三类误删：`merged + clean` 误删、issue `completed` 误删、stale batch source/replay evidence 尚未吸收时的误删
  - 证明 `post-merge acceptance` 只有在 `pre-tests.md` 显式声明时才进入 delete eligibility chain，而不是默认必经 gate
  - 完成一轮针对 `combined minimal contract v0` 的独立 acceptance review，确认 supporting pools 仍只支持 `stay_pre_brainstorm` 或已经足够升级到 IBM，而不是在当前 worker round 里靠作者自证
  - 冻结并独立复核 `retire_evidence_ref + remaining_cleanup_requirement` 的 no-extra-pointer 等价 contract，证明 runtime gate、cleanup handoff 与 delete guard 不需要额外 machine-readable absorption pointer
- final_sufficiency_closeout:
  - evidence_group: `validation_batch_governance_v1`
  - required_proof: `Validation batch governance:` `v1` 固定块、必留 key 与 key 顺序已经冻结，且 manager continuity 作为唯一治理真相面时，runtime/status/cleanup 读取不需要额外平行状态文件
  - current_state: `contract shape frozen; remaining gap is one explicit proof bundle showing the 17-key v1 block is sufficient as the only machine-readable truth surface and does not need a parallel state file`
  - next_step: `author this as the first closeout block and keep the proof scoped to manager continuity -> runtime/status/cleanup consumption only`
  - evidence_group: `runtime_gate_behavior`
  - required_proof: stale batch 不能再以 normal verification surface 启动；runtime 只允许 read-only cleanup / retire / rebuild planning，并且 superseded worker prompt 已留下可追溯 applied evidence
  - current_state: `route intent is stable, but proof is still narrative; the remaining gap is a minimal refusal contract that says stale batches cannot boot back into normal verification even when runtime recovery is otherwise healthy`
  - next_step: `freeze the smallest refusal semantics and applied-evidence specimen without turning watchdog into stale-batch owner`
  - evidence_group: `replay_retire_evidence`
  - required_proof: `replay_source_manifest`、`replay_order`、`retire_evidence_ref`、`remaining_cleanup_requirement` 足以表达 retire/rebuild/fresh-batch followthrough，且 no-extra-pointer 等价 contract 已被独立复核
  - current_state: `no-extra-pointer equivalence is already frozen; remaining work is to prove that replay source + retire evidence + remaining cleanup requirement form a complete followthrough handoff without another absorption pointer`
  - next_step: `write one minimal replay/retire matrix that distinguishes retire-now, rebuild-planning, and fresh-batch followthrough from generic cleanup narrative`
  - evidence_group: `acceptance_bridge`
  - required_proof: `acceptance_contract_state/source/blocker -> pre-tests.md` 的桥接稳定，能把 acceptance contract 缺口与 testing closeout 缺口分离，而不把 stale governance误收缩成纯 runtime gate 问题
  - current_state: `bridge direction is stable, but the candidate still needs a single closeout note that separates IBM acceptance incompleteness from runtime stale-batch enforcement and from post-merge testing closeout`
  - next_step: `freeze the acceptance bridge as a small state split, not a new owner search: missing acceptance contract, missing testing closeout, and stale-batch governance must remain distinct`
  - evidence_group: `delete_refusal_specimens`
  - required_proof: `specimen-S1/S2/S3` 能分别证明 `merged + clean`、issue `completed`、以及 stale source manifest 未被 fresh owner 吸收三类情形都必须 `delete_denied`
  - current_state: `specimen classes are fixed, but the candidate still lacks one condensed delete-denied proof set showing that git-cleanliness, issue completion, and stale-source evidence do not satisfy delete eligibility by themselves`
  - next_step: `close with one refusal-specimen table keyed to specimen-S1/S2/S3 and the existing completed/cleanup/verified-retirable/retired chain`
- open_questions:
  - `develop` 前进、protected-env 独有差异、cleanup/replay 证据未齐三者的优先级如何定义
  - stale 后哪些过渡动作被允许保留在 manager-owned lane 中，哪些必须直接进入 rebuild/cleanup
  - `replay_plan_state=pending|complete` 是否足够表达 manifest 已冻结但仍待执行的状态
  - manager 识别 IBM acceptance 缺口时，是否只消费已有 issue/brainstorm/prd/pre-tests artifact，还是需要额外的 IBM completion signal
  - `acceptance_contract_blocker` 的枚举是否还要覆盖 `missing_pre_merge_acceptance` 或 `missing_protected_env_boundary`
  - testing closeout 的 machine-readable evidence 应落在 issue / code-review / progress / runtime 哪个组合面，才能既可恢复又不制造平行真相
  - 是否只靠现有 `phase_state + cleanup gate + verified-retirable/retired evidence` 就足够，还是仍需更明确的 machine-readable 组合提示
  - 最终 delete guard 若落到 hook / guard，应该拦截本地 branch/worktree 删除、远程 branch 删除，还是两者都要管
  - 在不新增额外 machine-readable pointer 的前提下，哪一组最小 specimen / review evidence 足以证明 runtime gate、cleanup handoff 与 delete guard 都能稳定消费这条 frozen equivalence
  - `combined minimal contract v0` 是否已经足够小，可以从 pre-brainstorm 升级成单一 IBM issue，而不是再做一轮 supporting-pool 对读
- acceptance_reviews:
  - reviewer: `codex + subagent panel (Erdos/James/Singer)`
    mode: `independent candidate acceptance review`
    summary: `Direction valid; contract had to be narrowed to stale-batch governance, then frozen further around manager continuity truth surface, IBM-to-manager acceptance bridge, replay/retire evidence, and testing closeout bar.`
    verdict: `needs_more_contract_work_before_materialization`
  - reviewer: `gpt-5.4-mini explorer supporting-pool scan`
    mode: `independent route verification`
    summary: `Milestone, completed issue, semantic-audit artifacts, delegated continuation intake/prompt evidence, and the absence of any stronger progress/recovery/github-issue owner all reinforce that C-20260322-1801-B remains a pre-brainstorm candidate; no supporting pool cleanly upgrades it to IBM yet.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-with-handoff continuity review`
    mode: `independent candidate acceptance review`
    summary: `After re-reading the canonical pre-brainstorm, milestone, live-status, and supporting pools in the fresh session, the route still stays at pre-brainstorm. The remaining gap is no longer whether to review, but whether the manager continuity block syntax and delete-gate specimen evidence are frozen enough to materialize as a single IBM issue.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer contract-freeze review`
    mode: `independent candidate acceptance review`
    summary: `The route still stays at pre-brainstorm. The smallest remaining freeze item is the fixed machine-readable manager continuity block plus specimen/evidence proving it is sufficient for runtime gate and cleanup/delete decisions; until that is stable, the capability should not enter IBM.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool rescan`
    mode: `independent route verification`
    summary: `No canonical owner outside pre-brainstorm cleanly absorbs this lane yet: milestone still keeps C-20260322-1801-B as candidate, the completed issue remains explicitly bounded, progress/recovery/github-issue pools do not own it, and the handoff-referenced manager continuity artifact is missing in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex + explorer second-round acceptance review`
    mode: `independent candidate acceptance review`
    summary: `The route still stays at pre-brainstorm. The contract is materially tighter, but two blockers remain before IBM: whether retire_evidence_ref plus remaining_cleanup_requirement are sufficient to express fresh-batch absorption without another machine-readable pointer, and one more independent acceptance review must confirm the current delete-gate and validation-batch contract is stable enough to materialize.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer continuation supporting-pool rescan`
    mode: `independent route verification`
    summary: `This worker-round rescan found no stronger canonical owner outside pre-brainstorm: milestone still keeps only a candidate, I-20260322-1801 remains explicitly bounded, the 20260322-1802 audit is only supporting evidence, no docs/recovery owner exists, and no docs/progress artifact absorbs the lane. The missing handoff-referenced manager continuity file in this worktree reinforces that the contract freeze is still not stable enough to treat as IBM input.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-session first-jump revalidation`
    mode: `independent candidate acceptance review`
    summary: `After replaying the first-jump chain in a fresh session against AGENTS, CONSTITUTION, LAWS, PROJECT_INTENT, lead-agent, context-source-skill, milestones, and the current worktree state, the lane still resolves to continuation -> pre_brainstorm -> doc-pre-brainstorm-execution. Current hygiene does not force checkpoint or reroute, but no new canonical owner or stable IBM boundary appeared; the missing manager continuity artifact remains a freeze gap, not promotion evidence.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex live-status continuity revalidation`
    mode: `independent supporting-pool verification`
    summary: `Current live-status confirms the worker absorbed the delegated continuation in the current run: pending delegated continuations are empty, current_prompt_has_delegated_continuation=1, and consumed IDs cover 20260324-024929/024942/025910/030713. The same output still shows latest_manager_continuity_generated/consumed as unavailable, and the active launch metadata remains last_launch_kind=fresh_with_handoff and last_rotation_reason=context_compacted. That keeps runtime evidence in the same role: continuation-consumption mirror only, not a new IBM-ready canonical owner.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-batch-absorption review`
    mode: `independent candidate acceptance review`
    summary: `The lane must stay in pre-brainstorm. The added review does not find a stronger canonical owner or stable IBM boundary, and it sharpens the remaining blocker: retire_evidence_ref plus remaining_cleanup_requirement are still not sufficient to prove fresh-batch absorption has closed without an additional machine-readable pointer or an explicitly frozen equivalent contract.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-session continuity artifact refresh`
    mode: `independent candidate acceptance review`
    summary: `A current-session revalidation against the assigned worktree kept the route at pre-brainstorm: git hygiene still shows only the three canonical doc-loop files dirty, develop...HEAD is now 46 left / 15 right, live-status still reports pending delegated continuations as none while latest manager continuity remains unavailable, and no stronger owner appeared outside the candidate.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-owner scan`
    mode: `independent supporting-pool verification`
    summary: `No stronger canonical owner exists outside pre-brainstorm: the completed governance issue and its verification/pre-tests still keep follow-on stale-lifecycle capability as a separate lifecycle, intake/runtime evidence continues to route this lane back into C-20260322-1801-B, docs/progress only owns a separate continuity-consumption issue, and docs/recovery is absent in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool closure scan`
    mode: `independent supporting-pool verification`
    summary: `The latest supporting-pool scan still finds no stronger canonical owner outside pre-brainstorm. Milestone remains the strongest owner, the completed governance issue still keeps lifecycle management as a separate follow-on lifecycle, docs/progress only owns the continuity-consumption lane, and runtime/session evidence keeps the worker at continuation -> pre_brainstorm while the referenced manager continuity artifact remains missing in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex same-tool first-jump replay`
    mode: `independent route verification`
    summary: `Replaying AGENTS, CONSTITUTION, LAWS, PROJECT_INTENT, milestones, tools, lead-agent, context-source-skill, and doc-pre-brainstorm-execution kept the priority on milestone plus supporting pools and selected codex again because the work is still canonical doc-loop writeback inside the assigned feature worktree. Since selected_tool equals the active AI tool, the lane must continue in-session instead of stopping at next_prompt handoff, and no stronger owner or IBM-ready boundary appeared.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool ownership check`
    mode: `independent supporting-pool verification`
    summary: `No stronger canonical owner appeared outside C-20260322-1801-B. The completed issue and its verification still keep lifecycle management as a separate later lifecycle, the nearby progress artifact only owns latest manager continuity consumption timing, and .freely/run evidence still routes this lane back to the current candidate. The missing manager-continuity-20260324-021853.md matters only as missing provenance, not as contradictory ownership evidence.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex delegated-continuation closure refresh`
    mode: `independent supporting-pool verification`
    summary: `Current live-status plus the current run prompt_file confirm the worker is already executing the superseding delegated-continuation bundle in-session instead of leaving it as pending handoff. That still does not promote the lane: latest manager continuity remains unavailable, milestone/progress/issue pools do not provide a stronger owner, and the route stays continuation -> pre_brainstorm -> doc-pre-brainstorm-execution.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer ownership-and-freeze-gap scan`
    mode: `independent supporting-pool verification`
    summary: `The lane still belongs to C-20260322-1801-B. Milestone keeps it as candidate/in_pre_brainstorm, the completed issue and its IBM brainstorm keep lifecycle management as a later lifecycle, and the nearby progress artifact only owns latest manager continuity consumption timing. Runtime/session-state evidence still shows only a worker-consumption mirror, not IBM-ready ownership. The remaining freeze gap is still whether fresh-batch absorption needs an extra machine-readable pointer or an explicitly frozen equivalent contract.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer canonical-owner recheck`
    mode: `independent supporting-pool verification`
    summary: `A fresh read-only explorer pass again found no stronger canonical owner outside C-20260322-1801-B: milestone still keeps only a candidate, the completed governance issue explicitly leaves lifecycle management as a separate follow-on lifecycle, the neighboring progress doc only owns continuity-consumption timing, and live-status/runtime evidence remains continuation-consumption mirror only while the referenced manager continuity artifact is still missing in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer post-handoff reconfirmation`
    mode: `independent supporting-pool verification`
    summary: `The latest read-only subagent recheck after session handoff still found no stronger canonical owner than C-20260322-1801-B. Semantic-audit artifacts remain supporting evidence only, the neighboring progress doc still owns only manager-continuity consumption timing, and the single remaining freeze gap is still whether fresh-batch absorption needs an extra machine-readable pointer or an explicitly frozen equivalent contract.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool boundary check`
    mode: `independent supporting-pool verification`
    summary: `A read-only supporting-pool pass that also checked the completed issue's pre-tests and verification review still found no stronger owner than C-20260322-1801-B. Those artifacts deepen the acceptance and quality boundary for the already completed governance issue, but they do not absorb stale pre-test-merge lifecycle management as a new IBM-ready issue. The main freeze gap remains fresh-batch absorption proof: add an extra machine-readable pointer, or explicitly freeze and independently verify that retire_evidence_ref plus remaining_cleanup_requirement are sufficient without one.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session IBM-readiness check`
    mode: `independent candidate acceptance review`
    summary: `A fresh-session read-only review again kept the lane in pre-brainstorm. The strongest canonical owner is still C-20260322-1801-B plus its matching milestone candidate entry; the completed governance issue and acceptance-first issue only stabilize adjacent boundaries. Remaining freeze gaps are unchanged: fresh-batch absorption still needs either an extra machine-readable pointer or an explicitly frozen equivalent contract, the Validation batch governance v1 block and acceptance bridge still need stable independent proof, and specimen-S1/S2/S3 still have to prove the delete-eligibility chain separately from issue completion.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-session canonical-owner recheck`
    mode: `independent candidate acceptance review`
    summary: `A current-session read-only explorer pass again found no stronger canonical owner than C-20260322-1801-B. Milestone still keeps it in candidate/in_pre_brainstorm, the completed governance issue remains explicitly narrower, supporting progress/audit artifacts do not absorb ownership, and IBM readiness is still blocked on the fresh-batch absorption freeze gap.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-worktree canonical-owner cross-check`
    mode: `independent candidate acceptance review`
    summary: `A second read-only cross-check in the current worktree again confirmed that C-20260322-1801-B remains the strongest canonical owner. Milestone still keeps the lane in candidate/in_pre_brainstorm, the completed governance issue still stops at role-definition rather than lifecycle capability implementation, and the only dirty files are the same 3 canonical doc-loop artifacts, so no conflicting owner or IBM-ready fact emerged.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex governance precheck replay`
    mode: `independent route verification`
    summary: `Re-reading AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, tools, lead-agent, context-source-skill, and doc-pre-brainstorm-execution kept the lane at continuation -> pre_brainstorm -> doc-pre-brainstorm-execution. The prompt-required constitution/law precheck still held even though this worktree does not expose standalone constitution-guard or laws-enforcer skill files; direct document-level enforcement produced the same boundary, and current hygiene still shows only the 3 canonical doc-loop files dirty with develop...HEAD at 46 left / 15 right.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer final supporting-pool freeze-gap verdict`
    mode: `independent candidate acceptance review`
    summary: `A final current-session read-only scan again found no stronger canonical owner than C-20260322-1801-B. The completed issue remains explicitly narrower, the semantic audit is supporting evidence only, the nearby progress artifact owns a different issue, and the single highest-value remaining freeze gap is still fresh-batch absorption proof: either add an extra machine-readable pointer, or independently freeze and verify that retire_evidence_ref plus remaining_cleanup_requirement are sufficient without one.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-batch-equivalence freeze review`
    mode: `independent candidate acceptance review`
    summary: `Freezing the no-extra-pointer route is necessary but not sufficient. The contract must state verbatim that retire_evidence_ref plus remaining_cleanup_requirement is the canonical machine-readable absorption pointer for fresh-batch followthrough, and after freezing that equivalence one more independent acceptance review is still required before IBM materialization.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex same-session continuity refresh`
    mode: `independent supporting-pool verification`
    summary: `A current-run refresh kept the lane in pre-brainstorm while replacing stale handoff facts with repository truth: the assigned worktree now has only the 2 canonical doc-loop files dirty, develop...HEAD is 53 left / 22 right, live-status still reports last_launch_kind=fresh_with_handoff and last_rotation_reason=context_compacted, and delegated continuation consumption is still fully absorbed in the current prompt while manager continuity remains unavailable. That keeps runtime evidence in the same role: worker-consumption mirror only, not a stronger owner or IBM-ready boundary.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool owner recheck`
    mode: `independent candidate acceptance review`
    summary: `A fresh read-only supporting-pool recheck confirmed that C-20260322-1801-B remains the strongest canonical owner. The completed issue still stops at role-definition, the neighboring progress artifact owns only delegated-continuation consumption timing, the handoff-referenced manager continuity artifact is still missing, and the new develop...HEAD=53/22 fact only reinforces stale-batch divergence without closing the fresh-batch absorption freeze gap.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-session dirty-truth refresh`
    mode: `independent supporting-pool verification`
    summary: `A fresh-session writeback refresh kept the lane in pre-brainstorm while correcting the latest continuity facts to the current repository state: the assigned worktree now has only the 2 canonical doc-loop files dirty, develop...HEAD remains 53 left / 22 right, live-status still shows fresh_with_handoff plus context_compacted with delegated continuation already consumed, and the handoff-referenced manager continuity artifact is still missing. That keeps runtime evidence as consumption mirror only, not a stronger owner or IBM-ready boundary.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool independent gap check`
    mode: `independent supporting-pool verification`
    summary: `A fresh read-only pass over the completed governance issue, semantic-audit artifacts, neighboring progress doc, and the missing manager continuity file again found no IBM-ready owner outside C-20260322-1801-B. The completed issue remains only the strongest supporting formal artifact and still explicitly leaves lifecycle management as a later lifecycle. The smallest remaining gap stays the same: freeze how stale detection, retire, and rebuild are materialized into a dedicated issue contract instead of inferring them from supporting pools.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex first-hop continuation absorption refresh`
    mode: `independent supporting-pool verification`
    summary: `Re-running the current first-hop loop kept the lane at continuation -> pre_brainstorm -> doc-pre-brainstorm-execution. Current repository truth is narrower than the previous continuity note: git now shows only 2 canonical doc-loop files dirty with develop...HEAD at 68 left / 23 right, live-status reports role_hint=worker with activity_state=ai_active, last_launch_kind=fresh_with_handoff, last_rotation_reason=context_compacted, pending delegated continuations already empty, consumed IDs covering 20260324-024929/024942/025910/030713, and latest manager continuity still unavailable. That keeps runtime evidence as a consumption mirror only, while milestones, the completed governance issue, the neighboring progress doc, and the missing manager continuity file still leave C-20260322-1801-B as the strongest canonical owner.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer frozen-equivalence readiness review`
    mode: `independent candidate acceptance review`
    summary: `The lane still belongs to C-20260322-1801-B and must remain in pre-brainstorm. The strongest owner is unchanged, the handoff-referenced manager continuity artifact is still missing, and the progress doc still owns only delegated-continuation consumption timing. Most importantly, the no-extra-pointer fresh-batch absorption equivalence was still treated as pending rather than frozen inside the candidate contract, so IBM remains blocked until that equivalence is written into the canonical acceptance boundary and then rechecked by another independent review.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer post-freeze sufficiency review`
    mode: `independent candidate acceptance review`
    summary: `After the no-extra-pointer equivalence was frozen into the canonical contract, the lane still stays in pre-brainstorm. Milestone still marks C-20260322-1801-B as candidate/in_pre_brainstorm, the completed governance issue still leaves lifecycle management as a follow-on lifecycle, and live-status still shows only fresh-with-handoff continuation consumption while latest manager continuity remains unavailable. The remaining blocker is no longer whether to add another absorption pointer; it is whether the already frozen minimal contract has enough independent proof that Validation batch governance v1, runtime gate behavior, and cleanup/delete refusal evidence are sufficient to materialize.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer pre-IBM sufficiency recheck`
    mode: `independent candidate acceptance review`
    summary: `The lane still needs more research. Candidate state, milestone state, the completed governance issue, and the semantic-audit supporting pool all continue to show that stale-batch lifecycle management is a follow-on lifecycle rather than an IBM-ready issue. The remaining blocker is now purely evidence sufficiency: prove the frozen Validation batch governance v1 contract, runtime gate behavior, replay/retire evidence, and specimen-S1/S2/S3 refusal evidence are enough to materialize without reopening the pointer question.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-run live-status refresh`
    mode: `independent supporting-pool verification`
    summary: `A current-run check kept the lane in pre-brainstorm while refreshing the runtime facts to the active worker process: git still shows only the 2 canonical doc-loop files dirty with develop...HEAD at 68 left / 23 right, live-status reports role_hint=worker and activity_state=ai_active, current_prompt_has_delegated_continuation=1, pending delegated continuations already none, latest manager continuity still unavailable, and the active runtime still presents last_launch_kind=fresh_with_handoff plus last_rotation_reason=context_compacted. That keeps runtime evidence as continuation-consumption mirror only and does not create a stronger owner than C-20260322-1801-B.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex final-sufficiency-structure writeback`
    mode: `independent route verification`
    summary: `This worker round kept the lane in pre-brainstorm and converted the last blocker from narrative form into a fixed candidate-level closeout set: the only remaining gap is now explicit sufficiency proof across five evidence groups, namely Validation batch governance v1, runtime gate behavior, replay/retire evidence, acceptance bridge, and specimen-S1/S2/S3 delete/refusal evidence. The current supporting pools still do not create a stronger owner, so the only justified next step is to close those five proofs rather than reopen routing or owner discovery.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer five-group sufficiency verdict`
    mode: `independent candidate acceptance review`
    summary: `A fresh read-only explorer pass again found no stronger canonical owner than C-20260322-1801-B and confirmed IBM is still not ready. The pointer question is already frozen; the only remaining blocker is sufficiency proof for an explicit five-group closeout set: Validation batch governance v1, runtime gate behavior, replay/retire evidence, acceptance bridge, and specimen-S1/S2/S3 delete/refusal evidence.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-run supporting-pool verification`
    mode: `independent candidate acceptance review`
    summary: `A read-only subagent pass again found no stronger canonical owner than C-20260322-1801-B. The completed issue still leaves lifecycle management as a separate later lifecycle, the 20260322-1802 audit remains supporting evidence only, the nearby progress doc still owns only latest manager continuity consumption timing, and live-status still acts as mirror-only supporting evidence because latest manager continuity remains unavailable even though the delegated continuation bundle has already been consumed in the current prompt.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-session IBM-readiness verdict`
    mode: `independent candidate acceptance review`
    summary: `A current-session read-only verdict again kept the lane in pre-brainstorm. Milestone still carries C-20260322-1801-B as candidate/in_pre_brainstorm, I-20260322-1801 remains explicitly narrower and leaves lifecycle management as a later lifecycle, and the remaining blocker is still sufficiency proof that the frozen Validation batch governance v1 contract, runtime gate, replay/retire evidence, acceptance bridge, and cleanup/delete refusal evidence are enough to materialize. No stronger canonical owner appeared, so no reroute to IBM is justified.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex first-hop pool scan refresh`
    mode: `independent route verification`
    summary: `Re-running the lead-agent first-hop against AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, milestones, tools, lead-agent, context-source-skill, doc-pre-brainstorm-execution, live-status, the completed issue, semantic-audit evidence, the neighboring progress artifact, and the absence of recovery/github-issue owners again kept the lane at continuation -> pre_brainstorm -> doc-pre-brainstorm-execution. The highest-priority pool is still milestone plus the candidate's canonical pre-brainstorm owner, while project-intent, chat/session evidence, review/test acceptance evidence, progress, and runtime status all remain supporting input only.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session canonical-owner recheck`
    mode: `independent candidate acceptance review`
    summary: `A fresh-session read-only explorer recheck again kept the lane in pre-brainstorm. C-20260322-1801-B still carries the remaining gap as sufficiency proof for the frozen minimal contract; milestone still keeps it as candidate/in_pre_brainstorm; completed issue I-20260322-1801 remains intentionally narrower; the 20260322-1802 semantic audit is supporting evidence only; and the only nearby progress artifact still belongs to I-20260322-0445 delegated-continuation consumption timing rather than stale-batch retire/rebuild governance. No stronger progress/recovery/github-issue owner appeared.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer constrained-pool canonical-owner verdict`
    mode: `independent supporting-pool verification`
    summary: `A final constrained-pool read-only pass again found no stronger owner than C-20260322-1801-B. Milestone still keeps the lane at candidate/in_pre_brainstorm, I-20260322-1801 still leaves lifecycle management as a follow-on lifecycle, the 20260322-1802 semantic-audit pool remains supporting evidence only, the neighboring progress doc still owns delegated-continuation consumption rather than stale-batch retire/rebuild governance, and .freely/run evidence still routes the lane back to continuation -> pre_brainstorm.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-turn supporting-pool verification`
    mode: `independent candidate acceptance review`
    summary: `A current-turn read-only verification again found no stronger canonical owner than C-20260322-1801-B. Milestone still keeps the lane at candidate/in_pre_brainstorm, I-20260322-1801 remains explicitly narrower and leaves lifecycle management as a follow-on lifecycle, the 20260322-1802 semantic-audit bundle is supporting evidence only, the neighboring progress artifact still owns delegated-continuation consumption timing rather than stale-batch retire/rebuild governance, and live-status plus the missing manager-continuity-20260324-021853.md file still provide only worker-side continuation mirror evidence.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-with-handoff live-status truth sync`
    mode: `independent supporting-pool verification`
    summary: `The current live-status still keeps the lane in pre-brainstorm, and repository truth matches the fresh_with_handoff continuity guard rather than overriding it: the active worker runtime reports last_launch_kind=fresh_with_handoff and last_rotation_reason=context_compacted while keeping role_hint=worker, activity_state=ai_active, current_prompt_has_delegated_continuation=1, pending delegated continuations already none, and latest manager continuity still unavailable. That confirms the phase-appropriate continuity writeback was necessary without changing ownership: runtime remains continuation-consumption mirror only, and no stronger owner than C-20260322-1801-B appears.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer delegated-continuation sufficiency verdict`
    mode: `independent candidate acceptance review`
    summary: `A delegated read-only review again kept C-20260322-1801-B in pre-brainstorm. Ownership is already stable; the remaining blocker is contract sufficiency. The missing .freely/run/manager-continuity-20260324-021853.md cannot strengthen IBM readiness, and the only justified next step is evidence closure for Validation batch governance v1, runtime gate behavior, replay/retire evidence, acceptance bridge, and cleanup/delete refusal evidence without reopening scope.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-turn delegated-continuation writeback`
    mode: `independent route verification`
    summary: `This turn re-ran the required first-hop governance chain and absorbed the delegated continuation into the canonical candidate truth. The lane remains continuation -> pre_brainstorm -> doc-pre-brainstorm-execution, current hygiene stays within the assigned write scope because only docs/milestones.md plus this candidates.md are dirty, and the missing manager-continuity-20260324-021853.md still acts only as provenance gap rather than a stronger owner or IBM-ready input.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex latest live-status truth correction`
    mode: `independent supporting-pool verification`
    summary: `A direct ./bin/freely live-status check in this turn still keeps the lane in pre-brainstorm and confirms the delegated continuation bundle is already consumed, while the active runtime mirror continues to report last_launch_kind=fresh_with_handoff and last_rotation_reason=context_compacted together with role_hint=worker, activity_state=ai_active, and pending delegated continuations already none. latest_manager_continuity_generated/consumed remains unavailable, so runtime still acts only as continuation-consumption mirror and does not create a stronger owner than C-20260322-1801-B.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex fresh-session first-hop continuity refresh`
    mode: `independent route verification`
    summary: `This fresh session re-ran the required first-hop chain against AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, milestones, tools, lead-agent, context-source-skill, doc-pre-brainstorm-execution, the completed issue, and current live-status/git facts. The route still resolves to continuation -> pre_brainstorm -> doc-pre-brainstorm-execution: this worktree remains a worker-owned candidate lane, only docs/milestones.md and this candidates.md are dirty, develop...HEAD remains 68 left / 23 right, and the handoff-referenced .freely/run/manager-continuity-20260324-021853.md is still missing, so no stronger canonical owner or IBM-ready boundary appears.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool canonical-owner sweep`
    mode: `independent supporting-pool verification`
    summary: `A focused read-only sweep over the allowed supporting pools again found no stronger owner than C-20260322-1801-B. docs/milestones.md still keeps this lane as candidate/in_pre_brainstorm, I-20260322-1801 remains completed but intentionally narrower, and the completed issue's issue/PRD/pre-tests/issue-bound brainstorm all reinforce that lifecycle management capability is a later independent lifecycle. No relevant progress or github-issue owner appeared, and the missing manager continuity artifact weakens rather than strengthens any alternative owner claim.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-turn lead-agent/context-source rerun`
    mode: `independent route verification`
    summary: `This turn re-read AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, milestones, tools, lead-agent, context-source-skill, doc-pre-brainstorm-execution, human-interruption-handling, the completed issue, and current git/live-status facts. The highest-priority pool is still the milestone plus C-20260322-1801-B canonical candidate lane, so the route again resolves to continuation -> pre_brainstorm -> doc-pre-brainstorm-execution with codex as the correct same-tool second-hop executor rather than a handoff-only tool.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-turn canonical-owner verification`
    mode: `independent supporting-pool verification`
    summary: `A read-only explorer pass again found no stronger supporting-pool owner than C-20260322-1801-B. The closest competing artifact, I-20260322-1801, remains explicitly narrower and leaves lifecycle management capability as a separate follow-on lifecycle; the 20260322-1802 semantic-audit bundle marks itself as supporting evidence only; and the only relevant progress artifact, I-20260322-0445, still owns latest manager-continuity consumption timing rather than stale-batch lifecycle governance. No github-issue style owner appeared in the allowed scope.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session supporting-pool owner confirmation`
    mode: `independent supporting-pool verification`
    summary: `A fresh-session explorer pass again found no stronger canonical owner than C-20260322-1801-B in the allowed supporting pools. The 20260322-1802 semantic-audit bundle remains absorbed supporting evidence only, the neighboring progress doc still belongs to I-20260322-0445 latest-manager-continuity consumption timing rather than stale-batch lifecycle governance, no github-issue style owner appears in repo scope, and no .freely/run manager-continuity artifact matching 20260324-021853 exists in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool owner verification`
    mode: `independent supporting-pool verification`
    summary: `A read-only subagent verification again kept the lane in pre-brainstorm. It rechecked milestones, the completed governance issue plus PRD/pre-tests/tasks/issue-bound brainstorm/review, the 20260322-1802 semantic-audit pool, the only relevant progress artifact for I-20260322-0445, and .freely/run manager continuity presence. The result stayed unchanged: C-20260322-1801-B is still the strongest owner, I-20260322-1801 explicitly leaves lifecycle-management capability as a separate follow-on lifecycle, the semantic-audit pool is supporting evidence only, no progress artifact absorbs stale-batch lifecycle governance, and .freely/run/manager-continuity-20260324-021853.md still does not exist beyond prompt references.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-session runtime-truth correction`
    mode: `independent supporting-pool verification`
    summary: `Current repository truth still keeps the lane in pre-brainstorm, and the active runtime mirror continues to match the fresh-with-handoff continuity guard rather than superseding it: a fresh ./bin/freely live-status check reports role_hint=worker, activity_state=ai_active, current_prompt_has_delegated_continuation=1, pending delegated continuations already none, last_launch_kind=fresh_with_handoff, and last_rotation_reason=context_compacted, while latest manager continuity remains unavailable and .freely/run/manager-continuity-20260324-021853.md is still absent. Runtime therefore remains continuation-consumption mirror only and still does not create a stronger owner than C-20260322-1801-B.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-turn supporting-pool verification`
    mode: `independent candidate acceptance review`
    summary: `Supporting-pool verification still points to C-20260322-1801-B as the canonical owner, because the prior governance issue is completed, the semantic-audit pool is absorbed evidence only, the latest-manager-continuity timing docs remain adjacent runtime-consumption work rather than stale-batch lifecycle ownership, and the referenced manager continuity artifact for 20260324-021853 is absent.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer canonical-owner verdict from delegated read-only pass`
    mode: `independent candidate acceptance review`
    summary: `A fresh delegated explorer pass rechecked milestones, I-20260322-1801 and its IBM artifacts, the 20260322-1802 semantic-audit pool, and adjacent progress closeout lanes. The result stayed unchanged: no stronger canonical owner exists outside C-20260322-1801-B, and the missing manager-continuity-20260324-021853.md remains provenance gap only, not a competing IBM input.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-run live-status truth refresh`
    mode: `independent candidate acceptance review`
    summary: `A fresh ./bin/freely live-status check kept the runtime evidence in supporting-only territory while correcting one stale continuity fact: the active worker now reports last_launch_kind=fresh and last_rotation_reason=initial_start, while still keeping current_prompt_has_delegated_continuation=1, pending delegated continuations already none, the same consumed continuation bundle, and latest manager continuity unavailable. The prompt excerpt still carries the earlier fresh_with_handoff/context_compacted continuity note, so runtime continues to act only as continuation-consumption mirror rather than a stronger canonical owner or IBM-ready input.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex context-compacted continuity artifact refresh`
    mode: `independent candidate acceptance review`
    summary: `Because the incoming handoff explicitly carried context-compacted continuity, this round first refreshed the phase-appropriate pre-brainstorm artifact before expanding scope, then corrected runtime truth back to current repository facts. Re-reading AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, tools, lead-agent, context-source-skill, doc-pre-brainstorm-execution, live-status, the completed governance issue, the 20260322-1802 semantic-audit evidence, and the absence of any docs/recovery owner still keeps the lane at continuation -> pre_brainstorm -> doc-pre-brainstorm-execution. The implementation landing remains a combined minimal contract with manager continuity as truth surface and runtime/status/branch-management as consumers, not a standalone runtime-status or patrol-only issue.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex constitution/laws gate plus supporting-pool rescan`
    mode: `independent candidate acceptance review`
    summary: `This turn explicitly ran the workspace constitution-guard and laws-enforcer checks through the project truth sources and then re-scanned milestone, issue, semantic-audit, progress, recovery, tools, and live-status inputs. The result stayed unchanged: this worker feature worktree is allowed to keep writing only canonical pre-brainstorm artifacts, docs/recovery is still absent in the current worktree, adjacent progress artifacts still own delegated-continuation consumption or launch-linkage lanes rather than stale-batch lifecycle governance, and no stronger owner than C-20260322-1801-B appears. The lane therefore remains continuation -> pre_brainstorm -> doc-pre-brainstorm-execution, with manager continuity as the eventual truth surface and runtime/status/branch-management as consumers.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session sufficiency verification`
    mode: `independent candidate acceptance review`
    summary: `A new read-only explorer pass in this fresh session again found no stronger owner and still rejected IBM-ready promotion. Milestone keeps C-20260322-1801-B as candidate/in_pre_brainstorm, I-20260322-1801 remains intentionally narrower, the 20260322-1802 audit stays supporting evidence only, the adjacent progress lane still owns manager-continuity consumption timing rather than stale-batch lifecycle governance, and .freely/run/manager-continuity-20260324-021853.md is still absent. That leaves only the candidate's own final sufficiency closeout around the fixed Validation batch governance v1 block, replay/retire evidence, acceptance bridge, and delete-gate specimen proof; it does not justify another owner or IBM jump yet.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer first-jump continuation closure verdict`
    mode: `independent candidate acceptance review`
    summary: `A current-turn read-only explorer reran the required continuation input set and reached the same result: C-20260322-1801-B stays in pre-brainstorm because the owner remains unchanged, the handoff-referenced manager continuity file is still missing as provenance gap only, and the remaining blocker is sufficiency proof for Validation batch governance v1, runtime gate, replay/retire evidence, acceptance bridge, and delete/refusal specimen evidence rather than route ambiguity.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.1-codex-mini explorer canonical-owner and IBM-readiness review`
    mode: `independent candidate acceptance review`
    summary: `A fresh read-only explorer pass again confirmed that C-20260322-1801-B remains the strongest canonical owner: milestone still keeps it as candidate/in_pre_brainstorm, I-20260322-1801 remains intentionally narrower and completed only for role-definition, the 20260322-1802 semantic-audit bundle stays supporting evidence only, the neighboring progress artifact owns a different continuity-consumption issue, and .freely/run/manager-continuity-20260324-021853.md is still absent. IBM materialization therefore remains blocked on final sufficiency proof for the frozen combined contract, especially the Validation batch governance v1 block, runtime gate, replay/retire evidence, acceptance bridge, and specimen-S1/S2/S3 delete/refusal evidence.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session strongest-owner verification`
    mode: `independent candidate acceptance review`
    summary: `A current-turn read-only explorer again found no stronger canonical owner or IBM-ready boundary than C-20260322-1801-B. Milestone still keeps the lane at candidate/in_pre_brainstorm, I-20260322-1801 remains a narrower completed role-definition issue, 20260322-1802 is absorbed as supporting evidence only, the nearby progress artifacts still own delegated-continuation/latest-continuity consumption timing rather than stale-batch retire/rebuild governance, and both latest manager continuity plus .freely/run/manager-continuity-20260324-021853.md remain unavailable.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-run live-status drift correction`
    mode: `independent supporting-pool verification`
    summary: `A direct live-status check in the current session corrected the canonical writeback back to repository truth: the worker is still active, delegated continuation consumption is still fully absorbed, latest manager continuity is still unavailable, and the active runtime still reports last_launch_kind=fresh_with_handoff with last_rotation_reason=context_compacted. The previous fresh/initial_start wording was doc drift, not a new route or owner signal, so runtime remains continuation-consumption mirror only.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-run strongest-owner verification`
    mode: `independent candidate acceptance review`
    summary: `A parallel read-only subagent pass over the milestone entry, the completed governance issue, the neighboring progress lanes, the semantic-audit candidate, and the missing manager continuity file again found no stronger canonical owner than C-20260322-1801-B. IBM promotion still fails on the same final sufficiency set: Validation batch governance v1, runtime gate behavior, replay/retire evidence, acceptance bridge, and specimen-S1/S2/S3 delete/refusal proof.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-turn no-contradiction verdict`
    mode: `independent candidate acceptance review`
    summary: `A current-turn read-only explorer pass again found no stronger canonical owner than C-20260322-1801-B and no contradiction with the candidate's own next_action or revisit_trigger. I-20260322-1801 remains a narrower completed issue, the 20260322-1802 semantic-audit lane remains supporting evidence only, the neighboring progress artifact still owns continuity-consumption timing rather than stale-batch retire/rebuild governance, and .freely/run/manager-continuity-20260324-021853.md is still absent as provenance gap only. IBM therefore remains blocked on the same frozen five-group sufficiency proof.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool strongest-owner scan`
    mode: `independent supporting-pool verification`
    summary: `A parallel read-only sweep across milestones, the completed governance issue plus its IBM artifacts, adjacent progress lanes, and recovery/manager-continuity presence again found no stronger canonical owner than C-20260322-1801-B. I-20260322-1801 still only owns role-definition, the neighboring progress docs own continuity-consumption timing rather than stale-batch retire/rebuild governance, docs/recovery is absent, and manager-continuity-20260324-021853.md is missing as provenance gap only.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session no-contradiction confirmation`
    mode: `independent candidate acceptance review`
    summary: `A fresh read-only explorer pass over the milestone entry, completed governance issue and its pre-tests, adjacent progress lanes, the semantic-audit supporting pool, docs/recovery absence, and .freely/run manager-continuity presence again found no stronger canonical owner than C-20260322-1801-B. The lane is still not IBM-ready, and no contradiction appears against the current candidate or milestone next_action: stay in pre-brainstorm and finish the five-group final sufficiency closeout.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-run supporting-pool reconfirmation`
    mode: `independent candidate acceptance review`
    summary: `A parallel read-only sweep across the completed governance issue, its pre-tests, adjacent progress lanes, the 20260322-1802 semantic-audit bundle, and the missing manager-continuity-20260324-021853 artifact again found no stronger canonical owner than C-20260322-1801-B. IBM readiness did not change, and the current next_action/revisit_trigger remain internally consistent: stay in pre-brainstorm until the five-group final sufficiency closeout is independently proven.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer supporting-pool and github-issue-equivalent scan`
    mode: `independent candidate acceptance review`
    summary: `A dedicated read-only pass over the requested supporting pools again found no stronger canonical owner than C-20260322-1801-B. The nearby progress docs still own continuity-consumption/reentry timing only, docs/recovery is absent, 20260322-1802 remains supporting evidence only, the referenced manager continuity file is still missing as provenance gap only, and no repo-local github-issue-equivalent artifact exposes an IBM-ready owner.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer progress-recovery-github-owner patrol`
    mode: `independent candidate acceptance review`
    summary: `A fresh read-only patrol over docs/progress, docs/recovery, repo-local github-issue-equivalent artifacts, and nearby continuation issues again found no stronger canonical owner than C-20260322-1801-B. The neighboring progress lanes still only own continuity-consumption/cleanup timing, docs/recovery remains absent, the semantic-audit bundle stays supporting evidence only, and no repo-local tracker artifact exposes an IBM-ready owner.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer fresh-session strongest-owner verdict`
    mode: `independent candidate acceptance review`
    summary: `A fresh-session read-only explorer pass again concluded that C-20260322-1801-B remains `needs-more-research`, not `ready-for-ibm`. The strongest owner is still the candidate itself, I-20260322-1801 remains a narrower completed role-definition issue, 20260322-1802 remains supporting evidence only, and the only remaining blocker is sufficiency proof for the frozen five-group closeout: Validation batch governance v1, runtime gate behavior, replay/retire evidence, acceptance bridge, and delete/refusal specimens.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-turn first-hop closure and tool-selection writeback`
    mode: `independent candidate acceptance review`
    summary: `This fresh session re-read AGENTS, PROJECT_INTENT, CONSTITUTION, LAWS, milestones, workspace tools, lead-agent, context-source-skill, doc-pre-brainstorm-execution, the current candidate/issue/supporting-evidence set, and live-status before expanding scope. The result stayed unchanged: source_class=continuation, route_kind=pre_brainstorm, target skill=doc-pre-brainstorm-execution, and selected_tool=codex because the work remains canonical doc-loop writeback inside the assigned feature worktree. A parallel read-only explorer also rechecked progress/recovery/github-equivalent pools and nearby issue artifacts, again finding no stronger owner and no IBM-ready contradiction.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer concrete supporting-pool file check`
    mode: `independent candidate acceptance review`
    summary: `A current-turn read-only explorer rechecked the concrete supporting files and again found no stronger owner than C-20260322-1801-B. Milestone still keeps the lane as candidate/in_pre_brainstorm, I-20260322-1801 plus its pre-tests/verification artifacts still leave lifecycle management as a separate follow-on capability, the neighboring latest-manager-continuity progress lane still owns continuity-consumption timing only, and docs/recovery remains absent in this worktree.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer strongest-owner verification`
    mode: `independent candidate acceptance review`
    summary: `A fresh delegated read-only pass again confirmed that C-20260322-1801-B remains the strongest canonical owner. No competing issue/progress/recovery/github-equivalent artifact supersedes it, I-20260322-1801 still keeps lifecycle-management capability out of scope, 20260322-1802 remains supporting evidence only, and IBM readiness stays blocked on the same five-group sufficiency closeout.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer strongest-owner final confirmation`
    mode: `independent candidate acceptance review`
    summary: `A final read-only subagent pass again kept strongest_owner at C-20260322-1801-B with competing_owner_if_any=none and ibm_ready=false. The completed role-definition issue, semantic-audit supporting pool, adjacent progress lanes, absent docs/recovery path, and missing manager-continuity-20260324-021853.md file still do not create a stronger canonical owner than the current candidate.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex current-turn delegated-continuation absorption`
    mode: `independent route verification`
    summary: `This worker round re-ran the required first-hop chain in the assigned feature worktree and absorbed the delegated continuation into the canonical candidate truth. Repository facts now stay aligned with the current runtime mirror: only docs/milestones.md and this candidates.md are dirty, develop...HEAD is 74 left / 23 right, live-status reports role_hint=worker plus activity_state=ai_active, current_prompt_has_delegated_continuation=1, pending delegated continuations already none, consumed IDs covering 20260324-024929/024942/025910/030713, and latest manager continuity still unavailable while last_launch_kind/last_rotation_reason are now fresh/initial_start. That keeps runtime evidence as continuation-consumption mirror only and preserves continuation -> pre_brainstorm -> doc-pre-brainstorm-execution with codex as the same-tool second hop.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `gpt-5.4-mini explorer current-turn strongest-owner patrol`
    mode: `independent supporting-pool verification`
    summary: `A read-only subagent patrol over milestone, issue, progress, recovery-equivalent, and repo-local intake artifacts again found strongest_owner=C-20260322-1801-B, competing_owner_if_any=I-20260322-1801 only as supporting formal artifact, and ibm_ready=false. The neighboring completed issue still leaves lifecycle management as a later separate lifecycle, nearby progress docs only own continuity-consumption and cleanup-closeout timing, docs/recovery is absent in this worktree, and delegated continuation intake artifacts route back to handoff://continuation rather than creating a stronger issue-equivalent owner.`
    verdict: `stay_pre_brainstorm`
- priority: P1
- status: needs_research
- decision_reason: 这是治理规则落成工具能力的下一步，但当前稳定边界仍是 stale-batch combined minimal contract，而不是单点 runtime/status 补丁。human continuation `20260324-001134-continuation-dogfood-watchdog-fr` 及其 superseding delegated continuations `20260324-024929`、`20260324-024942`、`20260324-025910`、`20260324-030713`，连同多轮 supporting-pool rescan、`live-status` continuity 复核、fresh-batch absorption 独立 acceptance review、本轮 first-hop continuation absorption refresh、同工具首跳重放、ownership check、当前轮并行 supporting-pool reconfirmation、requested supporting-pool/github-issue-equivalent scan、以及最新 delegated explorer strongest-owner patrol，仍只证明应继续 pre-brainstorm：没有更强的 milestone/issue/progress/recovery/github-issue owner 吸收该 lane，而最高优先池仍是 milestone 加上 `C-20260322-1801-B` 的 canonical candidate owner。completed issue `I-20260322-1801` 现在最多只构成最强 supporting formal artifact，它仍明确把 lifecycle management capability 留作后续独立 lifecycle；补扫其 issue/PRD/pre-tests/issue-bound brainstorm 也只进一步加固这一边界，而不会吸收当前 capability。当前相邻的 `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md` 与 `docs/progress/workspace-routing-foundation/p-manager-continuation-handoff-consumption-governance.md` 只拥有 delegated-continuation / latest-continuity consumption timing，不拥有 stale-batch retire/rebuild governance，而 `20260322-1802` semantic-audit bundle 也已明确退化为 `supporting_evidence`；`docs/recovery/` 与 repo 内 github-issue-equivalent supporting pool 在当前 worktree 中同样不存在可吸收该 lane 的 owner。handoff 要求读取的 `manager-continuity-20260324-021853.md` 仍缺失，且当前 worktree 中不存在匹配 `20260324-021853` 的 manager-continuity artifact，不能被当成已稳定的 IBM 输入。当前运行态只证明 delegated continuation 已被当前 worker prompt 消费，且 `latest_manager_continuity_generated/consumed` 与 `manager_continuity_file` 仍 unavailable / none；当前 `./bin/freely live-status --project ...` 的仓库真值是 `last_launch_kind=fresh` 与 `last_rotation_reason=initial_start`，同时 prompt excerpt 仍保留更早的 fresh-with-handoff continuity 摘录。这说明 runtime 现在仍只是 continuation-consumption mirror，而不是新的 canonical owner。当前工具选择也没有改写边界：`tools.md` 与首跳 agent/skill 链都再次证明 `codex` 适合当前同 worktree 的 doc-loop 写回，因此必须在当前会话继续第二跳，而不是把 handoff 当完成。当前 hygiene 仍是 phase-appropriate doc-loop dirty：只有 `docs/milestones.md` 与本 `candidates.md` 两个 canonical writeback 文件未提交，不触发 checkpoint / ownership reroute，但也不能被误写成 clean 或 retirement-ready。最小剩余集合现在已收敛成单一路线：fresh-batch absorption 采用 no-extra-pointer 等价 contract，并明确冻结为 `retire_evidence_ref + remaining_cleanup_requirement` 就是 canonical machine-readable absorption pointer；实现落点保持为 combined minimal contract，由 manager continuity 承载真相，runtime/status/branch-management 只消费它。最新独立 acceptance review 与 subagent strongest-owner patrol 说明剩余 blocker 已进一步收敛，不再是是否需要额外 pointer，而是是否已有足够独立证据证明 `Validation batch governance:` `v1`、runtime gate、replay/retire evidence、acceptance bridge 与 cleanup/delete refusal evidence 足以 materialize。
- promoted_issue_path: `pending://pre-test-merge-lifecycle-management-capability`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: `C-20260322-1801-A` 已 materialize 成正式 issue；当前继续 pre-brainstorm，并将 `20260324-001134-continuation-dogfood-watchdog-fr` 及其 superseding delegated continuations 明确吸收到 `C-20260322-1801-B` 的 canonical contract 中，继续保留 `combined minimal contract v0`。本轮按当前仓库事实重判后，这棵 owner worktree 仍是 active canonical owner：branch 尚未被 `develop` 吸收，`git status --short --branch` 只显示 `docs/milestones.md` 与本 `candidates.md` 两个 canonical doc-loop 文件 dirty，`git rev-list --left-right --count develop...HEAD` 当前为 `74 23`，而 handoff 要求读取的 `.freely/run/manager-continuity-20260324-021853.md` 仍缺失。由于当前脏树只落在这两个 phase-appropriate continuity artifacts，本轮无需先切 checkpoint commit 或分流到其他 worktree。当前 fresh session 已完整重放首跳闭环：`constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> doc-pre-brainstorm-execution`，并再次确认 `selected_tool=codex` 不是默认偏好，而是因为当前工作仍是同一 feature worktree 内的 canonical doc-loop 写回，必须在当前会话继续第二跳。首跳需求池重扫、本轮 `live-status` 复核，以及新的 delegated read-only explorer 都再次确认四点：`I-20260322-1801` 仍只覆盖职责定义并把 lifecycle management capability 留在后续独立 lifecycle；`20260322-1802` 只剩 absorbed supporting evidence；相邻的 `p-latest-manager-continuity-worker-consumption-governance.md` 与 `p-manager-continuation-handoff-consumption-governance.md` 只拥有 continuity-consumption / reentry / launch-linkage closeout lane，并不拥有 stale-batch retire/rebuild governance；`docs/recovery/` 仍缺失。当前轮新的 concrete supporting-file explorer 还复核了 `I-20260322-1801` 的 pre-tests / verification artifacts，结论仍是它们只提供 supporting evidence，不吸收 stale-batch retire/rebuild owner。当前最高优先池仍是 milestone + candidate canonical owner，而不是 issue/progress/recovery/runtime，且 manager continuity 缺失只构成 provenance gap，不构成新的 owner，也不构成 IBM-ready 输入。当前 `live-status` 证明运行态仍只是 continuation-consumption mirror：`role_hint=worker`、`activity_state=ai_active`、`current_prompt_has_delegated_continuation=1`、`pending_delegated_continuation_ids=none`，最近 consumed continuation IDs 已覆盖 20260324-024929/024942/025910/030713；当前仓库真值同时显示 `last_launch_kind=fresh`、`last_rotation_reason=initial_start`，而 prompt excerpt 仍保留更早的 fresh-with-handoff continuity 摘录。最新 fresh-session read-only explorer、本轮并行 supporting-pool explorer，以及当前轮 progress/recovery/github-owner patrol 都确认 supporting pools 没有更强 owner，且与当前 `next_action` / `revisit_trigger` 不冲突。下一步不再扩 supporting-pool 重扫，也不再讨论额外 pointer；只做作者侧最终 sufficiency closeout，并严格按 `final_sufficiency_closeout` 中固定的 5 组证据收口：先冻结 `validation_batch_governance_v1` 作为唯一真相面，再写 `runtime_gate_behavior` 的最小拒绝语义，随后补 `replay_retire_evidence` 与 `acceptance_bridge`，最后用 `delete_refusal_specimens` 收口 delete-denied 证据。只有这 5 组证据都能支撑 combined minimal contract 由 manager continuity 承载真相、并被 runtime/status/branch-management 稳定消费时，才重新进入 IBM materialization 判断。
- current_fleet_position:
  - this worktree remains the active canonical owner for stale-batch governance
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/pre-test-merge` remains stale evidence-only and cannot be treated as an active verification surface
  - completed or merged trees in the same repo may enter cleanup-candidate / cleanup-pending pools, but none of them supersede this candidate's ownership until stale-batch delete-gate semantics are frozen
  - local git facts such as `clean`, `ahead=0`, and `merged into develop` are sufficient only for cleanup candidacy; they are not by themselves enough to declare `delete-ready`
  - any delete-ready conclusion that depends on family-level inference rather than an explicit canonical cleanup gate must be downgraded to `cleanup-candidate` until `verified-retirable -> delete guard -> retired` is written in issue/progress/cleanup truth
- revisit_trigger: 当 `Validation batch governance:` `v1` 固定块、runtime gate、replay/retire evidence、`acceptance_contract_state/source/blocker -> pre-tests.md` 质量 gate 的桥、pre-IBM validation matrix，以及“`completed` / cleanup gate / `verified-retirable` / `retired` / delete guard”组合和 `specimen-S1/S2/S3` 的 refusal evidence 都经独立 review 证实稳定，且最新 delegated explorer 复核后仍未出现新的 competing owner、`live-status`/runtime 侧继续只作为 continuation consumption mirror、fresh-batch absorption 的 no-extra-pointer 等价 contract 在 final sufficiency closeout 后未再暴露新的 contract blocker、且 manager continuity 缺失继续只表现为 provenance gap 而非 route blocker 时，重新进入 materialization 判断
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

### C-20260322-1801-C
- candidate_format_version: v2
- title: worker self-loop exit and scheduler closeout governance
- problem: Freely 缺少识别 worker verification-only / continuity-refresh 低价值自环并把 lane 回交 manager 的通用调度能力，导致 worker 槽位被长期占住，新的 lane 无法起跑。
- why_now: 这次 dogfood 里真正堵塞新 lane 的不是默认并发数 2，而是两个 worker 都停在低价值循环中。如果不把它独立建模，未来即使 stale `pre-test-merge` 被治理，其他 lane 仍会复现同类占槽问题。
- acceptance_criteria:
  - 定义 machine-readable `phase progress` 与 `loop stall` 判据，能区分正常 verification 收口与低价值自环
  - worker 达到阈值后会回交 manager，由 manager 重新决定 merge / freeze / cleanup / queue，而不是 worker 自行做生命周期决策
  - manager 在接收 self-loop exit 后会释放容量或重新排队，避免同一 lane 立刻以新 prompt 重占原槽位
  - 若当前 lane 被回交，manager continuity / runtime launch state 能把旧 prompt 标记为 superseded，而不是继续留在 active/queued 集合里
  - worker/skill lane 的局部完成不得直接升级为 issue `completed` 或删树结论；manager 必须显式判断后续 merge / cleanup / `verified-retirable`
  - worker continuity 必须先作为 stall 真相面，runtime launch state 只镜像 manager 已采纳的 supersede / capacity 结果
  - 若 lane 的上游 `Issue + Brainstorm + PRD -> pre-tests.md` acceptance 面不完整，manager 必须允许把问题回交为 IBM/acceptance contract 缺失，而不是仅按 scheduling stall 处理
  - 若 lane 还没跑完 integration / application-native real-environment testing closeout，manager 不得把“低活动”误判成可退休；它必须区分“未测完”与“测完后自环”
  - worker/skill lane 即使完成本轮局部交付，也只能把 issue 推近 `completed`；最终 delete worktree / branch 仍要等 manager 经过 cleanup gate、`verified-retirable` 与删除门禁再决定
- promotion_gate:
  - 冻结 phase progress 的最小证据标准
  - 冻结 loop stall 阈值与排除误伤正常验证/研究的保护条件
  - 冻结回交 manager 后的容量释放和 supersede 规则
  - 冻结 worker continuity 到 manager continuity 的最小承载语法，避免 stall 判断停留在自由叙述
- open_questions:
  - 哪些 artifact diff 或 phase_state 变化算真正推进
  - 连续多少轮、哪类重复 writeback 才能判为低价值自环
  - 与 `fresh_with_handoff`、resume/rotate 的关系如何定义
  - lane 回交 manager 后，如何区分“runtime 自环”与“上游 `I + B + PRD -> pre-tests.md` acceptance 面本来就不完整”
- acceptance_reviews:
  - reviewer: `codex + subagent panel (Erdos/James/Singer)`
    mode: `independent candidate acceptance review`
    summary: `This capability should remain split from stale pre-test-merge governance to keep regression surface smaller and force a separate machine-readable stall/handback contract.`
    verdict: `split_confirmed_but_not_ready_to_materialize`
- priority: P1
- status: proposed
- decision_reason: 这是通用 scheduling / closeout 能力，不应继续隐含在 `pre-test-merge` stale governance 里。
- promoted_issue_path: `pending://worker-self-loop-exit-and-scheduler-closeout-governance`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: 继续 pre-brainstorm，先冻结 phase-progress、loop-stall 与 capacity release 的 machine-readable 规则，再决定是否 materialize
- revisit_trigger: 当 loop stall 判据、manager 回交 contract、容量释放规则，以及“worker/skill 局部完成不等于 issue completed 或删树条件成立”的分流规则都能冻结成 issue contract 时，重新进入 materialization 判断
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

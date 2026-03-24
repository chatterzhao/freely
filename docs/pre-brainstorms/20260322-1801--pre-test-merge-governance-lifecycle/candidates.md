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
  - stale 后 manager 继续使用既有 `ownership / restart_point / next_action` 词典，但必须补齐 `replay source manifest`、`replay order`、`retire evidence`、`remaining cleanup requirement`
  - runtime 对 stale batch 只允许 read-only patrol、cleanup handoff、rebuild/replay handoff，不再把它恢复成普通 verification 会话
  - 所有指向 stale batch 的旧 queued worker prompts / delegated launches 都会被 supersede 或失效，不再继续消费旧 prompt 池
  - 只能使用现有状态与 gate 组合判断是否继续推进或删树：`done_ibm`、`completed`、cleanup gate、`verified-retirable`、`retired`；stale retire/rebuild 不得只依据 issue `completed` 或局部 loop 收口
  - 上述 contract 优先落在现有真源：manager continuity 为唯一治理真相面，`manager-worker-launch-state.env` 与 `live-status` 仅做消费镜像，不新增平行状态文件
  - manager continuity 必须带批次身份锚点与固定承载语法，至少包括 `validation_batch_id`、`integration_target`、`source_batch_base`，并以固定可解析块承载，而不是自由文本
  - 当前固定承载语法先冻结为 manager continuity 中连续的 `Validation batch governance:` `v1` 块，标题下每行固定为 `- key: value`，并保持固定 key 顺序
  - manager continuity 还必须固定承载 `acceptance_contract_state`、`acceptance_contract_source`、`acceptance_contract_blocker`，把 IBM acceptance 完整性桥接成 runtime 可消费字段，而不是让 runtime 读取 issue/brainstorm/prd 自行推理
  - runtime 在应用旧 prompt supersede 后，必须留下 machine-readable `superseded_worker_prompts_applied_at` 或等价信号，证明旧 prompt 已停止被消费
  - 当 issue 的 `I + B + PRD -> pre-tests.md` 派生链不足以恢复 issue-level acceptance、`post-merge acceptance` 或目标验证环境时，manager 必须写出 `acceptance_contract_state=incomplete` 与 blocker，而不是让 stale/retire 流程伪装成“只剩执行”
  - `pre-tests.md` 质量检查与 testing closeout 必须分开建模：前者确认 acceptance contract 是否完整，后者确认 acceptance 是否已真实执行并留痕
  - testing closeout 默认优先 integration / end-to-end 与 application-native real-environment testing evidence；若缺少这些证据，不得把 lane 判成 `completion_verification done` 或允许 worktree retirement
  - 必须固定一条最终完成检查顺序：`done_ibm` 之后先过 `pre-tests.md` 质量 gate，再做 dev / verification / testing closeout，逐项完成 `pre-tests.md` 后 issue 才可 `completed`；此后仍需继续经过 merge / post-merge acceptance / cleanup evidence / `verified-retirable`，最后才允许 delete worktree / branch
  - 若 merge / cleanup / `verified-retirable` / `retired` 链条尚未闭合，即使 issue 已 `completed`，也不得删除最后一个 owner worktree
  - 最终 delete worktree / branch 必须有单独删除门；若未来以 hook / guard 投影执行，该门只能消费已有状态与 evidence 组合，不得重造一套平行 completion 状态
  - 当前字段级冻结草案以 `combined minimal contract v0` 为准：manager continuity 最少承载 `validation_batch_id`、`validation_batch_state`、`validation_batch_mode`、`stale_reason`、`lifecycle_decision`、`integration_target`、`source_batch_base`、`replay_source_manifest`、`replay_order`、`retire_evidence_ref`、`remaining_cleanup_requirement`、`acceptance_contract_state/source/blocker`、`superseded_worker_prompts`、`superseded_worker_prompts_applied_at`
- promotion_gate:
  - 冻结 stale 判定的最低 machine-readable 字段、真相面和消费路径
  - 冻结 manager lifecycle transaction 与现有 patrol 词典的映射，不新增平行状态系统
  - 冻结 replay source manifest / replay order / retire evidence 的最小 schema
  - 冻结 `superseded_worker_prompts` 与 stale batch gate 的联动，保证旧 queued prompt 不会继续被 runtime 消费
  - 冻结 `validation_batch_mode=read_only_cleanup|rebuild_planning`，确保 `collect_cleanup_evidence` 不会被误读成恢复普通 verification
  - 冻结 `Validation batch governance:` `v1` specimen 与 key 顺序，并证明 runtime / cleanup skill 只靠该块就能稳定读到最小治理字段
  - 明确 `Issue + Brainstorm + PRD -> pre-tests.md` 派生链与 stale governance 的连接点，避免把 acceptance contract 缺失误修成纯 runtime stale 判定
  - 冻结 testing closeout 的最低 evidence bar，明确 application-native real-environment testing 属于主验证面；Freely self-host 时其当前实例才是 `freely chat`
  - 冻结最终 delete worktree / branch 门禁的最小输入组合与拒绝语义，并判断它是否应由现有 hook / guard 投影兜住
  - 用 `specimen-S1/S2/S3` 的 field audit/evidence 证明 delete gate 会拦住至少三类误删：`merged + clean` 误删、issue `completed` 误删、stale batch source/replay evidence 尚未吸收时的误删
  - 完成一轮针对 `combined minimal contract v0` 的独立 acceptance review，确认 supporting pools 仍只支持 `stay_pre_brainstorm` 或已经足够升级到 IBM，而不是在当前 worker round 里靠作者自证
- open_questions:
  - `develop` 前进、protected-env 独有差异、cleanup/replay 证据未齐三者的优先级如何定义
  - stale 后哪些过渡动作被允许保留在 manager-owned lane 中，哪些必须直接进入 rebuild/cleanup
  - `replay_plan_state=pending|complete` 是否足够表达 manifest 已冻结但仍待执行的状态
  - manager 识别 IBM acceptance 缺口时，是否只消费已有 issue/brainstorm/prd/pre-tests artifact，还是需要额外的 IBM completion signal
  - `acceptance_contract_blocker` 的枚举是否还要覆盖 `missing_pre_merge_acceptance` 或 `missing_protected_env_boundary`
  - testing closeout 的 machine-readable evidence 应落在 issue / code-review / progress / runtime 哪个组合面，才能既可恢复又不制造平行真相
  - 是否只靠现有 `phase_state + cleanup gate + verified-retirable/retired evidence` 就足够，还是仍需更明确的 machine-readable 组合提示
  - 最终 delete guard 若落到 hook / guard，应该拦截本地 branch/worktree 删除、远程 branch 删除，还是两者都要管
  - `retire_evidence_ref` / `remaining_cleanup_requirement` 是否已经足够表达 fresh-batch absorption，还是仍需额外指针
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
- priority: P1
- status: needs_research
- decision_reason: 这是治理规则落成工具能力的下一步，但当前稳定边界是 stale-batch combined minimal contract，而不是单点 runtime/status 补丁。delegated continuation `20260324-030713-manager-worker-20260324-021853-worker-pre-test-merge-lifecycle-management-followthrough-codex` 与 supporting pools 仍只证明应继续 pre-brainstorm；它们还没有把 manager truth surface、runtime gate、replay/retire evidence、acceptance bridge 与 delete gate 输入冻结成可直接 materialize 的单一 issue contract。
- promoted_issue_path: `pending://pre-test-merge-lifecycle-management-capability`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: `C-20260322-1801-A` 已 materialize 成正式 issue；当前继续 pre-brainstorm，并保留 `combined minimal contract v0`。本轮进一步把最小下一步冻结为三件事：先把 manager continuity 的 `Validation batch governance:` `v1` 块与固定 key 顺序写实成唯一承载语法；再用 `specimen-S1/S2/S3` 的 refusal specimen/evidence 证明这组字段已足够支撑 runtime gate 与 cleanup/delete 判断；随后再确认 `retire_evidence_ref` / `remaining_cleanup_requirement` 是否还需额外补强来表达 fresh-batch absorption，最后才重新判断是否进入 IBM
- revisit_trigger: 当 `Validation batch governance:` `v1` 固定块、runtime gate、replay/retire evidence、`acceptance_contract_state/source/blocker -> pre-tests.md` 质量 gate 的桥、pre-IBM validation matrix，以及“`completed` / cleanup gate / `verified-retirable` / `retired` / delete guard”组合和 `specimen-S1/S2/S3` 的 refusal evidence 都经独立 review 证实稳定，且未重新混入 `worker self-loop exit` 时，重新进入 materialization 判断
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

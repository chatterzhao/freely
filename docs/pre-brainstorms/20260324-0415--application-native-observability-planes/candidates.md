# Candidates - 20260324-0415--application-native-observability-planes

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260324-0415-A
- candidate_format_version: v2
- title: Application-native runtime observation contract and observability planes
- problem: Freely 当前已经有 `live-status`、`fleet-status`、session jsonl、cycle log、continuity artifact 等多种观察面，但还没有统一 contract 去说明“真实环境测试时先看什么、怎样判断仍在推进/已空转、怎样给用户提供插话着力点”。同时这套 contract 不能绑死在 Freely 自己的日志上，因为未来 Freely 要开发任意应用，而其他应用的可观察信号、日志形态和交互表面可能完全不同。
- why_now: 这次 `pre-test-merge` / `develop` 真实 dogfood 已经证明，单纯固定秒数不够，必须先读 session/cycle/artifact 的前进信号；而产品面也已经暴露出需求：CLI / TUI / GUI / future API 都要把当前应用的状态、会话、日志、多 worktree、多 subagent 的关系暴露给用户。
- acceptance_criteria:
  - 冻结一套应用无关的 `application-native runtime observation contract`，明确区分 `current-state plane`、`session plane`、`stream plane`、`fleet plane`、`artifact plane`
  - 明确“观察顺序”优先读取 progress signals，而不是先依赖固定时间窗口
  - 明确 Freely self-host 只是第一份 concrete profile，而不是唯一 profile；当前具体 surface 包括 `live-status`、`fleet-status`、session jsonl、cycle log、continuity/prompt artifacts
  - 明确该 contract 如何服务三类消费者：用户插话、manager/watchdog 监督、future CLI/TUI/GUI/API status surfaces
  - 明确该 contract 与 `I-20260320-1945`、`C-20260322-0715-A`、frontend probe 的依赖边界，避免重复建模
  - 明确多 worktree / 多 subagent / 多会话场景下，状态面与会话面之间的最小映射字段
  - 明确 testing closeout 中，哪些 observation surfaces 用来证明 application-native real-environment testing 已执行且有 evidence
  - 明确 product-facing 状态暴露 contract：状态卡片、deep refs、实时流展开、fleet drill-down、用户插话着力点如何跨 CLI/TUI/GUI/API 保持一致
  - 冻结 `plane identity block` 的最小字段：`plane_kind / entity_kind / entity_ref / owner_kind / owner_ref / loop_kind / phase_state / topic_ref / deep_ref`
  - 冻结 `progress signal schema`、`stall signal schema`、`acceptance evidence schema` 的最小字段与最小词典
  - 冻结 CLI/TUI/GUI/API 共享的 `status card minimum fields` 与 `deep ref groups`
- promotion_gate:
  - 冻结各 observation plane 的最小词典和职责
  - 冻结 progress signal / stall signal / acceptance evidence 的最小通用 schema
  - 冻结 Freely self-host concrete profile 对上述 schema 的映射，但保留其它应用的实现自由度
  - 冻结与既有 live-status、stall candidate、frontend probe 三条线的承接关系
  - 冻结 product-facing state exposure 的最小字段：status card summary、session deep refs、stream tail refs、artifact refs、fleet ownership refs
  - 明确这条线是上游 contract，不直接等于新 runtime patch 或新 UI 页面
  - 冻结 `acceptance evidence` 如何同时回答 `issue completion` 与 `delete gate`，避免再次把 merge-ready 误当终态完成
  - 完成至少一轮独立 acceptance review，确认这条线是新的 upstream contract，而不是 `live-status` 或 stall candidate 的扩写
- open_questions:
  - 独立 acceptance review 是否认可：`acceptance evidence schema` 的 canonical truth 固定落在 artifact plane，而 current-state/fleet/API 只镜像最小摘要与 `acceptance_ref`
  - 独立 acceptance review 是否认可：CLI/TUI/GUI/API 共享同一组最小 `deep ref groups`，richer surface 只能扩展不能替换
  - 当前 `current-state plane` / `fleet plane` 若继续由 `live-status` / `fleet-status` 承接，shared `status card minimum fields` / `deep ref groups` 是否已经足够支撑 IBM materialization
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author pre-materialization review`
    summary: `This should be treated as a new upstream contract line, not a patch to the old stall candidate and not a duplicate of live-status. It coordinates existing observation surfaces and generalizes them for future application-native testing.`
    verdict: `needs_independent_review`
  - reviewer: `codex + explorer second-round acceptance review`
    mode: `independent candidate acceptance review`
    summary: `This still stays at pre-brainstorm. The contract direction is valid, but the remaining IBM blockers are now narrow: canonical home and consumer contract for acceptance evidence schema, plus minimal CLI/TUI/GUI/API deep-ref compatibility rules. Existing live-status/fleet-status continue to carry current-state/fleet day-1, and subagents stay aggregated under lane/worktree/session surfaces rather than becoming first-class backend entities.`
    verdict: `stay_pre_brainstorm`
  - reviewer: `codex + explorer focused follow-up review`
    mode: `narrow blocker review`
    summary: `Acceptance evidence should remain canonical in the artifact plane, with current-state/fleet/API mirroring only a minimal summary plus acceptance_ref. Shared deep ref groups should be fixed across CLI/TUI/GUI/API, while richer surfaces may extend drill-down without replacing the minimum ref vocabulary. With these two points frozen, the remaining gate is one more independent acceptance review rather than further contract invention.`
    verdict: `ready_for_final_pre_ibm_review`
- priority: P1
- status: proposed
- decision_reason: 这条线已经从本次 Freely 自举现场中暴露出来，而且 clearly exceeds `live-status` / stall candidate 的原边界；但当前仍应停留在 pre-brainstorm，直到五个 plane 的 identity block、progress/stall/acceptance evidence schema、shared state exposure contract，以及与既有线的承接关系都冻结稳定。当前已有四项边界已经收口：`current-state plane` / `fleet plane` 默认继续承接现有 `live-status` / `fleet-status`，不另造平行 surface；多 subagent 默认继续通过 lane/worktree/session 暴露活动痕迹，而不是 day-1 backend 一等实体；`acceptance evidence schema` 的 canonical truth 固定落在 artifact plane，而 current-state/fleet/API 仅镜像最小摘要与 `acceptance_ref`；CLI/TUI/GUI/API 共享同一组最小 `deep ref groups`，richer surface 只能扩展不能替换。剩余 gate 已收窄为再做一轮独立 acceptance review，确认这条线足以进入 IBM shared contract materialization。
- promoted_issue_path: `pending://application-native-runtime-observation-contract-and-observability-planes`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: 继续 pre-brainstorm，但不再扩 contract 面。当前只需完成一轮独立 acceptance review，确认以下两点可直接作为 IBM 输入：`acceptance evidence schema` 的 canonical truth 固定落在 artifact plane 且 current-state/fleet/API 只镜像最小摘要与 `acceptance_ref`；CLI/TUI/GUI/API 共享同一组最小 `deep ref groups`，richer surface 只能扩展不能替换。通过后再进入 IBM shared contract materialization，而不是直接跳到 runtime patch 或 richer UI 实现。
- revisit_trigger: 当最终独立 acceptance review 认可当前 shared contract 已足够稳定，尤其是 artifact-plane canonical acceptance evidence 与 shared deep-ref compatibility rule 已成立后，重新进入 materialization 判断；若仍需 richer runtime/UI observability productization，则另起 follow-on issue
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

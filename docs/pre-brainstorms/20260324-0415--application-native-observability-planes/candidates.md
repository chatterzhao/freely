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
- promotion_gate:
  - 冻结各 observation plane 的最小词典和职责
  - 冻结 progress signal / stall signal / acceptance evidence 的最小通用 schema
  - 冻结 Freely self-host concrete profile 对上述 schema 的映射，但保留其它应用的实现自由度
  - 冻结与既有 live-status、stall candidate、frontend probe 三条线的承接关系
  - 明确这条线是上游 contract，不直接等于新 runtime patch 或新 UI 页面
- open_questions:
  - 对非 Freely 应用，哪些 signal 必须是 machine-readable，哪些允许只作为 human-readable deep refs
  - `stream plane` 是统一 event surface，还是不同 transport 各自承载而只共享词典
  - 多 subagent 的会话是否应成为一级可见实体，还是继续只通过 lane/worktree 聚合暴露
  - 当前 `live-status` / `fleet-status` 是否已足够承接 `current-state plane` / `fleet plane`，还是仍需新的 surface
  - testing closeout 的最低 observation evidence 应写在 `pre-tests.md`、verification evidence，还是未来 status API 中同步暴露
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author pre-materialization review`
    summary: `This should be treated as a new upstream contract line, not a patch to the old stall candidate and not a duplicate of live-status. It coordinates existing observation surfaces and generalizes them for future application-native testing.`
    verdict: `needs_independent_review`
- priority: P1
- status: proposed
- decision_reason: 这条线已经从本次 Freely 自举现场中暴露出来，但当前仍应先停留在 pre-brainstorm，直到 plane 词典、signal schema 和与既有 issue/candidate 的承接边界稳定。
- promoted_issue_path: `pending://application-native-runtime-observation-contract-and-observability-planes`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: 继续 pre-brainstorm，先冻结五类 observation planes、观察顺序、progress/stall/evidence schema，以及 Freely self-host concrete profile；随后再做一轮独立 acceptance review，判断是 materialize 新 issue，还是吸收到既有 observability/probe issue 族
- revisit_trigger: 当 observation planes 词典、通用 signal schema 与 Freely self-host concrete profile 都足够稳定，且与 `live-status` / stall / frontend probe 三条线的关系已无歧义时，重新进入 materialization 判断
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

# Candidates: watchdog-control-plane-governance

### C-20260319T022000Z-A: legacy issue

- candidate_id: `c-20260319-0220-a`
- title: `Watchdog umbrella term and sub-control-plane taxonomy`
- status: `dropped`
- summary: 把 `watchdog` 正式定义为 Freely 的外层监督与恢复控制面总称，并稳定 `availability / runtime / continuity watchdog` 三类 owner 边界；该候选已被现有正式 issue 与 skill 吸收，不再单独 materialize。
- decision_reason: `watchdog-control-plane` 已正式定义 umbrella taxonomy，`I-20260318T163000Z`、`I-20260318T140800Z` 与 `I-20260319T001800Z` 已分别承接 availability / runtime / continuity owner；继续保留为活跃 research 只会重复现有正式治理主线。
- promoted_issue_path: `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- milestone: `M-20260306-workspace-routing-foundation`
- related_artifacts:
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B2-docs/ibm/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- superseded_by:
  - `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B2-docs/ibm/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260319T022000Z-A: legacy issue

- candidate_id: `c-20260319-0220-b`
- title: `Skill-first watchdog capability extraction`
- status: `promoted`
- summary: 收敛 watchdog control plane 下哪些能力属于 skill 真源，哪些仍应保留为 Freely runtime 的 orchestration 语义；availability 与 runtime 已完成承接，剩余 continuity extraction 已正式并入 `I-20260319T001800Z` 的 IBM 收口。
- decision_reason: availability 与 runtime 分层已由 `watchdog-control-plane`、`ai-cli-availability-manager`、`runtime/freely` 和 `I-20260318T163000Z` 吸收；continuity 侧 capability extraction 也已经有稳定 issue 边界，应转入 `I-20260319T001800Z` 的 issue-bound IBM，而不是继续保留在 active candidate 队列。
- promoted_issue_path: `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- depends_on:
  - `C-20260319T022000Z-A`
- related_artifacts:
  - `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
  - `docs/system/workspace/skills/ai-cli-availability-manager/SKILL.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260319T022000Z-A: legacy issue

- candidate_id: `c-20260319-0220-c`
- title: `Historical watchdog productization worktree retirement handoff`
- status: `dropped`
- summary: 固化旧 watchdog 产品化工位的 `materialize_then_retire` 处置框架，并明确 cleanup 留痕与退休前置条件；该候选的治理结论已在 `CONVERGENCE.md` 与当前 pre-brainstorm 中完成承接。
- decision_reason: 旧工位的唯一提交、handoff target、cleanup 结果与 retirement precondition 已在 `CONVERGENCE.md` 和当前 brainstorm 留痕；这里不存在新的正式能力缺口，不应再维持为活跃研究线或重开 IBM。
- promoted_issue_path: `pending://issue-materialization`
- milestone: `M-20260306-workspace-routing-foundation`
- depends_on:
  - `C-20260319T022000Z-A`
- related_artifacts:
  - `docs/B1-docs/raw-CONVERGENCE.md`
  - `docs/B1-docs/raw-20260319T022000Z/brainstorms.md`
- superseded_by:
  - `docs/B1-docs/raw-CONVERGENCE.md`
  - `docs/B1-docs/raw-20260319T022000Z/brainstorms.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

## Current route judgment

- source_class: `discovery`
- route_kind: `pre_brainstorm`
- target_skill: `doc-pre-brainstorm-execution`
- workspace_action: `continue_current_worktree`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/B2-docs/ibm/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- why_now: 当前 worktree 已承载 watchdog governance 的专用上下文；本轮除了把 candidate 同步进 milestone，还需要回填这些 candidate 已被哪些正式 issue / skill / convergence 吸收，避免它们继续以“活跃新研究”名义漂在 pre-brainstorm。
- next_recommended_route: `doc-ibm-execution`
- promotion_gate:
  - A 与 C 已完成 binding，可转入 archive / trace
  - B 已提升并绑定到 `I-20260319T001800Z`，后续不再留在 milestone candidate 队列
  - 当前 pre-brainstorm 已完成 binding/disposition 收口；下一跳改为 `doc-ibm-execution`，继续在正式 issue 中完成 continuity IBM

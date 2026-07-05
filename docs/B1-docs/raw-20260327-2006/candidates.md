# Candidates - 20260327-2006--start-restart-control-plane-semantics

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260327-2006-A: legacy issue
- candidate_format_version: v2
- title: Start/restart control-plane semantics and project-vs-global lifecycle boundary
- problem: Freely 已经有 project-scoped pid ownership、project-local stop/start wiring，以及 global slot/account watchdog 能力，但还没有冻结 `freely start`、`freely start --force`、`freely stop`、`freely restart` 与 explicit global/shared control-plane reset 之间的命令语义边界。缺这层 contract 时，project command 很容易误触 global reset，或把 partial local recovery 和 shared watchdog/account recovery 混成一个 owner。
- why_now: 当前 dedicated worker handoff 就是围绕这组语义漂移展开，而且现有最接近的 owner `I-20260318-1630` 已 completed；若继续把新缺口塞回旧 issue，会破坏 completed issue 的边界，也会让 `start/stop` 的显式控制面继续悬空。
- adjacent_boundary: `C-20260323-1435-A` 负责 `freely init` 的 bootstrap/skip/force contract；本 candidate 只负责 runtime lifecycle/control-plane command family 的 start/stop/restart/force/global semantics，不吸收 init bootstrap 语义。
- acceptance_criteria:
  - 明确列出 project-scoped 与 global/shared control-plane assets 的 owner taxonomy
  - 冻结 `freely start`、`freely stop`、`freely restart`、`freely start --force` 的最小语义差异
  - 明确 project-scope `attach/reuse -> local repair -> fresh bootstrap -> global escalation` 的默认优先序
  - 明确 project force 允许触碰的 safe repair set，以及哪些对象必须留给 explicit global action
  - 明确 project-scope force 不能清理或杀伤其他项目的 runtime/AI/shared watchdog state
  - 明确 process discovery / kill identity 继续依赖 project anchor，而不是全局进程名匹配
  - 明确 interrupted local AI work 在 project restart 与 project force 下的默认行为
  - 明确 future global `stop/restart` 若存在，则语义上是 all-project lifecycle action，而不是 project force 的别名
  - 明确 global restart 必须保留 restore manifest，记住 restart 前处于 running 的 projects，并按该集合恢复
  - 明确 global restart 不会把 operator 已显式 stop 的 projects 误恢复
  - 若确实需要 global reset，明确它必须是独立语义面，而不是 project force 的隐式副作用
- promotion_gate:
  - `start` vs `restart` vs `start --force` 的 blast radius 已冻结
  - `restart` 已冻结为一等 command surface，而不是长期隐藏在 `stop + start` 组合里的 operator 语义
  - `start` 当前是 attach/reuse gate、project-local repair，还是 fail-fast bootstrap gate，已冻结成单一 contract
  - project-scoped stale pid / partial readiness / idle supervisor 的默认处理优先级已冻结
  - project force 的 safe repair set 与 global-only touch list 已冻结
  - 已明确当前不再新增第三个 repair-only 用户态 surface；`start` 与 `start --force` 的分工已冻结
  - global/shared reset 是否需要独立 command or flag family 已收敛
  - global `stop` / `restart` 是否属于独立 namespace 或显式 global flag family 已冻结，不再与 project `force` 混层
  - global restart 的 restore-on-restart contract 已冻结到足以 materialize issue
  - global restart 的 restore manifest 已明确排除 operator-stopped projects
  - global restart 的 restore manifest 已明确包含 project runtime intent、continuity anchor 与 interrupted AI handling 所需字段，并冻结到 `$FREELY_HOME/control-plane/restart/{latest.json,history/<timestamp>.json}` + keep-latest-and-last-20 retention
  - project restart 与 project force 对 interrupted local AI work 的默认行为已冻结，不再混成 silent resume 或 silent discard
  - explicit AI-work restore 已冻结为 dedicated project-scoped `restore-work` surface 优先，任何 `--restore-work` 只可作为 secondary alias
  - 与 `C-20260323-1435-A` 的 force/init family boundary 已明确，不会在 IBM 中重叠 owner
  - project-owned 与 global/shared asset taxonomy 已能指导 safe process discovery / kill scope
  - mandatory restore anchors vs auxiliary evidence 已冻结，不再把 `session-state.env` / `session-handoff.txt` / pid files 当作 restore 必需项
  - 已确认 follow-on IBM 应 materialize 为两个紧邻 issue：先 `project command semantics`，后 `global restart restore memory`
  - 已确认后续 global restore owner 只继承 project issue 已冻结的 taxonomy / restore-anchor 边界，不重新定义 project command blast radius
  - 已确认这条生命周期不会重新打开 `I-20260318-1630`，而是作为新的 follow-on owner 承接
- open_questions:
  - `codex-slot-cooldowns.tsv` 等 shared/watchdog memory 在后续 global restore issue 中应被定义为 required input 还是 opportunistic supporting evidence
- acceptance_reviews:
  - reviewer: `subagent:noether`
    mode: `fresh-process runtime-truth review`
    summary: `Runtime truth confirms this is still a discovery candidate rather than an issue continuation: there is no user-facing cmd_restart, no start --force surface, and no global restart manifest. Existing implementation only freezes project-scoped pid ownership, start/stop wiring, and valid_*_pid_for_project identity guards.`
    verdict: `supports remain_pre_brainstorm`
  - reviewer: `subagent:poincare`
    mode: `fresh-process demand-pool and continuity review`
    summary: `Milestone visibility is already lawful for a needs_research candidate. The missing worker handoff file is real, but manager interruption resolution, manager continuity, and current worker continuity provide stronger replacement evidence; therefore the lane should continue in the same worktree and remain visible without reopening I-20260318-1630.`
    verdict: `supports remain_pre_brainstorm`
  - reviewer: `subagent:kant`
    mode: `fresh-process canonical-truth sweep`
    summary: `Canonical truth still routes this family as a pre-brainstorm candidate rather than an existing issue continuation: milestones keep `C-20260327-2006-A` in candidate_issues, completed `I-20260318-1630` remains supporting truth only, current reviews prove start/dispatcher readiness but not restart/force/global-reset semantics, and there is no `docs/recovery/` artifact to lawfully classify this as recovery continuation.`
    verdict: `supports remain_pre_brainstorm`
  - reviewer: `subagent:kierkegaard`
    mode: `fresh-process demand-pool scan`
    summary: `The active demand-pool truth still centers on milestones + pre-brainstorm + .freely/run/.freely/intake continuity. Related progress and epic review/test artifacts only confirm the completed lower-layer watchdog/bootstrap owner and do not replace this lane's unresolved restart/force/global semantics boundary.`
    verdict: `supports remain_pre_brainstorm`
  - reviewer: `subagent:aquinas`
    mode: `fresh-process boundary review`
    summary: `The cleaner promotion is two adjacent issues, not one: `project command semantics` should own single-project start/stop/restart/start --force and interrupted-local-AI behavior, while `global restart restore memory` should own explicit global restart surface, fleet manifest durability, previously-running set, and operator-stopped exclusion. A single issue would re-mix project force with global reset and make the smaller project command contract wait on the heavier fleet manifest design.`
    verdict: `supports two-issue promotion handoff`
  - reviewer: `subagent:kierkegaard-runtime`
    mode: `fresh-process runtime truth review`
    summary: `Runtime truth is already strongly project-anchored under `.freely/run` and `--project` pid ownership, while global restore memory belongs to a separate all-project control-plane namespace under `$FREELY_HOME`. That makes `project command semantics` and `global restart restore memory` different blast radii, durable homes, and failure domains, with the global issue explicitly downstream of the project command taxonomy.`
    verdict: `supports two-issue sequencing`
- priority: P0
- status: promoted
- decision_reason: 当前 lane 已完成 `doc-ibm-execution` materialization，并把原始 candidate 明确拆成两个紧邻的 milestone-owned issue：`I-20260327-2006-A` 负责 project-scoped `start/stop/restart/start --force/restore-work` command family、repair order、safe repair set 与 interrupted-local-AI default；`I-20260327-2006-B` 负责 downstream 的 explicit global restart restore memory、manifest durability、previously-running project set 与 operator-stopped exclusion。这样既保留了同一来源主键，又避免 IBM 再次把 project `force` 与 global reset 混层。当前更晚的 branch-local truth 还显示 `I-20260327-2006-A` 已完成 worker implementation slice、feature-lane verification artifact 已落下，并已前移到 manager-owned `completion_verification`。
- next_action: milestone 正式编排已切到 `I-20260327-2006-A` / `I-20260327-2006-B`。当前 active route 保持 `I-20260327-2006-A` 的 manager-owned `completion_verification`，由 manager 消费现有 feature-lane verification evidence 做 merge review / canonical absorption judgement；即使本轮 fresh-session `live-status` 已变成 `last_ai_state=down`、`last_exit_reason=ai_exit_rc_1`，这也仍是 runtime-owned 恢复信号，而不是回退到 IBM 的依据。`I-20260327-2006-B` 继续保持 downstream `done_ibm` owner，等待前者完成 closeout 后再进入 `dev-loop-execution`。
- revisit_trigger: 当 IBM materialization 再次试图把 project command blast radius 与 global restore owner 混成同一 issue，或 live incident 暴露 project command 误杀其他项目进程 / 误清 shared state / global restart 丢失此前 running project 集合 / 误恢复 operator 已停止的 project / interrupted AI work 被 silent discard 或 cross-project restore / durable continuity 被 project force 误清 / stale supervisor 被误判为健康 attach / manager continuity 或 worker prompt consumption memory 被 project force 误删时，回到本 candidate 重新校正边界。
- promoted_issue_path:
  - `docs/B2-docs/ibm/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
  - `docs/B2-docs/ibm/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: 019d377f-37b7-7cf2-8b76-d6a4a36a4a7f
  - jsonl_path: /Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-49-37-019d377f-37b7-7cf2-8b76-d6a4a36a4a7f.jsonl
  - role: author
  - tool: codex
  - session_id: 019d3d46-4e39-7020-afdc-cd2f6822ae30
  - jsonl_path: unavailable://live-status-deep-ref-only
  - role: fresh-session-first-hop-recheck

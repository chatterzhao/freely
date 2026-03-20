# Milestones

本文件是 Freely 自举开发时的主动扫描入口，用来承接已进入活跃范围的 candidate / issue。

## Milestone Policy

milestone_status_policy_version: v2

candidate_policy:
- dropped: remove from active milestone queues
- needs_research: keep in candidate_issues with `next_action` and `revisit_trigger`, and route back to pre-brainstorms or issue-bound brainstorm; do not silently drop it from active scans
- promoted: bind to a milestone immediately; do not leave as long-term unbound state
- blocked: keep visible with blocker, next action, and revisit trigger

queue_policy:
- committed_issues: sequencing is clear and the item is the next active batch
- candidate_issues: belongs to the milestone, but still needs research or ordering
- completed_issues: delivered work kept for traceability within the same milestone

phase_state_policy:
- `phase_state=in_ibm`: keep the issue visible in `committed_issues` with `issue_path` and `next_action`; do not require `progress`
- `phase_state=done_ibm`: keep the issue visible in `committed_issues` with `issue_path` and a clear handoff into dev-loop
- `phase_state=in_dev`: keep the issue visible in `committed_issues` and require matching `progress`
- `phase_state=blocked_dev`: keep the issue visible with blocker, next action, and current execution context
- `phase_state=in_verification`: keep the issue visible until completion evidence is written back
- `phase_state=completed`: move the issue to `completed_issues` with evidence

session_policy:
- full `session_refs` live in candidate / issue / progress / recovery artifacts
- milestone may keep `active_session_ref` as a summary, but `issue_path` is the canonical detail pointer

sequencing_policy:
- ordered_by: dependency_then_control_plane
- allow_unordered_candidates: true

routing_policy:
- no_issue_path: stay in pre-brainstorms or continue doc-loop materialization
- issue_path_present: route by `phase_state` into issue-bound brainstorm, IBM, continuation, dev-loop, or completion verification
- unresolved candidate or issue never disappears just because the current round chose another priority; keep it in the appropriate queue with an explicit restart condition

## M-20260306-workspace-routing-foundation

- title: Workspace routing foundation for Freely dogfooding
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/candidates.md`
- intent: 把首跳路由治理候选正式纳入 milestone，避免 Freely 自己继续依赖悬空 candidate 工作
- why_now: 这批项定义 Freely 如何发现上下文、读取 milestone、并路由到下一跳 skill；如果 milestone 自身不先落盘，Freely 的狗粮链路就是断的

### committed_issues

1. `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md`
- next_action: review 与最小验证已落盘，但 `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`；当前需先按 ownership 收束或分流 dirty 改动，其中 `docs/system/workspace/**` / `tests/**` 与 session-lifecycle 相关产物更像上游未提交批次，应先处理，再补 promote / cleanup 证据后移入 completed_issues

2. `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md`
- next_action: review 与 verification 已落盘，但 `./bin/wt-status-all` 仍为 `Summary: total=6, dirty=1`；当前需先按 ownership 收束或分流 dirty 改动，其中 `docs/system/workspace/**` / `tests/**` 与 session-lifecycle 相关产物更像上游未提交批次，应先处理，再补 completion verification / cleanup 证据后移入 completed_issues

3. `I-20260318-0930`
- title: Checkpoint commit and multi-worktree supervision governance
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/candidates.md`
- next_action: runtime/status 的 dirty budget、project-level worktree summary、脚本级测试与 review 已落盘；当前保持 `in_verification`。本轮 `wt-status-all` 为 `Summary: total=6, dirty=1`，且唯一 dirty 工位就是当前 issue 的 verification continuity，因此无需分流无关改动，但仍未满足 promote / cleanup 前提；完成当前收口后再回到 `I-20260307-1201` 与 `I-20260308-0101` 做 completion verification / cleanup

4. `I-20260318-1408`
- title: Manager self-supervision and autonomous recovery
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/candidates.md`
- next_action: 主管自治的最小实现、PID 归属修复、fleet supervision alert、角色文档与“manager/worker runtime 不直接切全局账号”的回归均已落盘；当前保持 `in_verification`。下一步先做 review 与 promote/cleanup 判断，再决定是否并回 `develop`。更外层的 manager watchdog/ensure 仍是边界外后续问题，不在本批次继续扩 scope。

5. `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/candidates.md`
- next_action: `freely ensure-manager --watch`、坏号后真实 probe、过时 cooldown 账本兜底、manager bootstrap handoff 与 live recovery 测试均已通过；当前做 completion verification / review，并与 manager 自治主线一起决定 promote 顺序

6. `I-20260318-1825`
- title: Worktree hygiene supervision control plane
- milestone_state: committed
- phase_state: `in_verification`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/candidates.md`
- next_action: 新增 hygiene skill、checkpoint drift streak、manager hygiene alert 与回归测试已落盘；当前先做 review 与 promote 判断。若后续仍需专门 hygiene worker，再从同一预研线 materialize，不在本批次越界扩 scope

7. `I-20260319-0018`
- title: Token-efficient session continuity and rotation governance
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/candidates.md`
- next_action: IBM 产物已补齐，下一跳进入 `dev-loop-execution`，把 runtime / prompt / skill 的 continuity 触发边界统一收敛到 trigger matrix，并保持旧会话证据默认按需引用

8. `I-20260319-0148`
- title: Context-compaction continuity guard salvage
- milestone_state: committed
- phase_state: `in_dev`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/context-compaction-continuity-guard-salvage/issues/context-compaction-continuity-guard-salvage.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/candidates.md`
- next_action: 只收编旧 context-compaction 分支独有的 continuity guard 小能力，然后退休旧 worktree；不要重复主线已有的 continuity/rotation 设计

### candidate_issues

1. `C-20260318-0715-A`
- title: `commit-first after checkpoint-ready` 自治治理
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结 3 个边界：`checkpoint-ready` 的结构化输出、`LAWS/runtime/checkpoint-guard/supervisor` 的职责分层、以及进入 IBM 前的 promotion gate；在这些边界稳定前不得直接写成 IBM issue 或塞回 `I-20260318-0930`
- revisit_trigger: 当 `checkpoint-ready` 的结构化输出、supervisor 职责边界与 promotion gate 可以被稳定写成最小 issue contract 时，重新进入 materialization 判断

2. `C-20260319-1105-A`
- title: 三层循环能力映射、owner 边界与生命周期真源收敛
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先验证 `docs/system/workspace/three-loop-capability-lifecycle.md` 是否足以成为唯一细节真源；若仍需更多行为约束，再 materialize 为独立 IBM issue，而不是继续把细节散落到 `CONSTITUTION`、`PROJECT_INTENT` 和多个 skills 中
- revisit_trigger: 当 lifecycle 真源之外仍出现新的行为约束必须落到独立 issue，或 manager/doc/dev-loop 继续出现无法由当前真源解释的冲突时，重新进入 materialization 判断

3. `C-20260319-2315-A`
- title: CLI TUI interruption input box for Freely
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/candidates.md`
- next_action: 继续 pre-brainstorm，先收敛 TUI 是否只作为 interruption shell、中文输入的最低验收、以及输入框/状态区的最小布局；在这些边界稳定前不要直接写 UI 代码或把 TUI 做成第二套入口系统
- revisit_trigger: 当 TUI shell 边界、中文输入最低验收与布局最小集可以被明确冻结成 issue scope 时，重新进入 materialization 判断

4. `C-20260320-0252-A`
- title: Signal restart-point routing across interruption, review, test, and recovery
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://restart-point-routing-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/candidates.md`
- next_action: M1-M3 的 interruption 最小 slice 已落盘：主管 triage 已改成抽象 routing contract，且 `cleanup` followthrough 已形成第一条完整 event 链。下一步继续 pre-brainstorm，把同一 contract 扩到 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan，再决定是否 materialize 为统一 routing issue
- revisit_trigger: 当 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan 已共享同一 restart-point routing contract 时，重新进入 materialization 判断

5. `C-20260320-0908-A`
- title: Unresolved research candidate persistence and revisit governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先把“不能收口时必须显式保持在 candidate/blocked 队列并写清重启条件”的规则写入 lifecycle、lead prompt 与 doc-loop reference，再决定是否 materialize 为独立治理 issue
- revisit_trigger: 当后续 worktree 审查再次发现 unresolved candidate 仍会在队列层被跳过，或当前规则需要更强的 issue-bound enforcement 时，重新进入 materialization 判断

### completed_issues

1. `C-20260306-1101`
- title: `lead-agent.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/lead-agent-bootstrap.md`
- evidence: `docs/system/workspace/agents/lead-agent.md`
- completion_note: 已落地首跳中枢代理职责与首跳协议

2. `C-20260306-1102`
- title: `context-source-skill.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/context-source-skill-bootstrap.md`
- evidence: `docs/system/workspace/skills/context-source-skill/SKILL.md`
- completion_note: 已落地来源判定、milestone 扫描与 usable issue 决策规则

3. `C-20260306-1103`
- title: `doc-pre-brainstorm-execution.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-pre-brainstorm-execution-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- completion_note: 已落地 docs 前置收敛环，负责 pre-brainstorm 产物与 milestone 原子同步

4. `C-20260306-1104`
- title: `doc-ibm-execution.md` 与 `dev-loop-execution.md` 的外循环接驳边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-loop-dev-loop-handoff-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已收紧 issue-bound `IBM+G` 与 `DDD` 的接驳边界，状态交换统一回流给 auto-loop

5. `C-20260306-1105`
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/auto-loop-orchestrator-bootstrap.md`
- evidence: `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`, `docs/system/workspace/scripts/README.md`, `docs/system/workspace/scripts/tests/test-routing-foundation-loop`, `docs/system/workspace/hooks/pre-commit.sh`
- completion_note: 已把 `system/workspace` 真源、`scripts` / `hooks` 与运行时投影映射写回 orchestrator，并补齐最小闭环测试

6. `I-20260308-1631`
- title: 阶段前缀式主进度标识治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/candidates.md`
- evidence: `docs/LAWS.md`, `docs/PROJECT_INTENT.md`, `docs/milestones.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已把 `phase_state` 收敛为 Freely 自举阶段的主执行标识，并统一 `done_ibm -> in_dev` handoff 与 milestone 路由口径

7. `I-20260308-1931`
- title: 业务阻塞状态与系统崩溃恢复定位治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`, `docs/milestones.md`
- completion_note: 已明确分层业务阻塞与系统崩溃恢复，禁止用 `blocked_*` 伪造系统事件交接，并统一恢复定位顺序与最小字段口径

8. `C-20260319-0220-A`
- title: Watchdog umbrella term and sub-control-plane taxonomy
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- evidence: `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`, `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`, `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`, `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- completion_note: umbrella taxonomy 已由 `watchdog-control-plane` 与现有 availability / runtime / continuity issue 主线吸收，不再单独 materialize

9. `C-20260319-0220-C`
- title: Historical watchdog productization worktree retirement handoff
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/pre-brainstorms/CONVERGENCE.md`, `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/brainstorms.md`
- completion_note: 旧 watchdog 产品化工位的 `materialize_then_retire` handoff、cleanup 结果与 retirement heuristic 已完成留痕；该候选归档，不新开 IBM

10. `I-20260316-1801`
- title: Auto-run session lifecycle rotation and handoff governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260303-cli-orchestration-architecture/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260303-cli-orchestration-architecture/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/monitor-ai-cli.sh`, `docs/system/workspace/scripts/tests/test-freely-session-rotation`, `bin/test-freely-session-rotation`
- completion_note: 已把 `resume` 与 `fresh_with_handoff` 区分为显式 runtime 行为，并固定 Codex 默认模型为 `gpt-5.4`、默认 reasoning effort 为 `medium`

## M-20260308-frontend-probe-dogfooding-loop

- title: Frontend probe + backend increment dogfooding loop
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- intent: 把“backend-core-first + frontend-probe-from-day-1”收敛为 Freely 自举开发自己的正式候选批次，避免继续只有后端结论、没有产品面验证闭环
- why_now: Freely 的目标本身就是防止 AI 跑偏；如果自举开发中每个后端增量都不能立刻被前端观察、打断和回放，狗粮链路仍然不完整

## M-20260318-url-content-intake-skill-and-wechat-fetch-governance

- status: active
- linked_issue: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- intent: 把公众号链接抓取研究转成可分享的 skill、脚本和最小测试
- why_now: 研究已经证明本地浏览器 UA 抓取可行；如果不把脚本放进 skill，分享 skill 时能力仍然是不完整的

### committed_issues

1. `I-20260318-1908`
- title: URL 内容摄取 skill 与微信公众号抓取治理
- milestone_state: committed
- phase_state: `in_dev`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/candidates.md`
- next_action: 把 `url-content-intake` skill、自带抓取脚本与最小测试一起落齐，再评审是否并回 `develop`

### committed_issues

1. `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: IBM 已完成最小边界收敛；下一跳把 `C-20260308-1244-02` `Frontend/Backend Boundary Contract v1 for Frontend Probe` 提升到 issue-bound IBM，基于当前 issue 冻结更细的 boundary contract 与事件语义

2. `I-20260317-1001`
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: boundary contract v1 已完成最小 IBM 收敛；下一跳把 `C-20260308-1244-03` `Frontend Probe v0` 提升为 issue-bound IBM，基于当前 contract 收紧最小产品面与验收边界

3. `I-20260317-1002`
- title: Frontend Probe v0
- milestone_state: committed
- phase_state: `in_dev`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: frontend 侧 contract、transport、manifest 和错误面已基本收敛；backend bridge 缺口仍由 `I-20260317-1005` 承接。当前 Rust bridge 的本地 `cargo check` / `cargo test`、前端 `typecheck` / `build` 与公开 manifest 对齐验证都已通过；下一步等待真实 Tauri 宿主启动联调结果，再回到本 issue 收紧 frontend host integration 与 blocker 描述

5. `I-20260317-1004`
- title: Frontend Runtime Baseline for Probe
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- next_action: runtime baseline 已完成最小 IBM 收敛；下一跳回到 `I-20260317-1002`，把 baseline 真正接入 Probe v0 并尝试解除 `blocked_dev`

4. `I-20260317-1003`
- title: Incremental Dogfooding Gate for Backend Increments
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/issues/incremental-dogfooding-gate-for-backend-increments.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: Probe 验证门禁已完成最小 IBM 收敛；后续实现与评审阶段直接按该门禁检查后端增量，不再把验证当成可选项

6. `I-20260317-1005`
- title: Rust/Tauri Probe Bridge v1
- milestone_state: committed
- phase_state: `in_dev`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
- next_action: lead-agent 首跳重入后继续命中 `milestones` 池里的当前 committed `in_dev` issue，并在同一 `codex` 会话内进入 `dev-loop-execution`。当前已补齐 `src-tauri/icons/icon.png`，`bun run rust:preflight`、`bun run cargo:check:probe` 与 `cargo test -p freely-probe-bridge` 已通过；先前的 Rust toolchain / icon blocker 和 `dead_code` warning 均已解除。下一步继续围绕真实 Tauri 宿主启动联调推进，确认前端 `Transport=tauri` 不再停在 `bridge offline`

### candidate_issues

1. `C-20260317-1101`
- title: Frontend Runtime Baseline for Probe
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- next_action: 已提升为独立 issue；后续由 `I-20260317-1004` 承接 issue-bound IBM 收敛

### completed_issues

- none currently

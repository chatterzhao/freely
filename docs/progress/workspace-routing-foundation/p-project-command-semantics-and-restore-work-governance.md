# Progress: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- phase_state: `in_verification`
- runtime_state: `restart_required`
- branch: `feature/start-restart-control-plane-semantics-20260327-200651`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-200651-feature-start-restart-control-plane-semantics`
- issue_path: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- session_refs:
  - {tool: codex, session_id: "019d3752-80a1-7773-808d-081375e06aa7", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-00-47-019d3752-80a1-7773-808d-081375e06aa7.jsonl", role: "dev-loop-progress-refresh"}
  - {tool: codex, session_id: "019d377f-37b7-7cf2-8b76-d6a4a36a4a7f", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-49-37-019d377f-37b7-7cf2-8b76-d6a4a36a4a7f.jsonl", role: "completion-verification-continuity-refresh"}
  - {tool: codex, session_id: "019d3d46-4e39-7020-afdc-cd2f6822ae30", jsonl_path: "unavailable://live-status-deep-ref-only", role: "fresh-session-first-hop-recheck"}

## Summary

- `2026-03-30 16:12 PDT` 当前 parent owner 的 develop absorption 已完成于 commit `b93efd2`。本 progress 在当前 continuation 中只补一条 continuity writeback，目的是让 source candidate `C-20260327-2006-A` 的 parent lane 与 downstream split lane `I-20260327-2006-A-global-restart` 在同一 develop-bound diff 中保持可审计，不重新打开 parent scope。
- `2026-03-30 15:47 PDT` 本轮 manager-side merge review 先把 feature-lane verification 做实：`bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics` 重新通过，wall time 从此前实测约 `46.24s` 收敛到 `13.76s`，因为测试里的两个 background pid probe 不再把 `sleep 30` 的 stdout fd 留在 command substitution 上。同时该测试新增 signal-aware cleanup：若在 `ALRM/TERM/INT/HUP` 下被打断，会先对 late-bound `PROJECT` 执行 project-local `freely stop`，再清掉辅助 pid 与 temp dirs，故意用 `perl -e 'alarm ...' 5` 打断时现在返回 `RC=142` 且不再遗留 `ensure-interruption-dispatch --watch` orphan。当前 dirty slice 因此不再是“5-file verification writeback only”，而是“verification/progress writeback + focused regression cleanup hardening”，仍属于同一 issue 的 verification fixup，而不是 reopen IBM 或重开下游 `I-20260327-2006-B` 的理由。
- `2026-03-29 23:25 PDT` 当前轮 fresh session 再次按 `AGENTS.md -> constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> live-status` 复核。`live-status` 现在显示本 worker lane `last_ai_state=down`、`last_exit_reason=ai_exit_rc_1`、`last_launch_kind=resume`，同时 `pending_delegated_continuation_ids=none` 仍保持为空，`last_consumed_delegated_continuation_ids` 继续覆盖到 `20260328-062746`。因此这次变化仍然是 runtime-owned recovery/supervision evidence，而不是 route 变化；更强的 branch-local truth 仍是 `milestones -> issue -> progress -> verification artifact -> worker continuity`，所以本 lane 继续停在 manager-owned `completion_verification`。当前 worktree 的 5-file dirty slice 只是在补齐这层 verification/continuity writeback，不代表要回退到 IBM 或重开 dev-loop。
- `2026-03-29 22:47 PDT` 当前轮再次按 `AGENTS.md -> constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> live-status` 复核。`live-status` 继续显示当前工位 `role_hint=worker`、`activity_state=ai_active`、`current_prompt_has_delegated_continuation=1`、`pending_delegated_continuation_ids=none`，且 `last_consumed_delegated_continuation_ids` 已覆盖到 `20260328-062746`；因此当前 prompt 中残留的 IBM delegated continuation 继续只算 supervision history。更强的 branch-local truth 仍是 `milestones -> issue -> progress -> verification artifact -> worker continuity`，所以本 lane 继续停在 manager-owned `completion_verification`，不回退到 IBM，也不重新宣称 worker `in_dev`。
- 2026-03-28 这条 lane 已从 `done_ibm` 正式切到 `in_dev`，因为 runtime 真源已经开始 materialize project command family。
- `2026-03-28 19:20 PDT` 当前 worktree 已 clean，checkpoint `5bc3a86` 已落下，且 feature-lane verification artifact `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md` 已补齐。因此当前 branch-local truth 不再停留在 `checkpoint / verification-prep`，而是前移到 manager-owned `completion_verification` 收口；旧的 IBM handoff 继续只算 supervision history。
- `2026-03-28 19:16 PDT` 在决定是否切 checkpoint 前，再次补跑 `bash -n docs/system/workspace/scripts/runtime/freely`、`bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`、`bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready` 与 `./bin/governance-check`。结果继续通过，`governance-check` 仍只有仓库既有的 legacy pre-brainstorm naming warnings，因此当前 5-file dirty slice 继续可视为同一 issue 的 checkpoint-ready implementation set，而不是需要回退到 IBM 的未定边界。
- `2026-03-28 19:12 PDT` 再次读取 `live-status` 后，当前 worker 仍是同一条 active lane，且 `last_launch_kind` 已更新为 `resume`、`last_rotation_reason=unavailable`、`pending_delegated_continuation_ids=none`。同一份 readback 还带出了 `restart_storm_signal_reason=restart_storm_count_threshold`、`restart_storm_escalation_target=manager_bootstrap_handoff`，但由于 active AI / supervisor 进程和 branch-local `milestones -> issue -> progress -> worker continuity` 真相都未变化，这组信号继续只记为 runtime-owned 监督证据，不触发重新回 IBM 或扩 scope。
- `2026-03-28 19:07:34 PDT` 再次读取 `live-status` 后，当前 session evidence 已从 `current-thread` 降级占位升级为显式 Codex session：`session_id=019d3752-80a1-7773-808d-081375e06aa7`，`jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-00-47-019d3752-80a1-7773-808d-081375e06aa7.jsonl`。同一轮 `live-status` 继续显示 `last_launch_kind=fresh_with_handoff`、`last_rotation_reason=resume_streak_limit`、`pending_delegated_continuation_ids=none`，因此本 lane 仍应继续消费 branch-local `dev-loop` truth，而不是回退到旧 IBM handoff。
- `2026-03-28 19:03:14 PDT` fresh session 再次按 `AGENTS.md -> constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> live-status` 完成首跳闭环。当前 `live-status` 仍把本工位标成 active worker，并继续显示 `current_prompt_has_delegated_continuation=1`、`pending_delegated_continuation_ids=none`、`last_consumed_delegated_continuation_ids` through `20260328-062746`；因此旧的 IBM relaunch handoff 继续只算 supervision history，本轮直接续接 `I-20260327-2006-A` 的 `dev-loop-execution`。
- 同轮重新执行 `bash -n docs/system/workspace/scripts/runtime/freely`、`bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`、`bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready` 与 `./bin/governance-check`，结果全部通过；因此当前 dirty worktree 仍然是同一 issue 的 runtime/test/doc writeback，不需要因为 route 不确定而退回 IBM。
- 本轮也顺手校正了 issue 内部一致性判断：`tasks.md` 与 `pre-tests.md` 已经反映当前 focused runtime slice 和 regression 均已落地，因此 `progress` 后续不再把重点表述成“还有一批未实现 runtime slice”，而是切到 checkpoint / verification-prep 语义，避免同一 issue 在 dev-loop 内部自相矛盾。
- `2026-03-28 06:41:08 PDT` 本轮再次按 `AGENTS.md -> constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> live-status` 执行首跳闭环，结论仍然不是回到 IBM：`live-status` 显示当前 worktree 仍是 active worker，`pending_delegated_continuation_ids=none`，而 `last_consumed_delegated_continuation_ids` 已延伸到 `20260328-062715`、`20260328-062728`、`20260328-062746`。这些新 handoff 继续只提供监督层 relaunch history，没有推翻更晚的 branch-local `milestones -> issue -> progress -> worker continuity` 真相，所以当前 issue 继续保持 `in_dev`。
- 同日首跳重新核对 `AGENTS.md`、`PROJECT_INTENT`、`CONSTITUTION`、`LAWS`、`lead-agent`、`context-source-skill` 与 `doc-ibm-execution` 后，确认 manager 在 `2026-03-28 00:37:53 PDT` 生成的 IBM handoff 已被更新的 branch-local truth 超过：`docs/milestones.md`、source candidate、issue docs 与 worker continuity 都已把本 lane 固定到 `dev-loop-execution`，因此本轮不重复 IBM materialization，而是直接吸收到现有 `in_dev` 闭环。
- `2026-03-28 04:25:51 PDT` 本轮继续吸收 delegated continuation `20260328-041512`、`20260328-041942`、`20260328-042321`。按 `lead-agent -> context-source-skill` 的 continuation 规则，它们补充的是监督层 handoff，而不是新的 branch-local route truth；因此当前 worktree 仍应以既有 `candidate -> issue -> progress` 链为准，保持 `I-20260327-2006-A` 在 `dev-loop-execution`，并把旧 IBM prompt 继续视为 stale supervision history。
- `2026-03-28 06:10:41 PDT` runtime 因 `context_compacted` 触发 `fresh_with_handoff` 后重新拉起当前 worker，本轮先按 `live-status -> governance readback -> branch-local continuity` 复核，确认 prompt 注入的 delegated continuation `20260328-050900`、`20260328-050923`、`20260328-061034` 仍然只是同一 canonical lane 的监督层 relaunch handoff；更晚的 branch-local `milestones -> issue -> progress -> worker continuity` 真相继续把本 lane 固定在 `source_class=continuation`、`route_kind=dev_loop`、`target_skill=skill:dev-loop-execution`。
- 当前已落下的实现切片：
  - usage surface 增加 `freely start --force`、`freely restart`、`freely restore-work`
  - `cmd_stop()` 的 project-local kill / cleanup 逻辑被提取成 `stop_project_runtime()`
  - `start --force` 走 project-local stop reason `start_force`
  - `restart` 走 project-local stop reason `operator_restart`，默认不做 implicit work restore
  - plain `start` 现在会把 healthy same-project supervisor 视为 `ensure-up` / attach-reuse，而不是报 `already running`
  - plain `start` 在 attach/reuse healthy same-project supervisor 时，会顺手清掉不再属于当前 project AI truth 的 stale `ai.pid`，避免把 attach 成功后的 local run-state 留在过期 child pid 上
  - plain `start` 现在也会在 `supervisor.pid` 漂移缺失时，通过 project-safe process discovery 找回 live same-project supervisor 并回填 pid file，而不是误走 fresh bootstrap 再起第二个 supervisor
  - plain `start` 在发现 orphaned same-project `ai.pid` 时，会先做 project-local terminate-and-wait repair，再继续 supervisor restart；避免 local repair 与 fresh bootstrap 在 child 仍未退出时交叠
  - plain `start` 的 attach/reuse gate 现在要求 sidecar readiness 一并健康：worker 至少要有 interruption dispatcher，manager 还要有 watchdog；若只剩 partial supervisor，则降级回 project-local repair 而不是假装已经 up
  - `restore-work` 只接受 project-scoped continuity anchors；`session-state.env` 与 `session-handoff.txt` 明确保持 auxiliary-only
  - `pid_matches_project()` 不再把“cwd 恰好落在当前 repo 的无关进程”直接当作 Freely-owned runtime；现在必须先命中 Freely-specific command signature，cwd 只作为辅助 ownership 证据
  - `stop_project_runtime()` 现在会忽略不属于当前 project 的 stale `ai.pid`，避免 project-local stop / force 误杀无关进程
  - `start_project_runtime()` 现在会先清理不属于当前 project 的 stale `supervisor.pid`，而不是把它误判成合法的 already-running supervisor
  - `stop_project_runtime()` 现在会对合法的同项目 `ai.pid` / `supervisor.pid` / dispatcher / watchdog 走 terminate-and-wait，而不是只发信号后立刻 fresh bootstrap；此前 supervisor wait 分支因为 pid 文件已提前删除而实际上不会生效
  - `runtime_ai_pid_hint_for_project()` 不再把“ai.pid 指向任意仍存活 pid”当成当前 workcell 的 AI truth；它现在与 stop/start 一样继续要求 project identity 校验，避免 live-status 误报 `ai_active`，也避免 local continuation reentry 误杀 foreign live pid
- 本轮重新验证的结论：
  - plain `start` 的 healthy attach/reuse 路径已落到 runtime，与 issue 中“ensure current project up”定义一致
  - runtime main dispatch 仍稳定接入 `restart` 与 `restore-work`
  - focused regression `test-freely-project-command-semantics` 继续覆盖 `restart`、`start --force` 与 `restore-work` anchor gate
  - `test-freely-start-requires-interruption-dispatcher-ready` 继续锁定 project start 不会绕过 interruption dispatcher readiness gate
  - `./bin/governance-check` 通过；当前只剩仓库既有 legacy pre-brainstorm naming warnings，没有新增阻断
  - focused regression 现已把 project-identity anchored process handling 一并锁住：stale foreign pid 不会误阻塞 start，也不会被 stop / force 流误杀；same-project 但非 Freely command 的 shell / tool 进程也不会再被误认作 owned pid
  - focused regression 现已补上 runtime helper 层的 identity guard：foreign live pid 即使仍留在 `ai.pid`，也不会再把 activity state 误判成 `ai_active`，更不会被 `request_local_continuation_reentry()` 当成当前 workcell AI 去 terminate
  - focused regression 现已补上 project-local repair ordering 的等待语义：orphaned same-project AI child 会先终止并等待退出，再继续 supervisor restart
  - focused regression 现已补上 attach gate 的 health floor：live same-project supervisor 只有在 dispatcher/watchdog readiness 同时成立时才允许 attach；否则必须降级回 partial-repair path
  - focused regression 现已补上 attach-reuse 下的 stale child pid hygiene：healthy same-project supervisor 可以直接复用，但不会继续保留失效的 `ai.pid` 去污染后续 local run-state 观察
  - focused regression 现已补上 project-safe process discovery：即使 `supervisor.pid` 丢失，只要 live same-project supervisor 仍可识别，plain `start` 也会回填 pid file 并 attach/reuse，而不是直接 fresh bootstrap 出第二个 supervisor
  - focused regression 现已补上 `start --force` / `restart` 共用 stop path 的等待语义：合法的同项目 AI child 与 supervisor 会先退出，再写回 stopped state 并允许后续 fresh bootstrap
  - 本轮 fresh-with-handoff 之后再次复跑 `bash -n docs/system/workspace/scripts/runtime/freely && bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics && bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready && ./bin/governance-check`，结果继续通过；因此当前 dirty worktree 属于同一 issue 的未提交实现/文档写回，而不是需要分流到其他 worktree 的无关改动

## Current Focus

- 保持 `restart` / `start --force` / `restore-work` 的 project-local taxonomy 不回退，不把 global restart manifest owner 提前拉进当前 issue
- 保持 explicit `restore-work` 只消费 mandatory anchors，不把 transient pid/run-state 升格成 required truth
- 维持 attach/reuse、safe repair set、project-identity anchored pid handling 与 wait ordering 的已通过 focused regressions 作为当前 implementation floor
- 补齐 feature-lane verification harness 自身的 cleanup contract，避免短超时/中断把 `ensure-interruption-dispatch --watch` 留成 orphan，避免 manager verification 再次被假 hang 误导
- 当前 issue 的 worker implementation 已 checkpoint 并补齐 verification artifact；下一步重点改为 manager-owned `completion_verification` closeout，而不是继续扩写 runtime slice
- 为后续 `I-20260327-2006-B` 保留清晰的 downstream 依赖，不在当前 issue 提前混入 global restart manifest owner
- 当前 branch-local merge base 仍是 checkpoint commit `5bc3a86`，但 worktree 已进入 verification fixup 脏态；后续应把它当作同一 issue 的 closeout 清理，而不是伪装成“仍然 clean at checkpoint”
- `restart_storm_signal_reason=restart_storm_count_threshold` 已被当前 first-hop 记入 continuity/progress，但它仍属于 runtime-owned 监督面；在 branch-local issue truth 已前移到 `completion_verification` 后，仍不把它升格成新的 doc-loop 或 cleanup route

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- interruption cleanup probe: `perl -e 'alarm shift @ARGV; exec @ARGV' 5 bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics` -> expected `RC=142` with no `/tmp/freely-project-command-semantics*` watcher residue
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `./bin/governance-check`
- `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-200651-feature-start-restart-control-plane-semantics`
- explicit session evidence refresh: `session_id=019d3752-80a1-7773-808d-081375e06aa7`, `jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-00-47-019d3752-80a1-7773-808d-081375e06aa7.jsonl`
- latest resume-state refresh: `last_launch_kind=resume`, `last_rotation_reason=unavailable`, `pending_delegated_continuation_ids=none`, `restart_storm_signal_reason=restart_storm_count_threshold`, `restart_storm_escalation_target=manager_bootstrap_handoff`
- readback: `AGENTS.md`, `docs/PROJECT_INTENT.md`, `docs/CONSTITUTION.md`, `docs/LAWS.md`, `docs/milestones.md`
- readback: `docs/system/workspace/agents/lead-agent.md`
- readback: `docs/system/workspace/skills/constitution-guard/SKILL.md`, `docs/system/workspace/skills/laws-enforcer/SKILL.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- rerun after delegated-continuation absorption: `bash -n docs/system/workspace/scripts/runtime/freely && bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics && bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready && ./bin/governance-check`
- fresh-session rerun after current first-hop closure: `bash -n docs/system/workspace/scripts/runtime/freely && bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics && bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready && ./bin/governance-check`
- checkpoint-prep rerun: `bash -n docs/system/workspace/scripts/runtime/freely && bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics && bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready && ./bin/governance-check`
- feature-lane verification artifact: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md`

## Next Action

- 当前 fresh session 继续停在 manager-owned `completion_verification`，但 merge review 已经指出 test-harness cleanup 需要同 issue fixup；本 worktree 当前脏改动因此属于 verification/writeback + focused regression cleanup hardening，而不是新的 runtime feature batch
- 当前 route 已从 worker `dev-loop-execution` 收敛到 manager-owned `completion_verification`；本 worktree 默认不再继续实现，除非 merge review 明确指出需要 feature-lane fixup
- checkpoint `5bc3a86` 与 feature-lane verification artifact 已经构成当前批次的 worker closeout 证据；下一步由 manager 判断 merge review / canonical absorption
- 若后续实现再次暴露 project-vs-global owner 混层，再回 `doc-pre-brainstorm` / `doc-ibm`；在此之前保持当前 issue 作为唯一 project command owner
- 继续把 `20260328-050900`、`20260328-050923`、`20260328-061034`、`20260328-062715`、`20260328-062728`、`20260328-062746` 这组 IBM-style relaunch handoff 视为 stale supervision history；除非 branch-local `milestones/issue/progress` 再次退回 docs 缺口，否则不要回退到 IBM
- 当前 branch-local continuity/progress 已跟上 checkpoint 与 verification artifact，不再保留“先 checkpoint”这类过期 next action
- 若 runtime 后续真的把 `restart_storm` 升格成 manager-owned 恢复动作，再由 runtime/manager continuity 接管；当前 worker 只保留 evidence writeback，不把它误写成新的 issue owner
- 当前 issue 保持 `in_verification`，等待 manager-owned completion verification judgement；下游 `I-20260327-2006-B` 继续留在 downstream `done_ibm`

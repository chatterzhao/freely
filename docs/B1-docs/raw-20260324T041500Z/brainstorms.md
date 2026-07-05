# 预研：application-native runtime observation and observability planes

## Trigger

- 这轮 Freely 自举里，用户明确指出“固定 90 秒观察窗口”不如先看会话 `jsonl`、cycle log 和当前态末尾信号。
- 现有 `live-status` 已经解决了“当前谁在跑、在做什么”的最小 CLI 面，但还没有把“如何判断仍在推进 / 已经空转 / 已具备插话着力点”收成统一协议。
- Freely 未来要开发任意应用，不能把 `live-status / fleet-status / jsonl / cycle log` 写死成通用观察法；这些只是 Freely 自举时最先落地的 concrete profile。
- CLI / TUI / GUI / future API 都需要暴露当前应用的运行态给用户观察、插话和回放；多个 worktree、多个 subagent、多个会话/日志也要能被同一控制面解释，但不同应用的具体 surface 可以不同。

## Problem

当前仓库已经有三块相关能力，但缺桥：

1. `watchdog live-status surface` 解决了最小 current-state surface。
2. `pre-test-merge acceptance stall` 在收窄“什么时候 delegated continuation 真 stall”。
3. `frontend probe dogfooding loop` 在讨论用户可观察、可打断、可回放的产品面。

缺的部分是：

- 什么叫“应用原生真实环境测试”的观察协议。
- 主管、watchdog、用户插话之前，应该按什么顺序读哪些证据面。
- 多个状态平面、会话平面、流式日志平面、fleet 平面之间如何对应。
- 如何把 Freely 自己的观测信号泛化成未来任意应用都能消费的 contract。
- CLI / TUI / GUI / API 应该把哪些平面直接暴露给用户，才能让用户知道“系统现在在哪个状态、该往哪里插话、该展开哪条日志/会话继续判断”。

## Direction

不要把这条线写成“继续扩 live-status”，也不要把它收缩成“stall 检测技巧”。

更合适的能力边界是：

- `application-native runtime observation contract`
- `observability planes for CLI / TUI / GUI / future API`

它应该回答：

1. 当前应用有哪些 observation surfaces。
2. 哪些 surface 回答“现在谁在干活、在干什么”。
3. 哪些 surface 回答“这个 loop 还在推进还是已空转”。
4. 哪些 surface 回答“用户应该往哪个状态、哪个会话、哪个 artifact 插话”。
5. 哪些 surface 回答“什么时候测试真正通过，什么时候还不能删 worktree”。

## Product Surface Requirement

这条线不只是内部 watchdog 观察技巧，还要收敛成用户可消费的状态暴露 contract。

未来至少要支持：

- CLI surface：快速 current-state / fleet summary，以及可点击/可复制的 deep refs
- TUI surface：状态卡片、日志 tail、artifact drill-down、用户插话入口
- GUI surface：多平面视图、lane/worktree/session drill-down、实时流展开
- future API surface：结构化状态、session refs、artifact refs、queue/frozen/retire 状态暴露

这些 surface 不必 day-1 同时实现，但本线必须先冻结它们共享的最小信息架构。

## Proposed Planes

### 1. Current-state plane

回答：

- 当前有哪些 runtime / manager / worker / subagent 活着
- 每个 worktree 当前 phase / ownership / desired state 是什么
- 当前 continuity / prompt 聚焦点是什么

Freely 当前 concrete profile：

- `live-status`
- `fleet-status`
- `manager continuity`
- `worker prompts`

产品面要求：

- 每个状态卡片至少应带 `owner / phase / desired state / current activity`
- 卡片必须能告诉用户“下一步最相关的深挖入口是什么”
- 若当前适合插话，卡片必须能暴露对应 lane / topic / project 着力点

### 2. Session plane

回答：

- 当前状态对应哪个会话
- 哪个 `tool / session_id / jsonl_path / cycle_log / prompt_file` 是深挖入口
- 多个 worktree、多个 subagent 的会话如何映射回同一 topic / lane

Freely 当前 concrete profile：

- `session_refs`
- `~/.codex/sessions/**/*.jsonl`
- `.freely/logs/cycle-*.log`
- `.freely/run/prompt-*.txt`

产品面要求：

- 状态卡片能跳到对应 session / prompt / log
- 同一 topic 下多个 worktree / subagent 的 session 能映射回统一 lane
- deep ref 允许 human-readable，但最小映射字段要 machine-readable

### 3. Stream plane

回答：

- 当前有哪些实时日志 / 事件流可看
- 默认展示多少，何时展开
- 如何从“状态卡片”跳到实时流
- 具体 transport 可以是日志、事件流、trace、console 或其他应用原生 stream，只要能提供 tail 和 deep ref

Freely 当前 concrete profile：

- cycle log tail
- session jsonl tail

产品面要求：

- 默认只看 tail，但要能一键展开完整实时流
- 流式面必须标清它属于哪个 worktree / lane / session
- 若存在多个并行流，默认要能按 topic 或 owner 聚合，而不是只按文件名堆叠

### 4. Fleet plane

回答：

- 多 worktree / 多 lane / 多 subagent 的全局排班视图
- 哪些 active / queued / frozen / stale / retire-candidate
- 哪些 lane 是 manager-owned，哪些是 worker-owned

Freely 当前 concrete profile：

- `fleet-status`
- milestone / issue / progress / recovery

产品面要求：

- 必须能看到多 worktree / 多 lane / 多 subagent 的全局状态流转
- 至少区分 `active / queued / frozen / evidence-only / merge-ready-not-delete-ready / retire-candidate`
- 要能从 fleet 总览点进单个 lane 的状态卡片和 deep refs

### 5. Artifact plane

回答：

- continuity、resolution、verification、cleanup、pre-tests 等 canonical artifact 在哪里
- 当前 loop 是卡在 artifact 未生成、未消费，还是测试未完成

Freely 当前 concrete profile：

- interruption intake / resolution
- manager continuity
- worker continuity
- verification / cleanup evidence
- issue `pre-tests.md`

产品面要求：

- artifact plane 必须告诉用户“当前是缺 artifact、缺消费、缺测试、还是缺 cleanup”
- testing closeout 必须能从 artifact plane 直接看出：
  - `pre-tests.md` 是否存在
  - 是否逐项执行
  - application-native real-environment testing evidence 是否齐
  - 为什么 아직不能删 tree

## Minimum Shared Schema

本线若要接近 materialization，不能只停在“有五个 plane”的命名层；还要先冻结最小共享 schema。

### 1. Plane identity block

每条可观察记录至少应能回答：

- `plane_kind`
- `entity_kind`
- `entity_ref`
- `owner_kind`
- `owner_ref`
- `loop_kind`
- `phase_state`
- `topic_ref`
- `deep_ref`

解释：

- `plane_kind`: `current-state | session | stream | fleet | artifact`
- `entity_kind`: `project | worktree | lane | session | artifact | runtime`
- `owner_kind`: `manager | worker | watchdog | human | runtime`
- `loop_kind`: `auto-loop | doc-loop | dev-loop`
- `deep_ref`: 允许 human-readable，但必须稳定指向 deeper surface

### 2. Progress signal schema

progress signal 不判断“已经完成”，只判断“仍在推进”。

最小字段：

- `signal_class=progress`
- `progress_kind`
- `progress_ref`
- `observed_at`
- `topic_ref`
- `loop_kind`
- `entity_ref`
- `delta_summary`

`progress_kind` 最小词典：

- `state_transition`
- `artifact_generated`
- `artifact_consumed`
- `stream_activity`
- `test_step_completed`
- `cleanup_step_completed`

### 3. Stall signal schema

stall signal 不直接裁决 dead loop，只暴露“需要主管进一步判断”的证据。

最小字段：

- `signal_class=stall`
- `stall_kind`
- `observed_at`
- `topic_ref`
- `loop_kind`
- `entity_ref`
- `evidence_ref`
- `suspected_owner`

`stall_kind` 最小词典：

- `no_progress_delta`
- `repeated_same_stage`
- `stream_quiet_after_handoff`
- `artifact_missing_or_not_consumed`
- `restart_storm_suspected`
- `state_surface_conflict`

### 4. Acceptance evidence schema

acceptance evidence 要回答“测试有没有真的跑过，为什么还不能判完成”。

最小字段：

- `signal_class=acceptance_evidence`
- `acceptance_scope`
- `acceptance_target`
- `topic_ref`
- `issue_ref`
- `pre_tests_ref`
- `evidence_ref`
- `completion_state`
- `delete_gate_state`

`acceptance_scope` 最小词典：

- `integration`
- `application_native_real_environment`
- `post_merge_acceptance`
- `cleanup_closeout`

`completion_state` 只表达 issue 层：

## Materialization boundary

这条线进入 IBM 时，冻结的是 shared observation contract，而不是一次性把所有状态面实现完。

- IBM 应冻结：
  - 五类 plane 的最小词典与职责
  - `plane identity block`
  - `progress / stall / acceptance evidence` 三类 schema
  - CLI / TUI / GUI / API 共享的 `status card minimum fields` 与 `deep ref groups`
  - Freely self-host concrete profile 如何把现有 `live-status` / `fleet-status` / session / artifact surfaces 映射到共享 contract
- IBM 不应直接要求：
  - 新建并替换现有 `live-status` / `fleet-status`
  - day-1 把 subagent 做成一等后端实体
  - 一次性完成 richer runtime UI / transport / stream 产品化
- 因此当前最小剩余 blocker 已收窄为两类：
  1. `acceptance evidence schema` 的 canonical 落点，以及它如何被 current-state / API 摘要消费
  2. CLI / TUI / GUI / API 共享的 `deep ref groups` 最小兼容规则

其余边界当前已冻结：

- `current-state plane` / `fleet plane` day-1 继续由既有 `live-status` / `fleet-status` 承接
- 多 subagent day-1 继续聚合在 lane / worktree / session surfaces 下，而不是成为新的强实体
- richer runtime / UI observability productization 若超出 shared contract，应进入 follow-on issue，而不是继续阻塞本线 materialization

- `not_ready`
- `partially_evidenced`
- `fully_evidenced`

`delete_gate_state` 只表达 worktree 层：

- `not_merge_ready`
- `merge_ready_not_delete_ready`
- `delete_eligible`

## Product-facing State Exposure Contract

CLI / TUI / GUI / API 不必同一天实现同一渲染层，但应共享一套最小状态暴露 contract。

### Status card minimum fields

每张状态卡片最少应暴露：

- `summary`
- `owner_ref`
- `loop_kind`
- `phase_state`
- `current_activity`
- `next_best_ref`
- `interruption_anchor`
- `risk_flag`

其中：

- `next_best_ref` 指向最值得继续深挖的 plane / deep ref
- `interruption_anchor` 告诉用户应朝哪个 topic / lane / entity 插话
- `risk_flag` 只暴露高层风险，如 `stalled | conflicted | waiting_for_test | cleanup_blocked`

### Deep ref groups

不同 surface 应共享同一组 deep ref 分类：

- `session_ref`
- `stream_ref`
- `artifact_ref`
- `fleet_ref`
- `acceptance_ref`

CLI 可只给摘要与 ref；TUI / GUI / API 可进一步展开 richer drill-down，但不应发明另一套 ref 分类。

## Freely Self-host Concrete Profile Mapping

Freely self-host 当前 concrete profile 应作为 profile 示例，而不是通用实现强约束。

- `current-state plane`: `freely live-status`
- `session plane`: `session_refs`、prompt refs、jsonl refs
- `stream plane`: cycle log tail、session jsonl tail
- `fleet plane`: `freely fleet-status`、milestone/progress/recovery ownership surfaces
- `artifact plane`: interruption resolution、manager continuity、worker prompt/continuity、verification/cleanup evidence、`pre-tests.md`

关键边界：

- 其它应用不要求存在 `jsonl` 或 cycle log
- 其它应用只需提供能映射到同一 shared schema 的 native surfaces
- Freely 也不应把自己的 concrete profile 冒充成所有应用的唯一 contract

## Observation Order

本线的核心不是时间阈值，而是先观察“是否有前进信号”。

推荐顺序：

1. current-state plane
2. stream plane 的 tail（最后 10-20 行）
3. artifact plane 的增量
4. fleet plane 的状态冲突
5. 时间阈值只作为最后 watchdog fallback

对 Freely 自举来说，当前 concrete 顺序是：

1. `freely live-status`
2. 最新 cycle log tail
3. 对应 session jsonl tail
4. `manager-continuity` / `worker-prompts` / `live-status` generated-consumed delta
5. 需要全项目判断时再看 `fleet-status`
6. 超过 stall threshold 仅作为最后兜底

这里的关键不是“等几秒”，而是：

- 先看当前态是否已经给出插话着力点
- 再看 stream tail 是否还有推进信号
- 再看 artifact 是否真的在前进
- 最后才让时间阈值兜底

这样既适用于 Freely 自举，也能泛化到 future arbitrary apps。

## Boundary

本线不直接实现：

- 新的 stall recovery runtime patch
- 新的 TUI / GUI 页面
- 新的 JSON API server

本线先冻结：

- observation planes 词典
- application-native observation contract
- Freely self-host concrete profile
- product-facing state exposure contract
- 与现有 `live-status` issue、stall candidate、frontend probe 的依赖关系

当前仍不冻结：

- richer UI 的具体交互设计
- stream transport 的唯一实现方式
- 非 Freely 应用必须暴露哪些具体命令/日志文件

## Remaining Blockers Before Materialization

进入 materialization 前，至少还要把下面几件事收死：

1. `acceptance evidence schema` 的 canonical truth 固定落在 artifact plane；current-state / fleet / API 只允许镜像最小摘要字段与 `acceptance_ref`，不得复制完整 acceptance payload。
2. CLI/TUI/GUI/API 共享同一组最小 `deep ref groups`；richer surface 可以扩展 drill-down，但不得替换或重命名最小 ref 组。
3. 独立 acceptance review 只需再确认这条线确实是新的 upstream contract，而不是对 `live-status` 或 stall candidate 的重复建模。

已提前收口、暂不再作为 blocker 的边界：

- `current-state plane` / `fleet plane` 默认继续承接现有 `live-status` / `fleet-status`；若后续要扩 richer product surfaces，应建立在 shared `status card minimum fields` 与 `deep ref groups` 之上，而不是另造平行 current-state surface。
- 多 subagent 默认继续通过 lane/worktree surface 暴露活动痕迹与结果，不要求 day-1 backend 把每个 subagent 做成一等可观察实体。
- `acceptance evidence schema` 的 canonical home 固定为 artifact plane；current-state / fleet / API 只镜像 `completion_state`、`delete_gate_state`、`acceptance_scope`、`acceptance_target` 与 `acceptance_ref` 这一最小摘要。
- CLI / TUI / GUI / API 的最小 `deep ref groups` 固定为：`session_ref`、`stream_ref`、`artifact_ref`、`fleet_ref`、`acceptance_ref`；允许 richer surface 扩展，但不得删除或改名这些共享 ref 组。

## Coordination With Existing Lines

### 与 `I-20260320T194500Z` 的关系

- `I-20260320T194500Z` 已完成最小 `live-status` surface。
- 本线不是重开它，而是定义后续如何把 `live-status` 放进更大的 observation planes 框架。
- 若未来需要扩 CLI/TUI/API 的多平面暴露，可回到该 issue 族或由本线 materialize 新 issue 承接。

### 与 `C-20260322T071500Z-A` 的关系

- `0715` 关注 delegated acceptance stall 何时成立。
- 本线为它提供上游观察协议：先看哪些 plane、哪些 tail、哪些 artifact delta。
- `0715` 不应自己再定义一套独立观察顺序。

### 与 frontend probe 的关系

- frontend probe 关注产品界面和交互承载。
- 本线定义这些界面/接口到底应该展示哪些 plane、怎么让用户找到插话着力点。
- 也就是说，本线是 probe/UI 的信息架构与观测 contract 上游。

## Intended Landing

若后续边界稳定，最终真源预计会落到：

- `docs/system/workspace/skills/multi-worktree-supervision/**`
- `docs/system/workspace/skills/watchdog-control-plane/**`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/tools.md`
- CLI / TUI / GUI / future API 的状态 surface 真源

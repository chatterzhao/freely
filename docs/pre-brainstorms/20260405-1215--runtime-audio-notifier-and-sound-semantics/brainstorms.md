# Brainstorm - 20260405-1215--runtime-audio-notifier-and-sound-semantics

## Problem

Freely 是自治运行时，但当前没有稳定的“任务开始/结束/阻塞/失败”的声音语义系统。用户希望在自治执行过程中，不必持续盯住 UI 或终端，也能通过不同提示音区分 manager、worker，以及开始、结束等关键状态变化。

这个问题不能简单等同于“watchdog 播音”。需要先明确：

1. Freely 应消费什么作为 canonical completion/start signal。
2. 这些 signal 应由 watchdog 产出，还是由独立的 event/notifier 能力消费。
3. manager / worker / blocked / failed 是否需要不同声音语义。
4. 第一轮是否只做标准路径，不实现 fallback。

## Confirmed Facts

- 现有 `watchdog-control-plane` 已把 watchdog 分成 `availability / runtime / continuity` 三层，职责是监督、恢复、状态暴露，不是用户提醒执行器。
- `runtime/freely` 当前已经混合承担两类职责：
  - supervisor / recovery / state writeback
  - 从 `cycle_log`、`debug_log`、`jsonl` 提取低层 signal，例如 `context compacted`、Codex token/rate-limit、Claude->Codex MCP 调用痕迹
- `session-evidence-resolver.sh` 已能解析 Claude session -> Codex thread -> Codex jsonl 证据链，说明“原始工具事件/证据 -> Freely canonical signal”这条思路已经有局部实现，只是尚未抽象成统一 event source。
- 当前前端探针已经具备 Tauri event listen 能力，说明“runtime emit event -> 前端消费 event”是现成路径。
- 当前 Tauri 配置和前端代码中还没有稳定的音频资源、音频策略或音频执行器。
- OpenAI 官方当前为 Responses API / background response 提供结构化 lifecycle event，例如 `response.completed`；这意味着至少对 Codex API 路径，主设计不必退化成会话全文监听。

## Boundary Judgment

- 这不是现有 watchdog owner 的直接小补丁。
- 这更接近一个新的 Freely runtime capability：`runtime event -> sound semantics -> audio notifier`。
- watchdog 仍应保留为监督/恢复 owner；音频提醒应由独立 notifier/event-router 消费 canonical event。
- 第一轮先做标准路径：
  - canonical runtime event
  - manager / worker / blocked / failed / interruption 等声音语义
  - Tauri/UI 侧播放打包音频资源
- fallback 暂不进入第一轮：
  - 不先做 `afplay` / `aplay` / PowerShell / terminal bell`
  - 不先做“无原生事件时 grep 自然语言全文”的通用兜底

## Key Questions

1. 第一轮 canonical sound event 最小集合是什么，是否至少包含：
   - `manager.run.started`
   - `manager.run.completed`
   - `manager.run.failed`
   - `worker.run.started`
   - `worker.run.completed`
   - `worker.run.failed`
   - `worker.run.blocked`
   - `human.interruption.received`
2. 第一轮标准路径的 owner 落点应属于 runtime、frontend probe，还是一个跨层 capability owner？
3. 音频资源应作为 Tauri bundle resources 管理，还是前端静态资源管理？
4. manager / worker 的音频是否必须显著区分，还是只区分 started / completed / blocked / failed 即可？
5. `task.completed` 是否应优先消费工具原生 event/notice，而不是由 watchdog 自行猜测？

## Current Judgment

- Freely 需要一条显式的声音语义系统。
- `watchdog != notifier` 应继续保持。
- 主设计应为：
  - native notice/event source
  - or tool-specific evidence adapter
  - -> canonical runtime event
  - -> sound policy
  - -> audio notifier
- 对 Codex/Responses 一类支持原生 lifecycle event 的路径，应优先消费结构化 event，而不是监听会话自然语言。
- 对尚无原生 event 的工具，后续可以通过 adapter / fallback 补齐，但不进入本轮。

## Recommended First Scope

1. 定义 canonical runtime sound events。
2. 定义 manager / worker / blocked / failed / interruption 的声音语义矩阵。
3. 在 Tauri/UI 路径引入打包音频资源与播放执行器。
4. 让 runtime 能发出供前端消费的标准 event。
5. 暂不实现 CLI/headless fallback，也不扩展到所有工具 notice 适配。

## Next Routing

- 这条能力已达到可 materialize 的程度，但在 owner 落位前仍属于 pre-brainstorm 阶段。
- 下一跳应以 narrow owner 冻结：
  - canonical event contract
  - sound policy
  - bundled audio resources
  - manager/worker started/completed 的标准路径实现
- 其他工具 notice 适配与 OS-level fallback 留作 follow-on。

# PRD: runtime-audio-notifier-and-sound-semantics-governance

## Goal

为 Freely runtime 冻结第一轮标准语音提醒路径：native/tool notice 或 bounded evidence adapter 产出 canonical audio cue event，前端/Tauri 订阅后按稳定声音语义播放已打包的音频资源。

## Why Now

当前 runtime 已有 event bridge、session/run/agent signal 与 Tauri probe 骨架，但没有：

- canonical `audio cue` event
- manager / worker / started / completed 的稳定声音语义
- 不依赖 OS 命令分支的标准播放路径

用户已明确要求自治运行时在任务开始/结束时给出不同声音提醒，因此这条能力不能继续停留在 pre-brainstorm，也不应被混回 watchdog supervision。

## Product Surface

- `src-tauri/src/event_kind.rs`
- `src-tauri/src/event_payload.rs`
- `src-tauri/src/bridge_logic.rs`
- `src/frontend_probe_v0/contracts.ts`
- `src/frontend_probe_v0/useAudioNotifier.ts`
- `src/frontend_probe_v0/audio/`
- `src/frontend_probe_v0/*audio*`

## Non-Goals

- OS-level fallback（`afplay` / `aplay` / PowerShell 等）
- 自然语言全文 grep 或 generic session transcript 监听
- blocked / failed / interruption 全矩阵
- 其他工具 notice/feed 的一次性全量接入

## Non-Negotiables

- `watchdog != notifier`
- 第一轮只走标准路径，不补 fallback
- 声音策略必须区分至少 `manager|worker × started|completed`
- 播放逻辑不能绑在 snapshot refresh 或 UI 描述字符串上

## Canonical Contract Frame

第一轮 canonical event 至少包含：

1. `type = AudioCueRequested`
2. `cueKey`
3. `actor = manager | worker`
4. `lifecycle = started | completed`
5. `reason`

`AudioCueRequested` 是 runtime 对 notifier 的稳定 contract；未来若某个工具已提供原生 notice / completion 事件，应优先接入该 native source，再映射到此 canonical event，而不是重回 transcript 监听。

## Prototype Path

1. 在 Rust bridge 新增 `AudioCueRequested` event kind 与 payload builder
2. 在现有 command routing 中，为标准 probe path 产出首批 cue：
   - session create/resume -> `manager started`
   - worker-targeted chat / run start-resume-retry -> `worker started` 或当前 actor started
   - run terminate -> 当前 actor completed
3. 在 frontend probe 新增独立 `useAudioNotifier()` 订阅同一事件流
4. 打包四个内置音频资源并建立 cue policy
5. 补齐 Rust/TS focused regressions

## Eval Plan

成功：

- 同一事件桥既能给 UI 列表展示，又能独立驱动 audio notifier
- manager/worker started/completed 各有稳定 cue
- mock 与 Tauri transport 均不需要 OS-specific 音频调用分支
- 后续 Codex/native tool notice 接入时只需补 source adapter，不需重开 sound semantics

失败：

- notifier 通过 watchdog 或 transcript grep 推断完成
- 音频播放依赖系统命令分支
- cue 语义继续与 UI 文案或 snapshot polling 混层

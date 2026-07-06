# Issue: runtime-audio-notifier-and-sound-semantics-governance

- issue_id: `I-20260405-1215-A`
- title: Runtime audio notifier and sound semantics governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-audio-notifier-and-sound-semantics-governance`
- issue-name: `runtime-audio-notifier-and-sound-semantics-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-1215-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/raw-20260405-1215/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/raw-20260405-1215/code-reviews
- depends_on:
  - `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 现在能把 runtime signal 暴露到 Tauri/frontend，但还没有一条稳定的自治声音能力链路。

当前缺口不是“系统怎么播声音”本身，而是 runtime 还没有把以下事实冻结成独立 contract：

- 哪些事件值得提醒
- manager 与 worker 如何区分
- started 与 completed 如何区分
- 原生 tool notice 与 fallback evidence adapter 未来如何在同一平面汇合

因此这条 owner 的职责是冻结标准路径与 sound semantics，而不是把 watchdog 继续做胖。

## Scope

1. 冻结 canonical `AudioCueRequested` runtime event。
2. 第一轮覆盖 `manager|worker × started|completed` 四类 cue。
3. 在 probe/Tauri 标准路径中产出上述 cue。
4. 在 frontend probe 新增独立音频 notifier 订阅与播放逻辑。
5. 打包四个内置音频资源。
6. 记录为何本轮不做 OS fallback，也不做 transcript 监听。

## Non-Goals

1. 不实现 OS-level audio fallback。
2. 不把 notifier 做成 watchdog / recovery / session transcript parser。
3. 不一次性接完 blocked / failed / interruption。
4. 不把所有工具的 native notice 接入审计塞进同一 owner。

## Acceptance

1. Rust bridge 与 TS contract 都暴露 `AudioCueRequested`，且字段至少包含 `cueKey / actor / lifecycle / reason`。
2. 第一轮四个标准 cue `manager-started`、`manager-completed`、`worker-started`、`worker-completed` 已冻结。
3. Frontend 音频 notifier 独立订阅事件流，不依赖 snapshot polling 或 UI 描述字符串。
4. 四个标准 cue 音频被项目打包，probe host 能解析并播放。
5. 现有事件桥与 Tauri validation 不因新增 audio cue contract 回归。
6. issue / PRD / pre-tests / tasks 对 `watchdog != notifier`、`standard path only`、`no fallback this round` 保持一致。

## Ready For Dev

实现建议按三个 slice 推进：

1. contract slice
   - Rust `event_kind / event_payload / bridge_logic`
   - TS `contracts`
2. playback slice
   - audio asset catalog
   - cue policy
   - `useAudioNotifier`
3. verification slice
   - Rust payload/routing tests
   - frontend audio policy/notifier tests
   - governance + type/build validation

## Verification

- `bun test src/frontend_probe_v0`
- `bun run typecheck`
- `cargo test --manifest-path src-tauri/Cargo.toml`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` via guarded merge `a9eba5b`.
- Post-merge closeout verification is recorded in `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-canonical-closeout-verification.md`.
- Reopen only for follow-on lifecycle expansion such as blocked/failed/interruption cues, native notice adapters for more tools, or explicit host-level fallback playback.

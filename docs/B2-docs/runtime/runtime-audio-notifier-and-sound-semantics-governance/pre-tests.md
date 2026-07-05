# Pre-tests: runtime-audio-notifier-and-sound-semantics-governance

## Acceptance Targets

### AT-001 audio cue event contract

- acceptance target: `Rust bridge and TS contract expose canonical AudioCueRequested payloads with stable cue metadata.`
- testing layer: integration
- target environment: Rust bridge contract plus frontend contract consumer
- required evidence: `cargo test --manifest-path src-tauri/Cargo.toml` and `bun test src/frontend_probe_v0`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 lifecycle routing semantics

- acceptance target: `Manager and worker start/completion flows emit the bounded four-cue matrix without watchdog or transcript coupling.`
- testing layer: integration
- target environment: bridge routing logic and probe adapter tests
- required evidence: `cargo test --manifest-path src-tauri/Cargo.toml` and `bun test src/frontend_probe_v0`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 bundled playback path

- acceptance target: `Frontend notifier resolves bundled cue assets and production build packages the four wav files.`
- testing layer: integration
- target environment: frontend probe build and notifier path
- required evidence: `bun run build`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 canonical post-merge probe validation

- acceptance target: `Canonical develop preserves the Tauri command/event bridge, including AudioCueRequested, after guarded replay.`
- testing layer: integration
- target environment: canonical develop probe host
- required evidence: `bun run tauri:validate:probe` and closeout verification note
- blocker taxonomy: `execution_pending_or_failed`

### AT-005 develop-bound decision note present

- acceptance target: `Develop-bound runtime/audio edits are backed by an issue-bound implementation decision note.`
- testing layer: IBM review
- target environment: verification artifact dir
- required evidence: `implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `rust-event-contract`
   - Rust bridge 暴露 `AudioCueRequested`
   - payload 至少包含 `cueKey / actor / lifecycle / reason`
2. `command-routing`
   - session create/resume 触发 `manager-started`
   - worker-targeted path 或 worker actor start path 触发 `worker-started`
   - terminate path 触发 `*-completed`
3. `frontend-audio-policy`
   - frontend 能把 `AudioCueRequested` 稳定映射到音频资源
   - 去重/订阅逻辑不依赖 snapshot refresh
4. `bundled-assets`
   - 四个标准 cue 音频被前端 build 打包并可被 notifier 引用

### Post-merge integration acceptance

1. Tauri probe 真宿主仍可完成现有 command/event 往返，不因新增音频事件回归。
2. Frontend probe 在收到 `AudioCueRequested` 后能触发对应播放调用；若测试环境无法真实播声，至少验证资源 URL 解析与 `play()` 调用链。
3. 新 contract 不要求 watchdog 介入，也不引入 OS fallback 分支。

### Non-Goals

1. 本轮不要求 blocked / failed / interruption cue。
2. 本轮不要求其他工具 notice 全量审计完成。
3. 本轮不要求 headless CLI 也能播声。

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `AudioCueRequested remains the canonical cross-bridge event payload with stable cue metadata.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-verification.md`

### AT-002
- id: `AT-002`
- requirement: `The bounded manager/worker started/completed cue matrix is emitted by runtime logic without watchdog/transcript fallback semantics.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The standard playback path resolves bundled cue assets and ships the four wav files in production build output.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-verification.md`

### AT-004
- id: `AT-004`
- requirement: `Canonical develop still passes Tauri probe validation after guarded replay and continues emitting AudioCueRequested in the observed event set.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-canonical-closeout-verification.md`

### AT-005
- id: `AT-005`
- requirement: `Develop-bound implementation is backed by an issue-bound decision note.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-audio-notifier-and-sound-semantics-governance/code-reviews/20260405-runtime-audio-notifier-implementation-decision.md`

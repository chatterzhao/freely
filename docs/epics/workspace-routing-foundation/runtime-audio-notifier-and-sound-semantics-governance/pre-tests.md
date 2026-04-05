# Pre-tests: runtime-audio-notifier-and-sound-semantics-governance

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

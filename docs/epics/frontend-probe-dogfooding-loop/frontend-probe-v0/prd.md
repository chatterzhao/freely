# PRD: frontend-probe-v0

## Goal

提供一个最薄但可运行的 Frontend Probe，使 Freely 能在自己的产品面中观察、打断、恢复和回放 day-1 run。

## Requirements

1. 支持 project switch。
2. 支持 session create / resume。
3. 支持 message input。
4. 支持 stream output 与 embedded terminal。
5. 支持 status、stop、retry、resume。
6. 支持 `control bar`、`chat intervention panel`、`agent roster` 的最小布局。
7. 前端运行时保持 Bun，不引入 Node.js 产品运行时。

## Product rules

1. Probe 只通过 boundary contract 调用 backend。
2. 应用内终端 / 控制台是 day-1 主入口，不依赖外部 shell。
3. 人类输入与控制命令必须可见且可追溯。
4. UI 只消费 snapshot / events，不私自持有运行事实。

## Minimal panels

- `control bar`
- `chat intervention panel`
- `agent roster`
- `embedded terminal`

## Minimal flows

- project switch
- session create / resume
- message input
- stream output
- stop / retry / resume

## Exit criteria for `done_ibm`

1. Probe v0 的最小 UI 范围已冻结。
2. 必需交互流与状态面已明确可验收。
3. 与 boundary contract 的依赖关系已清晰，不需要再回退争论接口归属。

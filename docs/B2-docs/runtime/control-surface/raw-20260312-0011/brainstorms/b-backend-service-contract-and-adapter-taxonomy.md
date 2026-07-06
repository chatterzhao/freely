# Brainstorm: backend-service-contract-and-adapter-taxonomy

## Focus

把 Freely 的稳定语义层和 transport / runtime 承载层明确拆开，避免后续 UI、runtime、第三方接入继续混写。

## Key Questions

1. Freely 的 `backend service contract` 到底包含哪些稳定语义，哪些只是 transport 细节。
2. `tauri_adapter`、`ws_adapter`、`local_process_adapter` 与 `openclaw_adapter/profile` 应如何分类。
3. 哪些字段和对象必须跨 adapter 保持不变，哪些只允许在承载层映射。
4. 如何让后续 control surface、probe 和 runtime 设计都引用同一套边界，而不是各自发明说法。

## Working direction

- day-1 先冻结 contract 真源，再谈 transport。
- adapter 只能改变承载方式，不得改业务语义。
- OpenClaw 作为 optional runtime/profile，不得抬成 Freely 的主定义。

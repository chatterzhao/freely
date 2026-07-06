# PRD: backend-service-contract-and-adapter-taxonomy

## Goal

冻结 Freely 的 backend service contract 与 adapter taxonomy，使 transport 和 runtime 成为可替换承载层，而不是产品语义本体。

## Requirements

1. 定义 `ClientCommand`、`ServerEvent`、`Snapshot` 的业务语义边界。
2. 区分 `tauri_adapter`、`ws_adapter`、`local_process_adapter` 与 `openclaw_adapter/profile`。
3. 明确 adapter 只能映射承载，不能修改业务语义。
4. 明确 OpenClaw 只是 optional adapter/profile，不是 Freely 主定义。
5. 为后续 control surface / runtime / intervention issue 提供统一 contract 真源。

## Product rules

1. protocol layer 不依赖单一 transport。
2. backend service contract 是稳定语义层。
3. adapter 是实现策略，不是语义层。
4. 未来新增 adapter 必须复用同一对象族与错误面。

## Minimal contract surface

- business objects:
  - `ClientCommand`
  - `ServerEvent`
  - `Snapshot`
- adapter classes:
  - `tauri_adapter`
  - `ws_adapter`
  - `local_process_adapter`
  - `openclaw_adapter/profile`

## Exit criteria for `done_ibm`

1. contract 与 adapter taxonomy 已冻结到对象级别。
2. 兼容原则明确，可直接供后续 issue 复用。
3. 后续 runtime / UI / intervention issue 不需要再争论语义层和承载层的边界。

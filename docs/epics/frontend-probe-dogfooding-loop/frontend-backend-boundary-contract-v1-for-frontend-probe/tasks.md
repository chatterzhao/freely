# Tasks: frontend-backend-boundary-contract-v1-for-frontend-probe

- 冻结 Probe day-1 必需的 `ClientCommand` 对象族。
- 冻结 Probe day-1 必需的 `ServerEvent` 对象族。
- 冻结首屏 / resume 所需的 `Snapshot` 最小语义。
- 收紧 sessions / stream / history / status 的 contract 入口。
- 明确 request correlation、stream ordering、error surface、attach/resume 的最小字段。
- 约束 `tauri_adapter` 与未来 `ws_adapter` 的兼容原则。
- 明确 `done_ibm -> Frontend Probe v0` 的交接条件。
- 冻结 contract 的最小字段规则与错误面分类。

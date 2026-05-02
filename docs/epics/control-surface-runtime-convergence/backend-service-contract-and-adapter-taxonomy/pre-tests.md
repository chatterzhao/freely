# Pre-Tests: backend-service-contract-and-adapter-taxonomy

1. 文档必须明确 backend service contract 与 adapter taxonomy 的分层关系。
2. 文档必须说明 `ClientCommand`、`ServerEvent`、`Snapshot` 属于业务语义层。
3. 文档必须区分 `tauri_adapter`、`ws_adapter`、`local_process_adapter` 与 `openclaw_adapter/profile`。
4. 文档必须明确 adapter 只能映射承载，不得改变业务语义。
5. 文档必须明确 OpenClaw 只是 optional adapter/profile，而不是 Freely 主定义。
6. 后续 issue 必须可以直接引用本 issue，而不是重新发明 contract 说法。

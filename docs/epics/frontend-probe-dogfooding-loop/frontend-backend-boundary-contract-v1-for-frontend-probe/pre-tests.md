# Pre-Tests: frontend-backend-boundary-contract-v1-for-frontend-probe

1. 文档必须把 sessions / stream / history / status 收敛成最小 contract，而不是只停留在方向描述。
2. `ClientCommand`、`ServerEvent`、`Snapshot` 三类对象都必须具备 Probe 可直接消费的最小定义。
3. contract 语义不得写死为 Tauri 私有调用方式，也不得预设远端 HTTP 才是正式形态。
4. 文档必须明确 request correlation、stream ordering、error surface、attach/resume 的最小语义。
5. 文档必须保持 frontend 不直接侵入 runtime/workspace，而是只依赖 boundary contract。
6. 本 issue 完成后，`Frontend Probe v0` 必须可以直接基于该 contract 继续 IBM / dev-loop。
7. contract 字段规则必须足够让 `tauri_adapter` 与未来 `ws_adapter` 共享同一业务对象族。

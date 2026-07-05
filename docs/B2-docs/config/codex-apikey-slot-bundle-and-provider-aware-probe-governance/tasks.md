# Tasks

1. 保持 Codex slot manifest vocabulary、slot bundle shape 和 kind-prefixed naming rule 作为当前 verification baseline，不再回退到 `auth.json` 单文件语义。
2. 维持 Codex `auth.json + config-auth.toml` 的 save/materialization contract、legacy slot compatibility 与 cross-kind switch matrix 作为当前 canonical truth。
3. 维持 watchdog / status / switch-auto 的 slot-kind-aware probe routing contract，并确保 `account-*` 与 `apikey-*` 的 truth source 不混用。
4. 保持 non-Codex capability tier 只反映当前 verified evidence，避免把 inventory-only 工具误宣称为 switchable/probeable。
5. 保持长期拆分方向为 `ai-switch-cli` backend，但把 extraction timing 继续交由 `I-20260405-1415-A` 的 `done_ibm` handoff package 约束。
6. 保持 `switch auto` / `best` / `probe` 的最小 JSON/CLI 分工稳定，使 Freely 后续能消费 machine-readable output 而不是额外 stdout heuristics。
7. 保持 `freely init` backend 检测/安装/启用流程与 `freely ai login` priority-list 插入 contract 作为冻结的后续集成边界，不在本 verification lane 内重新扩大实现范围。
8. 把当前 owner 留在 verification，直到 merge / cleanup evidence 写回；不要再从 candidate-stage IBM 重新路由。

# Pre-Tests: frontend-probe-v0

1. 文档必须明确 Probe v0 不是完整工作台，而是最薄产品面。
2. 文档必须覆盖 project switch、session create/resume、message input、stream output、status、stop/retry/resume。
3. 文档必须明确 `control bar`、`chat intervention panel`、`agent roster`、`embedded terminal` 的最小职责。
4. Probe 必须只通过 boundary contract 访问 backend，不直接侵入 runtime/workspace。
5. day-1 主入口必须明确为应用内终端 / 控制台。
6. project switch、session create/resume、message input、stream output、stop/retry/resume 必须都有最小交互流定义。

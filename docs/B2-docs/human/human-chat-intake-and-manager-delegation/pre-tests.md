# Pre-Tests: human-chat-intake-and-manager-delegation

1. `freely intake chat --project <abs_path> --message <text>` 会写入 `.freely/intake/**`。
2. `freely intake status` 能看见 pending intake item。
3. `freely intake claim` 能把 intake item 标记为可监督的 claimed state。
4. `freely intake resolve` 会生成 resolution artifact，并回写 absorption target。
5. `manager-agent` 与 `skill:human-interruption-handling` 对 human interruption 的职责边界一致。

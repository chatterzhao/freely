# Pre-tests

1. delegated manager continuation handoff 进入当前工位后，runtime 能写出 pending handoff evidence。
2. 下一轮 prompt 若包含 `Delegated continuation handoff`，runtime 会写出 consumed handoff evidence。
3. `live-status` 能显示这两类 evidence。
4. session rotation 的 handoff 生成不再触发 shell command substitution 错误。

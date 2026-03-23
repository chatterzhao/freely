# Brainstorm: active-lifecycle-boundary-and-dogfooding-capability-discovery

## Boundary To Freeze

### 1. historical vs active lifecycle

- `historical` 不是“文件创建得早”。
- `historical` 必须同时满足：
  - 当前 issue 生命周期已完成
  - 对应 worktree / merge / cleanup 已收口
  - 不再属于当前活跃执行链
- 只要上述任一条件未满足，就仍属于 `active lifecycle`。

### 2. active artifacts may be refactored

- 当前活跃生命周期里的真源允许继续改。
- 但目标应是应用产物收敛重构，而不是 append-only 记流水账。
- 局部阅读也应能得到正确边界，不能要求读完整个文件才能发现前后冲突。

### 3. dogfooding-first capability discovery

- Freely 开发 Freely 时暴露的问题，默认先判断是否可泛化。
- 若用户项目也会遇到，优先视为 Freely 能力发现输入。
- 若只是一次性本地偶发细节，才保留为项目经验或临时处置。

## Wording Direction

- 三层 loop 真源负责定义生命周期边界。
- `PROJECT_INTENT` 负责定义狗粮发现能力的产品原则。
- 不把这轮讨论回写到已完成的历史 issue 中。

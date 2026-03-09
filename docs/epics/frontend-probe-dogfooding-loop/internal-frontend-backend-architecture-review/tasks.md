# Tasks: internal-frontend-backend-architecture-review

- 重新定义 Freely 当前形态下的 frontend / backend 边界。
- 收敛状态归属矩阵。
- 定义可插拔协议分层。
- 明确 `ClientCommand`、`ServerEvent`、`Snapshot` 的最小语义。
- 约束第一阶段 transport 与未来 `ws_adapter` 的兼容原则。
- 冻结 frontend view state 与 backend source-of-truth 的状态归属矩阵。
- 冻结 day-1 `ClientCommand`、`ServerEvent`、`Snapshot` 最小对象族。
- 定义 input arbitration 的优先级与留痕要求。
- 锁定第一阶段技术栈和 Node.js 排除边界。
- 定义 `MVP autonomy milestone` 与“何时开始自己开发自己”的能力门槛。
- 定义 human interaction policy 与多输入源优先级模型。
- 定义应用内终端 / 控制台作为 day-1 主入口的要求。
- 定义 AI team visibility UI 的最小布局与信息模型。
- 明确 `done_ibm -> boundary contract v1` 的交接条件。

# Workspace Scripts

本目录是 Freely 工作区脚本的定义真源。

定位：
- `scripts/` 负责显式执行入口
- `hooks/` 负责 Git 生命周期触发入口
- `bin/`、`.githooks/` 是运行时投影位置，不是主定义源
- `docs/system/workspace/scripts/` 是系统真源
- `docs/user/workspace/scripts/` 预留给用户覆盖或补充能力
- 三个 loop 下脚本能力在整个系统中的归宿、owner 边界与生命周期细节见 `docs/system/workspace/three-loop-capability-lifecycle.md`

## 目录分层

- `runtime/`
  - 启动、监督、恢复、状态相关脚本真源
- `worktree/`
  - 分支/worktree/merge 卫生相关脚本真源
- `quality/`
  - 质量检查与辅助文档脚本真源
  - `checkpoint-guard` 负责 checkpoint budget / staged scope gate
- `tests/`
  - 脚本级回归测试真源
- 根目录下保留的 `start-lead-agent.sh`、`compose-context-source-prompt.sh`、`monitor-ai-cli.sh`
  - 属于 auto-loop 首段与 AI CLI 监控入口
  - 继续保留在 `scripts/` 顶层，减少首跳链路阅读摩擦

## 当前脚本

- `start-lead-agent.sh`
  - 最小首跳启动器
  - 接收项目路径、意图路径、宪法路径、AI 规格
  - 生成交给外部 AI CLI 的首跳提示
  - 明确进入 manager 主循环
  - 不在脚本层决定最终路由，只负责把 AI 送入可自治理解的首跳语境
  - prompt 中引用 workspace 资产时，统一使用相对 `workspace/` 根的路径
- `compose-context-source-prompt.sh`
  - `auto-loop` 首段的 context-source 提示词组装器
  - 接收 human chat / review / test / recovery 等 source input
  - 将 source input、milestone、workspace 技能路径组装成下一跳 AI 提示
  - 不编码最终路由结论，只要求 AI 理解后决定
  - 若当前事项已收敛为 manager-owned `completion_verification` / `cleanup_governance`，提示词必须保留这一 owner boundary，而不是伪装成新的 doc-loop / dev-loop
- `monitor-ai-cli.sh`
  - AI CLI 运行时监控定义源
  - 启动外部 AI CLI、准确写入真实 pid、阻塞等待进程结束
  - 供 `bin/freely` 这类运行时投影层调用
- `runtime/freely`
  - Freely supervisor 真源
  - 负责 fresh / resume / fresh_with_handoff 的运行时轮换策略
  - 在需要切新会话时生成最小 handoff 交接文件，并把它拼接进下一轮 prompt
  - 对支持结构化 token 计数的工具负责 context-window-aware 容量治理（warn / rotate）
  - 负责 project dirty budget / checkpoint governance 提示
  - 提供 `baseline-status` 基线快照视图
  - 提供 `status` family 聚合入口，可切 `baseline / live / fleet`
  - 提供 `live-status` 当前态监督视图，承接 day-1 `current-state plane`
  - 提供 `fleet-status` 项目级 worktree 监督视图，承接 day-1 `fleet plane`
  - 提供 `develop-push` followthrough truth 的读取 / defer / clear 入口，供主管在 merge 后显式记录合法延迟窗口
  - 两者只镜像最小 acceptance 摘要与 shared deep refs，不替代 artifact plane 上的 acceptance evidence 真相
  - 根目录 `bin/freely` 只是投影包装层
- `worktree/*`
  - worktree / merge / status 相关命令真源
- `quality/*`
  - `governance-check`、`new-review` 等辅助命令真源
  - `checkpoint-guard`
    - 判断当前 worktree 或 staged commit 是否必须先 checkpoint
    - 供 hooks、runtime 与多工位监督 CLI 复用
- `tests/*`
  - 路由、监控、worktree、merge 等脚本测试真源
- `worktree/wt-fleet-status`
  - 以项目级视图展示所有 worktree 的 branch / dirty / checkpoint / runtime 状态
  - 同时暴露 `desired runtime` / `role` / `exit reason`，以及 canonical `develop` 的 push followthrough 摘要，供主管判断哪些工位是正常冻结，哪些是应运行但已掉线

## 输入面

- `--project <abs_path>`
- `--intent <abs_file>`
- `--constitution <abs_file>`
- `--ai <tool[:model][:mode]>`
- `--source-input-file <abs_file>`（`compose-context-source-prompt.sh`）

## 输出面

- 校验通过后输出首跳 prompt
- 该 prompt 由运行时脚本或外部 AI CLI 消费
- 不在这里直接承载完整 supervisor / restart / state 逻辑
- 不在这里硬编码“走 IBM 还是走 pre-brainstorm”
- prompt 中仍可保留项目绝对路径用于定位仓库根和 `docs/milestones.md`
- `monitor-ai-cli.sh` 会将真实 AI CLI pid 写入 pid 文件，并持续阻塞到该 AI CLI 退出

## Observability Contract

day-1 共享观察面：

- `current-state plane`
  - 由 `live-status` 承接
  - 回答“当前谁在运行、处于哪个 loop / phase、现在在做什么”
- `fleet plane`
  - 由 `fleet-status` 承接
  - 回答“整个 worktree fleet 当前分别处于什么状态”
- `artifact plane`
  - 由 continuity、worker prompts、issue / progress / review / cleanup evidence 承接
  - `acceptance evidence` 的 canonical home 在此

shared deep ref groups：

- `session_ref`
- `stream_ref`
- `artifact_ref`
- `fleet_ref`
- `acceptance_ref`

约束：

- `live-status` / `fleet-status` 可以展示 signal 与最小 acceptance 摘要，但不直接宣告 `completed` / `delete-ready`
- 主管若要判断完成、cleanup gate、delete gate，必须顺着 `acceptance_ref` 回到 artifact plane

## 投影规则

- `docs/system/workspace/scripts/**` 可按命令语义投影到根目录 `bin/`
- 投影后的运行时包装层不得改变这里定义的输入面和首跳语义
- 投影层不应包含真实业务逻辑；真实实现必须回到 `workspace/scripts/**`

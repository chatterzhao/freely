# 预研头脑风暴：插话入口自动准备最小运行面

## 背景
- `freely chat` / `freely tui` 是用户正式入口，语义上应是“把一句插话交给 Freely”。
- 上一版把它们收成了 `runtime preflight or fail`：若 dispatcher/supervisor 都没运行，则直接报错。
- 这修掉了“假成功”，但仍把用户暴露给了运行面细节，产品语义还是太底层。

## 收敛判断
- 用户只应该面对一个正式插话入口：`freely chat`。
- `freely tui` 只是 `freely chat` 的交互壳，不应有另一套运行面语义。
- 遇到运行面未就绪时，高层入口应先自动准备，再提交，而不是优先报错。

## 最小自动准备边界
- 自动准备的目标不是完整业务主循环，而是“最小 interruption control plane ready”。
- 当前最小链路是：
  - intake durable write
  - interruption dispatcher watch
  - interruption manager handler triage
- 若当前没有 dispatcher：
  - 优先直接拉起 dispatcher
  - 若 supervisor 已存在，则仍沿既有 supervisor + dispatcher 协作链
- 只有当 dispatcher 无法在短时间内 ready，或 doc gate / config / project state 本身损坏时，才向用户报“无法自动准备环境”。

## 为什么不默认启动完整 supervisor
- 启动完整 supervisor 会顺带拉起主 manager loop 和 AI 主循环，代价更高。
- 对单条插话而言，真正必须的是“有人立刻注意到并 claim/triage”，不是完整主线都起来。
- delegate case 后续是否升级到 worker，是主管 AI 的职责，不应被 CLI 入口硬编码。

## CLI 语义
- `freely chat`：
  - 自动 bootstrap interruption control plane
  - 成功后提交插话
  - 只在 bootstrap 失败时报错
- `freely tui`：
  - 与 `freely chat` 共用同一后端链
- `freely intake chat`：
  - 继续保留为内部 primitive/脚本能力
  - 不再作为用户推荐语义

## 验证目标
- 在无 dispatcher / 无 supervisor 的项目里，`freely chat "..."` 不报“没启动”，而是自动准备后成功写入并被 claim/triage。
- `freely tui --once` 也同样成立。
- 真实狗粮测试使用插话：
  - `检查已经合并到develop的worktree，应该怎么收口`

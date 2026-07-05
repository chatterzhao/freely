# 研究：mem9 作为 Freely 共享记忆/跨工具连续性后端的适配性

## 结论（先给答案）

`mem9-ai/mem9` 值得研究，但当前更适合作为 **Freely 的外部记忆基础设施候选**，不是直接替换 Freely 现有治理/loop/runtime 的现成方案。

原因：

1. `mem9` 的产品目标非常接近 Freely 的长期方向：为多种 AI coding agent 提供跨会话、跨工具、跨机器的持久共享记忆。
2. 它已经覆盖 Claude Code、OpenCode、OpenClaw，并且 README 明确主打“stateless agents + cloud memory”，这和 Freely 未来多工具编排方向高度相关。
3. 但它当前聚焦的是 **memory service + plugin integration**，而 Freely 当前主轴是 **worktree / governance / auto-loop / doc-loop / dev-loop / checkpoint / supervisor**。两者不是替代关系，更像上下层。

所以这条研究的正确问题不是“Freely 要不要换成 mem9”，而是：

- Freely 是否应提供一个 `mem9` skill / backend adapter？
- Freely 的 continuity / recovery / cross-worktree supervision，是否应支持把摘要与关键状态写入外部 memory service？
- 如果接入，Freely 应保留哪些本地治理事实源，哪些适合外部化？

## 外部输入摘要

研究对象：`https://github.com/mem9-ai/mem9`

公开信息（2026-03-18）：
- repo: `mem9-ai/mem9`
- description: `Unlimited memory for OpenClaw`
- default branch: `main`
- language: `TypeScript`
- stars: `408`
- license: `Apache-2.0`

README 关键信息：
- 定位：`Persistent Memory for AI Agents`
- 核心能力：agent 共享、云持久化 memory，支持 hybrid vector + keyword search
- 形态：`mnemo-server` + 多种 agent plugin
- 已支持平台：
  - Claude Code
  - OpenCode
  - OpenClaw
  - 任意 HTTP client
- 设计原则：agent plugin 无状态，状态集中在 server

## 与 Freely 的相关性

### 高相关点

- Freely 也在做多工具协同：`codex`、`iflow`、未来其他 AI 工具。
- Freely 已经有 continuity / recovery / session rotation / multi-worktree supervision。
- Freely 当前跨会话记忆主要靠本地文档与 worktree 治理产物，尚未形成“外部共享记忆后端”。

### 不重合点

- `mem9` 不处理 Freely 的受保护分支、worktree 生命周期、checkpoint commit、merge gate。
- `mem9` 解决的是“记住什么”和“如何共享”，不是“什么时候做事、在哪个工位做、何时提交/合并”。

## 初步架构判断

如果接入 `mem9`，合理边界应是：

1. Freely 继续保留本地权威事实源：
   - `docs/CONSTITUTION.md`
   - `docs/LAWS.md`
   - `docs/PROJECT_INTENT.md`
   - `docs/B1-docs/`
   - issue / milestone / review / tests 等治理产物

2. `mem9` 只承接可外部化的“连续性增强层”：
   - session summary
   - cross-tool memory recall
   - cross-machine personal/team memory
   - worker handoff hints

3. Freely 不应让外部 memory 反客为主，不能把正式治理状态只放在 `mem9`。

## 候选落地方向

### 方向 A：Freely skill

新增 `mem9-memory-backend-evaluation` 或 `mem9-continuity-bridge` skill，用于：
- 判断何时把 continuity artifact 同步到外部 memory
- 判断召回内容如何进入首跳 prompt
- 明确哪些内容不能外发

### 方向 B：runtime adapter

在 `runtime/freely` 的 session rotation / recovery 分支上增加可选 backend：
- `local-only`
- `local + mem9`

### 方向 C：对外部项目的集成模式研究

Freely 未来若服务用户项目，可研究：
- Freely 作为 control plane
- mem9 作为 cross-agent memory plane

## 风险与约束

- 外部服务引入额外可用性/网络依赖，不适合作为 Freely 当前自治闭环的硬依赖。
- 记忆外发涉及隐私与治理边界，需先定义 redact / allowlist 规则。
- 如果没有明确事实源优先级，外部 memory 容易与本地文档真相冲突。

## 下一步建议

1. 继续读取 `mem9` 的设计文档与插件目录，确认它对 OpenClaw/OpenCode/Claude Code 的接入模型。
2. 评估 Freely 当前 continuity artifact 中，哪些字段值得外部化。
3. 已 materialize issue：`Mem9 shared memory evaluation for Freely continuity plane`。
4. 已将落点限定为 `skill:mem9-continuity-bridge`，后续若要进入 runtime 集成，再从 issue 继续推进，不把外部 memory 直接抬成治理真源。

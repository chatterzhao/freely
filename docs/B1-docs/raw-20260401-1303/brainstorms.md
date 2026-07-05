# Brainstorms - 20260401-1303--freely-product-security-baseline-governance

## Context

近期开发链路安全事件已经从“某个依赖有 CVE”转向“发布身份、CI tag、install hook、agent 外连、源码暴露面”被直接利用。

同时，本轮对话把另一个产品事实明确了：

- Freely 作为宿主调度器，默认就是为了高自治而以免交互、自动批准方式调用下游 `codex` / `cc` / 类 OpenClaw 工具
- 这不是异常高风险模式，而是 Freely 的能力体现
- 因此 Freely 安全治理的重点不应是“把自治默认关掉”，而应是“先按免交互、自动批准实现，再把真实执行边界和风险前置揭示，并要求用户在统一入口做显式知情同意”
- 沙盒、隔离设备、网络约束、专用账号等 safeguard 应被 Freely 强提醒、强建议、尽量支持，但默认不是启用自治的强制前置条件

还要明确当前预研的产品取向：

- “允许交互批准”不是本轮默认主路，因为那不符合 AI 自主开发的核心定位
- 用户若想修改工具安全面，属于后续独立需求；本轮先冻结 Freely 默认自治姿势和提醒/落盘 contract
- Freely 不是要把 OpenClaw 一类高自治工具降级，而是要把其风险揭示和配置边界做得更清楚

## Product Philosophy

Freely 的目标不是“一个保守的 AI 辅助壳”，而是 owner-grade AI autonomy：

- AI 需要理解项目是什么、为什么做、应该如何前进
- AI 需要以项目所有者心智推进 issue、文档、实现、验收与治理
- Freely 应鼓励 AI 通过更强的内部思考、复核和决策继续推进，而不是频繁退回给人类逐步批准

因此本条默认假设是：

- 启用阶段做强阻塞式风险知晓
- 运行阶段保持高自治
- 遇到高风险或高不确定时，先走内部 subagent / cross-tool 决策升级
- 只有当 AI 决策梯度也无法产出可信下一步时，才进入最小风险状态
- 阻塞的是“是否已充分理解并明确接受高自治运行”，而不是“是否已经搭好完整安全环境”

对 Freely 自身而言，这不是单纯的用户项目建议，而是产品默认安全基线缺口：

- `init` 目前主要负责项目注册、AI 规格和 hooks 初始化
- `doctor` 目前只覆盖文档门禁和 hook 门禁
- runtime 已经有网络代理、watchdog、slot/tool 编排等能力，但没有独立的 security baseline contract

当前实现 truth 还不完全统一，这正是本条预研要收口的现状事实：

- `tools.md` 与 runtime launcher 已经把 `codex` / `cc` 的 `auto` 路径定义为免交互、自动批准
- 原始 split 曾表现为 `freely init` 生成的项目级 `.codex/config.toml` 仍保持 guarded posture，而 `tools.md` / launcher 已偏向 auto posture
- 当前第一条 materialization slice 已经落地：`auto` 模式的项目级 `.codex/config.toml` 会写入 `approval_policy = "never"`；剩余收口点主要是 tool docs / launcher / 其他工具边界的一致性
- 因此本条不是“发明一个新方向”，而是要把 repo 内已经分裂的自治/安全姿势冻结成 canonical truth

最近对话中已经收敛出的高优先级缺口包括：

1. 凭证治理不能只看“是否被 git 跟踪”
2. 依赖安全不能只看“固定版本号”
3. 供应链策略需要考虑 minimum package age、provenance、GitHub Actions 可变 tag、install script
4. source map / 调试工件即使不进 git，也可能通过打包、静态托管、预览目录、runtime 产物或工具副产物外流
5. AI agent / MCP / Claude Code / Codex 这类执行面需要有统一治理，而不是让每个项目临时发明自己的安全姿势
6. 自动批准场景下，用户在运行时的逐步控制面被 Freely 主动拿掉，必须以前置检测、明确提示、显式同意和持续可见性来补偿

## Existing Governance To Reuse

已有最接近的前史是：

- `docs/B1-docs/20260329-2155--sensitive-local-artifact-ignore-governance/**`
- `docs/epics/workspace-routing-foundation/sensitive-local-artifact-ignore-governance/**`

这条线已经证明：

- Freely 仓库里真实出现过敏感本地产物误落
- 当前治理可以承接“最小默认保护”这一类问题
- 但它只覆盖 narrow ignore contract，不覆盖更高层的 security baseline

另有可复用输入：

- project-scoped proxy / launcher inheritance 已经是已完成能力
- `tool-cc-codex-mcp-runtime` 已经定义了工具接入策略
- `url-content-intake` 说明了外部内容抓取类能力可沉淀成 skill

## Problem

Freely 自身现在缺少一层明确的产品级安全默认值，导致以下判断容易散落在对话里而不是进入 canonical truth：

1. 什么安全检查必须在 `init` 时落默认配置
2. 什么安全检查必须在 `doctor` 时变成 baseline gate
3. runtime 默认应限制哪些外部访问、工具权限、输出落盘行为
4. 哪些风险属于 Freely 自身产品治理，而不是交给单个 repo 的 ad hoc 习惯
5. 当 Freely 明确以免交互、自动批准方式运行时，哪些风险必须统一揭示，哪些能力必须单独显式启用
6. Freely 自身 canonical policy、tool adapter 注入、tool-local config materialization 之间的职责如何分层

## Boundary

本条预研只讨论 Freely 自身产品治理和默认基线，不直接定义独立可复用 skill 的完整执行细节。

本条应优先回答：

1. Freely 自身应内建哪些默认安全 contract
2. 它们更适合落在 `init`、`doctor`、runtime config、hooks、还是 status surface
3. 哪些应通过“检测 + 显式知情同意”处理，哪些仍应单独显式启用

本条不直接处理：

1. 具体某个 security skill 的详细工作流
2. 外部生态全量 threat intelligence ingestion
3. 历史所有 secrets / artifacts 的回溯清理

## Working Hypothesis

Freely 自身至少应形成六块 baseline：

1. autonomy and consent baseline
   - Freely 默认以免交互、自动批准方式调用下游工具
   - `init` / 项目 `init` 必须检测真实执行边界，并明确提示当前是否沙盒、是否联网、是否自动批准
   - 用户若不同意，应获得明确配置修改路径，而不是只看到抽象 warning
   - 交互批准模式保留为未来可配置能力，不作为本条默认主路

2. execution boundary baseline
   - 沙盒是否存在、是否可用、是否已启用
   - 网络是 deny / allowlist / unrestricted
   - 可写根、可读敏感路径、额外目录挂载范围
   - 下游工具是否处于 `bypassPermissions` / `dangerously-bypass-approvals-and-sandbox` 一类模式
   - Freely canonical policy 如何映射为 tool adapter flags / env / project-local config

3. secret materialization baseline
   - tracked / staged / untracked 高风险路径
   - runtime 日志、continuity、prompt、artifact 的敏感内容约束

4. dependency and release baseline
   - lockfile / immutable pin / minimum package age
   - provenance / trusted publishing / install script 风险

5. artifact exposure baseline
   - source map
   - 调试符号
   - 不应外发的 build side products

6. agent and state baseline
   - MCP / tool approval / domain allowlist
   - 外部内容到工具调用之间的 trust boundary
   - continuity、debug/cycle log、todo/memory、subagent handoff 这类状态落盘面

## Initial Direction

优先把 Freely 自身产品面的安全默认值冻结为：

- `init` / 项目 `init` 负责检测当前自治模式下的真实执行边界，并做显式风险揭示与知情同意记录
- `init` 同时负责写入默认安全配置与最小忽略/模板，并优先生成项目级工具配置而不是污染用户全局配置
- `init` / `doctor` 还应给出可操作的 safeguard 建议，例如沙盒、隔离 workspace、网络限制、专用实验设备，但这些默认是 advisory support，不是自治前置门槛
- `doctor` 负责做 baseline security audit，并复核当前风险承认是否与真实配置一致
- runtime 负责执行时边界落实，以及把 Freely canonical policy 动态注入到具体工具
- `baseline-status` / `live-status` 负责暴露关键安全 posture，而不是把它藏在内部脚本

## Consent Model Direction

Freely 不应把“自动批准”伪装成普通配置细节，而应明确声明：

- Freely 默认以高自治模式运行下游 agent/tool
- 当前项目的真实边界是什么
- 如果用户不同意，该如何修改 Freely 或下游工具配置

这里的“修改配置”应明确分层：

1. Freely canonical policy
   - Freely 自己记录项目的自治姿势、风险确认、边界偏好

2. tool adapter injection
   - runtime 启动时把 Freely policy 映射成 `codex` / `cc` / MCP 的 flags、env、system prompt

3. tool-local config materialization
   - 能项目级落盘的工具配置优先写到项目内
   - 只能写到用户 home 的工具配置默认只给 manual 指引，不自动污染用户全局

一个可行的统一入口应至少展示：

1. 当前是否免交互
2. 当前是否自动批准
3. 当前是否沙盒
4. 当前网络策略
5. 当前可写范围
6. 当前是否允许外部 agent / MCP / 子 agent

并提供至少三类动作：

1. 接受当前模式并继续
2. 按建议修改工具或 Freely 配置后继续
3. 停止初始化，并给出明确配置修改指引

这里的关键不是“默认不让用”，而是“默认不隐藏真实风险边界”。

对于 safeguard guidance，还应明确：

- Freely 应主动建议更安全的运行面，例如沙盒、容器、VM、专用设备、专用账号、受限网络
- Freely 应尽量帮助用户搭建这些环境，或至少输出具体操作指引
- 但若用户明确表示当前设备/环境就是可接受的高自治实验面，这些 safeguard 默认不构成阻塞条件
- Freely 应记录“已提示哪些 safeguard、用户当前接受的边界是什么”，而不是把“未启用 safeguard”一律判成不可运行

对于首次启用高自治 profile，这一步应视为 activation consent，而不是普通 warning：

- 阻塞式展示风险摘要
- 要求用户明确理解
- 可要求重复输入固定确认语或多次确认
- 确认结果写回项目级 canonical artifacts

这一步是启用高自治能力的前置门，不是运行中的逐步人工审批回路。

因此 activation consent 应阻塞以下内容：

- 用户是否已经明确理解 Freely 默认是免交互、自动批准、高自治
- 用户是否已经明确看到当前执行边界与主要风险

但 activation consent 不应默认阻塞以下内容：

- 尚未启用沙盒
- 尚未迁移到隔离设备或 VM
- 尚未完成 Freely 提供的所有 safeguard 建议

## Autonomous Escalation Ladder

Freely 运行中默认应继续推进，不应因为“有风险”就轻易停下。更合适的模型是分层升级：

1. 单 agent 自主判断并继续
2. 一个 security-focused subagent 复核
3. 多个 reviewer 并行评审
4. 跨工具评审，例如 `codex` 与 `cc` 互相复核
5. 若仍无法产出可信下一步，再进入最小风险状态

也就是说：

- 停止不是主路
- 人工逐步批准不是主路
- 内部 AI 决策升级才是主路
- safeguard 缺失本身也不自动等于“立刻停机”；更常见的主路应是先给建议、评估边界、内部复核，再决定是否继续

## Security Decision Participation

Freely 默认不把用户重新拉回逐步批准链路，但这不代表安全决策只能靠单 agent 直觉。

对于以下场景，可引入一个或多个 security-focused subagent 参与判断：

1. 当前执行边界与项目声明不一致
2. 检测到非沙盒、高权限网络或敏感路径暴露
3. 检测到 artifact / source map / secret / supply-chain 高风险项
4. 需要判断某项能力是默认允许、单独显式启用，还是仅 warning

这类 subagent 更接近“安全决策委员”，职责是：

- 复核现状
- 给出风险摘要
- 产出建议的 Freely policy / tool adapter 调整
- 把结论写回 canonical artifacts

它们不是用户交互批准的替代，而是 Freely 在保持自治前提下引入的内部决策增强。

## Minimal Risk State

即使 Freely 目标是高度自治，也不应把“继续执行”误解为“无论如何都要硬冲过去”。

当出现以下情况时，Freely 可以进入最小风险状态：

1. 当前能力边界外不存在可信下一步
2. 一个或多个 security reviewer 仍无法收敛建议
3. 环境前提缺失，继续动作只会变成破坏性试错
4. 需要外部条件，例如额外资源、外部工具、额外环境能力，当前运行面无法自行获得

最小风险状态应做的是：

- 停止高风险继续动作
- 保存证据与当前上下文
- 明确写出为什么停
- 明确写出继续所需条件

这不是默认保守化，而是 owner-grade autonomy 在能力边界外的正确行为。

## Open Questions

1. 非沙盒自动批准应作为可知情同意的常规高风险模式，还是单独显式启用能力
2. minimum package age 应该是 Freely 全局默认，还是 per project override
3. source map 应只做 warning，还是对 production-facing output 做单独显式启用门
4. secret 扫描应只扫描文件系统，还是也扫描 runtime 产物与 continuity artifacts
5. agent 网络权限应默认为 deny-all 还是 allow-minimal

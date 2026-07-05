# 预研：Claude Code + Codex MCP 工具路由

## Context

- 日期：2026-03-20
- 触发：当前有可用的 Codex 订阅，但希望以 Claude Code 作为主执行器，把 Codex 作为 Claude Code 内部可调用的 MCP 工具，而不是把 Freely 顶层 tool 直接切换成 `codex`。
- 待回答问题：
  1. Claude Code 是否真的可以接入 Codex MCP server
  2. 应优先使用哪种 server：内置 `codex mcp-server` 还是第三方 `codex-cli-mcp-tool`
  3. 若可行，Freely 应如何建模 tool / model / capability，避免把“顶层执行器”和“内部 MCP 能力”混在一起

## Outcome Update

后续实现与用户交互约束已把本预研进一步收敛为：

- 顶层保留两个显式工具：
  - `cc`
  - `cc-use-codex-cli`
- setup / provider / MCP 安装与验证收敛为：
  - `skill:tool-cc-codex-mcp-runtime`
- runtime 不再只停留在 capability 建模，而是显式支持：
  - 固定 Codex MCP policy
  - per-workcell `Claude session-id`
  - `Claude jsonl -> Codex threadId -> Codex jsonl` 的双层会话证据

也就是说，本预研的早期“不要让 `cc-use-codex-cli` 成为顶层工具名”的判断，已经被后续用户侧操作要求和 runtime 实装路径替代；当前应以实际落地结果为准。

## Done Definition For This Research Worktree

当前 research worktree 的完成，不是指 runtime 已经改完，而是指以下研究产物已经收口：

1. 已证明 `Claude Code + Codex MCP` 在本机可实际工作
2. 已证明 `Codex MCP` 不能替代 `Claude Code` 主 provider
3. 已形成对 `tool=cc`、`tool_capabilities=[codex-cli]`、provider readiness、`codex/codex-reply` continuity 的明确建模
4. 已把结果沉淀成：
   - pre-brainstorm 结论
   - candidate
   - 一个可转实现的 skill contract 草案

满足以上条件后，本 worktree 应收口为 research-only，不继续承载 runtime 真代码改动。
后续实现应新建 dedicated worktree，依赖当前 research 分支继续推进。

## Verification

### 1. Claude Code 协议侧支持 MCP server

- Claude Code 本机命令面确认支持：
  - `claude mcp add`
  - `claude mcp add-json`
  - `claude mcp get`
  - `claude mcp serve`
- 说明 Claude Code 可以作为 MCP client 连接外部 stdio / HTTP MCP server。

### 2. Codex CLI 协议侧支持作为 MCP server 暴露

- 本机 `codex --help` 明确包含：
  - `mcp`
  - `mcp-server`
- 本机 `codex mcp-server --help` 明确说明：
  - `Start Codex as an MCP server (stdio)`

### 3. 项目级接线 PoC

在研究 worktree 根目录写入：

```json
{
  "mcpServers": {
    "codex-cli": {
      "type": "stdio",
      "command": "/Users/zhaoyu/.bun/bin/codex",
      "args": ["mcp-server"]
    }
  }
}
```

然后执行：

```bash
claude mcp get codex-cli
```

观察结果：

- 在当前沙箱中，`codex mcp-server` 会因环境限制启动失败，因此 `claude mcp get codex-cli` 初始显示 `Failed to connect`
- 在无沙箱限制执行时，`claude mcp get codex-cli` 显示 `Status: ✓ Connected`

结论：

- 这条路径在协议和本机 CLI 能力上都成立
- 当前阻断不是“Claude Code 不支持”或“Codex 不能做 MCP server”，而是沙箱 / 权限环境会影响 server 启动

### 4. 第三方 wrapper 状态

- `codex-cli-mcp-tool` 在 npm 存在：
  - name: `codex-cli-mcp-tool`
  - version: `1.0.5`
  - repository: `https://github.com/Mr-Tomahawk/codex-cli-mcp-tool`
- 它是第三方 wrapper，不是当前本机 Codex CLI 内置能力的唯一入口

结论：

- 若目标只是“让 Claude Code 调用 Codex”，优先使用内置 `codex mcp-server`
- 只有在第三方 wrapper 提供了内置 server 缺少的强需求能力时，才考虑依赖 `codex-cli-mcp-tool`

### 5. 无登录状态验证

清理动作：

- 卸载并重装 `Claude Code`
- 删除 `~/.claude`、`~/.claude.json`
- 清理研究 worktree 中的临时 `.mcp.json`
- 对 `~/.zshrc`、`~/.bashrc` 先备份再做最小变更

关键发现：

- 机器上原本存在：
  - `ANTHROPIC_AUTH_TOKEN=test`
  - `ANTHROPIC_BASE_URL=http://127.0.0.1:3456`
- 这意味着之前并不是“纯未登录”，而是在走本地 provider

在显式移除这两个环境变量后执行：

```bash
env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL claude auth status
env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL claude -p "Reply with exactly: hi"
```

结果：

- `auth status` 返回 `loggedIn: false`
- `claude -p` 直接报 `Not logged in · Please run /login`

结论：

- `Codex MCP` 不能替代 `Claude Code` 自身的认证 / provider 前置
- Claude Code 必须先有可用主 provider，随后才能把 Codex 当 MCP 工具调用

### 6. provider 假登录 / 本地路由验证

本机可用的“假登录”并不是真登录，而是：

- `ccr activate` 注入
  - `ANTHROPIC_AUTH_TOKEN=test`
  - `ANTHROPIC_BASE_URL=http://127.0.0.1:3456`

初始失败原因：

- `ccr` 当时未运行
- `127.0.0.1:3456` 直接 `connection refused`

继续排查后确认：

- `ccr` 是 `Claude Code Router`
- 当前配置使用 `modelscope` provider
- 旧配置里 `api_base_url` 写成了 `https://api-inference.modelscope.cn`
- 这会导致上游返回欢迎信息，而不是 OpenAI-compatible completion payload

修正后配置：

```json
"api_base_url": "https://api-inference.modelscope.cn/v1/chat/completions"
```

然后验证：

```bash
curl -X POST http://127.0.0.1:3456/v1/messages \
  -H 'Authorization: Bearer test' \
  -H 'Content-Type: application/json' \
  -d '{"model":"claude-sonnet-4-6","messages":[{"role":"user","content":"Reply with exactly: ping"}],"max_tokens":32,"stream":false}'
```

结果：

- 本地 `ccr` 返回有效消息体
- 实际上游模型为 `MiniMax/MiniMax-M2.5`

结论：

- 当前机器上的可用路径不是“Claude 官方登录”
- 而是 `Claude Code -> CCR -> ModelScope`
- 只要 `ccr` 可用，Claude Code 主请求就能工作

### 7. 安装 Codex MCP

最终采用的安装方式：

```bash
claude mcp add codex-cli -s user -- /Users/zhaoyu/.bun/bin/codex mcp-server
```

结果：

- 用户级 MCP server 写入 `~/.claude.json`
- `claude` 后续无需每次传临时 `--mcp-config`

同时保留过的临时验证方式：

```bash
claude -p --strict-mcp-config --mcp-config /tmp/cc-codex-mcp.json ...
```

该方式只用于验证，不作为最终配置入口。

### 8. 正常使用验证

先验证 Claude 主请求：

```bash
claude -p -- "Reply with exactly: hi"
```

结果：

- 返回 `hi`

再验证 Codex MCP 实际调用：

```bash
claude -p --permission-mode bypassPermissions -- \
  "You must first use the codex-cli MCP tool to determine whether the current directory contains a docs folder. After using the tool, answer with exactly one word: yes or no."
```

结果：

- 返回 `yes`

调试日志进一步确认：

- `MCP server "codex-cli": Successfully connected`
- `MCP server "codex-cli": Calling MCP tool: codex`
- `Tool 'codex' completed successfully`

结论：

- 现在不只是“能连接 Codex MCP”
- 而是 `Claude Code` 已经真实调用 `Codex` 完成一次工具执行

### 9. 默认可用性处理

为避免“每次手动起 CCR”：

- 在 `~/.zshrc`
- 在 `~/.bashrc`

加入最小启动逻辑：

1. `eval "$(ccr activate)"`
2. 若 `3456` 没监听，则后台启动 `ccr`
3. 最多等待 10 秒直到端口 ready

因此当前机器上的默认使用路径是：

```text
新开 shell
  -> shell 注入 CCR 环境
  -> 若未启动则自动拉起 CCR
  -> claude 读取用户级 codex-cli MCP 配置
  -> Claude 主请求走 CCR/provider
  -> 需要时调用 Codex MCP
```

补充验证：

- 用新的交互 shell 执行：

```bash
zsh -ic 'claude -p --permission-mode bypassPermissions -- "You must first use the codex-cli MCP tool ... "'
```

- 返回 `yes`

说明当前配置已达到“新开终端即可用”的状态

### 10. provider fake-key 反证实验

为了判断“当前是不是已经在用 Codex 当 Claude 的底层 AI API”，做了一个可逆实验：

1. 备份 `~/.claude-code-router/config.json`
2. 把 `modelscope.api_key` 改成假的
3. 重启 `ccr`
4. 分别测试：
   - `claude` 普通请求
   - `claude + codex-cli MCP` 请求

日志结果：

- `ccr` 向 `https://api-inference.modelscope.cn/v1/chat/completions` 发请求
- 上游返回：

```text
401 Authentication failed, please make sure that a valid ModelScope token is supplied.
```

结论：

- 只要 `CCR/ModelScope` 的主 provider key 失效，`Claude Code` 整体就会失效
- 即使 `codex-cli MCP` 已挂载，也不能顶替主 provider
- 因而当前架构不是“Codex 作为 Claude Code 的底层模型 API”
- 当前真实架构仍然是：

```text
Claude Code -> CCR -> ModelScope
                    \
                     -> Codex MCP tool (按需调用)
```

实验后已恢复真实 key 并验证 provider 可继续正常返回。

### 11. 除了 MCP 之外还有什么方式

本轮检索到的可行方向有三类：

1. **MCP server**
- 当前已跑通的方式
- 形式：`claude mcp add ... -- codex mcp-server`
- 优点：接入清晰，Claude 原生支持
- 缺点：Codex 是工具，不是底层模型替换

2. **Skill / prompt 教 Claude 直接调用 `codex` CLI**
- 有实践文章明确提到：可用 skill 让 Claude Code 学会调用 `codex exec`
- 这本质上不是 MCP，而是通过 Claude 自己的 Bash / Skill 路径去调 Codex CLI
- 优点：更灵活、可定制、可减少 MCP 工具定义带来的上下文消耗
- 缺点：仍然不是“底层模型替换”，而是另一种工具调用

3. **自定义 provider / router / proxy**
- 让 Claude Code 的 Anthropic 请求被转发到其他模型后端
- 当前本机的 `CCR -> ModelScope` 就属于这一类
- 这条路可以替换 Claude 的“主模型提供者”
- 但它不是 Codex 订阅的直接官方接法；若要让它直接变成“Codex 当底层 API”，需要额外实现一个兼容 Anthropic 请求语义的代理层

本轮没有找到“官方支持的、直接把 Codex 订阅无缝变成 Claude Code 底层模型提供者”的现成方案。

结论：

- **现成可用**：MCP、Skill、Router/Proxy
- **其中真正能替换主模型的**：只有 Router/Proxy 类方案
- **但 Codex 订阅本身目前并没有现成文档表明可直接当 Claude Code 的底层 provider**

### 12. 怎样让 Claude 更稳定地总是优先调用 Codex

目标不是每次都显式写“use codex”，而是让 Claude 在需要时稳定优先用它。

本轮收敛出的办法：

1. **最稳的是 Hook / Skill / 子代理规则**
- 纯 prompt 提示长期不稳
- 更稳的是：
  - 定义专门的 skill / subagent
  - 或用 pre-tool hook / policy 把某些任务重定向到 `codex-cli`

2. **MCP Tool Search 不是强制优先级机制**
- Claude Code 官方文档与相关实践都说明，MCP tool search 只是“按需加载工具”
- 它不会天然保证“总是先用 codex”

3. **可操作策略**
- 给 `codex-cli` 写清楚 `serverInstructions`
- 在 Claude 的技能/代理约定里写明：
  - 代码实现
  - 大改动
  - 仓库内修复
  - diff review
  优先调用 `codex-cli`
- 若要进一步提高强制度，使用 hook 拦截某些默认工具并提示改走 `codex-cli`

结论：

- “总是优先用 Codex”可以做，但更像**策略层约束**
- 不是通过简单安装 MCP 就会自动发生
- 因此在 Freely 中更适合表达为：
  - `tool=cc`
  - `tool-capability=codex-cli`
  - 外加 `tool-policy` / `skill-policy` / `routing-preference`

### 13. 当前 CCR 配置应如何总结

当前机器上的可用 CCR 要点：

1. 配置文件：
- `~/.claude-code-router/config.json`

2. 当前有效 provider：
- `name=modelscope`
- `api_base_url=https://api-inference.modelscope.cn/v1/chat/completions`
- `models=[MiniMax/MiniMax-M2.5]`

3. 本地入口：
- `HOST=127.0.0.1`
- `PORT=3456`
- `APIKEY=test`

4. shell 注入：
- `eval "$(ccr activate)"`
- 负责设置：
  - `ANTHROPIC_AUTH_TOKEN=test`
  - `ANTHROPIC_BASE_URL=http://127.0.0.1:3456`
  - 其他相关环境变量

5. 默认可用性保证：
- 若 3456 未监听，则后台启动 `ccr`
- 最多等待 10 秒直到 ready

因此，要让当前机器上的 `cc` 正确工作，最小必要条件是：

```text
CCR config 正确
CCR 进程在运行
shell 已注入 ccr activate 环境
Claude 用户级已注册 codex-cli MCP
```

## Converged Workflow

这份预研的最终目标不是单纯说明“可行 / 不可行”，而是收敛出一条 Freely 之后可复用的执行工作流。

面向未来 Freely 的标准化目标句式：

```text
安装 cc
配置 ccr（或其他可用 provider/router）
在 cc 中安装 codex 相关 MCP
完成配置
做验证测试
```

### 标准工作流草案

#### A. 安装 Claude Code

目标：

- `claude --version` 正常返回
- shell 中可直接调用 `claude`

最小动作：

```bash
npm install -g @anthropic-ai/claude-code
```

#### B. 配置主 provider

目标：

- Claude Code 自身先能完成主请求
- 这一步可以是：
  - 官方登录
  - `CCR`
  - 其他 router / proxy / provider

若走 `CCR`：

1. 配置 `~/.claude-code-router/config.json`
2. provider 要能返回有效 completion，而不是欢迎页或错误页
3. shell 中注入：

```bash
eval "$(ccr activate)"
```

4. 确保 `CCR` 进程在运行

最小验收：

```bash
claude -p -- "Reply with exactly: hi"
```

返回 `hi`

#### C. 在 Claude Code 中安装 Codex MCP

优先方式：

```bash
claude mcp add codex-cli -s user -- /Users/zhaoyu/.bun/bin/codex mcp-server
```

说明：

- 优先内置 `codex mcp-server`
- 第三方 wrapper 只作备选

#### D. 配置默认使用环境

目标：

- 新开 shell 后可以直接使用

最小要求：

1. shell 注入主 provider 环境
2. 若 provider 需要本地进程（如 `CCR`），要有自动启动或等效守护策略
3. `claude` 用户级已存在 `codex-cli` MCP 配置

#### E. 验证 Codex MCP 真实调用

不是只看“已安装”，而是要验证真实调用。

推荐测试：

```bash
claude -p --permission-mode bypassPermissions -- \
  "You must first use the codex-cli MCP tool to determine whether the current directory contains a docs folder. After using the tool, answer with exactly one word: yes or no."
```

验收证据：

- 返回有效答案
- 调试日志中出现：
  - `Calling MCP tool: codex`

### Freely 未来应该如何响应这类用户请求

当用户对 Freely 说：

```text
安装 cc
配置 ccr
在 cc 安装 codex mcp
让它可用
```

正确响应不应只是“给几个命令”，而应按以下阶段执行：

1. 检查 / 安装 `Claude Code`
2. 检查 / 配置主 provider（`CCR` 或其他）
3. 验证 `claude` 主请求是否可用
4. 安装 `codex-cli` MCP
5. 验证 `codex-cli` 是否被 Claude 真实调用
6. 将必要的 shell / user config 持久化
7. 回写验证结果与前置条件

### 未来 Freely 的规范化表达

如果要让 Freely 在治理上能稳定执行这类请求，本预研最终应沉淀成：

1. 一个正式 `tool=cc` 接入方案
2. 一个 `provider setup` 标准步骤
3. 一个 `codex MCP install + verify` 标准步骤
4. 一个 `cc usable` 验收清单
5. 一个对应 skill / workflow，供以后遇到相同用户意图时直接复用

## Skill Direction

### 1. Skill 命名应表达“在 CC 中调用 Codex”

这里最容易误解的命名是：

- `tool-cc-setup`
- `tool-codex-setup`
- `tool-cc-and-codex-setup`

这些名字都容易让人误解成：

- 分别安装两个顶层工具
- 或者只是把 `cc` 与 `codex` 并列配置

但本预研收敛出的真实语义是：

```text
顶层执行器是 CC
Codex 是 CC 内部通过 MCP 调用的能力
```

因此 skill 命名应尽量表达：

- `cc`
- `codex`
- `mcp`
- `within / inside / via`

推荐命名方向：

- `skill:tool-cc-codex-mcp-setup`
- `skill:tool-cc-codex-within-cc`
- `skill:tool-cc-codex-mcp-runtime`

本轮更推荐：

```text
skill:tool-cc-codex-mcp-runtime
```

原因：

- `tool-cc`：顶层执行器仍是 Claude Code
- `codex-mcp`：Codex 通过 MCP 进入
- `runtime`：不只是安装，还包含默认执行、路由和验证

若后续想把安装拆开，可再有：

- `skill:tool-cc-provider-setup`
- `skill:tool-cc-codex-mcp-runtime`

其中后者依赖前者。

### 2. Codex MCP 的两个调用面意味着什么

Codex MCP 暴露的核心工具面是：

1. `mcp__codex-cli__codex`
- 创建新会话
- 适合首次进入一个新任务 / 新 issue / 新上下文批次

2. `mcp__codex-cli__codex-reply`
- 续接已有会话
- 适合同一任务在同一 thread 上继续推进

这意味着 Freely 若把 `cc + codex mcp` 做成正式能力，不能只停留在“已安装 mcp”。
还必须定义：

- 何时开新 Codex thread
- 何时复用已有 thread
- threadId 存在哪里
- thread 何时失效 / 轮换

### 3. 对 Freely 应抽象成什么能力

Freely 不应把上面的 MCP 细节直接暴露给用户。

更合理的抽象是：

```text
cc-internal-codex-execution
```

或作为 `tool=cc` 下的内部能力：

```text
provider_backend = ccr|official|other
tool_capabilities = [codex-cli]
tool_policy = prefer-codex-for-repo-work
```

对 Freely runtime 而言，真正要开发的不是“再加一个 tool”，而是：

1. `cc` 模式下的 Codex 路由器
2. thread continuity 管理
3. 自动批准 / 非交互参数映射

### 4. 当用户使用 CC 且该模式启用时，所有 AI 命令如何自动转成 MCP 调用

这里要区分两个层次：

1. **Claude 主请求**
- 永远还是先进入 `Claude Code`
- 这层不能被 Codex MCP 替代

2. **Claude 内部执行仓库工作时的实现能力**
- Freely 应尽量让它优先走 Codex MCP

因此“所有 AI 命令自动转成这个 MCP 调用模式”的正确理解不是：

```text
用户命令 -> 直接不经过 Claude -> 全部转给 Codex
```

而是：

```text
用户命令 -> Claude Code
            -> 按策略优先调用 codex-cli MCP
            -> 必要时继续用 codex-reply 维持同一线程
```

### 5. 应为 Freely 设计什么 skill

本预研建议最终 skill 至少包含下面三个子职责：

#### A. provider/setup

- 安装 `cc`
- 配置 `ccr` 或其他 provider
- 验证 `claude` 主请求可用

#### B. codex-mcp/install

- 安装 / 注册 `codex-cli`
- 写入用户级或项目级 MCP 配置
- 验证 MCP server 可连接

#### C. codex-mcp/runtime-policy

- 定义何时调用 `mcp__codex-cli__codex`
- 定义何时调用 `mcp__codex-cli__codex-reply`
- 定义 threadId 的保存与轮换
- 定义默认自动批准和 sandbox 映射

因此更完整的 skill 体系可拆成：

- `skill:tool-cc-provider-setup`
- `skill:tool-cc-codex-mcp-setup`
- `skill:tool-cc-codex-mcp-runtime`

若只保留一个聚合 skill，则推荐：

```text
skill:tool-cc-codex-mcp-runtime
```

并把 setup 作为该 skill 的前置阶段。

### 6. 自动批准 / 免交互模式应如何映射

你要求这一模式要和 Freely 里其他工具一样支持免交互自动批准。

这点需要分层映射：

#### Claude 层

Claude Code 非交互自动批准可对应：

```bash
claude -p --permission-mode bypassPermissions
```

#### Codex MCP 层

调用 `mcp__codex-cli__codex` 时，应传：

- `approval-policy=never`
- `sandbox=workspace-write` 或按 Freely 当前策略映射
- `cwd=<当前工作目录>`
- `model=<配置值>`

也就是说，Freely 在 `cc` 模式下若启用 `codex-cli` 能力，自动批准策略应做双层对齐：

```text
Freely auto
  -> Claude permission-mode=bypassPermissions
  -> Codex approval-policy=never
```

step 模式则对应：

```text
Freely step
  -> Claude 默认 permission mode
  -> Codex approval-policy=on-request
```

### 7. 运行时路由草案

对于 `tool=cc` 且启用 `codex-cli` capability 的情况，建议 Freely runtime 用如下路由：

1. 首次命中 repo 实现型任务
- 调用 `mcp__codex-cli__codex`
- 传入：
  - `prompt`
  - `cwd`
  - `model`
  - `sandbox`
  - `approval-policy`

2. 同一 issue / 同一 continuity 会话继续推进
- 优先调用 `mcp__codex-cli__codex-reply`
- 使用保存的 `threadId`

3. 触发 thread 轮换时
- 再次调用 `mcp__codex-cli__codex`
- 新建 thread
- 更新 continuity artifact 中的 `threadId`

### 8. Freely 未来对用户请求的正确响应

当用户说：

```text
安装 cc
配置 ccr
在 cc 里装 codex mcp
让它默认以这种模式工作
```

Freely 正确的执行方式应是：

1. 运行 `tool-cc-provider-setup`
2. 运行 `tool-cc-codex-mcp-setup`
3. 写入 `tool=cc` 的默认 capability / policy
4. 让 `cc` 模式下的实现型任务优先路由到：
   - `mcp__codex-cli__codex`
   - `mcp__codex-cli__codex-reply`
5. 以自动批准模式完成端到端验证

### 9. Skill Contract Draft

若将本预研推进为正式 skill，建议先按单 skill 聚合设计：

```text
skill:tool-cc-codex-mcp-runtime
```

后续若实现体量变大，再拆成：

- `skill:tool-cc-provider-setup`
- `skill:tool-cc-codex-mcp-setup`
- `skill:tool-cc-codex-mcp-runtime`

#### 触发意图

以下用户意图应命中该 skill：

- 安装 `Claude Code`
- 配置 `CCR`
- 让 `Claude Code` 使用第三方 provider
- 在 `Claude Code` 中安装 `Codex MCP`
- 让 `Claude Code` 在仓库工作时优先走 `Codex`
- 验证 `cc + codex mcp` 是否可用

#### 输入

最小输入建议：

- `provider_kind`
  - `official`
  - `ccr`
  - `other`
- `provider_backend`
  - 例如 `modelscope`
- `codex_mcp_mode`
  - `user`
  - `project`
- `execution_mode`
  - `auto`
  - `step`
- `codex_model`
  - 例如 `gpt-5.2-codex`
  - 可空，空则走默认
- `sandbox_policy`
  - `read-only`
  - `workspace-write`
  - `danger-full-access`

#### 前置检查

skill 执行前必须检查：

1. `claude` 是否已安装
2. `codex` 是否已安装
3. 主 provider 是否可工作
4. 若走 `CCR`
   - `config.json` 是否存在
   - provider endpoint 是否正确
   - 本地端口是否可监听
5. MCP 配置是否已存在同名 server

#### 步骤

建议固定为 5 阶段：

1. `install_cc`
- 安装或确认 `Claude Code`

2. `setup_provider`
- 官方登录或配置 `CCR/other provider`
- 验证 `claude -p` 主请求

3. `install_codex_mcp`
- 注册 `codex-cli`
- 验证 MCP 连接

4. `configure_runtime_policy`
- 写入默认 capability / policy
- 对齐 `auto/step` 到 Claude 与 Codex 两层批准策略
- 配置 thread continuity 策略

5. `verify_end_to_end`
- 验证 `Claude` 可用
- 验证 `Codex MCP` 被真实调用

#### 运行时策略输出

该 skill 执行完成后，应至少产出以下结构化结果：

- `tool=cc`
- `provider_ready=true|false`
- `provider_kind`
- `provider_backend`
- `tool_capabilities=[codex-cli]`
- `codex_mcp_ready=true|false`
- `default_runtime_policy`
  - `prefer_codex_for_repo_work=true|false`
  - `auto -> claude permission mode`
  - `auto -> codex approval-policy`
  - `step -> claude permission mode`
  - `step -> codex approval-policy`
- `verification`
  - `claude_main_request_ok`
  - `codex_mcp_connected`
  - `codex_mcp_called`

#### `codex` / `codex-reply` 路由契约

skill 应指导 runtime 使用以下默认规则：

1. 无现存 continuity thread
- 调用 `mcp__codex-cli__codex`

2. 有同一 issue / 同一会话 continuity thread
- 调用 `mcp__codex-cli__codex-reply`

3. thread 不健康或上下文应轮换
- 重新走 `mcp__codex-cli__codex`
- 并更新记录的 `threadId`

#### 验收

skill 完成后，至少要满足：

1. `claude -p -- "Reply with exactly: hi"` 成功
2. `claude` 能识别已注册的 `codex-cli` MCP
3. 强制要求使用 `codex-cli` 的测试提示成功返回
4. 调试日志出现真实 `Calling MCP tool: codex`
5. 若将 provider key 改为假值，主请求失败
   - 以证明当前不是“Codex 直接充当 Claude 底层 provider”

#### 失败分支

这个 skill 不应在失败时只给笼统报错，而应明确归类：

1. `cc_not_installed`
2. `codex_not_installed`
3. `provider_not_ready`
4. `ccr_not_running`
5. `provider_auth_failed`
6. `mcp_not_registered`
7. `mcp_connected_but_not_called`
8. `policy_not_persisted`

### 10. 对 Freely runtime 的直接启发

如果 Freely 后续要真正支持 `tool=cc`，runtime 至少需要新增三块状态：

1. `provider_backend`
- 区分 `official / ccr / other`

2. `tool_capabilities`
- 例如 `[codex-cli]`

3. `capability_continuity`
- 至少能存 `threadId`
- 并与 issue / progress / recovery 关联

否则 runtime 无法稳定地从 `codex` 过渡到 `codex-reply`。

## Modeling Decision

### 不应把 Freely 顶层 tool 命名成 `use-codex-in-cc`

原因：

1. Freely 顶层 `tool` 表达的是“主执行器是谁”
- 这里主执行器是 `Claude Code`
- Codex 只是 Claude Code 内部通过 MCP 可调用的能力

2. 若把顶层命名成 `use-codex-in-cc`
- 会把执行器、provider、能力 profile 三层混成一个名字
- 后续会不可扩展，例如：
  - `cc + github mcp`
  - `cc + browser mcp`
  - `cc + codex + browser`

3. 用户心智也更稳定
- “我现在用的是 Claude Code”
- “它有没有启用 Codex MCP profile”
- 而不是“我在用一个长名字的新 tool”

### 建议建模

- 顶层 tool：`cc`
- model：仍表示 Claude Code 主模型，例如 `sonnet`
- mode：仍保持 `auto|step`
- 额外 capability/profile：显式描述 Claude Code 挂载了哪些 MCP server

示意：

```text
tool=model-runner
capability=runner-internal tools
```

对应到 Freely：

```text
ai_spec = cc:sonnet:auto
cc_mcp_profile = codex-cli
```

或：

```text
ai_spec = cc:sonnet:auto
tool_capabilities = [codex-cli]
```

## Interface Recommendation

### CLI

不要把这个信息继续塞进现有 `tool:model:mode` 三段式里。

原因：

- `tool:model:mode` 已经表示主执行器契约
- 把 MCP profile 再塞进 `tool` 或 `model` 会让解析变脆

建议：

```bash
freely start --ai cc:sonnet:auto --cc-mcp-profile codex-cli
```

或通用化后：

```bash
freely start --ai cc:sonnet:auto --tool-capability codex-cli
```

若后续允许多个：

```bash
freely start --ai cc:sonnet:auto \
  --tool-capability codex-cli \
  --tool-capability browser
```

### TUI

建议不要单独暴露另一个“工具类型”。

而应在选择 `cc` 后显示：

- MCP Profiles
  - `[x] codex-cli`
  - `[ ] browser`
  - `[ ] github`

### GUI

建议表现为：

- Tool 下拉：`cc`
- Model 下拉：Claude 主模型
- 高级选项：
  - `Enable Codex MCP`
  - 或更通用的 `Enabled MCP Profiles`

如果 GUI 未来支持多个 profile，勾选框应升级为多选列表，而不是只做一个写死的 Codex 开关。

## Freely Impact

若 Freely 正式支持这条路径，建议改动方向是：

1. 宪法允许新增顶层 tool：`cc`
2. runtime 支持 `cc` 的 CLI 启动与 resume 策略
3. runtime 支持把 project-scoped `.mcp.json` 或等效 profile 写入 Claude Code 配置输入
4. `tools.md` 把 `cc` 记为“主执行器”，并明确：
   - Claude 主模型负责总体推理
   - Codex MCP 负责 runner 内部某些编码/仓库能力
   - 若 `cc` 走 router/provider，还需显式区分 `provider_backend`
5. 选择策略上，不把 `codex-cli` 当顶层 `selected_tool`
   - 顶层仍是 `cc`
   - `codex-cli` 只作为 `cc` 的 capability / profile 被启用

## Decision

本轮研究结论：

1. `Claude Code + Codex MCP` 不只是概念可行，而是已在本机跑通
2. `Codex MCP` 不能替代 Claude Code 的认证 / provider；必须先保证 Claude 主请求可用
3. 当前机器上的可用主路径是 `Claude Code -> CCR -> ModelScope`
4. `Codex` 在该结构里是 MCP tool，不是 Claude Code 的底层模型替身
5. 优先用内置 `codex mcp-server`，不优先依赖第三方 `codex-cli-mcp-tool`
6. Freely 若采用此方案，顶层 tool 应叫 `cc`
7. Codex 应作为 `cc` 的 MCP capability / profile，而不是单独发明一个长名字 tool
8. 若要“尽量总是用 Codex”，需要 skill / hook / routing policy 配合，而不是只靠安装 MCP
9. 目前没有确认到“Codex 订阅直接充当 Claude Code 底层 provider”的现成官方方案
10. 配置入口建议：
   - CLI：附加 capability/profile 参数
   - TUI：在 `cc` 下展示 MCP profile 勾选
   - GUI：在 `cc` 下展示 Codex MCP 开关或 profile 多选
11. 本预研的最终落地方向应是“`cc install -> provider setup -> codex mcp install -> verification`”标准工作流，而不是停留在概念分析

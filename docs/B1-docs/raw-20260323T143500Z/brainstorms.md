# 预研头脑风暴：interactive-init-bootstrap-and-force-governance

## 背景

- `freely init` 的真实产品语义不是“静默写一份配置”，而是项目接管入口。
- 但 Freely 仍是 CLI-first 应用，因此 `init` 不能只服务人工交互；它必须同时支持：
  - human-friendly 交互式接管
  - AI / 脚本可调用的非交互式接管
- 这次对话暴露出当前实现和预期之间有明显偏差：
  - 当前实现会直接重写 `.freely/config.env`
  - 现有测试默认项目已经 `git init -b develop`
  - `init` 还没有覆盖“目录确认 -> 空仓 bootstrap -> 细粒度 skip/force”这条完整链路
- `init` 也还没有形成可稳定供 AI 使用的非交互参数面
- Freely 的 hook 又带来一个特殊约束：
  - `main` / `develop` / `test-pre-merge-*` 上禁止常规开发提交
  - 但空仓库如果没有 bootstrap commit，又会因为缺少 `HEAD` 让分支、hook 与后续治理流程都无法稳定成立
- 这次狗粮还额外暴露了一个配置分层偏差：
  - 项目级 `.codex/config.toml` 应作为版本化项目资产随 worktree 一起出现
  - `init` 不应写用户全局 `~/.codex/config.toml`
  - sibling `{project}-worktrees` 访问权限应通过项目级工具配置声明，而不是把 Freely 变成用户目录修改器

## 主问题

需要一次收敛三个边界：

1. `freely init` 如何先判定“当前目录 / 指定目录 / git root / repo root”，并在交互式与非交互式模式下得到一致结果。
2. 空目录或非 git 目录如何通过一次受控 bootstrap，建立 `main -> initial commit -> develop` 基线，同时不和日常 hook 语义冲突。
3. 已有项目上的 `init` 应如何逐项 detect/skip/apply，而不是把所有项都当成一次性覆盖动作。
4. 项目级 AI 工具配置应如何版本化并随 worktree 继承，同时避免 Freely 改写用户级 home 配置。

## 已形成判断

### 1. `init` 首先是目录接管流程，不是配置写入流程

- CLI:
  - `freely init --project <path>` 明确指定目录
  - 无 `--project` 时先从当前目录出发
- TUI / GUI:
  - 默认当前目录
  - 当前目录不明确时，先让用户确认或重新选择项目目录
- 非交互 CLI:
  - 必须允许 AI 或脚本用显式 flag 直接表达“用当前目录 / 用 git root / 初始化 git / 接受 bootstrap”
  - 不能把关键决策只留给交互式问答
- 若当前目录位于某个 git repo 内但不是 repo root，必须先决定：
  - 接管 repo root
  - 还是接管当前子目录
- 不能在目录边界未确定前就直接 `git init` 或写项目配置

### 1A. CLI-first 是硬边界，交互只是人类友好壳

- Freely 的 `init` 必须满足：
  - 默认可交互
  - 但必须存在完整的非交互 contract
- 这意味着 `init` 的每个关键决策都需要可参数化，例如：
  - 目标目录
  - 使用 git root 还是当前目录
  - 是否允许空目录 `git init`
  - 是否执行 `main -> bootstrap commit -> develop`
  - 是否对 Freely-managed 项执行 `--force`
- AI 在自然语言指导下，应能稳定落成一条完整 CLI 命令，而不是依赖 TUI/GUI 才能“做对”

### 2. `git init` 不是第一步，而是“当前目录不是 git repo”分支下的一项动作

推荐顺序：

1. resolve target path
2. probe existing git state
3. confirm project root / repo root
4. if no git repo: bootstrap repo
5. then run Freely-managed bootstrap items

这次讨论已经明确，之前把 `git init` 当作 `init` 的默认首动作是逻辑错误。

### 3. 空仓 bootstrap 需要显式的初始化提交语义

- 对空目录或非 git 目录，`init` 应执行：
  - `git init`
  - 建立 `main`
  - 写初始 `.gitignore`
  - 做一次 bootstrap commit
  - 从 `main` 创建 `develop`
  - 最终切到 `develop`
- 这次 bootstrap commit 的语义不是“main 上开发提交”，而是“建立仓库 HEAD 与治理基线的初始化提交”
- 因此需要一个受控 bootstrap path，而不能简单套用日常 hook 约束

### 4. `init` 的正确模型是细粒度 orchestrator

每个 bootstrap 项都应独立判定：

- 已缺失：自动补
- 已存在：默认 skip
- skip 必须打印原因
- skip 必须打印手工处理方式
- 只有 `--force` 才允许覆盖该项
- 非交互模式下也必须保留同样的结构化输出，而不是沉默跳过

这条规则应至少覆盖：

- git repo bootstrap
- `main` / `develop` 分支基线
- `.gitignore`
- `AGENTS.md`
- `.freely/config.env`
- `.codex/config.toml` 等项目级工具配置
- sibling worktree 根目录访问配置
- Freely 项目级 AI / context 默认策略

### 4A. 项目级 `.codex/config.toml` 应跟踪，不应忽略

- 这次核查已经确认：
  - 主仓存在项目级 `.codex/config.toml`
  - 但它被 `.gitignore` 的 `.codex/` 规则屏蔽，没有进入版本控制
  - 结果是其他 worktree 不会自然继承这份配置
- 这与 Freely 的 worktree-first 约束冲突，因为 sibling worktree 本来就应作为标准开发工位存在。
- 因此更合理的边界是：
  - 项目级 `.codex/config.toml` 应纳入版本控制
  - `init` 在缺失时创建它，在已有时细粒度 skip 或 `--force` 更新 Freely-managed key
  - 该文件应写明每个默认项为什么存在，避免变成不可解释的“神秘魔法值”

### 4B. `init` 不应改写用户级 `~/.codex/config.toml`

- 用户 home 目录是工具全局状态，不是单项目 bootstrap 的安全写入面。
- Freely 若直接修改 `~/.codex/config.toml`，会带来：
  - 污染其他项目
  - 难以回滚
  - AI 代表用户执行时的权限和意图边界不清
- 因此 `init` 的正确责任是：
  - 在项目内生成/维护 `.codex/config.toml`
  - 把 worktrees 根访问、上下文窗口、sandbox/approval 等项目默认值写在项目内
  - 若运行某个工具仍依赖用户侧显式 trust，Freely 只打印 manual hint，不自动写 home 配置

### 4C. `init` 应为各工具创建项目级配置，而不是只写 `.freely/config.env`

- 仅写 `.freely/config.env` 不够，因为不同 AI CLI 对项目边界的理解和读取入口不同。
- `init` 应把“可被工具直接消费的项目级配置”也纳入 managed items，例如：
  - `.codex/config.toml`
  - 后续若存在其他工具的项目级配置文件，也应按同样模式接入
- 每个受管配置都应满足：
  - 被版本控制
  - 可随 worktree 带出
  - 默认值旁边有简短备注，说明为什么需要
  - 只更新 Freely-managed key，不吞掉用户自定义段落

### 4D. `init` 需要 tool adapter 分层，而不是把所有工具揉成一套写入逻辑

- 当前仓库已经天然分成三层：
  - Freely 抽象运行时配置：`.freely/config.env`
  - 工具启动与参数注入：`docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - 工具/账号级全局切换：`docs/system/workspace/scripts/runtime/ai-cli`
- 因此 `init` 不应把 Codex / Claude / Kiro / IfLow / OpenCode 直接写成一大坨条件分支；更合理的模型是：
  - 先写 Freely 自己的 canonical intent
  - 再按 tool adapter 决定是否生成项目级配置文件
  - 最后继续由 launcher 把抽象 intent 翻译成 argv / env

建议的 adapter contract：

- `supports_project_config_file`
- `project_config_path`
- `managed_keys`
- `supports_project_comments`
- `home_level_requirements`
- `manual_hints`

其含义是：

- `supports_project_config_file`
  - 该工具是否存在官方支持、值得版本化的项目级配置面
- `project_config_path`
  - 若支持，Freely 应写到哪个项目内文件
- `managed_keys`
  - Freely 只维护哪些 key，避免吞掉用户自定义配置
- `supports_project_comments`
  - 是否允许像 `.codex/config.toml` 这样把“为什么要配”直接写在文件内
- `home_level_requirements`
  - 哪些前提只能在用户目录满足，例如 Codex 的 trust 项
- `manual_hints`
  - 当某项无法项目内落地时，`init` 应输出什么手工说明

### 4E. 现阶段各工具应落在哪一层

- `codex`
  - 项目级配置：支持，落 `.codex/config.toml`
  - 适合项目内管理的项：
    - context window / compact 阈值
    - project doc budget
    - sandbox / approval 默认值
    - sibling worktrees 根访问
  - 特殊项：
    - `projects.<abs-path>.trust_level` 只能在用户 `~/.codex/config.toml`
  - 结论：
    - `init` 生成/维护项目级 `.codex/config.toml`
    - trust 项单独列为 home-level requirement

- `cc` / `cc-use-codex-cli`
  - 当前仓库里主要通过 CLI 参数和 system prompt 注入
  - Freely runtime 已有 `CLAUDE_SESSION_ID_*` continuity 与 codex-cli policy 注入面
  - 目前没有冻结的项目级配置真源
  - 结论：
    - `init` 只写 `.freely/config.env`
    - 不额外生成伪造的项目级 Claude 配置文件

- `kiro-cli`
  - 当前也是 launcher 参数注入型
  - 现有能力主要依赖 `--no-interactive`、`--trust-all-tools` 等启动参数
  - 结论：
    - `init` 不生成项目级配置文件
    - 若未来官方出现稳定项目级配置面，再纳入 adapter

- `iflow`
  - 当前主要通过参数与环境变量注入
  - sibling worktrees 访问问题更像 launcher 的 include-directories 责任
  - 结论：
    - `init` 当前不生成项目级配置文件
    - worktrees 可访问性继续由 launcher/product policy 解决

- `opencode`
  - 当前仍是潜在工具，不是已接入 runtime 的 canonical surface
  - 结论：
    - 先在 adapter registry 预留扩展位
    - 不进入第一版 `init` materialization scope

### 4F. 因此 `init` 的稳定分层应是

1. `.freely/config.env`
   - Freely 的 canonical runtime intent
   - 工具无关，表达默认 tool / model / mode / reasoning / runtime policy
2. 项目级工具配置
   - 仅在工具官方支持且值得版本化时创建
   - 第一版先接 `.codex/config.toml`
3. launcher 注入
   - 继续负责把 intent 翻译成各工具的 CLI 参数 / 环境变量 / system prompt
4. home-level 特殊前提
   - 仅保留真正无法项目内落地的项
   - 默认打印 manual hint，显式授权后再处理

### 5. 不是所有项都适合 `--force` 自动覆盖

- `.freely/config.env`、Freely-managed `.gitignore` block、项目级工具配置中的 Freely-managed key、bootstrap state 适合 `--force`
- `AGENTS.md` 这类项目治理真源不应被轻易自动覆盖；即使有 `--force`，也更可能需要显式 warning 或单独确认
- 也就是说，`--force` 是“允许覆盖 Freely-managed bootstrap items”，不是“允许粗暴重写所有文件”

## 候选方向

1. 先把 `init` 重构成明确步骤：
   - `path_resolve`
   - `git_probe`
   - `root_confirm`
   - `repo_bootstrap_if_needed`
   - `branch_bootstrap_if_needed`
   - `managed_items_apply_or_skip`
   - `summary`
2. 给每个步骤定义统一输出：
   - `apply: <item>`
   - `skip: <item> (reason)`
   - `manual: <command-or-file-path>`
   - `prompt: <decision-needed>` 仅在交互式模式出现
3. 对“bootstrap commit”引入专用语义，避免和日常 hook 规则冲突
4. 把现有只覆盖 `.freely/config.env` 的行为改成“默认保留已有配置，CLI 参数只有在 `--force` 时才覆盖”
5. 为 `init` 明确增加非交互 contract，让 AI 可以用一条 CLI 调用完成项目接管，而不是被迫进入交互问答
6. 为项目级工具配置建立模板与 merge 策略，先从 `.codex/config.toml` 开始：
   - 创建缺失文件
   - 保留非 Freely-managed 段落
   - 更新 Freely-managed key
   - 对每个 key 附带理由注释
7. 为 `init` 冻结 tool adapter contract，明确：
   - 哪些工具只写 `.freely/config.env`
   - 哪些工具还要生成项目级配置文件
   - 哪些前提只能作为 home-level requirement 输出

## 验收提示

- 在已存在 `.freely/config.env` 的项目里，`freely init` 默认不覆盖已有值，并明确打印 skip/manual hint
- 在缺失项目级 `.codex/config.toml` 的项目里，`freely init` 会创建并写入带理由注释的默认项
- 在已有 `.codex/config.toml` 的项目里，`freely init` 默认只跳过或补 Freely-managed key，不改用户 home 目录
- `codex`、`cc`、`kiro-cli`、`iflow` 的 bootstrap 路径有统一 adapter contract，不再把所有工具逻辑硬编码在 `cmd_init`
- 同样场景下，`freely init --force` 才会按当前参数重写 Freely-managed 项
- 在非 git 项目目录里，`freely init` 能通过交互或显式确认完成：
  - `git init`
  - `.gitignore`
  - bootstrap commit
  - `develop` 创建
- bootstrap 完成后，项目进入正常治理基线，后续 `main` / `develop` 仍继续受 hook 保护
- 相同决策在交互式与非交互式模式下得到一致结果；AI 可通过显式参数稳定驱动 `init`
- sibling `{project}-worktrees` 目录的工具访问需求通过项目级配置落地，不依赖 Freely 自动改写 `~/.codex/config.toml`

## 相关落点

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/tests/test-freely-init-*`
- `docs/system/workspace/scripts/tests/test-worktree-entry-flow`

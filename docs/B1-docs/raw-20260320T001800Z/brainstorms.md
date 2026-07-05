# 研究：默认项目解析与已授权项目记忆

## Context

- 日期：2026-03-20 00:18 PDT
- 触发：`freely chat` / `freely tui` / `freely intake status` 等 CLI-first 人类入口仍频繁要求显式传 `--project <abs_path>`。这对“插话”体验过于底层，也不符合用户通常已经位于当前仓库目录中的语境。
- 当前已知事实：
  - `freely init` 已在项目内写入 `.freely/config.env`。
  - `freely chat` 和 `freely tui` 已是 human interruption 的第一层前台入口。
  - 当前实现可以运行，但默认项目解析还不稳定，外部目录下会把任意 `$PWD` 误判为项目。

## 主问题

需要回答：

1. `--project` 在哪些命令上应保留为显式 override，而不应成为默认必传。
2. Freely 应如何解析“当前项目”，既符合 CLI-first，也避免误伤错误目录。
3. “记住已授权项目”应落在哪一层，才能低耦合且不制造第二套配置真源。

## 已形成的判断

### 1. `--project` 应保留，但不应是日常默认入口

对于以下命令，默认应尽量自动解析当前项目：

- `freely init`
- `freely doctor`
- `freely chat`
- `freely tui`
- `freely intake chat`
- `freely intake status`
- `freely start|baseline-status|fleet-status|stop`

显式 `--project` 的职责应降级为：

- override 当前解析结果
- 处理多项目 / 非当前目录场景
- 支持脚本化与远程调用

### 2. 默认项目解析应有稳定优先级

推荐优先级：

1. 显式 `--project`
2. `FREELY_PROJECT`
3. 当前 git root 且该 root 已初始化 `.freely/config.env`
4. 当前目录自身已初始化 `.freely/config.env`
5. 当前 git root 是“明显的项目根”，且命令允许未初始化项目
6. 当前目录自身是“明显的项目根”，且命令允许未初始化项目
7. 全局已授权项目索引中仅存在一个项目时，回退到该单项目
8. 否则报错

这里“明显的项目根”至少应满足：

- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `AGENTS.md`
- `docs/B1-docs/raw-`

它不应把任意目录当作项目，也不应仅凭最近使用项目静默漂移。

### 3. 已授权项目记忆应是全局索引，不是第二套真源

真源仍然应是项目内：

- `.freely/config.env`

全局只保留轻量索引，例如：

- `~/.freely/projects.tsv`

其职责仅是帮助 CLI 在“当前目录外但只有一个已授权项目”的场景下完成定位，而不是承载项目配置本身。

### 4. `chat` / `tui` 的产品语义必须围绕“当前项目插话”

用户语义通常是：

- 我就在当前项目目录里
- 我要对当前项目插话

因此：

- `freely chat "..."` 应默认作用于当前项目
- `freely tui` 应默认打开当前项目的 interruption 前台

只有当当前目录无法确定项目时，才要求显式 `--project` 或先 `freely init`

### 5. 这项能力应落在 runtime，而不是 TUI 私有逻辑

默认项目解析属于 CLI/runtime 能力，不是 TUI 专属逻辑。

否则会出现：

- `chat` 一套解析规则
- `tui` 一套解析规则
- 其他子命令再各自兜底

正确做法应是：

- runtime 提供统一 resolver
- `chat` / `tui` / `status` / `start` 等共同复用

## Open Questions

1. “明显的项目根”是否还应要求存在 `.git`，还是文档门足够？
2. 若全局索引中存在多个项目，CLI 是否应提供 `freely use <project>` 这类显式切换命令，还是继续只保留 `--project`？
3. `init` 是否还需要在成功后给出“以后可直接在项目内运行 freely chat / tui”的显式提示？

## 初步结论

- 这项工作应 materialize 为 runtime CLI 能力增强，而不是单独在 TUI 层做局部优化。
- `--project` 应保留，但默认用户路径应尽量走“当前项目自动解析”。
- 已授权目录记忆应只做轻量索引，不得与项目内 `.freely/config.env` 争夺真源。

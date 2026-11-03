# Brainstorms: 工作树种子清单

## 1. 事实

- `git worktree add` 只检出被跟踪文件；`.freely/` 整个目录在 `.gitignore` 里。
- 上一轮为 `agent-table.toml` 在 `wt-create` 里加了一条硬编码 `cp`。
- 这不是孤例：`.env`、本地凭证、证书、生成物都可能属于“工位必需但未被跟踪”。
- 现有 `wt-create` 已经有一套“克隆 `.freely` 状态”的逻辑（`freely.db`、`a2a_task.db`、`test-gate.env`），说明这个需求本来就存在，只是没有被抽象。

## 2. 三个 Option

### Option A：继续在 `wt-create` 里逐条硬编码

- 优点：零抽象成本。
- 否决：每发现一个缺失文件就要改一次脚本、重新走一遍 PR；换项目不通用；清单散落在 shell 里，用户无法维护。上一轮的 `agent-table.toml` 就是证据。

### Option B：把清单写进 `.freely/config.toml`

- 优点：复用现有配置读取路径。
- 否决：`.freely/` 被完全忽略，配置不随仓库走。换机器 / 重新 clone 后要重新配一遍，正好违背“用户以后在任何项目都能维护”的诉求。而且 `config.toml` 是生成物，用户手改容易与 init 冲突。

### Option C：tracked 清单 + 独立执行器（选中）

- 清单：`docs/system/workspace/worktree-seed.toml`，随仓库跟踪。
- 执行器：`docs/system/workspace/scripts/worktree/worktree_seed.py`，纯函数 + CLI。
- 接入：`wt-create` 在 dev 与 test 两个工位创建完成后各执行一次。
- 回落：清单不存在时用内置默认（`agent-table.toml`，`copy`，`required=false`），保证现有项目不需要任何配置就能维持现状。
- 优点：清单可随仓库分发；执行器可单测；`wt-create` 只留一个调用点；未来任何项目只要写这份文件。
- 代价：多一个文件与一个脚本要维护；清单与真实需求可能漂移（有人加了文件但没写进清单）。

## 3. 设计细节（在 C 内部再做的取舍）

| 取舍 | 决定 | 理由 |
|---|---|---|
| 复制还是链接 | 默认 `copy`，清单可逐条声明 `link` | 复制隔离、可改；链接适合“必须跟随主树”的配置（如 agent-table 的 slot） |
| 目标已存在 | 跳过，不覆盖 | 工位里可能已有人工修改；覆盖会静默丢工作 |
| 源缺失 | `required=false` 告警、`required=true` 失败 | 缺 `agent-table.toml` 应在建工位时立刻炸，而不是等 daemon 报一句无关的错误 |
| 目录 | 支持递归复制 | `.env.d/`、`certs/` 是常见形态 |
| 越界 | 拒绝绝对路径与 `..` | 清单是项目内文件，不该能把 `/etc/...` 搬进工位 |
| 与既有 `.freely` clone 的关系 | 保留 clone（`freely.db` 语义不同），seed 只负责清单内路径 | 数据库是状态、不是配置；混在一起会让人误以为 seed 会同步运行态 |

## 4. 不做什么

- 不做双向同步（工位改完回写主树）。
- 不做模板渲染（`${VAR}` 替换）。
- 不把 `freely.db` 放进默认清单。
- 不在 seed 里删除目标多余文件（只增不改）。

## 5. 风险

| 风险 | 缓解 |
|---|---|
| 有人把大目录（`node_modules`）写进清单，建工位变慢 | 输出耗时与字节数；文档标注“只放配置，不放依赖” |
| `link` 模式下工位改动会写回主树 | 默认 `copy`；`link` 必须显式声明 |
| 清单与需求漂移 | `freely wt-seed list` 展示生效清单与来源（manifest / builtin），便于核对 |
| 与既有 clone 逻辑重复 | 保留 clone，注释说明分工；seed 不碰 DB |

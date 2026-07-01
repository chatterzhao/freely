# Workspace Hooks

本目录是 Freely hook 规则与模板的定义真源。

定位：
- hook 不是普通脚本别名
- hook 绑定触发时机、阻断语义、Git 上下文
- `.githooks/` 是安装后的运行时位置
- 只有 `git config core.hooksPath .githooks` 后，Git 才会实际执行这些 hook；仓库里仅存在脚本文件并不等于门禁已生效
- hook 属于本地 gate，不是宿主级绝对防线；protected-branch bypass 默认仍属违规，永不豁免

## 当前模板

- `pre-commit.sh`
  - 分支 / worktree 治理门禁
  - 阻止在受保护分支直接开发
  - 阻止在 primary worktree 上继续 feature 分支提交
- `pre-push.sh`
  - 分支推送方向门禁
  - 阻止 feature/release/hotfix 跨分支名推送
  - 强制提升动作在目标分支 worktree 中完成
- `pre-merge-commit.sh`
  - develop-bound governance merge gate 与 promotion ownership gate
  - gate 失败时默认回到来源 feature worktree 修源，不得用任何方式跳过 hook
- `reference-transaction.sh`
  - 受保护分支 ref 更新门禁
  - 阻止 `git merge --ff-only`、`git reset` 等没有 canonical protected-merge receipt 的 ref-only advance
  - 允许 receipt-bearing protected merge commit 继续更新 `main` / `develop` / `test-pre-merge-*`

## 投影规则

- `docs/system/workspace/hooks/*.sh` 定义 hook 行为
- 安装流程将其投影到根目录 `.githooks/`
- 运行时包装层可以补路径解析，但不能篡改这里定义的门禁语义

## Bypass 禁令

- hook/gate bypass（包括 `--no-verify`）永久禁止。无例外。
- hook/gate 失败时，默认动作是回源修正；不要把“我相信这是误判”当成自动豁免。
- gate 误判应通过修正 gate 模式或向 `FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"` 白名单收敛解决，不得绕过。
- canonical 治理依赖：hook 时机阻断 + `pr-merge-guarded` 受控 receipt + `governance-check` post-merge audit。

## Guarded Completion Handshake

受保护分支 merge conflict completion 的 machine-readable handshake 由 `pr-merge-guarded` 写入环境变量、由 hook 消费；这不是自由约定文本。

- `FREELY_GUARDED_MERGE_COMPLETION=1`
  - 表示当前提交是受控 merge completion，而不是裸 `git commit`
  - 必须与 git-dir scoped guarded completion state 一起出现；单独设置环境变量不构成合法握手
- `FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"`
  - 唯一合法 bypass 机制：仅跳过 IBM governance 文档门禁，保留安全/分支保护门禁
  - 仅限 document|cleanup|format 等结构上无需 IBM lifecycle 证据的变更

运行时语义：
- `pr-merge-guarded` 负责写入 `MERGE_MSG` receipt 和 git-dir scoped guarded completion state
- `pre-commit` 只接受带 `FREELY_GUARDED_MERGE_COMPLETION=1` 且 guarded state 与 `MERGE_HEAD` / current branch 对齐的 protected-branch merge completion
- `pre-merge-commit` 校验 guarded state 与 `MERGE_HEAD` / current branch 对齐
- 事后 `governance-check` 还会审计 merge receipt；hook pass 不等于 post-hoc audit 免责

## 安装检查

- 检查当前仓库：`git config --get core.hooksPath`
- 预期结果：`.githooks`
- 若不是 `.githooks`，立即执行：`git config core.hooksPath .githooks`
- `test-pre-merge-*` 依赖这些 hook 才能落实“允许 merge/cherry-pick 装配、允许直接写文件验证、禁止手动 add+commit 原创提交与 push、测试完即删”的语义
- `pre-merge-commit` 会在本地把当前权威 `test-pre-merge-*` 批次并入 `develop` 时运行 develop-bound governance materialization gate，检查本次 merge 涉及的 candidate / milestone / IBM issue 链是否断裂
- merge conflict completion 不能默认回退到裸 `git commit`；受保护分支上的 completion 必须走 `freely pr-merge-guarded complete`
- `pr-merge-guarded` 是 protected-branch merge receipt 的唯一 canonical 入口

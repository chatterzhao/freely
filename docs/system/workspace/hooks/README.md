# Workspace Hooks

本目录是 Freely hook 规则与模板的定义真源。

定位：
- hook 不是普通脚本别名
- hook 绑定触发时机、阻断语义、Git 上下文
- `.githooks/` 是安装后的运行时位置
- 只有 `git config core.hooksPath .githooks` 后，Git 才会实际执行这些 hook；仓库里仅存在脚本文件并不等于门禁已生效
- hook 属于本地 gate，不是宿主级绝对防线；protected-branch bypass 默认仍属违规，只有 `docs/LAWS.md` §2D 的 break-glass 白名单才允许最小化例外路径

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
  - gate 失败时默认回到来源 feature worktree 修源，不得直接用裸 `--no-verify` 跳过
  - 若命中 break-glass，只能通过受控 completion path 留下 receipt 并承担 follow-on 修复责任

## 投影规则

- `docs/system/workspace/hooks/*.sh` 定义 hook 行为
- 安装流程将其投影到根目录 `.githooks/`
- 运行时包装层可以补路径解析，但不能篡改这里定义的门禁语义

## Bypass 边界

- 本地 hook 是受保护分支治理门禁的一部分，但不是绝对不可绕过的硬件防线；`--no-verify` 等 client-side bypass 仍然存在。
- 因此 canonical 治理必须同时依赖：
  - hook 时机阻断
  - 受控 merge receipt / break-glass receipt
  - `governance-check` 或等价 post-merge audit
- `--no-verify` 不是正常工作流；只有 `docs/LAWS.md` §2D 定义的 break-glass 场景才允许临时豁免。
- hook/gate 失败时，默认动作是回源修正或 materialize follow-on owner；不要把“我相信这是误判”当成自动豁免。

## Guarded Completion Handshake

受保护分支 merge conflict completion 的 machine-readable handshake 由 `merge-guarded` 写入环境变量、由 hook 消费；这不是自由约定文本。

- `FREELY_GUARDED_MERGE_COMPLETION=1`
  - 表示当前提交是受控 merge completion，而不是裸 `git commit`
- `FREELY_BREAK_GLASS_REASON`
  - 仅 break-glass completion 使用；必须命中 `docs/LAWS.md` §2D 白名单
- `FREELY_BLOCKED_GATE`
  - 仅 break-glass completion 使用；指明被证明误判或不可用的 gate
- `FREELY_OPERATION_SCOPE`
  - phase-1 必须为 `merge_completion_only`
- `FREELY_FOLLOW_ON_ISSUE`
  - 指向承接 gate 缺陷或治理缺口的 owner
- `FREELY_EVIDENCE_REFS`
  - 以 `||` 连接的一组 evidence ref；hook 只消费 machine-readable payload，不从自然语言中猜

运行时语义：
- `merge-guarded complete ...` 负责写入 `MERGE_MSG` receipt，并设置上面这些变量
- `pre-commit` 只接受带 `FREELY_GUARDED_MERGE_COMPLETION=1` 的 protected-branch merge completion
- `pre-merge-commit` 在 break-glass 模式下只校验白名单 reason、blocked gate、scope、follow-on owner 与 evidence refs
- 事后 `governance-check` 还会审计 merge receipt 与 break-glass ledger；hook pass 不等于 post-hoc audit 免责

## 安装检查

- 检查当前仓库：`git config --get core.hooksPath`
- 预期结果：`.githooks`
- 若不是 `.githooks`，立即执行：`git config core.hooksPath .githooks`
- `test-pre-merge-*` 依赖这些 hook 才能落实“只允许 merge 装配、禁止普通提交与 push、测试完即删”的语义
- `pre-merge-commit` 会在本地把 feature replay 到 `develop` 时运行 develop-bound governance materialization gate，检查本次 merge 涉及的 candidate / milestone / IBM issue 链是否断裂
- merge conflict completion 不能默认回退到裸 `git commit`；受保护分支上的 completion 应优先走 `./bin/merge-guarded complete ...`
- `merge-guarded` 是 protected-branch merge receipt 的 canonical 正常入口；如果必须进入 break-glass，也要留下可审计 receipt，供后续 `governance-check` 识别

## Guarded Completion Handshake

受保护分支上的 merge conflict completion 必须走 `merge-guarded` 和 hook 间的 machine-readable 握手，而不是裸 `git commit`：

- `FREELY_GUARDED_MERGE_COMPLETION=1`
  - 表示这次提交是 `merge-guarded complete ...` 驱动的受控 merge completion
  - `pre-commit` 只在该标记存在时放行 protected-branch merge completion
- `FREELY_BREAK_GLASS_REASON`
  - 仅 break-glass completion 使用
  - 当前只允许 `tooling_unavailable`、`verified_false_negative`
- `FREELY_BLOCKED_GATE`
  - 仅 break-glass completion 使用
  - 当前只允许 `pre-commit`、`pre-merge-commit`、`governance-merge-gate`、`governance-promotion-gate`、`pretests-gate`、`checkpoint-guard`
- `FREELY_OPERATION_SCOPE`
  - 仅 break-glass completion 使用
  - phase-1 必须是 `merge_completion_only`
- `FREELY_FOLLOW_ON_ISSUE`
  - 仅 break-glass completion 使用
  - 必须指向负责后续修复误报/缺口的 owner issue
- `FREELY_EVIDENCE_REFS`
  - 仅 break-glass completion 使用
  - 必须是非空 evidence ref 列表，供 `pre-merge-commit` acknowledgement 与后续 `governance-check` receipt ledger 审计消费

语义：
- `merge-guarded` 负责写 merge receipt trailer，并在 `git merge --continue` 前设置这些环境变量
- `pre-commit` 只负责挡住裸 completion，确保 protected branch completion 不会回落到自由提交
- `pre-merge-commit` 负责验证 break-glass 白名单字段是否完整、是否合法，并在合法时打印 acknowledgement
- `governance-check` 再用 merge commit trailer 和 `protected-branch-breakglass-receipts.md` 做 post-merge audit

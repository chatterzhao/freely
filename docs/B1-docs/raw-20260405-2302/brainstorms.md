# 预研头脑风暴：worktree-helper-shell-source-compatibility

## 背景

Freely 当前把 `source ./bin/wt-add ...` 与 `source ./bin/wt-enter ...` 作为正式 helper 入口写进了 [AGENTS.md](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-2302-feature-worktree-helper-shell-source-compatibility/AGENTS.md) 和相关 workspace guidance。

但在真实 dogfood 里，默认 shell 是 `zsh`，而 `bin/wt-add` / `bin/wt-enter` wrapper 直接依赖 `BASH_SOURCE`，导致用户按文档执行时立刻失败：

1. `zsh -lc 'source ./bin/wt-add -- README.md'`
2. `zsh -lc 'source ./bin/wt-enter develop'`

两条命令都会在 wrapper 的前几行报 `BASH_SOURCE[0]: parameter not set`，随后拼出错误的脚本路径。

## 这为什么是一个新问题

已有 `worktree-tool-boundary-bootstrap` owner 解决的是：

1. sibling worktree 中的 tooling rematerialization
2. `wt-create` 和 `post-checkout` 的 managed path
3. worktree boundary contract

它并没有冻结“正式 helper wrapper 在默认 shell 下可 source”这个入口契约。当前 regression 也证明现有回归只直接测了内部脚本，没有测用户真正执行的 `bin/` wrapper。

## 问题收敛

当前缺口有三个层面，而且它们应该在同一窄 owner 中收口：

1. `bin/wt-add` / `bin/wt-enter` wrapper 必须在默认 shell 环境下保持 shell-safe source contract。
2. 用户实际命令路径必须被回归测试覆盖，而不是只测 `docs/system/workspace/scripts/worktree/*` 内部脚本。
3. workspace guidance 必须明确这些 helper 是 documented convenience entrypoints，但不能假定操作者已经先切进 `bash`。

## 初步边界

这条 owner 只解决：

1. source-able wrapper shell compatibility
2. helper wrapper 到内部 worktree scripts 的路径解析
3. focused regression 覆盖 documented command path

## 明确不做

1. 不重开整个 worktree boundary/bootstrap owner
2. 不改 `wt-create` 的主规范地位
3. 不引入新的 shell abstraction layer 或 wrapper framework
4. 不扩大到所有 `bin/*` wrapper 的统一重写，除非这轮证据证明 `wt-add` / `wt-enter` 之外也同样 broken

## 初步结论

这是一个明确的 CLI-first 命令契约回归，应 materialize 成新的窄 follow-on owner，而不是静默吸收到旧 closeout owner 或只补一句文档。

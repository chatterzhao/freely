# Workspace Hooks

本目录是 Freely hook 规则与模板的定义真源。

定位：
- hook 不是普通脚本别名
- hook 绑定触发时机、阻断语义、Git 上下文
- `.githooks/` 是安装后的运行时位置
- 只有 `git config core.hooksPath .githooks` 后，Git 才会实际执行这些 hook；仓库里仅存在脚本文件并不等于门禁已生效

## 当前模板

- `pre-commit.sh`
  - 分支 / worktree 治理门禁
  - 阻止在受保护分支直接开发
  - 阻止在 primary worktree 上继续 feature 分支提交
- `pre-push.sh`
  - 分支推送方向门禁
  - 阻止 feature/release/hotfix 跨分支名推送
  - 强制提升动作在目标分支 worktree 中完成

## 投影规则

- `docs/system/workspace/hooks/*.sh` 定义 hook 行为
- 安装流程将其投影到根目录 `.githooks/`
- 运行时包装层可以补路径解析，但不能篡改这里定义的门禁语义

## 安装检查

- 检查当前仓库：`git config --get core.hooksPath`
- 预期结果：`.githooks`
- 若不是 `.githooks`，立即执行：`git config core.hooksPath .githooks`
- `test-pre-merge-*` 依赖这些 hook 才能落实“只允许 merge 装配、禁止普通提交与 push、测试完即删”的语义

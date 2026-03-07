# Workspace Hooks

本目录是 Freely hook 规则与模板的定义真源。

定位：
- hook 不是普通脚本别名
- hook 绑定触发时机、阻断语义、Git 上下文
- `.githooks/` 是安装后的运行时位置

## 当前模板

- `pre-commit.sh`
  - 最小治理检查模板
  - 确认首段闭环产物存在
  - 防止工作区继续回退到“只有口头路由，没有定义源”

## 投影规则

- `docs/system/workspace/hooks/*.sh` 定义 hook 行为
- 安装流程将其投影到根目录 `.githooks/`
- 运行时包装层可以补路径解析，但不能篡改这里定义的门禁语义

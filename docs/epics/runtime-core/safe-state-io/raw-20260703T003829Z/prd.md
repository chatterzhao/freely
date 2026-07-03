# PRD: 修复 write_workcell_state unsafe source

- issue_id: I-20260703T003829Z-A

## Goal

消除 `write_workcell_state()` 中 `source "$state_file"` 的命令注入风险，
使 daemon 启动不再因 env 文件中的多词值而意外执行命令。

## 实现方案

用已有的 `meta_env_value` 函数替换 `source`。
`meta_env_value` 使用 `awk -F '"'` 按双引号分割安全提取值，
不执行 shell 命令。

改动范围：`docs/system/workspace/scripts/runtime/freely` 1 处，4 行 → 1 行。

附带：`git rm --cached .freely/run/workcell-state.env` 将误提交的运行时文件从 git 移除。

## Dev-Loop Handoff

- 改动文件: `docs/system/workspace/scripts/runtime/freely`
- 改动行: 8423-8428
- 验证方式: daemon 启动不再触发 pr-create-guarded

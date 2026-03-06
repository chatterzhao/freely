# Workspace Scripts

本目录是 Freely 工作区脚本的定义真源。

定位：
- `scripts/` 负责显式执行入口
- `hooks/` 负责 Git 生命周期触发入口
- `bin/`、`.githooks/` 是运行时投影位置，不是主定义源

## 当前脚本

- `start-lead-agent.sh`
  - 最小首跳启动器
  - 接收项目路径、意图路径、宪法路径、AI 规格
  - 生成交给外部 AI CLI 的首跳提示
  - 明确进入 `lead-agent`
  - 不在脚本层决定最终路由，只负责把 AI 送入可自治理解的首跳语境

## 输入面

- `--project <abs_path>`
- `--intent <abs_file>`
- `--constitution <abs_file>`
- `--ai <tool[:model][:mode]>`

## 输出面

- 校验通过后输出首跳 prompt
- 该 prompt 由运行时脚本或外部 AI CLI 消费
- 不在这里直接承载完整 supervisor / restart / state 逻辑
- 不在这里硬编码“走 IBM 还是走 pre-brainstorm”

## 投影规则

- `docs/system/workspace/scripts/*.sh` 可投影到 `bin/`
- 投影后的运行时包装层不得改变这里定义的输入面和首跳语义

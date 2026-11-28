# PRD: 入口命令名与 dispatcher 对齐

## Goal
消除 `bin/freely` 注释对未实现 `freely install` 的承诺，并建立防复发的静态命令名契约。

## 实现方案
- 修改 `bin/freely` 头部三段注释：prod mode 描述、PATH 示例、marker 说明。
- 新增 `docs/system/workspace/scripts/quality/command_name_contract.py`（只读 + 自测反例）。
- 新增 AT `docs/system/workspace/scripts/tests/test-command-name-contract.py`，注册进 `bin/test-all`。

## Dev-Loop Handoff
1. 先运行 AT 确认 RED（baseline 仍承诺 `freely install`）。
2. 再改注释并新增 checker。
3. 同步 test 工位跑全量测试，最后按封装链提 PR。

# Tasks — I-20261108T134701Z-A

- T1: 写 AT-001（test-command-name-contract.py），在 develop 基线跑 RED 并落证据。
- T2: 新增 `docs/system/workspace/scripts/tests/command_name_contract.py`（只读、自测反例、fail-closed）。
- T3: 修 `bin/freely` 头部注释，注册 AT 到 `bin/test-all`，跑 `bin/check-runtime-size` 回归。
- T4: 同步 test 工位跑全量 GREEN，按封装链提 PR / review / merge / wt-close。

# Implementation Decision Note
- issue_id: I-20261106T084804Z-A
- decision: wt-create 主流程顶层三处 `return 1` 改为 `exit 1`，只改控制流关键字
- why_this: 该文件由 `bin/wt-create` 以 `exec bash` 直接执行，主流程不在函数内，顶层 `return` 非法；失败时 bash 语法错误遮蔽业务错误，且失败语义依赖 `set -e` 隐式兜底，一旦被 wrapper/source 包裹就可能失败后继续往下跑。
- alternatives_considered: 把函数内 22 处 return 一起改成 exit（破坏 helper 组合语义）；抽 `main()` + `BASH_SOURCE` 守卫以支持 source（架构改动，需独立 issue）；改 shim（破坏唯一入口）；顺手修四态判定或预存红测试（越界）。#4153 是库文件被 source 时把顶层 exit 改成 return，方向相反，不可照抄。
- boundary_non_goals: 不改函数内 return、shim 结构、四态判定/恢复/legacy/seed 单一真源、三条业务文案与清理动作；不夹带 #4153 / #4157 / #4151。
- residual_risk: ①若未来确实需要支持被 source，需另开 issue 抽 `main()` 并加守卫；当前 `exit` 在被 source 时会终止调用方 shell，但本脚本设计上不是库。②2 个预存红测试归 #4151。
- verification: AT-001 基线 RED 4 失败 / 12 既有能力 PASS → GREEN 20 项全通过；顶层 return 3→0、函数内 22→22；三条失败分支端到端断言 exit 1 / 业务文案 / 无 bash 语法错误 / dev 分支清理；9 个回归 PASS，2 个预存红测试与基线一致 → 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；相邻现象已被 #4153 / #4157 / #4151 覆盖，未重复立项。

# Tasks: raw-20261126T114403Z

- T1: adapter 增 `close-local-ids` 批量子命令，一次读取 records 后复用判据，输出逐 id 汇总与 rc 0/3/1。
- T2: `cmd-close.sh` 增 `cmd_close_orphans_all()` 枚举 terminal 本地文档并委托 adapter；失败打印 retry。
- T3: dispatcher 注册 `--all-completed`，`commands.md` 更新用法；AT 覆盖结构 + 行为 + 回归。

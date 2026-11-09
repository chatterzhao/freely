# Implementation Decision Note
- issue_id: I-20261103T132622Z-A
- issue_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261103T132622Z/issues/I-20261103T132622Z-A.md
- decision: 启动锁的回收改成「age + owner」双校验（不引入新锁原语）；DB daemon 在 fork 前用 `fcntl.flock` 抢 pid 文件、bind 前探测、cleanup 校验 owner
- why_this: 两个后果都是「控制面分裂 / 全项目 DB 不可用」，且表现为 AI 行为怪异而非崩溃。TOCTOU 的真正常态只有一个毫秒级窗口（mkdir→写 state.env），修复点是回收判定而不是创建方式；DB 双实例的根因是 check-then-act 加无条件 unlink 别人的 socket。
- alternatives_considered: ①`flock` fd 继承给 supervisor——会把启动窗口互斥变成运行期独占，改变 stop/restart 语义；②`ln` 硬链接原子锁——需要把锁从目录改成文件，影响 5 处读取路径，收益与风险不成比例；③只加 age 校验——DB 面完全没覆盖；④保留 SQLite 的 `database is locked` 兜底——那是症状不是约束，RED 已证明它让 pid 文件指向错误进程。
- boundary_non_goals: 不改锁持有语义与 `freely start` 对外行为（已有实例仍返回 0）；不动 `active-but-stalled` 既有回收路径；不覆盖派发 CAS / SSE / pkill（拆 #4239）。
- residual_risk: ①`ps` 在受限环境不可读时 cmdline 校验退化为「属于」，PID 复用会回到旧的等待超时行为（不会误杀，但会白等）；②`fcntl.flock` 在 NFS 上语义弱，本项目都在本地盘；③派发仍非幂等（#4239），所以「双 supervisor」被堵住后，worker 重复拉起仍可能发生，两者独立；④`/tmp/freely-db-<hash>.pid` 是全局路径，测试并发跑同一 project 会互相干扰（本轮用唯一临时项目规避）。
- verification: AT-001 develop 基线 RED `5 ok / 8 failed`（pid 文件指向 `94129` 而已存活进程是 `94128`，loser 靠 SQLite `database is locked` 才崩）→ 工位 GREEN `13 ok / 0 failed`（loser 输出 `singleton lock held`）。
- self_bootstrap_findings: ①issue 写的「flock 持有 fd 并继承给 supervisor」在 macOS 上无 `flock` 命令，且会改变锁语义——已改为复用项目既有 `fcntl.flock` 范式并只覆盖启动窗口；②`active-but-stalled` 既有路径会让「几小时前的 started_at」被立刻回收，测试夹具必须用当前时间才能测到 cmdline 分支；③本机 `ps` 被沙箱禁用，AT 对「cmdline 不可读」单独做了保守断言。

## Implementation Decision Note
- decision: 回收判定加 age+owner 双校验；DB daemon fork 前 flock + bind 前探测 + cleanup owner 校验
- why_this: TOCTOU 与 check-then-act 让控制面分裂、DB 全停
- alternatives_considered: fd 继承 / ln 原子锁 / 只加 age / 依赖 SQLite 兜底
- boundary_non_goals: 锁语义、start 对外行为、既有 stalled 回收、派发/SSE/pkill 均不动
- residual_risk: ps 不可读时退化、NFS 语义、派发仍非幂等、/tmp 路径并发干扰

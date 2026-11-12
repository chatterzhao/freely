# Implementation Decision Note
- issue_id: I-20261104T080259Z-A
- issue_path: docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/issues/I-20261104T080259Z-A.md
- decision: 清 `.githooks/` 6 个非 wrapper 文件并把 `post-checkout` 迁到真源；新增 `projection_verify.py` + `projection.lock`（copy/delegate 双语义、四类投影）+ `bin/projections` + runtime 内联分派；`deploy-skills` 写回 hash；修生成器与模板 9 处幽灵 skill 名；AT + 单测进 CI。
- why_this: 投影此前完全无法机器校验。但「所有投影比 hash」是错的模型——wrapper 是委托而非副本；区分 mode 后既能证明部署副本一致，也能证明 wrapper 仍指向真源，且不会把 61/62 条正常委托误判成漂移。
- alternatives_considered: ①一律字节 hash——61/62 全红，模型错误；②skills 也进仓库 lock——会把 `$HOME` 绝对路径提交给所有人；③agents 按字节 hash——生成的 AGENTS.md 项目专属，hash 无意义；④为新增分派上调行数预算——违反 R31「只许下调」契约，改用内联 exec 先例。
- boundary_non_goals: 不动 `bin/worktree-common.sh`（真源 hook 硬依赖）；不迁 `bin/` 剩余 35 条 implementation-in-bin（归 #4302）；不上调 `.size-budget`；不改 wrapper 的 fail-closed 语义（缺真源仍 exit 2）。
- residual_risk: ①未部署机器上 skills 类无记录；②真源有意变更后需手动 `record`；③agents 名字提取规则依赖 `skill:` 前缀与模板反引号约定；④lock 的 hash 与真源绑定，跨机器 checkout 后若文件权限/换行差异会判红（当前仓库统一 LF，未出现）。

## 为什么 delegate 型要 pin 真源而不是 wrapper

wrapper 只有 11 行且允许自由改写（注释、日志），只要它还 `exec` 真源就没问题。
真正不能悄悄变的是**真源**——所以 lock 记它的 hash，verify 同时检查
「真源未变」与「wrapper 仍指向它」。两侧任一被破坏都算漂移，AT 的 b18 对两侧各测一次。

## 为什么行数预算不能上调

R31 立的契约是「单体只许变小」。本轮新增分派让它到 27162 行，门禁直接 refuse。
正确做法不是改预算，而是换更省的写法：文件里已有 `harness-status) exec ...` 的内联先例，
照它写就不需要额外的 3 行函数壳，正好回到 27158。这也是本轮最有价值的自证：
门禁对作者本人生效。

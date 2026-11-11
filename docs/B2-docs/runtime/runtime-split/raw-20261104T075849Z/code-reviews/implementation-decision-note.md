# Implementation Decision Note
- issue_id: I-20261104T075849Z-A
- issue_path: docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/issues/I-20261104T075849Z-A.md
- decision: 先建 `scripts/runtime/lib/common.sh` 作为 helper 唯一 owner，再把 3 个子命令外移到 `bin/test-gate` / `bin/evidence`，单体只留 `exec` 投影；新增 `bin/check-runtime-size` + `.size-budget` 锁行数；新增脚本生成的依赖矩阵与 Rust PoC 文档。
- why_this: 单体已从 26,823 涨到 27,272 且 `check-file-size` 对它完全跳过，所以「拆分」的第一步必须是可机检的行数承诺；而外移的真实阻塞是 helper 内联，先把 helper 单源化，后续每个 phase 1/2 外移都只需 `exec` 一行。
- alternatives_considered: ①一次性搬 daemon/supervisor/dispatch——13 个 phase 3 命令通过全局变量耦合，一轮内给不出可复现 RED；②只写拆分计划不动代码——不满足验收 2/3（至少 3 个外移 + 行数下降）；③把 helper 复制进每个 `bin/<cmd>`——必然漂移，且 lint 无法发现。
- boundary_non_goals: 不写 Rust、不改 `Cargo.toml`、不搬 phase 2/3 的 35 个命令、不改 `bin/freely` 的 source 契约、不改 gate 逻辑、不动 `state_file.py`。
- residual_risk: ①只完成 3/56，进度需按 `split-plan.md` 续推；②预算需每轮下调，否则守卫钝化（AT 已断言预算 < 基线）；③`bin/test-gate` 依赖 `ROOT_DIR` 定位仓库根；④`exec` 投影使被外移命令只能被子进程调用，与既有 `cmd_wt_create` 一致但与「source 后直接调函数」的测试写法不兼容。

## 为什么 helper 要单独成 lib 而不是留在单体

三个被外移的命令都需要 `log_error`，两个还需要 `run_dir_for_project` 与
`current_timestamp_utc_for_machine`。留在单体意味着 `bin/test-gate` 必须
`source` 27k 行单体 —— 循环依赖且拖慢每次调用；复制则双份真相。所以
`lib/common.sh` 是**外移的前置条件**，不是顺手重构。

## 为什么行数守卫要自建

`bin/check-file-size` 的 `should_skip()` 命中单体的 `# file-size: skip` 标记后直接
`[SKIP]` 返回 0，所以「阻止回升」这条验收标准用现有工具根本不可能满足。新增的
`bin/check-runtime-size` 只管这一个文件、只读一个预算数字，超了 fail-closed。

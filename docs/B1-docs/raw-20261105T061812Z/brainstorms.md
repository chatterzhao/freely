# Brainstorms: raw-20261105T061812Z

## 问题

`wt-create` 的四态幂等判定只用 `git show-ref --verify --quiet refs/heads/<branch>` 检查分支是否存在，完全不检查对应 worktree 目录是否仍然存在、也不检查 test 工位是否完成初始化。于是：

- 「两个分支都在、两个工位目录都被删掉」→ 误判 no-op exit 0，实际无任何可用工位。
- 「test 分支+目录在，但 Step 2 初始化未完成（缺 test-gate.env）」→ 同样误判 no-op，PR 门禁随后报 pretests_not_tested。
- 「dev 缺 / test 在」的不一致拒绝态只有静态断言，没有独立行为回归测试。

本轮 RED 在隔离 git 仓库精确复现前两种：旧实现打印「工位已存在，无需创建」并 exit 0，而 `git worktree list --porcelain` 中 dev/test 目录均为空。

## 规模与边界评审

- 修复只改 `wt-create` 的 pre-flight 判定与恢复路径，不改 `worktree-common.sh` 的路径解析函数（#4191/R4 是独立 issue，禁止夹带）。
- `_init_test_worktree_state()` 保持为初始化单一真源；`test-gate.env` 作为初始化完成标记（该函数在成功末尾写入），接受任意 `TEST_STATUS` 值——GREEN 后值为 `completed`，重跑仍应识别为已初始化。
- 「dev 缺 / test 在」继续拒绝；双工位齐全继续幂等 no-op 且不产生重复工位；legacy 补建与 Q1/#4186 恢复能力不退化。
- R2 修复后本轮物化已自动带 H1（自举验证通过），不再需要现场补标题。

## 关键设计

1. 新增 `_wt_registered_dir(branch)`：用 `git worktree list --porcelain` 找该分支**实际注册**的目录，并要求 `-d` 为真。不能用 `freely_wt_resolve_target_path()`（那是「为即将新建的工位算目标路径」，目录已存在时会追加 hash 后缀，正是 R4 的根因）。
2. 新增 `_wt_test_initialized(dir)`：`test-gate.env` 存在且含 `^TEST_STATUS=`。
3. pre-flight 的 no-op 条件升级为「两分支 + 两注册目录 + 初始化标记」五项齐全；其余 dev 分支存在的情况一律进入恢复模式。
4. 恢复路径按缺失项分别处理：dev 目录缺 → `git worktree add <path> <branch>`（分支已存在，**不能带 -b**）；test 目录缺且 test 分支在 → 同样不带 -b；test 分支也不在 → 复用 `_create_worktree`（带 -b）；test 目录在但标记缺 → 只重跑 `_init_test_worktree_state()`。

## Related findings（自举评审，已按规范处理）

- **新发现并创建独立 raw issue**：`wt-create` 主流程顶层（非函数内）在 `:889` / `:909` / `:917` 用了 `return 1`。隔离仓库实测失败时输出 `line 889: return: can only \`return' from a function or sourced script`，业务错误被 bash 语法错误遮蔽；虽然 `set -e` 目前兜住退出码 1，但失败语义依赖 shell 隐式行为。逐条证伪：#4153 是 `runtime/freely` **被 source 时把顶层 exit 改成 return**（方向相反）；#4157 是 watchdog 的 `PRE_CHECK_MAP` 与「失败表达成正常结束」（不同文件、不同语义）。两者都未覆盖本缺陷 → 用 `./bin/freely feedback` 创建 **`raw-20261106T084804Z` / #4201 / IKTHI3**，排入 goal R6.5，本 PR 不夹带修复。
- 2 个预存红测试（`test-wt-create-source-local`、`test-wt-create-syncs-tooling`）在 develop 基线同码失败，属 #4151 覆盖的测试漂移，未重复建 issue。

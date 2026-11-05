# PRD: wt-create 中断恢复与 test-pre-merge 工位补建

- issue_id: I-20261104T083043Z-A
- source_raw: raw-20261104T083043Z

## Goal

让 `freely wt-create` 在「Step 1 完成、Step 2 未完成」的中断残留状态下，用**同一条命令**即可补齐 test-pre-merge 工位并完整初始化；同时让 legacy 模式兑现帮助文本中「补建测试工位」的承诺。恢复出来的 test 工位必须与正常创建出来的完全等价，不得缺少 seed、`.freely` 状态或 `test-gate.env`。

## 非目标

- 不修 `platform-adapter.py` 的 raw key 漂移（独立缺陷，另有 raw issue）。
- 不引入 trap 回滚、不改变超时策略、不修改 `wt-close`。
- 不新增子命令；不修改 `bin/wt-create` 转发 shim。

## 现状与约束

- 真源：`docs/system/workspace/scripts/worktree/wt-create`（877 行）。`bin/wt-create` 为 5 行 `exec bash` 转发层。
- 标准模式 Step 1（:722-740）与 Step 2（:742-787）连续执行，无事务边界、无恢复入口。
- :302-308 与 :310-324 两道检查在部分成功时一律 exit 1。
- test 工位初始化逻辑内联于 :748-787，无法被其他路径复用。
- legacy 模式 :257-259 将 `test_pre_merge_branch` 置空，:859-861 仅裸建工位，base 为 `develop`。
- 接口判定 :141-142 把**默认非空**的 `skill_path` 计入 `using_new`（`[[ -n "$raw_key" || -n "$source_val" || -n "$skill_path" || -n "$slug" ]]`），使该变量恒为 1。整个 legacy 分支因此不可达，`wt-create <branch>` 一律在参数校验处报 `Missing required: --raw-key` 并打印 usage——这才是「帮助声称可补建、实测直接打印 usage」的直接根因。只写补建代码而不修接口判定，补建代码就是 dead code。

## 实现方案

### 0. 修复接口判定（legacy 可达的前提）

不再用带默认值的变量判定接口，改为按调用方**实际传入**的参数判定：

- 传入位置分支名 → legacy 模式；传入 `--raw-key/--source/--kind/--slug` 任一 → 标准模式；两者混用 → 报错；两者都无 → 打印 usage。
- `skill_path`、`base` 有默认值，禁止参与接口判定。
- 由 AT-003 行为测试守护：补建必须真实执行、以 dev 分支为 base、dev 缺失时拒绝且不回退 develop。

### 1. 抽出唯一初始化真源

新增 `_init_test_worktree_state <target>`，收纳原 :748-787 中针对 test 工位的三部分：

- `_seed_worktree "$target"`（声明式 seed，真源 `worktree_seed.py`）。
- 克隆 `.freely/freely.db`、`a2a_task.db`（不复制 `run/`、`logs/`）。
- 写 `.freely/run/test-gate.env`：`TEST_STATUS="not_tested"`、`LAST_TESTED_AT`、`LAST_TESTED_COMMIT=""`。

标准模式 Step 2 改为调用该函数；恢复模式与 legacy 补建同样调用，保证三条路径产物一致。

### 2. 标准模式四态幂等

在 :300-324 以 `resume_mode` 记录状态：

| dev 分支 | test 分支 | 行为 |
|---|---|---|
| 缺 | 缺 | 正常创建（保持原路径） |
| 在 | 缺 | `resume_mode=1`，只补 test |
| 在 | 在 | 幂等 no-op，exit 0，打印两个工位路径 |
| 缺 | 在 | exit 1，状态不一致 |

恢复模式跳过 fuzzy-match（该检查会把已存在的 dev 分支自身判为「已有工位」）。

### 3. 恢复执行点

放在 `_create_worktree` / `_seed_worktree` 定义之后、`git fetch` 之前：此时所有 helper 已可用，且无需为恢复动作同步 develop 或访问远程。执行内容：

- 解析 test 目标路径、以 `dev_branch` 为 base 调 `_create_worktree`。
- 调 `_init_test_worktree_state`。
- 失败时清理新建 test 工位与分支，退出非零。
- 成功后 `_update_scan_state` 并打印恢复摘要，exit 0。

### 4. legacy 补建

`dev_branch` 匹配 `^test-pre-merge-([0-9]{8}[-T][0-9]{4,6}Z?)-(.+)$` 时：

- 取 raw key，在 `git branch` 中定位含 `raw-<key>` 且前缀为 `fix/`、`feature/`、`hotfix/` 的分支作为 base。
- 找不到则报错退出，不回退到 `develop`。
- 创建后调用 `_init_test_worktree_state`，并输出与标准模式一致的提示。

不匹配时保持 legacy 原有行为（纯文档、init develop、release 分支），避免扩大影响面。

### 5. 帮助文本

usage 明确写出「标准模式可重跑恢复」「legacy 传 `test-pre-merge-*` 分支名才补建」，删除与实际不符的笼统表述。

## Dev-Loop Handoff

- 测试先行：`docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree`，先 RED 后实现；PR review 追加 AT-003 覆盖 legacy 真实行为。
- 证据落 `verification/test-evidence/AT-001-{RED,GREEN}.log`、`AT-002-{RED,GREEN}.log`、`AT-003-{RED,GREEN}.log`。
- 实现只改 `docs/system/workspace/scripts/worktree/wt-create` 一个运行时文件 + 新增一个测试文件 + 治理文档。
- GREEN 后进入 test-pre-merge 工位执行 pre-tests，再走 PR 门禁。

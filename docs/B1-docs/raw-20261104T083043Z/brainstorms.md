---
b1_id: B1-20261104T083043Z
phase_state: completed
source_raw: raw-20261104T083043Z
source_url: https://github.com/chatterzhao/freely/issues/4186
produced_candidate: C-20261104T083043Z-A
created_at: 2026-11-05
---

# B1_IBM: wt-create 中断后不可恢复

## Input

- GitHub #4186 / Gitee IKSWU2，优先级 P0。
- 事实边界：`wt-create` 标准模式本身可一次走完。本轮在真实项目上执行 `freely wt-create --raw-key 20261104T083043Z --source platform --kind fix --slug wt-create-resume-test-worktree`，耗时 1m57s，Step 1（dev 工位）与 Step 2（test 工位）均创建成功，包含 seed、`.freely` 状态克隆与 `test-gate.env` 初始化。因此本问题不是「命令跑不完」或性能问题。
- 缺陷只在：调用侧在 Step 2 之前中断（本次历史记录为 120 秒超时 SIGTERM）之后，无法用同一个官方命令恢复。

## Problem

标准模式 `docs/system/workspace/scripts/worktree/wt-create` 的创建过程分两步且没有事务边界：

- Step 1（:722-740）：建 dev 工位、pull raw issue、填 platform_ids、更新 scan 状态。
- Step 2（:742-787）：建 test 工位、对两个工位做 seed、克隆 `.freely` 状态、初始化 `test-gate.env`。

进程在 Step 1 完成后、Step 2 完成前终止，会留下 dev 工位与 dev 分支。此时重跑同一命令被两道检查连续阻断：

- :302-308 `Branch already exists: fix/raw-{key}-{slug}` → exit 1。
- :310-324 fuzzy-match `raw-{key} 已有工位/分支` → exit 1。

结果：无法用官方命令补齐 test 工位，只能手工 `git worktree add`，违反「所有工位由 wt-create 创建」的约束；手工建出的 test 工位还缺 seed、`.freely` 状态与 `test-gate.env`，PR 门禁报 `pretests_not_tested`。

## Root Cause

1. **幂等性缺失**：存在性检查把「部分成功」当作「重复创建」一律拒绝，没有区分「两个工位都在」与「只有 dev 在」这两种状态。
2. **初始化逻辑内联**：test 工位的完整初始化（seed / 状态克隆 / gate 文件）只写在 Step 2 的内联代码块里，没有可复用入口，恢复路径无法复用。
3. **帮助与实现不符**：usage :8 与 :874 声称 legacy 模式可「已有开发工位但缺 test-pre-merge 工位时补建测试工位」，但 :257-259 把 `test_pre_merge_branch` 置空，:859-861 的 legacy 分支只做一次裸 `_create_worktree "$dev_branch" "$tp_target" "$base"`，其中 `base` 默认是 `develop` 而不是对应的 dev 分支，也不会执行 seed 与 `test-gate.env` 初始化。

## Brainstorm

### Option A: 由调用方保证不中断，残留时手工补建

- 论据：改动最小，命令实现不动。
- 反证：调用方无法保证网络、超时、手动取消不发生；本次事故正是 120 秒超时造成。手工补建既违反约束，又漏掉三项初始化，属于把缺陷转移给人。放弃。

### Option B: 标准模式幂等恢复 + 抽出 test 工位初始化函数（推荐）

- 论据：用同一条命令、同一组参数即可恢复，调用方无需学习新命令；把 :748-787 抽成 `_init_test_worktree_state()` 后，标准路径与恢复路径共享唯一真源，避免「恢复出来的 test 工位少初始化」。
- 状态机：`dev 不存在 + test 不存在` → 正常创建；`dev 在 + test 缺` → 恢复模式，只补 test；`两者都在` → 幂等 no-op，exit 0；`dev 缺 + test 在` → 拒绝，状态不一致。
- 代价：需要放宽 :302-324 的存在性检查并让 fuzzy-match 在恢复模式下跳过（否则 dev 分支自身会触发阻断）。

### Option C: 新增独立 `wt-create --resume` 子命令

- 论据：语义显式，不改动默认路径。
- 反证：多一个入口就要多一份同步与测试；自动化轮次只会重跑原命令，仍会撞上 `Branch already exists`。放弃。

### Option D: 在 Step 1 之前加 trap 回滚

- 论据：从源头避免残留。
- 反证：能减少新增残留，但无法恢复已经存在的残留工位，也无法覆盖 Step 2 中途失败；与 Option B 互补而非替代。本 PR 不实现，列为残余风险。

## Decision: Option B

选择 B，并在 legacy 分支中兑现帮助文本的承诺：当传入分支名匹配 `test-pre-merge-<raw-key>-<slug>` 时，推导 raw key、找到对应 dev 分支作为 base，并执行与标准模式相同的 `_init_test_worktree_state()`。这样「中断后重跑标准命令」与「显式 legacy 补建」两条路径都收敛到同一初始化真源。

不纳入本 PR 的边界：不修改 `platform-adapter.py` 的物化逻辑（key 漂移是独立缺陷，已另行记录）；不增加 trap 回滚；不改变 `wt-close` 行为；不调整超时策略。

## Candidate

- candidate_id: C-20261104T083043Z-A
- status: promoted
- milestone: M-20261104T083043Z-A
- next_hop: `freely-doc-B2_IBM-execution` → `freely-test-RED-execution`

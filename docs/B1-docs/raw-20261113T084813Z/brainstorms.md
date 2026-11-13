# B1 Brainstorm — raw-20261113T084813Z

## 0. 立项来源：用户强约束

「出现门禁问题，千万不要第一时间想着绕过。如果门禁要修改，也是要找到整个项目当时为什么要这样设计门禁，现在要改是否真的是当时设计错误，或者实现不达标。千万不能改错门禁。」

本轮**恢复**被 R33.9/R33.10 放宽的门禁，改修实现缺口；不改错门禁。

## 1. 设计意图（已核实项目自身源码与验收测试）

1. `docs/system/workspace/scripts/tests/test-wt-close-protected-branch-guard` Test 1–3 明确断言：`main` / `develop` / **`test-pre-merge-*` 一律 blocked**；Test 4 只允许 fix/feature/hotfix。
2. `docs/system/workspace/AGENTS.md.example`：`test-pre-merge-*` 是「临时测试面，用完即删，不可 commit/push」的丢弃型沙箱。
3. `wt-close` Phase 6b（`Cleanup companion test-pre-merge via raw-key`）是设计上删沙箱的路径：从 `fix/raw-{key}-{slug}` 推导同 key 的 `test-pre-merge-{key}-{slug}` 并一起删除。即**沙箱随 dev 分支一起退休，不是独立收口目标**。
4. `_is_protected_branch` + `Error: '...' is a protected branch, cannot close` 由 `4d01714f6 feat: wt-close — unified worktree retirement with phase_state validation` 引入，与上述契约配套。

## 2. R33.9 / R33.10 改错门禁的过程

- 现象：R33.6 遗留一个 `test-pre-merge-20261112T040108Z-r336-selfproof`（dev 分支已被 wt-close 删掉），phase 6b 只在 `branch == fix/raw-*` 时运行，覆盖不到。
- R33.9 给 `_resolve_branch_from_raw_key` 加了 `test-pre-merge-<key>-*` 回退解析，把沙箱变成 `wt-close --raw-key` 的**主 branch**；R33.10 又在 protected 守卫上开了 `--force --discard-unmerged` 例外。
- 结果：既有验收测试断言的「test-pre-merge-* 一律 blocked」被推翻；真机输出出现 `closing platform issue for raw-...`、`syncing develop across platforms` 等本不该由丢弃型沙箱触发的完整生命周期副作用；Phase 7 从死代码变成被错误路径触发。
- **结论**：这是 **Phase 6b 实现覆盖不全**（实现不达标），不是 protected 门禁设计错误。放宽门禁属于「改错门禁」。

## 3. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 恢复守卫一律拒绝；撤销 resolver 的沙箱回退（保留 R33.9 修好的 `_count` 数值守卫）；新增 companion-only 回收路径——在 reason gate 之后只删工位+分支，不触发平台关单/Phase 7 | 门禁强度恢复 + 修实现缺口 ✅ |
| B | 保留例外，只把 Phase 7 / 平台关单跳过 | 门禁仍被放宽，与既有验收测试冲突 |
| C | 从 `_is_protected_branch` 移除 test-pre-merge-* | 更宽，禁止 |
| D | 手工 `git worktree remove` / `branch -D` | 违反铁律 |

## 4. companion-only 为何不降级

- 仍要求 `--force` + `--discard-unmerged` + 合规 reason（复用 `_require_reason`，不新增第二套校验）；
- 唯一歧义（多个同 key 沙箱）仍 `DENIED ambiguous`；
- `--dry-run` 零副作用；
- main/develop/test-pre-merge 在主路径仍一律 protected；
- 不触发平台关单、不触发 Phase 7 develop 同步（沙箱没有这两项语义）。

## 5. 证伪

- 「Phase 7 是设计给沙箱用的」→ 否：Phase 7 注释写的是 "Only sync when closing a test-pre-merge-* branch (PR was merged to develop)"，但主路径守卫一直拒绝它，说明它是历史遗留死代码；让沙箱走完整生命周期是错误触发。
- 「R33.9 的 test-pre-merge 回退是必要能力」→ 否：真机输出证明它把沙箱带进了完整生命周期，属于路径错误；新 companion-only 路径已覆盖残留回收。
- 「恢复门禁会丢能力」→ 否：R33.11 之后工位已全清；未来残留由 companion-only 路径回收，AT 在 sandbox git 仓库里真删工位/分支验证。

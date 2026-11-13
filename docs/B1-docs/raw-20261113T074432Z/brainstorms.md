# B1 Brainstorm — raw-20261113T074432Z

## 1. 现场（真机，R33.9 合并后）

R33.9 修好 `_resolve_branch_from_raw_key` 后，执行回收 R33.6 自证残留工位的命令：

    ./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force \
      --reason "违规绕过门禁中，理由充分，是：..."

输出：

    wt-close: raw key '20261112T040108Z' → branch 'test-pre-merge-20261112T040108Z-r336-selfproof'
    wt-close: branch = test-pre-merge-20261112T040108Z-r336-selfproof
    Error: 'test-pre-merge-20261112T040108Z-r336-selfproof' is a protected branch, cannot close

分支解析成功，但下一道门禁拒绝；工位与分支仍在。

## 2. 根因（已定位到行）

- `wt-close:144` `_is_protected_branch`：`case main|develop|test-pre-merge-*) return 0`。
- `wt-close:433` 守卫：`if _is_protected_branch "$branch"; then echo Error...; exit 1; fi`，**无 FORCE 例外**。
- 注释写「test-pre-merge is disposable, skip checks」，实现却是一律拒绝；
  `Phase 7`（`if [[ "$branch" == test-pre-merge-* ]]` 同步 develop）成为死代码。
- 结果：R33.9 的 test-pre-merge 回退解析只是把「找不到分支」变成「被保护分支拒绝」，
  唯一剩下的手段是手工 `git worktree remove` / `branch -D`，违反铁律。

## 3. 证伪

- 「R33.9 已完成 #4316 的期望 3」→ 否：#4316 的 AT 只覆盖 resolver 函数，真机全链路仍失败；本条是独立缺口。
- 「加 --force 就能过」→ 否：守卫在 FORCE 判断之外，且 reason gate 只校验格式不改变守卫。
- 「该工位还有活跃 agent」→ 否：raw 20261112T040108Z 已双平台 CLOSED，只有一条 chore 临时提交；`_autonomous_close_gate` 在 FORCE=true 时直接放行。

## 4. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 守卫内增加窄例外：`test-pre-merge-*` + `FORCE=true` + `DISCARD_UNMERGED=true` 时放行，main/develop 仍一律拒绝 | 最小、reason 前缀已由上层校验 ✅ |
| B | 从 `_is_protected_branch` 移除 test-pre-merge-* | 会让所有 `wt-close --raw-key` 都能删测试工位，过宽 |
| C | 新增 `--retire-sandbox` 参数 | 多一个 CLI 分支，且现有 `--force --discard-unmerged` 已表达「丢弃未合并提交」 |
| D | 手工删工位 | 违反铁律 |

## 5. 结论

采用 A；合并后用同一条命令真机回收残留工位，作为 End-to-End 证据。

# B1 Candidates — raw-20261113T074432Z

## C-20261113T074432Z-A：test-pre-merge 沙箱的受控回收

- kind: fix
- 范围：
  1. `wt-close` 保护分支守卫增加窄例外：`test-pre-merge-*` 且 `FORCE=true` 且 `DISCARD_UNMERGED=true` 时放行并打印 `retiring disposable test sandbox`；main/develop 仍一律拒绝；缺任一 flag 时给出可执行诊断。
  2. 新增 AT `test-wt-close-test-premerge-guard.py`（静态 5 + 抽取真实守卫块行为 7 + 基线控制 1）与 unit `t-wt-close-premerge-guard-01.sh`，CORE/CI_CORE 各 +1。
  3. 合并后用 `wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason <合规前缀>` 真机回收残留工位。
- 验收：
  - 两个 flag 齐备 → 守卫放行（rc=0）且明确打印；
  - 缺任一 flag → 拒绝；
  - develop / main 即使两个 flag 齐备仍拒绝；
  - develop 基线同条件仍拒绝（RED 真实）；
  - 合并后 `git worktree list` 只剩主工位。
- 不退化边界：
  - 不放宽 main/develop 保护；不改 `_is_protected_branch` 的枚举；
  - 不放宽 `--force` 的 reason 前缀与 closeout-gate 的活跃 agent 检查；
  - 不改 R33.9 的分支解析与计数守卫；不改平台关单通道。

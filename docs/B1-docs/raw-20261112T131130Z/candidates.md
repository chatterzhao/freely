# B1 Candidates — raw-20261112T131130Z

## C-20261112T131130Z-A：wt-close 分支解析的数值守卫与残留工位回收

- kind: fix
- 范围：
  1. `_resolve_branch_from_raw_key` 的 `_count` 计算改为 `grep -c . || true`，只取第一行，
     用 `^[0-9]+$` 校验；非数字时打印诊断并 `return 1`（不再静默成功）。
  2. 无 fix/feature/hotfix 匹配时，回退匹配**唯一**的 `test-pre-merge-<raw-key>-*`（或同名）分支，
     使「只剩测试沙箱」的残留可被 `wt-close --raw-key ... --discard-unmerged` 收口。
  3. 新增 AT `test-wt-close-branch-count.py`（静态 6 + 沙箱 git 行为 5 + 基线负向控制 1）
     与 unit `t-wt-close-count-01.sh`，CORE/CI_CORE 各 +1。
- 验收：
  - 无匹配 → rc=0、空输出、**无 bash 语法错误**；
  - 单个 fix 分支 → 仍返回该分支（不退化）；
  - 只有 test-pre-merge 分支 → 返回该分支（新能力）；
  - 两个等长候选 → 仍 `DENIED ambiguous` 且非零退出（不退化）；
  - develop 基线跑同一行为断言必须出现 `syntax error in expression`（证明 RED 真实）。
- 不退化边界：
  - 不改 closeout-gate / pretests-retirement-gate / dev-test 一致性判据；
  - 不改 `--force` / `--discard-unmerged` 语义与 reason 格式要求；
  - 不放宽 ambiguous 判定；平台关单仍只经封装命令。
- 修复后动作：用 `./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason "<合规前缀+理由>"`
  回收 R33.6 自证残留工位，并在 goal 记录 `git worktree list` 只剩主工位。

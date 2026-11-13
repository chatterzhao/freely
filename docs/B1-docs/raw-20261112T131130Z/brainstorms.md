# B1 Brainstorm — raw-20261112T131130Z

## 1. 现场（真机，R33.6 收尾）

执行 `./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason "..."` 想回收
R33.6 自证用的临时工位，结果：

    wt-close: line 305: [[: 0
    0: syntax error in expression (error token is "0")
    wt-close: line 306: [[: 0
    0: syntax error in expression (error token is "0")

命令 **exit 0**，但 `git worktree list` 里 `test-pre-merge-20261112T040108Z-r336-selfproof` 与分支都还在。
该 raw 已双平台 CLOSED，只剩一个 test-pre-merge 工位（没有 fix/feature 分支）。

## 2. 根因（已定位到行）

`docs/system/workspace/scripts/worktree/wt-close:303`：

    _count=$(printf '%s\n' "$match_list" | grep -c . 2>/dev/null || echo 0)

- `grep -c` 在无匹配时**自己输出 `0` 并以 1 退出**；
- `|| echo 0` 再追加一个 `0` → `_count` 变成 `$'0\n0'`；
- `[[ "$_count" -eq 0 ]]` 变成 `[[ 0\n0 -eq 0 ]]` → `syntax error in expression`；
- 函数既没 `return 0` 也没 `exit 1`，最终返回 0 且 **stdout 为空**；
- 调用方看到空结果只打印「no fix/feature branch found」并 exit 1，真实原因（语法错误）被掩盖；
- 更糟的是本例因为 `--force` 走的是 `_autonomous_close_gate` 的 sweep 分支，用户看到的是两条语法错误 + 静默成功。

## 3. 第二个缺口

`_resolve_branch_from_raw_key` 只匹配 `fix/|feature/|hotfix/raw-<key>-*`。
「dev 工位已收口、只剩 test-pre-merge 沙箱」的残留（自证工位、异常中断）根本没有对应分支，
即使计数修好，也只会走到「no fix/feature branch found」而无法用封装命令回收。

## 4. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | 收紧计数（`|| true` + 只取首行 + 正则校验）+ 增加 test-pre-merge 单匹配回退 + 失败非零退出 | 最小、覆盖两个缺口 ✅ |
| B | 完全重写分支解析为 Python | 改动面大，超范围 |
| C | 只把 `\|\| echo 0` 换成 `\|\| true` | 语法错误消失，但残留工位仍收不掉，且没有数值校验 |
| D | 手工 `git worktree remove` / `branch -D` 清理残留 | 违反「禁止手工删 worktree/分支」铁律 |

## 5. 证伪记录

- 「是 grep 版本差异」→ 否：`grep -c` 无匹配时输出 0 且退出 1 是 POSIX/BSD/GNU 一致行为。
- 「--force 导致」→ 否：不带 `--force` 同样在 303 行炸；`--force` 只是改变了前面 closeout gate 的输出。
- 「残留工位属于另一个 agent」→ 否：该 raw 双平台 CLOSED，只有一条 chore 临时提交，无活跃 agent；`closeout-gate` 在带 `--force` 时已允许 sweep。

# Brainstorms: raw-20261106T084804Z

## 问题

`docs/system/workspace/scripts/worktree/wt-create` 是**入口脚本**（`bin/wt-create` 用 `exec bash <path>` 直接执行），其主创建流程是顶层内联代码，却在三处失败分支用了 `return 1`。`return` 只允许出现在函数内或被 `source` 的脚本中；直接执行时 bash 报 `return: can only \`return' from a function or sourced script`，把业务错误遮蔽成语法错误，失败语义依赖 `set -e` 的隐式兜底。

## 覆盖域与 scope

一个独立问题（可执行脚本顶层误用 return），一个 candidate，改动 3 行。三处失败分支：raw-issue-pull 失败后的清理、dev worktree seed 失败后的清理、test worktree 初始化失败后的清理（行号因 R3/R4/R6 已从 889/909/917 漂移到 998/1018/1026）。

## 不退化边界（逐条评审）

1. **只改顶层 3 行**：函数内部的 22 处 `return` 全部合法（`_pull_raw_issue`、`_seed_worktree`、`_create_worktree`、`_init_test_worktree_state` 等），**不得改成 exit**——那会破坏函数组合语义。
2. **`bin/wt-create` shim 结构不变**：仍是 `exec bash`，本脚本不是被 source 的库。
3. **清理动作与错误文案逐字不变**：`git worktree remove --force` / `git branch -D` 带 `|| true` 兜底，三条业务错误文案保持原文。
4. **四态幂等判定、恢复模式、legacy 补建、seed 单一真源不动**（#4186/#4190、R3/R4）。
5. **与既有 open issue 严格区分**：#4153 是 `runtime/freely` **被 source 时把顶层 `exit 1` 改成 `return 1`**（方向相反，那个文件是库）；#4157 是 watchdog 的 `PRE_CHECK_MAP` 里 `return 1` 结束 `while` 子壳 + 「失败表达成正常结束」（不同文件不同语义）。两者都未覆盖本缺陷，故 R3 RED 期间已按自举规则独立立项，未合并。
6. 本轮不含任何功能改动；R2 物化 H1、R6 平台回退等本轮之前的修复全部保持。

## 关键设计

- 三处顶层 `return 1` → `exit 1`。直接执行时显式以 1 终止，输出只有业务错误文案；若将来脚本被包一层 wrapper 或 source，`exit` 仍会终止整个命令，不会「失败后继续往下跑」。
- 新增 `test-wt-create-top-level-return`（static 8 项 + behavior 12 项）：static 用括号深度分析统计顶层/函数内 return 数，断言 0 / 22；behavior 复用既有隔离 git 仓库骨架，注入三条失败分支（pull identity mismatch、dev seed 强制失败、test init 强制失败），断言 exit 1、业务文案存在、无 bash `return` 语法错误、dev 分支已清理。

## Related findings（自举评审）

本轮未发现「现有 open issue 未覆盖」的新缺陷。2 个预存红测试（`test-wt-create-source-local`、`test-wt-create-syncs-tooling`）在 develop 基线同码失败，已被 #4151 覆盖，未重复立项。

---
raw_id: raw-20261103T132605Z
status: brainstormed
created_at: 2026-11-09
---

# Brainstorms

## 覆盖域

issue 给了三步（source 安全 / 搬 skills 库 / 拆 lib）。**本次只做第 1 步**，issue 的「范围与非目标」已明确：不拆 26,823 行单体、不迁 Rust、不改 551 个测试语义。

实测核对：

| 证据点 | develop 实测 | 结论 |
|---|---|---|
| 顶层 `set -euo pipefail`（`:19`） | 仍在，source 时改变调用方 shell 选项 | 成立 |
| 两个顶层 `exit 1`（`:32-35`、`:39-42`） | 仍在 | 成立 |
| `BASH_SOURCE` 守卫只保护 `main` | 守卫在文件末尾，只包 `main "$@"` | 成立 |
| `stop_project_runtime` 内 `\|\| exit 1` | 23747 行（`freely_stop`），被 `cmd_restart`/`cmd_task_mode set`/`cmd_stop` 复用 | 成立 |

## 方案方向

### 方向 A：`return 1` + 由 `main` 统一退出

issue 建议。但顶层 `return` 只在「被 source」时合法，直接执行会打印 `can only return from a function or sourced script`。

### 方向 B：区分执行/被 source（选中）

- 文件头算一次 `_FREELY_IS_SOURCED`；
- 只有直接执行才 `set -euo pipefail`（sourced 时保持调用方选项）；
- 缺库时：sourced → `FREELY_LIB_LOAD_ERROR` + `return 1`；直接执行 → 依赖已生效的 `set -e`，用 `false` 以 1 退出（**不写 `exit` 字面量**，满足 issue 的「库加载段 0 处 exit」静态断言）。

### 方向 C：把库加载移到子 shell

- `( source ... )` 隔离副作用，但也隔离了函数定义，库函数不会进入调用方 → 不可行。

**选 B**。

## fidelity 基线

- 静态：前 70 行无 `^\s*exit [0-9]`；`freely_stop` 分支用 `|| return 1`。
- 行为：happy path 能 source；**sourcing 不改变调用方 `set +o` 输出**；缺库时 sourced 路径存活并拿到非零 rc + 错误变量；直接执行仍 rc=1。

「shell 选项不变」是本条最容易糊过去的点：如果只把 `exit` 换成 `return` 但保留顶层 `set -e`，调用方仍会在 `source` 返回非零时被 `-e` 杀掉。所以必须一起改。

## 价值判定

- 不过时：两处 `exit 1` 与顶层 `set -e` 都还在。
- 不重叠：#4239 是并发（派发/SSE/pkill），#4153 是「库被 source 时的副作用」，正交。
- 高价值：缺一个库文件 → watchdog/dispatcher/promotion gate/supervisor 同时以 1 退出，supervisor 30 秒后拉停整个 daemon。

## 被否决

- **只把 `exit 1` 改 `return 1`**：顶层 `return` 在直接执行时非法，且不改 `set -e` 仍会杀掉调用方。
- **移除 `set -euo pipefail`**：直接执行路径失去严格模式，风险更大；只在 sourced 时跳过。
- **子 shell 加载库**：函数不会进入调用方。
- **本轮顺带搬 skills 库 / 拆 lib**：issue 明确非目标，且会让「行为不变」无法验证。

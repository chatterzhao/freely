# PRD: 补齐打包 allowlist 运行时必需文件并建立防复发检查

- issue_id: I-20261106T100938Z-A
- source_raw: raw-20261106T100938Z
- workflow_kind: fix
- milestone: M-20261106T100938Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

让安装态成为「完整可用的 Freely」：能自举打包、seeder 读到随包发布的 manifest、AGENTS 模板与 doctor 清单齐全；并用机器约束防止以后再漏配。

## 唯一改动范围

1. `package-allowlist.txt` 显式新增 5 个运行时必需顶层文件（3 个纯文档经评审不随包）。
2. 新增只读 `quality/package-runtime-file-parity.py`（职责与 R5 seed parity 分开）。
3. `bin/freely-package` 在 R5 parity 之后、`rm -rf` 之前调用该检查。
4. 新增回归测试 `test-package-runtime-allowlist-parity`。

## 不退化边界

- 保留显式白名单机制（不得自动包含整个目录，#4157）。
- 不改 R5 的 `package-seed-parity.py`、`worktree-seed.toml` 三条声明、输出路径守卫（#4158）与调用顺序。
- 不改 `worktree_seed.py` 的 `load()` / `apply()` 与 builtin 回退。
- 不改 allowlist 复制循环与既有后置 `integrity: verified` 校验。
- 不夹带 #4194 / #4179 / #4168 / #4201；不批量改写历史安装版本。

## 功能需求

- FR-1: 5 个运行时文件进入打包产物且 sha256 与真源一致。
- FR-2: 安装态 `freely-package` 自举成功；`worktree_seed.load()` 返回 `source=manifest`；R5 parity 通过。
- FR-3: checker 只读比对「运行时引用的 tracked 顶层文件」与 allowlist，未声明则点名并 exit 1；扫描范围排除 tests / 治理文档 / `__pycache__` / 自身。
- FR-4: 回归测试覆盖真实打包、安装态自举、防复发拦截、9 个既有回归基线对比。

## 验收

见 `verification/pre-tests.md` 与 AT-001 RED/GREEN 证据：AT-001 全 GREEN（static 14 项 + behavior 8 项），10 个回归全 PASS、9 个基线对比 0 新增失败。

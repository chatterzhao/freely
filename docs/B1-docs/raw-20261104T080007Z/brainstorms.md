---
raw_id: raw-20261104T080007Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审（#4165 正文写于 2026-11-04，数字与结论已漂移）

| 验收项 | 真源核对 | 结论 |
|---|---|---|
| 核心 runtime 26,823 行、无单测目录 | 实测 `wc -l` = **27,272**；`tests/` 603 项里**没有** `unit/` 目录 | 成立（行数已漂移）。**本轮修复**：`tests/unit/` 14 个函数级测试 |
| 测试以端到端/脚本级为主 | 抽查 `test-freely-*` 全部是「建沙箱 repo → 跑 `bin/freely <cmd>` → 断言输出」；只有极少数 source 库文件 | 成立。**本轮修复**：直接 source 运行时库，断言单函数 |
| PR 模板缺 RED 字段 | 仓库**没有任何** `.github/PULL_REQUEST_TEMPLATE.md`；`pr-create-guarded` 的 body 默认是 `See commits for details.` | 成立且比 issue 描述更糟：连模板都不存在，改模板也不会生效（`gh pr create --body` 会覆盖模板）。**本轮修复**：body 由 `worktree/pr_body.py` 组合，强制带 `## RED 证据` |
| `pr-review-guarded` 不校验 RED | 775 行里只有 worktree 清洁、PR 号、路径、ACP、verdict、收尾清洁；无任何 TDD 检查 | 成立。**本轮修复**：新增 Step 2.5 `quality/runtime_red_gate.py` |
| 至少 3 个已合并修复补齐 RED→GREEN | 缺的是「函数级测试」，不是缺历史结论 | **本轮修复**：用历史修复点做基线快照复现 RED（见下） |

## 关键事实：runtime 本来就是可 source 的库

`docs/system/workspace/scripts/runtime/freely` 头部有 `_FREELY_IS_SOURCED`（#4153）：
被 source 时不 `set -euo pipefail`、不执行 `main`。实测 65ms 即可加载，
所以函数级测试不需要重构 27k 行，只需要一个 harness。

## 方案方向

### 方向 A：`tests/unit/` harness + 两个契约脚本（选中）

- `tests/unit/harness.sh`：`ut_load_runtime` / `ut_sandbox` / assert 家族 / `ut_report`；
- `tests/unit/run.sh`：每个 `t-*.sh` 独立 bash 进程（运行时里有**故意 exit 1** 的守卫，
  共享进程会把一次守卫变成半截测试），累加各测试的 `SUMMARY`；
- 14 个测试覆盖三类：**状态机**（state 路径/desired 读取/退出原因/pid 角色）、
  **锁**（SSE claim 活主/僵尸接管/建目录/中断 triage 互斥）、**退出码**
  （绝对路径守卫/项目解析/日志轮转/按数量清理）+ 事件可观测 + DB schema 版本；
- PR body：`worktree/pr_body.py` 渲染 `## RED 证据`，runtime 变更无证据即 exit 3；
- review：`quality/runtime_red_gate.py`，0=pass / 1=refuse / 2=skip。

### 方向 B：只加 PR 模板（否决）

仓库没有 PR 模板，且 `pr-create-guarded` 用 `--body` 显式传值，模板永远不会生效。
模板只能当文档，不能当门禁。

### 方向 C：给 27k 行做大规模重构抽出纯函数（否决）

超出一个 issue 的范围，且会把「建立证据链」变成「重写运行时」。

### 方向 D：review 侧只做人工提示（否决）

issue 明确要求「缺失则 needs_changes」；提示会被忽略，本轮直接把 gate 接在
ACP reviewer 之前。

## 3 个补录 RED 的基线选择（可复现，不靠回忆）

| 补录 | 缺陷 | 修复合并点 | RED 基线 | 复现方式 |
|---|---|---|---|---|
| A | SSE watchdog pid 文件 check-then-act 竞态 | `56d4cd2c9`（R23.10 / #4254） | `6715a67a2` | 快照 + 注入 `tests/unit` → `t-lock-01/02/03` FATAL |
| B | runtime 事件无 severity/trace_id；cycle-*/crash-* 无保留上限 | `9348b2661`（R25.5 / #4281） | `83ba84a74` | 同上 → `t-event-01` 5 项失败、`t-exit-04` FATAL |
| C | DB 无 `user_version`，迁移失败被吞 | `9348b2661`（R25.5 / #4281） | `83ba84a74` | 同上 → `t-db-01` 4 项失败（SCHEMA=missing / VERSION=0 / REFUSED=0） |

## fidelity 基线

- RED（develop `d315b5409` + 最终版 AT-001）：`2 ok / 19 failed` —— 无 `tests/unit`、
  无 `pr_body.py`、无 `runtime_red_gate.py`、body 默认裸文案。
- GREEN（工位）：`21 ok / 0 failed`；单元语料 14 文件 / 68 断言全绿。
- 补录 RED：A/B/C 三份日志各自复现失败（见 `verification/test-evidence/`）。
- 既有失败（develop 基线同样失败，非本轮引入）：local `test-all` 的
  `test-github-label-autocreate.py`；`test-command-lifecycle-consumer-boundaries.py`
  4 errors（基线一致）。

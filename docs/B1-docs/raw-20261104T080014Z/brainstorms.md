---
raw_id: raw-20261104T080014Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审（#4166 正文写于 2026-11-04，行号与部分结论已漂移）

| 验收项 | 真源核对 | 结论 |
|---|---|---|
| 平台写只剩 adapter 一处 | `bin/issue-sync:447-480` 仍直连 `gh issue create/comment/close/edit`；Gitee 已走 `gitee-issue.py`；adapter 已有 `create-issue` / `update-issue` / `close-multi`（含 0/3/1 退出码） | **本轮修复**：adapter 新增单平台 `issue-write-one`，issue-sync 4 个 `_gh_*` 改调它 |
| `feedback` 与 `issue-sync create` body/标签一致 | `feedback` 走 adapter `create-issue`（已设 labels）；`issue-sync create` 剥离 frontmatter 后传 labels | 基本一致，本轮不动；逐字对齐留待拆分轮 |
| 部分成功独立退出码 | adapter `create-issue` 已 0/3/1；`issue-sync close` 已有 3 | **已实现**，本轮不重复 |
| `issue-sync` 行数下降 ≥50%、拆子命令 | 单文件约 1300 行，拆分是大重构 | **不在本轮**，由 follow-up raw 承接 |
| `issue-sync-bootstrap` 直连 `gh issue delete` | 只用于运维删除，adapter 无 delete 契约 | 登记为例外，不在本轮 |

## 方案方向

### 方向 A：adapter 增单平台写命令，issue-sync 只编排（选中）
- `issue-write-one <platform> <action> <number> <title> <body> <labels>` 路由到现有 handler；
- `_gh_create/comment/close/update` 改调它，`GH_REPO` 通过 `FREELY_PLATFORM_REPO` 显式传入；
- 好处：写实现只有 adapter 一份，Gitee/GitHub 错误语义、标签创建、重试策略统一。
- 否决：把 `cmd_create` 整体改成一次 `create-issue` 双平台调用——会重写 platform_ids 回写与 partial 处理，风险大于收益，留给拆分轮。

### 方向 B：issue-sync 内联改调 adapter 的 Python API（否决）
adapter 文件名带连字符，`importlib` 加载 + 传参比 CLI 更脆；CLI 契约已有测试覆盖。

### 方向 C：直接删 `_gh_*`，全部走 `create-issue`（否决）
同上，会同时改创建编排与回写，超出「收口写入口」的范围。

## 被否决
拆 1300 行 `issue-sync`（独立重构）、改 `feedback` 的 body 拼装（另有 issue）、给 adapter 加 `delete`（运维专用，登记例外）。

## fidelity 基线

- RED：issue-sync 仍含 4 种直连 `gh issue` 写；adapter 无 `issue-write-one`；单平台 create 行为不可用。
- GREEN：issue-sync 无直连写、走 adapter；stub `gh` 下 adapter create 带 labels 并返回 url。
- 已知既有失败：`test-issue-sync-replica-guard.py` 在 develop 基线 6 failed（工位 4 failed），失败集中在 receipt/close-multi 路径，与本轮写入口改动无新增失败类别。

## 价值判定

写入口收口后，标签、body、错误与重试只有一份实现；`feedback` / `issue-sync` / guarded 命令不再各自演化。拆文件与 `feedback` 逐字对齐作为独立重构继续跟踪。

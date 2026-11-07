# PRD: 关闭路径先校验后执行，部分成功独立退出码

- issue_id: I-20261104T082603Z-A
- source_raw: raw-20261104T082603Z
- workflow_kind: fix
- milestone: M-20261104T082603Z-A
- story: gate/platform（复用 wt-create 已物化的 story）

## 目标

`issue-sync close` 的每一次结果都必须是「本地状态与平台状态同时可解释」的：要么全关且本地标记 closed，要么什么都没动并给出原因，要么明确报「部分成功」并保留重试能力。

## 改动范围（3 个真源 + 1 个测试）

1. `docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py`：`close_platforms()` 四段式（校验 → 执行 → 回写 → 退出码）。
2. `docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py`：终态校验错误信息带 `current` phase 与期望集合。
3. `docs/system/workspace/scripts/sync/platform-adapter.py`：`_close_exit_code()` + `close-multi` / `close-raw` 退出码 0/3/1。
4. `bin/issue-sync`：`cmd_close` 严格路径上抛 3/1；非严格路径逐平台记账，禁止「无条件写 closed」。
5. 新增 `docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first`（AT-001）。

## 不退化边界

- 非终态 raw 的**平台状态**必须保持不变（fail-closed），不许「先关再报错」。
- 关闭的幂等性：已关闭平台再次 close 仍返回成功，因此「部分成功 → 重跑」可自愈。
- `create` / `comment` / `update` 通道、读通道、`pr-merge-guarded`、`.githooks/` 不动（入口层收口归 #4166）。
- 现有 `test-platform-write-channel`（22 ok）、`test-command-lifecycle-raw-metadata`、`test-raw-reconciliation`、`test-platform-open-parity`、`test-platform-handler-probe` 基线对比零新增失败。

## 功能需求

- FR-1: 非终态 raw 关闭 → 退出非零、平台零调用、frontmatter 不变、错误含 `current` phase。
- FR-2: 终态 raw + 全平台成功 → `platform_state=closed` 落盘、退出 0。
- FR-3: 终态 raw + 部分成功 → 退出 3、`platform_state` 保持原值、逐平台 status 可读。
- FR-4: 终态 raw + 全失败 → 退出 1、`platform_state` 保持原值。
- FR-5: 非严格路径（I-*）任一平台失败不得写 `platform_state=closed`；部分 3 / 全失败 1。
- FR-6: adapter `close-multi` / `close-raw` 退出码与 `create-issue` 同口径 0/3/1。

## 验收

AT-001 基线快照 RED（顺序/退出码/自证三类失败）→ 工位 GREEN；5 个相关回归基线对比零新增失败；真实仓库只读核验非终态关闭 fail-closed。

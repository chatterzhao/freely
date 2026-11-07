# PRD: pull 按可用平台回退并复用 sync-debt 记账

- issue_id: I-20261104T082549Z-A
- source_raw: raw-20261104T082549Z
- workflow_kind: fix
- milestone: M-20261104T082549Z-A
- story: platform/raw-replica-reconciliation（复用既有 story，epics-map.svg 无需改动）

## 目标

双平台真正互为备份：任一平台不可读时，工位创建仍能从未读平台之外物化 raw issue；未读平台记为待对账债务，而不是当作不存在的事实。

## 唯一改动范围

1. `platform-adapter.py`：`pull_raw_issue()` 增加 `preferred_platform`，按 `status == "ok"` 选读源；三个循环只遍历可读副本；返回 `degraded_platforms`/`partial`；`pull` CLI 部分成功 `SystemExit(3)`。
2. `bin/raw-issue-pull`：新增 `--platform`，捕获退出码，partial 时复用既有 `sync-debt.py record` 记账，保持 stdout 单一 JSON 文档。
3. `wt-create`：新增 `--source-platform` 并透传；`_pull_raw_issue()` 把退出码 3 视为「继续」。
4. 新增回归测试 `test-raw-issue-pull-platform-fallback.py`。

## 不退化边界

- 双平台都 ok 时 primary 与 platform_ids 与修复前完全一致；返回字典仅新增两个字段。
- 全部不可读仍 FATAL；显式指定不可读平台失败而不静默回退。
- 既有 sync-debt 账本格式、`raw_reconciliation` 的 allow_degraded 决策、`_fill_platform_ids` 容错不变。
- R2 物化 H1、Q2 created_at 兼容分支、标题契约、identity 校验不变。
- 不夹带 R7/#4195、R11/#4149、#4194、#4201；平台写（close/update）按可用平台执行不在本 PR。

## 功能需求

- FR-1: `--platform gitee` / `--source-platform gitee` 明确从 gitee 读取并写回 primary_platform 与 platform_ids。
- FR-2: 默认取第一个可读平台；不可读平台记入既有 sync-debt 账本，不阻断工位创建。
- FR-3: 部分成功退出码 3（CLI 与 wt-create 语义一致），失败 1，全成功 0。
- FR-4: stdout 恰好一个 JSON 文档；platform_ids 不含无 issue_id 的副本。
- FR-5: 回归测试覆盖 RED/GREEN、端到端 CLI 退出码与账本落账、11 个既有回归基线对比。

## 验收

见 `verification/pre-tests.md` 与 AT-001 证据：基线 9 项失败 / 3 项既有能力 PASS → 修复后 12 项全绿；12 个回归全 PASS，11 个基线对比 0 新增失败。

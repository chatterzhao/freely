# PRD: 读失败显式标记，健康路径零变化

- issue_id: I-20261105T122053Z-A
- source_raw: raw-20261105T122053Z
- workflow_kind: fix
- milestone: M-20261105T122053Z-A
- story: platform/issue-parity（复用既有 story，epics-map.svg 无需改动）

## 目标

让「平台读失败」与「该平台确实没有 open issue」在结果里可区分，扫描不再基于部分清单做生命周期判断，parity 不再报假差异；健康路径保持 107 条纯字典、调用方零改动。

## 唯一改动范围

1. `platform-adapter.py`：`PlatformHandler.read_health` 契约；GitHub / Gitee 三个读通道记录 ok/error/partial；模块级 `list_open_issue_records()` 在失败时产出 `__degraded__` 并跳过非 dict 记录。
2. `test-platform-open-parity.py`：`collect_open_issues()` 返回降级平台清单；main 在降级时 SKIP + 重试提示。
3. 新增回归测试 `test-open-list-read-degraded.py`。

**不改** `task-lifecycle-scan.py`：其 `:773` 已有 `__degraded__` 消费逻辑，聚合层产出标记后自动进入既有降级语义。

## 不退化边界

- 健康路径返回纯 `{platform:issue_id -> record}` 字典，记录字段、键格式、调用方均不变。
- REST 回退保留：GraphQL 两次失败后仍走 REST；合法空响应表示「确实没有 open issue」，只有 REST 失败才降级。
- 不改 `pull_raw_issue()` 读源选择（R6）、写通道、`_discover_one` 的 unknown/missing/ambiguous 语义。
- 不夹带 R11/#4149（写通道静默失败）、R8/#4146（fail-open）、#4151（预存红测试）。

## 功能需求

- FR-1: 每个 handler 的最近一次读取产出 `ok` / `error` / `partial`。
- FR-2: 聚合层任一平台失败时附加 `__degraded__`（platform/platforms/error/ok/partial），保留可读平台记录。
- FR-3: handler 异常不产生假记录或 TypeError。
- FR-4: parity 降级时跳过并给出重试提示；健康时仍正常比较。
- FR-5: 回归测试覆盖 RED/GREEN、真实双平台健康路径、12 个回归基线对比。

## 验收

AT-001 基线 RED 5 项失败 / 4 项既有能力 PASS → GREEN 9 项全通过；真实双平台健康路径 102 条无降级标记；13 个回归全 PASS，12 个基线对比 0 新增失败。

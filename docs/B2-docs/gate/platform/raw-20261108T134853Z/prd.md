# PRD: GitHub handler 自动补齐缺失标签

- issue_id: I-20261108T134853Z-A
- source_raw: raw-20261108T134853Z
- workflow_kind: fix
- milestone: M-20261108T134853Z-A
- story: gate/platform

## 目标

`freely feedback create` 在任意 GitHub 仓库（含从未建过 severity 标签的）都能双平台成功，不再产生 PARTIAL raw；且不掩盖真实的认证/权限/网络失败。

## 改动范围（1 个真源 + 1 个测试）

1. `docs/system/workspace/scripts/sync/platform-adapter.py`：`GitHubHandler` 增加标签补齐与有限重试。
2. 新增 `docs/system/workspace/scripts/tests/test-github-label-autocreate.py`（AT-001）。

## 功能需求

- FR-1: label-not-found → 每个标签各建一次 + 重试一次 → created。
- FR-2: 标签齐备 → 零 label-create、一次 issue create。
- FR-3: 非 label 错误不重试、不建标签；二次失败有界返回 error。
- FR-4: `labels=""` 旧路径不变；4 参 `create_issue` 与 CLI 第 5 参保持兼容。

## 不退化边界

Gitee handler、R15 severity 链、平台关闭/更新/评论语义均不动；16 个回归零 DIFF。

## 验收

AT-001 基线快照 RED `7 ok / 12 failed` → GREEN `19 ok / 0 failed`；16 个回归全 MATCH；真机 feedback 双平台 created。

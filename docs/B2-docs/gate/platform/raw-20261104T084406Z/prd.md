# PRD: severity 从校验值变成可追溯的一等数据

- issue_id: I-20261104T084406Z-A
- source_raw: raw-20261104T084406Z
- workflow_kind: fix
- milestone: M-20261104T084406Z-A
- story: gate/platform（复用既有 story，不改 epics-map）

## 目标

`--severity P0|P1|P2` 创建出的 raw issue，在本地 frontmatter、双平台 label、scan 报告中都可被读到，且存量文档零改写。

## 改动范围（4 个真源 + 1 个测试）

1. `lifecycle/raw_metadata_contract.py`：可选字段、校验、读视图回填。
2. `runtime/freely`：feedback 落盘 + 传标签。
3. `sync/platform-adapter.py`：建单链路 labels 通道（向后兼容）。
4. `bin/issue-sync`：`_labels` 标签 + `cmd_scan` 排序。
5. 新增 `docs/system/workspace/scripts/tests/test-feedback-severity.py`（AT-001）。

## 不退化边界

- `RAW_METADATA_FIELDS` 仍是 21 字段；59 份 strict 文档与 824 份历史 raw 全部零改动。
- 旧 `create_issue()` 调用与自定义 2 参 handler 行为不变。
- 不修改任何平台已存在 issue；只影响新创建。
- 14 个相关回归基线对比零 DIFF。

## 功能需求

- FR-1: `--severity P0` → frontmatter `severity: P0`；默认 → `severity: P2`。
- FR-2: 平台 issue 带 `severity/Pn` label，两个 handler 都收到；旧 2 参 handler 不退化。
- FR-3: `scan` 按 P0→P1→P2 排序，存量文档按 P2 参与。
- FR-4: `validate()` 拒绝非法 severity，接受 21 与 22 两种合法形状。
- FR-5: `normalize()` / `_labels()` 对无字段或非法值回填 P2。

## 验收

AT-001 基线快照 RED `3 ok / 14 failed` → GREEN `30 ok / 0 failed`；14 个回归全 MATCH。

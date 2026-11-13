# PRD: bin 投影注册表分类落地（C-A）

- issue_id: I-20261111T125724Z-A
- source_raw: raw-20261111T125724Z
- workflow_kind: feature
- milestone: M-20261111T125724Z-A
- story: command-wrapper/pr-review-projection（复用既有 story）

## 目标

把 R32 遗留的 35 条 `implementation-in-bin` 占位登记，按项目设计意图逐条判定为
`standalone-tool`（22，自包含 lint/聚合/one-shot，保留在 bin/）或
`implementation-in-bin`（13，判定应迁移，分后续批次）。
**关键约束：`standalone-tool` 不是永久豁免**——`check-bin-projection` 的 coverage /
staleness / shrink 三条规则对它同样生效。

## 唯一改动范围

- `docs/system/workspace/scripts/bin-projections.yaml`：`classes` + 35 条 class/reason + note。
- `bin/check-bin-projection`：class 白名单校验、占位 reason 拒绝、docstring 说明；三条原规则一条不改。
- `docs/system/workspace/scripts/bin-inventory.md`：总览与 35 条表格同步。
- 新增 AT `test-bin-projection-classification.py`、unit `t-bin-projection-01.sh`，`bin/test-all` 双数组各 +1。

## 不退化边界

- `threshold_lines=40` 不变；三条门禁规则不变；不新增任何豁免；
- **本轮不迁移任何实现**，`bin/` 下除 `check-bin-projection` / `test-all` 外零改动；
- 不改 `projection.lock`、不改平台 adapter、不夹带 C-B/C-C/C-D 的迁移。

## 功能需求

- FR-1：22 条 standalone、13 条待迁移，每条 reason 为具体判定依据（无占位文案）。
- FR-2：lint 拒绝未声明 class 与占位 reason（提高强度）。
- FR-3：三条原规则逐条负向验证，且对 standalone-tool 同样生效。
- FR-4：develop 基线必须因 35 条占位 reason 与缺失 class 而判红。

## 验收

AT-001 RED `7 ok / 9 failed`（develop `63de67645` 快照，基线 R1/R2）→ GREEN `14 ok / 0 failed`；
unit `7 ok / 0 failed`；`bin/test-all --ci` 全绿；三门禁不变。

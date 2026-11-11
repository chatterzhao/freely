# Brainstorms: 把 pr-review-guarded 的业务实现移回 scripts/

- source_raw: raw-20261104T080200Z
- 覆盖域：`bin/` 投影层边界、800 行实现的迁移、其余入口盘点、投影一致性门禁。

## 真源普查

| issue 描述 | 实测（develop `cad8b5875`） | 结论 |
|---|---|---|
| `bin/pr-review-guarded` 约 1,200 行 | **806 行** | 数字偏大，问题成立 |
| `scripts/` 下无对应实现 | 确认：`scripts/worktree/` 有 pr-create/pr-merge/wt-* 等，**独缺 pr-review** | 缺口成立 |
| 需一并盘点其他入口 | `bin/` 共 **99** 个文件，**38 个超 40 行** | 盘点可行，但不宜一轮全迁 |

## 关键判断：不是所有「超阈值」都该迁

`bin/` 里有两类合理存在：

1. **dispatcher**（3 个）：`bin/issue-sync` 之类只做模块加载与路径解析，不含业务判断；
2. **自包含工具**（`check-*`、`test-all` 等）：它们本身就是那条工具的真源，不是某份
   `scripts/` 实现的投影。

所以「一行超过 40 就迁移」是错的判据。本轮采用可机检的中间判据：
**超阈值必须登记理由**（`bin-projections.yaml`），且**一旦变成投影必须删除条目** ——
既覆盖全部 99 个入口，又不会为了指标去搬不该搬的东西。

## 方案对比

1. **一次迁 38 个**：其中多数是自包含工具，硬迁会产生「影子实现」→ 否决。
2. **只迁 pr-review-guarded**：满足验收 1，但验收 2/3（全量盘点 + CI 覆盖）落空 → 不够。
3. **迁 pr-review-guarded + 注册表 + 门禁 + 清单 + 后续 raw 承接剩余 35 条**（本轮）→ 采用。

## Decision

- `bin/pr-review-guarded` 806 → 4 行 `exec` 投影；实现移到
  `scripts/worktree/pr-review-guarded`（只改 `ROOT_DIR` 的推导方式）。
- `scripts/bin-projections.yaml` 登记 38 个超阈值入口，分 `dispatcher` /
  `implementation-in-bin` 两类；后者挂 `followup: raw-20261111T125724Z`。
- `bin/check-bin-projection` 三条规则：未登记即失败、登记但文件已删即失败、
  登记但已降到阈值内即失败（强制删除过期豁免）。
- `scripts/bin-inventory.md` 列出全部 99 个入口与类别。
- 剩余 35 条 `implementation-in-bin` 用 `freely feedback` 另立 raw 承接，不假装完成。

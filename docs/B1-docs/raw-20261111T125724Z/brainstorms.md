# B1 Brainstorm — raw-20261111T125724Z（R32.5）

## 0. 立项与设计意图（已核实项目自身文档，非推测）

- `docs/system/workspace/scripts/README.md`：「`bin/`、`.githooks/` 是运行时投影位置，不是主定义源」；「投影层不应包含真实业务逻辑；真实实现必须回到 `workspace/scripts/**`」。
- `bin/check-bin-projection` 头注释定义三条机器可判定规则：① `bin/` 超过 `threshold_lines`(40) 的文件必须登记带 reason（coverage）；② 登记项文件必须存在（no stale entries）；③ 登记项一旦变成投影（≤ 阈值）必须删除条目（**no permanent exemptions — this is what makes the debt shrink**）。
- `docs/system/workspace/scripts/bin-inventory.md`：99 个入口 = 47 projection + 3 dispatcher + 35 implementation-in-bin + 14 leaf；35 条由本 raw 判定。
- 本 raw 的「修复方案」明确：**不搞一刀切**——自包含的 lint/聚合入口（`check-*`、`test-all`）保留在 `bin/`，并在注册表里标 `standalone-tool`、理由写清楚；判定应迁移者才做投影化，每批独立可合并、行为不变。

## 1. 关键约束：`standalone-tool` 不能变成永久豁免

`check-bin-projection` 的第三条规则（变投影就删条目）是**债务只会收缩**的保证。若引入 `standalone-tool` 后允许长期 >40 行且不受该规则约束，就与门禁设计意图冲突、属能力降级。

因此本轮分类落地的边界是：
- `standalone-tool` **只是分类标签 + 更具体的 reason 要求**；
- coverage / staleness / shrink 三条规则对它**同样生效**（不新增任何豁免）；
- lint 新增 class 白名单校验与「占位 reason」拒绝，属于**提高**门禁强度，不是放宽。

## 2. 35 条逐条判定

### 2.1 `standalone-tool`（22 条，保留在 bin/，理由逐条写明）

| 文件 | 行数 | 判定依据 |
|---|---|---|
| `bin/batch-closeout-raw-issues` | 48 | 只读诊断报告，不产生生命周期事实 |
| `bin/check-bin-projection` | 93 | 门禁 lint 自身，自包含无业务实现 |
| `bin/check-coordination-contract` | 82 | 契约 lint |
| `bin/check-cross-process-contract` | 123 | 契约 lint |
| `bin/check-db-writers` | 102 | 边界 lint |
| `bin/check-epics-map` | 143 | 文档一致性 lint |
| `bin/check-file-size` | 114 | 通用 lint |
| `bin/check-runtime-size` | 52 | 行数预算 lint |
| `bin/check-rust-toolchain` | 44 | 工具链探测 lint |
| `bin/check-skill-frontmatter` | 117 | skill 语料 lint |
| `bin/check-state-file-keys` | 168 | 状态键契约 lint |
| `bin/check-state-file-sources` | 74 | 状态协议迁移 lint |
| `bin/check-tauri-probe-host` | 46 | 探针宿主 lint |
| `bin/migrate-issue-phase-state` | 63 | one-shot 审计，明确不重写生命周期状态 |
| `bin/raw-issue-backfill-h1` | 165 | one-shot、dry-run-first 回填工具 |
| `bin/tauri-validate-probe-interactions` | 43 | 交互校验脚本 |
| `bin/test-all` | 135 | 聚合测试入口（本 raw 修复方案点名保留） |
| `bin/test-cache-hit` | 87 | 缓存命中率诊断工具 |
| `bin/issue-migrate-intake` | 58 | one-time 迁移脚本 |
| `bin/issue-sync-batch.py` | 144 | 已 DEPRECATED，仅保留参考、无调用方 |
| `bin/skill-route` | 59 | 自包含路由查询工具 |
| `bin/freely` | 43 | 命令分派入口，不含业务实现（与 3 个 dispatcher 同类但仅 43 行） |

### 2.2 仍为 `implementation-in-bin`（13 条，判定应迁移，分后续批次）

| 文件 | 行数 | 建议真源域 |
|---|---|---|
| `bin/agent-table-query` | 336 | `scripts/runtime/` 或 `scripts/agents/` |
| `bin/freely-package` | 270 | `scripts/packaging/` |
| `bin/deploy-skills` | 216 | `scripts/skills/` |
| `bin/freely-review` | 202 | `scripts/worktree/`（与已有 `pr-review-guarded` 同域） |
| `bin/test-pre-merge-selfhost` | 170 | `scripts/tests/` |
| `bin/raw-issue-pull` | 145 | `scripts/sync/`（注意 R33.11 刚修过它的 comments/终态逻辑，迁移必须行为不变） |
| `bin/issue-index` | 137 | `scripts/lifecycle/` |
| `bin/freely-cycle` | 129 | `scripts/runtime/` |
| `bin/cache-baseline` | 125 | `scripts/runtime/` |
| `bin/git-worktree-guard` | 111 | `scripts/worktree/` |
| `bin/freely-watchdog` | 88 | `scripts/runtime/` |
| `bin/pre-init-runtime` | 71 | `scripts/runtime/` |
| `bin/issue-sync-bootstrap` | 62 | `scripts/sync/` |

> 3 个 `dispatcher`（`bin/evidence`、`bin/issue-sync`、`bin/test-gate`）与 14 个 leaf 不在本轮 35 条判定范围内，保持原样。

## 3. 为何本轮只做分类、迁移另立 raw

本 raw 的修复方案要求「每批迁移独立可合并、行为不变」。35 条里 13 条真正迁移涉及 6 个不同域、其中 `raw-issue-pull` / `deploy-skills` 等刚在 R33.x 修过，混在一个 PR 里会放大回归面且违背「不夹带」。

**流程硬约束**：`pr-create-guarded` Step 0b 要求 raw `phase_state: absorbed`（必须先 `promote-finalize` 关掉 raw），所以**同一个 raw 无法跨多个 PR 保持 open**。因此 C-B/C-C/C-D 不能作为本 raw 的后续 children；按项目既有惯例「部分完成 → 另立新 raw」（R25、R28.5 等），C-A 合并后用 `./bin/freely feedback` 登记一条新 raw 承接 13 条迁移，再由它的 B1 按域拆批次。

- **C-A（本轮，唯一 candidate）**：注册表分类落地（`classes` + 35 条逐条 class/reason）+ lint 的 class 白名单与占位 reason 拒绝 + `bin-inventory.md` 同步 + AT。**不迁移任何实现**，门禁三条规则一条不放松。
- **后续**：13 条迁移按域分批，每批独立 PR、行为不变、改到 `scripts/runtime/` 的批次同轮补 `tests/unit/t-*.sh`（R27 契约）。

本 raw 的完成范围如实标注为「分类落地」，不谎称 13 条迁移已完成。

## 4. 证伪

- 「所有 >40 行文件都该投影化」→ 否：raw 修复方案明确点名 `check-*` / `test-all` 保留；把这些自包含 lint 硬搬进 `scripts/` 只会增加无意义投影种类。
- 「引入 standalone-tool 就是永久豁免」→ 否：三条门禁规则对它同样生效，仅增加标签与更严格 reason 校验（见 §1）。
- 「可以一个 PR 迁移完 13 条」→ 否：跨 6 个域且含刚修过的热路径，违背 raw 的「每批独立可合并」与 goal 的「不夹带」。

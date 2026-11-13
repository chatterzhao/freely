# bin/ 入口清单（投影层盘点）

- issue: raw-20261104T080200Z / #4175（R32）
- 规则：`bin/` 是投影层，业务实现属于 `docs/system/workspace/scripts/**`；超过 **40 行**的文件必须在 `bin-projections.yaml` 登记理由。
- 门禁：`bin/check-bin-projection`（0 通过 / 1 违规 / 2 注册表缺失）。
- 本次已迁移：`bin/pr-review-guarded`（806 行 → 4 行投影），实现移到 `scripts/worktree/pr-review-guarded`。

## 总览（99 个入口）

| 类别 | 数量 | 含义 |
|---|---|---|
| projection | 47 | `exec` 投影，真源在 `workspace/scripts/**` |
| dispatcher | 3 | 只做模块加载与路径解析 |
| standalone-tool | 22 | 自包含 lint / 聚合 / one-shot 工具，按 raw 修复方案保留在 `bin/`；**不是豁免**，coverage/staleness/shrink 三条门禁规则照常生效 |
| implementation-in-bin | 13 | 判定应迁移，按域分批投影化（C-B/C-C/C-D） |
| leaf | 14 | 未超阈值，无需登记 |

> 分类依据见 `docs/B1-docs/raw-20261111T125724Z/brainstorms.md` §2。`standalone-tool` 只是标签 + 具体 reason 要求，`bin/check-bin-projection` 对它同样要求「>40 行必须登记」「文件必须存在」「变成投影就删条目」。

## 分类清单（35 个，承接 issue `raw-20261111T125724Z`）

| 文件 | 行数 | class | 判定 |
|---|---|---|---|
| `bin/agent-table-query` | 336 | implementation-in-bin | business implementation still in bin/; migrate to scripts/agents or scripts/runtime in a later batch |
| `bin/freely-package` | 270 | implementation-in-bin | business implementation still in bin/; migrate to scripts/packaging in a later batch |
| `bin/deploy-skills` | 216 | implementation-in-bin | business implementation still in bin/; migrate to scripts/skills in a later batch |
| `bin/freely-review` | 202 | implementation-in-bin | business implementation still in bin/; migrate to scripts/worktree in a later batch |
| `bin/test-pre-merge-selfhost` | 170 | implementation-in-bin | business implementation still in bin/; migrate to scripts/tests in a later batch |
| `bin/check-state-file-keys` | 168 | standalone-tool | self-contained lint for the state-key contract |
| `bin/raw-issue-backfill-h1` | 165 | standalone-tool | one-shot dry-run-first H1 backfill utility |
| `bin/raw-issue-pull` | 145 | implementation-in-bin | business implementation still in bin/; migrate to scripts/sync in a later batch |
| `bin/issue-sync-batch.py` | 144 | standalone-tool | DEPRECATED reference copy with no callers; not a runtime entry |
| `bin/check-epics-map` | 143 | standalone-tool | self-contained lint validating epics-map.svg against docs/B2-docs |
| `bin/issue-index` | 137 | implementation-in-bin | business implementation still in bin/; migrate to scripts/lifecycle in a later batch |
| `bin/test-all` | 135 | standalone-tool | aggregate test runner; explicitly kept in bin/ by the raw's repair plan |
| `bin/freely-cycle` | 129 | implementation-in-bin | business implementation still in bin/; migrate to scripts/runtime in a later batch |
| `bin/cache-baseline` | 125 | implementation-in-bin | business implementation still in bin/; migrate to scripts/runtime in a later batch |
| `bin/check-cross-process-contract` | 123 | standalone-tool | self-contained lint for the Bash-Python data contract |
| `bin/check-skill-frontmatter` | 117 | standalone-tool | self-contained fail-closed lint over the skill corpus |
| `bin/check-file-size` | 114 | standalone-tool | self-contained generic line-count lint |
| `bin/git-worktree-guard` | 111 | implementation-in-bin | business implementation still in bin/; migrate to scripts/worktree in a later batch |
| `bin/check-db-writers` | 102 | standalone-tool | self-contained boundary lint for DB write ownership |
| `bin/check-bin-projection` | 93 | standalone-tool | self-contained lint for the projection registry itself; no business logic |
| `bin/freely-watchdog` | 88 | implementation-in-bin | business implementation still in bin/; migrate to scripts/runtime in a later batch |
| `bin/test-cache-hit` | 87 | standalone-tool | self-contained cache hit-rate diagnostic |
| `bin/check-coordination-contract` | 82 | standalone-tool | self-contained contract lint over contracts/coordination |
| `bin/check-state-file-sources` | 74 | standalone-tool | self-contained lint for the state-file protocol migration |
| `bin/pre-init-runtime` | 71 | implementation-in-bin | business implementation still in bin/; migrate to scripts/runtime in a later batch |
| `bin/migrate-issue-phase-state` | 63 | standalone-tool | one-shot audit that never rewrites lifecycle state |
| `bin/issue-sync-bootstrap` | 62 | implementation-in-bin | business implementation still in bin/; migrate to scripts/sync in a later batch |
| `bin/skill-route` | 59 | standalone-tool | self-contained skill alias/loop resolution query tool |
| `bin/issue-migrate-intake` | 58 | standalone-tool | one-time historical intake migration script |
| `bin/check-runtime-size` | 52 | standalone-tool | self-contained runtime size budget lint |
| `bin/batch-closeout-raw-issues` | 48 | standalone-tool | read-only closeout drift report; produces no lifecycle facts |
| `bin/check-tauri-probe-host` | 46 | standalone-tool | self-contained Tauri probe host lint |
| `bin/check-rust-toolchain` | 44 | standalone-tool | self-contained toolchain probe lint |
| `bin/freely` | 43 | standalone-tool | CLI dispatch entry point; contains no business implementation |
| `bin/tauri-validate-probe-interactions` | 43 | standalone-tool | self-contained probe interaction validator |

## dispatcher（3 个）

| 文件 | 行数 | 理由 |
|---|---|---|
| `bin/issue-sync` | 161 | loads modules and resolves paths; holds no domain logic |
| `bin/test-gate` | 129 | loads modules and resolves paths; holds no domain logic |
| `bin/evidence` | 48 | loads modules and resolves paths; holds no domain logic |

## 其余 14 个入口

| 文件 | 行数 | 类别 |
|---|---|---|
| `bin/wt-add` | 33 | leaf |
| `bin/wt-enter` | 33 | leaf |
| `bin/worktree-common.sh` | 19 | leaf |
| `bin/release-ai-auth-templates` | 18 | leaf |
| `bin/toml2env` | 12 | leaf |
| `bin/a2a-exit` | 11 | leaf |
| `bin/cargo-check-probe-bridge` | 9 | leaf |
| `bin/tauri-probe-dev` | 9 | leaf |
| `bin/gitee-issue` | 5 | leaf |
| `bin/governance-merge-gate` | 5 | leaf |
| `bin/a2a-report` | 4 | leaf |
| `bin/governance-closeout-gate` | 4 | leaf |
| `bin/harness-select` | 4 | leaf |
| `bin/harness-status` | 4 | leaf |

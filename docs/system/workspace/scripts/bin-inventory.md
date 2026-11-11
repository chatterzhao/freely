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
| implementation-in-bin | 35 | 实现仍在 `bin/`，由后续 raw 判定 |
| leaf | 14 | 未超阈值，无需豁免 |

## implementation-in-bin（35 个，承接 issue `raw-20261111T125724Z`）

| 文件 | 行数 | 处理方式 |
|---|---|---|
| `bin/agent-table-query` | 336 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/freely-package` | 270 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/deploy-skills` | 216 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/freely-review` | 202 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/test-pre-merge-selfhost` | 170 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-state-file-keys` | 168 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/raw-issue-backfill-h1` | 165 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/raw-issue-pull` | 145 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/issue-sync-batch.py` | 144 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-epics-map` | 143 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/issue-index` | 137 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/test-all` | 135 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/freely-cycle` | 129 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/cache-baseline` | 125 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-cross-process-contract` | 123 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-skill-frontmatter` | 117 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-file-size` | 114 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/git-worktree-guard` | 111 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-db-writers` | 102 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-bin-projection` | 93 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/freely-watchdog` | 88 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/test-cache-hit` | 87 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-coordination-contract` | 82 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-state-file-sources` | 74 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/pre-init-runtime` | 71 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/migrate-issue-phase-state` | 63 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/issue-sync-bootstrap` | 62 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/skill-route` | 59 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/issue-migrate-intake` | 58 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-runtime-size` | 52 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/batch-closeout-raw-issues` | 48 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-tauri-probe-host` | 46 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/check-rust-toolchain` | 44 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/freely` | 43 | implementation still lives in bin/; judged case by case in the follow-up |
| `bin/tauri-validate-probe-interactions` | 43 | implementation still lives in bin/; judged case by case in the follow-up |

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

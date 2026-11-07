# PRD: 门禁 fail-open 收敛为 fail-closed

- issue_id: I-20261103T132458Z-A
- source_raw: raw-20261103T132458Z
- workflow_kind: fix
- milestone: M-20261103T132458Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

让「环境异常」与「真实通过」不再共用退出码 0；统一 0=通过 / 1=不通过 / 2=环境不可用（按不通过处理）。R9/R10 的前置。

## 唯一改动范围

1. 6 个 `.githooks/` shim（`-x`→`-f`，末尾 `exit 0`→诊断 + `exit 2`）。
2. `docs/system/workspace/hooks/pre-commit.sh`（hooksPath、helper、门禁真身守卫、file-size 接线）。
3. `pr-create-guarded` 4 处 not-found skipping → `[ERROR]` + `exit 2`。
4. `checkpoint-guard` 默认 `FAIL_ON_REQUIRED=1`。
5. `check-file-size` 新增 `--staged-only` 增量模式 + 全量扫描覆盖无扩展名脚本。
6. 新增回归测试 `test-gate-fail-closed`。

## 不退化边界

- `.githooks/post-checkout` 逐字节不变（自包含实现，`git worktree add` 会触发）。
- 外部项目使用 installed freely hook 时的合法早退保留（无 `bin/worktree-common.sh` 属正常）。
- `pr-create-guarded` 「no raw key found in branch」正常路径仍继续。
- `check-file-size` 历史遗留超限文件不阻断未来提交（增量模式）。
- 不接线 `.githooks/bin/git`（独立基础设施改动）；R11/#4149、#4151 不夹带。

## 功能需求

- FR-1: shim 族 fail-closed、无需执行位。
- FR-2: pre-commit.sh 所有「拿不到依据」路径非零。
- FR-3: PR 门禁缺失即失败，不再 `[WARN] skipping`。
- FR-4: checkpoint-guard 默认严格。
- FR-5: check-file-size 有调用点、覆盖无扩展名真源、增量不阻断历史。
- FR-6: 真实工位 `git commit` 仍成功（不自锁）。

## 验收

AT-001 基线 RED 26 失败 / 2 既有能力 PASS → GREEN 28/28；真实 commit 冒烟 exit 0；14 个回归基线对比 0 新增失败（4 个预存红测试输出逐字节一致）。

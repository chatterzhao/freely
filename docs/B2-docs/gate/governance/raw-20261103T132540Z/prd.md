# PRD: 合并门禁读 verdict，评审判定不再默认通过

- issue_id: I-20261103T132540Z-A
- source_raw: raw-20261103T132540Z
- workflow_kind: fix
- milestone: M-20261103T132540Z-A
- story: gate/governance（复用既有 story，epics-map.svg 无需改动）

## 目标

让「评审通过」这件事第一次携带证据：合并侧读 review 文档里的 verdict，写侧不再把「无法判定」当 pass，审计侧不再因为 `completed` 就把 review 要求整体关掉。

## 改动范围（4 个文件 + 1 个测试）

1. 新增 `docs/system/workspace/scripts/worktree/review_verdict.py`：单一 verdict 解析真源（Python）。
2. 新增 `docs/system/workspace/scripts/worktree/review-verdict.sh`：bash wrapper，导出 `freely_parse_review_verdict` 与合并决策 `freely_review_verdict_check`。
3. `docs/system/workspace/scripts/worktree/pr-merge-guarded`：review 块由「查文件存在」改为「读内容 → 共用判定 → 非 pass 阻断并打印原因」。
4. `bin/pr-review-guarded`：默认值 `pass` → `needs_changes`；`--verdict` 覆盖只接受三值、必须带 `--reason` 且落痕进 review 文档；manual 模式拒绝覆盖。
5. `docs/system/workspace/scripts/quality/governance-merge-gate`：`phase == "completed"` 不再裸 `continue`，改为要求「与该 issue 绑定的 review 产物 + 声明 verdict=pass」；显式非 pass 不可被 completed 翻盘。
6. 新增 `docs/system/workspace/scripts/tests/test-verdict-contract`（AT-001）。

## 不退化边界

- 历史两种 verdict 写法（`- verdict: pass` 与 `- verdict: **pass**`）都必须解析成功；402 份真实 review 文档零不可判定。
- `pr-merge-guarded --dry-run` 仍不要求 review 文件。
- `completed` 的历史记账豁免保留：仍不强制 `verification_artifact_dir`，避免对大量历史缺失字段的 issue 立即自锁。
- 不改 `.githooks/`、`commit-msg.sh`、R8/R9/R9.5 的 fail-closed 语义。

## 功能需求

- FR-1: 读侧只认字面 `pass`；`fail` / `needs_changes` / 缺失 / 不可解析一律阻断并打印判定与原文 verdict 行。
- FR-2: 写侧「无法判定」落 `needs_changes`；`_review_verdict="pass"` 不再作为默认值出现。
- FR-3: 覆盖必须可解释：缺 `--reason` 直接 exit 2；reason 写入 review 文档（ACP 路径与文档生成路径都落痕）。
- FR-4: 审计侧对 `completed` 的 issue 仍要求 review 证据与 pass verdict。
- FR-5: 解析逻辑只有一份（脚本内不得出现第二份 verdict 正则）。

## 验收

AT-001 基线 RED（静态 18 项中 14 项 FAIL、behavior 因 helper 缺失中止）→ GREEN 13 ok / 0 failed；回归基线对比零新增失败；真实工位以 `verdict: fail` 探针验证阻断，再以真实 pass 完成受控合并。

---
schema_version: '1'
local_id: raw-20261107T090847Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261107T090847Z-A
platform_ids:
  github:
    issue_id: '4211'
    url: https://github.com/chatterzhao/freely/issues/4211
    synced_at: ''
  gitee:
    issue_id: IKTNCE
    url: https://gitee.com/zhaoquan/freely/issues/IKTNCE
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-07T09:08:47Z'
updated_at: '2026-11-07T09:48:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-07T09:50:00Z'
closeout_note: ''
---

# fix: governance-check 的 merge receipt 审计只认旧值且被 set -e 提前退出，第三层护栏失真

workflow_kind: fix

## 优先级

P1 — post-merge 审计层失真。`hooks/README.md` 宣称的第三层「`governance-check` post-merge audit」会把当前所有**合法**的 `pr-merge-guarded` merge commit 判为非法 receipt；同时由于脚本 `set -euo pipefail` 在更早的检查处提前退出，这条误报在真实运行中根本不出现，形成「既有假阳性又不生效」的双重失真。第一层提交期阻断由 #4147 / R9 接线补上，但第三层仍是坏的。

## 根因

`docs/system/workspace/scripts/quality/governance-check` 的 `audit_current_protected_branch_merge_receipt()`（`:340-386`）里：

```
case "$merge_path" in
  merge-guarded|merge-guarded-complete) ;;
  *) fail "protected branch '$branch' HEAD merge commit has unknown Freely-Merge-Path '$merge_path'" ;;
esac
```

只接受旧的 `merge-guarded*`。而当前受控合并由 `docs/system/workspace/scripts/worktree/pr-merge-guarded:296-307` 的 `render_merge_message()` 写入 `Freely-Merge-Path: pr-merge-guarded`（或 `pr-merge-guarded-complete`）；`docs/system/workspace/hooks/commit-msg.sh` 接受的也是 `pr-merge-guarded*`。三处契约不一致。

## 证据（2026-11-07 R9 评审期间实测）

- 在 develop HEAD `ba1a1ece8`（2 parents 的受保护 merge）上，`git log -1 --format=%B` 为
  `Freely-Merge-Path: pr-merge-guarded` / `Freely-Bypass-Mode: forbidden` / `Freely-Source-Branch: fix/...`，是 `pr-merge-guarded` 生成的合法 receipt。
- 单独抽取 `audit_current_protected_branch_merge_receipt()` 函数体在真实 develop 仓库执行（自包含 `fail()`、脱离脚本其余部分）：输出
  `[FAIL] protected branch 'develop' HEAD merge commit has unknown Freely-Merge-Path 'pr-merge-guarded'`，`PROBE_ERRORS=1`。即函数逻辑确凿地把合法 merge 判为非法。
- 但完整执行 `./bin/governance-check`（develop 上）输出只有 5 条预存 `[FAIL] missing file: ...` / 命名规范告警，**没有**该 receipt 诊断，也没有末尾的 `Governance check failed with N error(s)` 汇总行，退出码 1。说明脚本在到达 `:878 audit_current_protected_branch_merge_receipt` 之前就被 `set -e` 中断，审计层实际未运行。
- 全仓历史 receipt 取值统计（`git log --all --format=%B | grep '^Freely-Merge-Path:'`）：`merge-guarded` 1205 次、`merge-guarded-complete` 84 次、`merge-guarded-break-glass` 23 次、`pr-merge-guarded` 675 次、`pr-merge-guarded-complete` 8 次、另 1 条异常格式。两代取值都在历史里，不能简单只认新值或只认旧值。
- 现有 open issue 中只有 #4147（本轮 R9，commit-msg 接线）提到 `governance-check`/receipt，其验收标准是「自复查不再是唯一校验点」，并未覆盖这个 allowlist 不一致与提前退出问题。

## 影响

- 第三层护栏对 675+ 个合法的新式 merge 全部误报；若把提前退出修好，develop 每次 audit 都会红。
- 反过来，因为提前退出，任何**真正的** receipt 缺失/伪造也不会被这一层发现——审计形同虚设，与 README 宣称的三层强度不符。
- 与 #4147 叠加时容易误判：以为提交期接线完成后三层齐全，实际第三层仍是坏的。

## 修复方案

1. `governance-check` 的 `merge_path` allowlist 同时接受两代合法值：`merge-guarded|merge-guarded-complete|pr-merge-guarded|pr-merge-guarded-complete`（`break-glass` 走独立 ledger，另按既有语义处理，不要无差别放宽）。与 `commit-msg.sh` 的取值契约对齐，并写明「历史兼容」注释。
2. 修复 `set -e` 提前退出：把顶层检查链里导致非零返回的调用改为显式捕获（例如 `|| true` / 记录 errors），保证 `:878` 的 receipt 审计与末尾汇总**总会执行**；禁止用删除检查的方式绕过。
3. 补回归测试：①真实 develop 式 `pr-merge-guarded` merge → audit 不报 unknown；②历史 `merge-guarded` merge → 仍被接受；③缺 trailer / 伪造值 → 明确 fail；④完整 `governance-check` 在预存 `[FAIL]` 存在时仍跑完并输出汇总行。
4. 顺带核对 `protected_branch_merge_source_allowed()` 对 `test-pre-merge-*` 来源的判定与新式 source_branch 是否一致（本轮不做功能改动，只记录结论）。

## 明确不纳入（评审否决，禁止夹带）

- 不改 `pr-merge-guarded` 的 trailer 写入值（675+ 个历史 merge 已用 `pr-merge-guarded`，改写入会制造新的不一致）。
- 不改 `commit-msg.sh` 的 allowlist（#4147 / R9 刚接线并验证，禁止二次改动）。
- 不删除或削弱 `governance-check` 任何既有检查项；提前退出必须靠「让检查跑完」修复，不是跳过。
- 不重写 history / backfill ledger；不批量改写历史 merge commit。
- 与 #4151（测试证据链）区分：本缺陷是**审计真源逻辑 + 控制流**，不是测试未被 CI 执行。

## 验收标准

- GREEN：对真实 `pr-merge-guarded` 受保护 merge，audit 函数不报 unknown，且完整 `governance-check` 输出包含汇总行。
- GREEN：历史 `merge-guarded` 取值仍被接受（历史兼容）。
- GREEN：缺 trailer 或非法取值仍明确 fail，不受提前退出影响。
- GREEN：新增回归测试覆盖上述四类；`commit-msg.sh` 与 `pr-merge-guarded` 逐字节不变。

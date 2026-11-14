---
schema_version: '1'
local_id: raw-20261114T031043Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T031043Z-A
platform_ids:
  github:
    issue_id: '4521'
    url: https://github.com/chatterzhao/freely/issues/4521
    synced_at: ''
  gitee:
    issue_id: IKV9IH
    url: https://gitee.com/zhaoquan/freely/issues/IKV9IH
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-sync-modules/raw-20261114T031043Z/issues/I-20261114T031043Z-A.md
last_synced_comment_at:
  github: '2026-11-14T05:22:19Z'
  gitee: '2026-11-14T05:22:19Z'
hash: ''
created_at: '2026-11-14T03:10:43Z'
updated_at: '2026-11-14T05:22:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T031043Z-A
source_candidate: ''
completed_at: '2026-11-14T05:22:18Z'
closeout_note: ''
severity: P1
---

# fix: daemon 自动 batch 无 raw 范围，跨 raw 改文档并误建平台 issue

workflow_kind: fix

## fix: daemon 自动 batch 无 raw 范围，跨 raw 改文档并误建平台 issue

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T031043Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T03:10:43Z |
| updated | 2026-11-14T03:10:43Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T031043Z`。实现前请用 `wt-create --raw-key 20261114T031043Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

从任一工位执行任意 `./bin/freely ...` 命令时，runtime 会在 daemon 扫描前**无范围**跑一次 issue-sync batch：

```
# docs/system/workspace/scripts/runtime/freely:24146
t  local _sync_bin="$project/bin/issue-sync"
t  if [[ -x "$_sync_bin" ]]; then
t    log_info "running issue-sync batch before daemon scan"
t    bash "$_sync_bin" batch 2>&1 | while IFS= read -r _line; do
```

后果（R33.16 真机实测）：

1. **绕过 raw 范围**：不传 raw-key，batch 会遍历 `docs/B1-docs` 与 `docs/B2-docs` 下全部文档，处理**其它 raw 的 children**。
2. **绕过 governance-only lane**：它直接在工位（issue lane）里改 `docs/B2-docs/**` 的 90+ 个跨 raw 文档，随后 `pr-create-guarded` 的 GATE 1 必然判红——执行者要么回滚（丢数据），要么违规提交。
3. **有平台副作用**：对历史 raw 会 `create` 平台上不存在的 issue（实测新建了 #4516 / #4518 等），并把本地 `platform_ids` 写进工位文档；工位一旦被 wt-close 删除，这些映射在 develop 丢失，下次 batch 会重复创建。
4. **不可中断**：batch 在 `freely` 内部同步执行且不打印总量，用户看到的是「命令很慢 + 文档莫名变脏」。

## 设计意图（已核实）

- `docs/LAWS.md` / GATE 1：一个工位只处理一个 raw issue。
- `raw-20261103T091157Z`：跨 raw 的文档物化/回填必须走 **governance-only lane + `FREELY_SKIP_IBM_GATE`**。
- R33.18 已给 `issue-sync batch` 加了 `--raw-key` 范围，但 daemon 这条调用没有传。

## 期望

1. daemon 的 `issue-sync batch` **默认只处理当前工位所属的 raw**（从分支名或 `.freely/worktree.json` 解析 raw-key），不跨 raw。
2. 需要全量对齐时，必须显式走 governance-only lane（`FREELY_SKIP_IBM_GATE` + 单独 raw），并在 batch 输出里标注 lane。
3. 若确实无法解析 raw-key（例如主仓），daemon **不得**执行 batch，改为打印「全量同步需走 governance-only lane」并跳过。
4. batch 开始即打印 `scope=<raw-key|ALL>` 与候选总数，结束时打印 closed/created/updated/skipped 统计，避免黑箱。
5. AT：
   - 工位内 `freely` 触发的 auto-batch 只处理本 raw（负向控制：其它 raw 的文档零变更、adapter 零调用）；
   - 主仓 / develop 上 auto-batch 直接跳过并给出 governance lane 提示；
   - 显式全量 batch 只有带 governance lane 环境变量时才允许跨 raw。

## 边界

- 不放宽 GATE 1；不为「让流程走通」而关掉 daemon 的同步能力；
- 不改 `cmd_batch` 的收口判据（R33.18 已定）；
- 承认平台侧已被误建的历史 issue，但**不手工删除**，由其对应 raw 走正常收口。

### comment-20261114T052218Z
- source: system
- event: promote_finalized
- children: ["I-20261114T031043Z-A"]

拆解为以下任务:
1. [I-20261114T031043Z-A](will-be-updated)

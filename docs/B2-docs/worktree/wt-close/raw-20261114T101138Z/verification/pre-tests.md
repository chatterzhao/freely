# Pre-Tests: dropped 收口自动写关闭理由并防重新物化

- issue_id: I-20261114T101138Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: `close_dropped` 评论先于关闭；GitHub 以 `not planned` 关闭；Gitee 关闭带 `--comment`；评论失败不关任何平台；`close_issue` 扩展默认参数后既有 `close-raw`/`close-multi`/CLI `close` 行为不变；`pull_raw_issue` 全 CLOSED 副本返回 None；`wt-close --force --reason` 关单前本地瞬时 `phase_state=dropped` 且 `completed_at`/`closeout_note` 齐全、`validate()` 通过；Gitee 关闭理由不重复写两次
- acceptance_target: dropped 收口把关闭理由落盘到平台评论并以 not-planned 关闭，且不破坏既有关闭路径
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: 真实执行 adapter、wt-close 内嵌 Python 片段与 raw 元数据契约
- required_evidence: AT-001 GREEN 10/0；develop 基线 RED 1 ok / 9 failed；实现评审补测 RED 7 ok / 3 failed
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py
- expected_output: Ran 10 tests / OK
- expected_RED_output: AttributeError / TypeError（close_dropped 不存在或 close_issue 无 reason 参数）；补测后为 ModuleNotFoundError + 重复 comment 断言失败
- actual_RED_output: develop 基线无 close_dropped、无 `--reason`、无 dropped transition 片段（1 ok / 9 failed）；修复前实现对补测用例 7 ok / 3 failed，其中 `test_transition_snippet_writes_valid_dropped_state` 真实报 `ModuleNotFoundError: No module named 'raw_metadata_contract'`
- actual_output: Ran 10 tests / OK（10 ok, 0 failed）
- evidence_file: docs/B2-docs/worktree/wt-close/raw-20261114T101138Z/verification/test-evidence/AT-001-BASELINE-RED.log,AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1
- case_design: S1–S7 用 FakeHandler 记录每次平台调用顺序，断言 comment 先于 close、GitHub 传 `--reason not planned`、Gitee 传入 comment_body、评论失败时 `_dropped` 标记与无平台关闭、handler 默认参数不退化、discover 全 CLOSED 时 pull fail-closed；S8 断言 Gitee 不重复写 comment（其 close 命令已带 `--comment`）；S9 从 `wt-close` 抽取 `<<'PY'` 片段并断言不含未展开的 `"$PROJECT_ROOT`；S10 用 `new_raw_metadata` 造真实 proposed raw 文档，在子进程执行该片段，断言 `phase_state=dropped`、`completed_at`、`closeout_note` 齐全且 `validate()` 通过。
- red_how: fix RED — ① develop 基线用 `FREELY_PA_PATH`/`FREELY_WT_CLOSE_PATH` 指向 `git show develop:...` 导出物跑同一 AT；② 实现评审补测后在修复前实现上重跑同一 AT，制造可复现的三条失败。

## 实现评审补记（2026-11-14T12:27Z）

首版 AT 只覆盖 adapter 层，7/0「绿」不能证明功能可用。补测后暴露三项实现问题，均已在同一 raw scope 内修复、不新开 issue：

| # | 问题 | 证据 | 修复 |
|---|---|---|---|
| 1 | `wt-close` 的 `<<'PY'` heredoc 内写 `"$PROJECT_ROOT/..."`，单引号 heredoc 不展开 shell 变量 → `ModuleNotFoundError`，`--force` dropped 收口第一步即失败 | AT-001-RED.log `test_transition_snippet_writes_valid_dropped_state` 真实 traceback | 项目根改由 `argv[4]` 传入，`sys.path.insert(0, sys.argv[4] + "/...")` |
| 2 | `close_dropped` Step A 对双平台 `add_comment`、Step B 又给 Gitee `close --comment`，关闭理由重复写两次 | AT-001-RED.log `test_gitee_closing_note_written_once` | 新增 `_CLOSE_WITH_COMMENT_PLATFORMS`，Step A 只对不能随关闭携带评论的平台写 |
| 3 | 失败标记未断言；原 `test_comment_failure_blocks_close` 依赖 Gitee 评论失败，与修复后的分流不匹配 | 补全断言 | 改由 GitHub 的 add_comment 作为 fail-atomic 检查点，并断言 `_dropped` 标记传到 CLI |

不退化边界不变：不新造 flag、不走正常 close 分支、不写 `phase/dropped` 标签、不改 `runtime/freely`、不改 `validate()`/GATE 1。

## Unit

- acceptance_target: close_dropped / handler 签名 / pull guard / wt-close transition 片段
- testing_layer: unit
- target_environment: fix/raw-20261114T101138Z-dropped-closeout
- required_evidence: AT-001 S1–S10
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py

## Integration

- acceptance_target: 既有 adapter / wt-close 测试不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all 相关用例全绿（test-platform-adapter-raw-identity / test-command-lifecycle-raw-metadata / test-issue-sync-close-linked / test-wt-close-dryrun-safety / test-wt-close-dropped-closeout）
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End

- acceptance_target: dropped 收口在真实工位按 --force --reason 跑通，平台评论 + not-planned 关闭落地
- testing_layer: end-to-end
- target_environment: 下一轮开工或独立验证工位
- required_evidence: 对一个 proposed raw 执行 `freely wt-close --raw-key <key> --force --discard-unmerged --reason "违规绕过门禁中，理由充分，是：<业务理由>"`，确认平台出现关闭评论且 issue 以 not planned 关闭
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮开工前用真实 raw 验证一次

## GREEN 验证（test-pre-merge 工位，2026-11-14T12:59Z）

- dev 提交同步方式：`git -C <test-pre-merge> merge --no-edit fix/raw-20261114T101138Z-dropped-closeout`（fast-forward），dev/test 同为 `764e29df1`，两边 `git status` 干净。
- `./bin/freely test-gate run --worktree <test-pre-merge> --command "bin/test-all --ci"` → `rc=0`、`SUMMARY: 41 ok, 0 failed, known-broken=590`。
- `.freely/run/test-gate.env`：`TEST_STATUS=completed`、`LAST_TESTED_COMMIT=764e29df159296a4db703af6fc8f19c9b2f50a20`、`EVIDENCE_HEAD` 同值；证据日志 `.freely/run/test-evidence.log`。
- `bin/pretests-retirement-gate --project <dev> --worktree-path <test>` → rc=0；`bin/governance-merge-gate --range develop..HEAD` → rc=0（一条顺序警告已在 code-review 如实登记）。

## Real-Environment

- real_environment_status: pass
- real_environment_reason: AT S1–S8 以 FakeHandler 验证 close_dropped 的评论顺序、GitHub not-planned、Gitee `--comment` 且不重复、评论失败不关任何平台；S10 用真实 `raw_metadata_contract.new_raw_metadata` / `write_issue` / `validate()` 在子进程执行 wt-close 内嵌片段，确认 dropped 终态可落盘；`pull_raw_issue` 全 CLOSED 副本 fail-closed 已断言。真实平台的关闭评论/关闭动作仍由 `wt-close --force` 编排，待下一轮真实 raw 端到端验证（对应上一节 End-to-End）。

## 副本一致性门禁（pr-create Step 0b）解除阻塞 — 2026-11-14T13:50Z

`pr-create-guarded` 首次执行时 Step 0b 返回 `block`，两个 fact 都不是本 issue 的实现问题，而是归一化链路自身失效：

| fact | 根因 |
|---|---|
| `github / ambiguous: 3 matches` | `_resolve_raw_identity()` 只认标题前缀 `[RAW-<key>]`；GitHub #4653 标题缺前缀，回退到 #4654/#4655 共 3 个 body 匹配 |
| `local / content_diverged` | ① `raw_reconciliation._COMMENT_BLOCK` 以「下一个 1–4 级标题」切块，而镜像评论正文本身以 `## 开头`，块被截断成空、正文残留进 body；② `_scan_state_record_sync()` 只写 `mtime`/`synced_at` 从不写 `hash`，而 `_changed_since_last_sync()` 只读 `hash` → `issue-sync update` 对所有 issue 恒为 no-op，平台标题/正文永远无法归一 |

### 实现修复（4 处，均带基线红）

- `bin/issue-sync.d/lib-state.sh`：`_scan_state_record_sync` 记录 `hash`；历史条目（有 `synced_at` 无 `hash`）视为已变更，使一次普通同步即可修复；无任何记录的首次同步仍判 unchanged，保留「初始批量不刷屏」语义。
- `bin/issue-sync.d/cmd-update.sh`：移除批量 dedup。`update` 是操作者显式单条命令，意图即变更；`scan`/`batch` 仍走变更检测。
- `docs/system/workspace/scripts/lifecycle/raw_reconciliation.py`：`_COMMENT_BLOCK` 块边界改为「下一个 comment/resolution 标记」，镜像评论正文以 `##` 开头也能被完整归入评论、并从 body 中剔除。
- `docs/system/workspace/scripts/sync/issue_create_contract.py`：新增 `strip_local_h1()`，正文投影不再重复输出本地 `# 标题`（平台侧已由 `## <title>` + 元数据表承载；真实平台正文如 #4654 亦无 H1）。

### 证据

- 新增 AT `docs/system/workspace/scripts/tests/test-issue-sync-update-not-noop.py`：基线 RED 10 ok / 6 failed（`AT-002-BASELINE-RED.log`），修复前 RED 7 ok / 5 failed（`AT-002-RED.log`），GREEN 16 ok / 0 failed（`AT-002-GREEN.log`）。
- 扩展 `test-raw-reconciliation.py`：新增「镜像评论以标题开头」用例，RED 1 failed（`AT-003-RED.log`），GREEN 4/4 OK（`AT-003-GREEN.log`）。
- 回归：`test-issue-sync-modules.py` 35 ok / 0 failed（含「issue-sync 与 contract 渲染同一 body」）。

### 平台侧归一（全部走封装命令，无手工 gh/gitee）

1. `freely feedback edit --raw-key 20261114T101138Z --title "fix: dropped 收口应自动写关闭理由并防重新物化"` → 两平台标题归一为 `[RAW-20261114T101138Z] …`（命令内部走 `canonical_raw_title()`）。
2. `freely issue-sync update raw-20261114T101138Z` → 两平台标题/正文/标签按同一投影重写。
3. 本地 `issue.md` 内嵌元数据表由 `proposed`/`none` 校正为当前 frontmatter（`absorbed` + `canonical_issue_path`），属派生快照对齐。
4. 最终 `raw-reconciliation-gate --require-local` → `ok=true, decision=allow`，`diagnostics=[]`、`degraded=[]`。

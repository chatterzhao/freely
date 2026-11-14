# B1 Brainstorm — raw-20261114T101138Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 契约: `raw_metadata_contract.py:258-266`「`elif event == "dropped": if current["phase_state"] != "proposed": raise ...; reason = ...; if not reason: raise "dropped requires reason"; current["phase_state"]="dropped"; current["completed_at"]=at; current["closeout_note"]=reason`」；`:194-196`「`if phase == "dropped": if not completed_at or not closeout_note: raise "dropped requires completed_at and closeout_note"`」；`:272` `platform_closed` 要求 phase ∈ {absorbed, dropped}。
  - 骨架（FORCE 已满足）: `wt-close:1279` dirty 检查 `FORCE != true`、`:569` phase 检查 `FORCE == false`、`:986` platform_state 检查 `FORCE != true`、`:1008` `--force` 分支内 `_close_issue_platforms_readonly` 已关平台、`:1338` `--discard-unmerged` 已 `-D` 删分支。
  - 缺口: `platform-adapter.py:329` GitHub `close_issue` 只 `gh issue close`（无 `--reason`）、`:671` Gitee `close_issue` 无 `--comment`（但 `gitee-issue.py:355` `cmd_close --comment` 能力存在）；`add_comment` 在 `:1000` 存在但 `close-raw` 路径不调；`wt-create:448` 终态保护依赖本地文件存在；`platform-adapter.py:1420 pull_raw_issue` 不检查 replica state。
  - 设计文档: `freely-doc-B1_IBM-execution/SKILL.md:47`「标记 dropped……直接终止 B1_IBM 流程」；`LAWS.md:304` `FREELY_SKIP_IBM_GATE` 仅限 document/cleanup/format；`platform-adapter.py:1491`「platform `phase/*` label is a CREATION-TIME snapshot」。
  - 既有验收测试: `test-command-lifecycle-raw-metadata.py:315-330`（drop 与 platform_closed 是两次独立合法转换）、`test-postmerge-commit-guard.py`、`test-issue-sync-close-linked.py`。
- 判定（五分类）: **实现未完成 + 实现偏差**。契约层两段 transition 本就正确（`#4/#5` 是命令层没接线）；`--force` 骨架本就满足 dropped 收口（前两次 B1 修正里的「新 flag / 不 commit / 正常 close 分支」是**基于局部得出的过度设计，已作废**）；`stateReason=COMPLETED` 属实现偏差。**不是设计错、不是 bug**（契约与骨架都在）。
- 与既有断言的冲突: 无。扩展 `close_issue` 用**默认参数**保持所有既有调用零改动；不动 `RAW_METADATA_FIELDS`、不动 GATE 1、不动 `validate()`。
- 影响面: `platform-adapter.py`、`wt-close`、新增 AT、`bin/test-all`、`projection.lock`；不改 runtime/freely（27158 预算）、不改 `freely comment`（#4654 独立）、不改 wt-create 的既有终态保护逻辑（只加全 CLOSED 副本的前置 fail-closed）。

### 0.1 全局适配反思（四问）

1. 类别：流程能力（dropped 收口命令），不是副本传播、不是实现 bug 修复、不是治理元数据迁移。
2. 职责边界：`raw_metadata_contract.transition` 拥有状态合法性；`issue-sync`/adapter 是唯一平台写通道；`wt-close` 拥有工位/分支清理。本轮只在 `wt-close --force` 分支**编排**三者，不新开通道（避免 R33.12 的「第二套 linked 收口」教训）。
3. 结构性冲突：若新造 `--drop` flag 或走正常 close 分支 → 与 FORCE 骨架重复且逼用户先 commit（反设计）。**已作废**。若给平台写 `phase/dropped` 标签 → 第二真相源（L0 Q4），已否决。
4. 门禁失配：`--force` 本就跳过 dirty/phase/platform_state 三检查，dropped 走它**不存在失配**；`governance-merge-gate` 管的是 PR/diff，dropped 不产生 PR，不在其测量面内。不改门禁。

## 1. P0 关键词广搜与多文档交叉（按 B0 要求）

| 组 | 关键词 | 命中 | 判定 |
|---|---|---|---|
| A | `--force` / `--discard-unmerged` / FORCE 条件 | `wt-close` 全部 8 处 FORCE 分支 | 当前生效实现，骨架已满足 |
| B | `dropped` / `transition("dropped")` / `closeout_note` | `raw_metadata_contract.py`、8 份历史 B1、`test-command-lifecycle-raw-metadata.py` | 契约层正确；历史 B1 的 `closeout_note='平台 issue 已关闭…'` 是 batch 收口残留，非 dropped 理由 |
| C | `stateReason` / `not planned` / `--reason` / `close --comment` | GitHub handler `:329`、Gitee `cmd_close:355` | 能力存在但未接 |
| D | `--state all` / `search_raw_issue` / `pull_raw_issue` / `materialize` | `platform-adapter.py:365/703/1420`、`wt-create:534` | 物化入口需加 CLOSED fail-closed |
| E | `governance-merge-gate` / `FREELY_SKIP_IBM_GATE` / PR | gate `:1108`、`pr-create-guarded:133` | dropped 不产生 PR，无关 |
| F | 历史 dropped 完整流程 | `raw-20260409T171500Z`（narrow followthrough owner + guarded merge） | **局部/过期**：其 `open_questions` 自留「Should future dropped research packets always materialize a narrow followthrough owner?」未定论 |
| G | 本会话三条收敛评论（#4653 平台评论 2 条） | GitHub #4653 comments | 最终权威：复用 FORCE 骨架 |

**交叉比对结论**：契约（B）与骨架（A）已存在；缺的是把 C 的 comment/reason 接进 A 的 `--force` 路径，并补 D 的防重新物化。历史 F 不能当规范。

## 2. 现状矩阵（最终收敛版）

| 诉求 | 现状 | 本轮动作 |
|---|---|---|
| 不检查提交与否 | dirty 检查被 FORCE 跳过 | 不动 |
| 不拦 dropped 的 phase | phase 检查被 FORCE 跳过 | 不动 |
| 关平台 / 删工位 / 删分支 | `_close_issue_platforms_readonly` + `-D` 已有 | 不动骨架 |
| 本地瞬时合法终态 | 无（我上次手工只改 phase_state） | **新增**：`transition("dropped", reason=...)` |
| 自动写关闭理由到平台 | 无（靠手工 `freely comment`） | **新增**：adapter `close-dropped` 先写评论再关 |
| `stateReason=NOT_PLANNED` | `COMPLETED` | **修**：GitHub `--reason "not planned"`、Gitee `--comment` |
| 失败原子 | 无 | **新增**：评论失败不关平台、关平台失败不删工位 |
| 防重新物化 | 无（本地文档抹除后保护失效） | **新增**：`pull_raw_issue` 全 CLOSED 副本 fail-closed |
| dropped 标签 / 新 flag / 正常 close 分支 / 不 commit 约束 / `-d` 替代 `-D` | — | **明确不做**（前两次修正的过度设计，作废） |

## 3. 方案（唯一，按 #4653 第 2 条评论收敛）

1. **adapter 新增 `close-dropped` 动作**：`close_dropped(raw_key, platform_ids, comment_body)` —
   - 对每个配置平台先 `add_comment`（`--force` 时 issue 仍 OPEN，可写）；任一平台评论失败 → 整体失败、**不关任何平台**；
   - 全部评论成功 → 逐平台 `close_issue` 带 `close_reason="not planned"`（GitHub `gh issue close --reason`；Gitee `cmd_close --comment` 复用 `--comment` 能力）；
   - 扩展 `close_issue` / close handler 用**默认参数**（`close_reason=""`, `comment_body=""`），所有既有调用零改动；
   - 返回逐平台结果 + 聚合退出码。
2. **`wt-close --force` 分支编排**（不改骨架，只在 `:1008` 关平台前插入）：
   - 调 `transition_issue(issue_file, "dropped", reason=<FORCE_REASON 的业务理由>, at=<now>)` 写瞬时本地状态（`phase_state`+`completed_at`+`closeout_note`），**不 commit**（工位随后删除）；
   - 组装关闭评论 = `closeout_note` + 工位内 B1 研究（`brainstorms.md`/`candidates.md`，未提交也读得到）；
   - 调 `close-dropped`；失败则 `exit 1`（**不删工位**）；
   - 成功才继续既有删工位/分支流程。
3. **防重新物化**：`pull_raw_issue` 内，若所有 `readable` replica 的 `get_issue_state` 均为 `closed` → 返回 `None` 并打印带「已关闭/关闭理由见平台评论」的 fail-closed 错误；`wt-create --reopen` 透传允许显式重开（必须带新理由）。`search_raw_issue` 的 `--state all` 不变（副本发现）。加 AT 钉住不进入物化路径。
4. **不做 PR/review/merge**；B1 研究与候选留平台时间线，本地零痕迹、develop 零污染。

## 4. 证伪

- 「该修 `wt-close:571` 让 dropped 走正常收口」→ 否：dropped 走 FORCE 路径，正常路径的 phase 检查本就不参与；修它属可选，非本轮必需（#4653 评论已降级）。
- 「给平台加 `phase/dropped` 标签更直观」→ 否：`platform-adapter.py:1491` 明确标签是创建时快照，写它会造第二真相源。
- 「先关平台再补评论也一样」→ 否：`add_comment` 对 CLOSED issue 返回 `blocked`（`:1008`），顺序必须「评论→关平台」；且这正是失败原子的落点。
- 「dropped 研究必须不 commit」→ 否：FORCE 跳过 dirty 检查，提交与否都能收口；`--discard-unmerged` 处理已提交情形，无需约束。

## 5. 边界

- 不改 `RAW_METADATA_FIELDS` / `validate()` / GATE 1 / `freely comment`(#4654) / runtime 行数预算；
- 不加 dropped 平台标签、不新造 flag、不要求先手动 `issue-sync drop`；
- 不把 B1 研究合进 develop、不追溯重开 #4574；
- 不手工 `gh`/`gitee` 直连关单（仍走 adapter 唯一通道）；
- `issue-sync drop` 本轮**不新增**（`transition("dropped")` 由 wt-close 内部直接复用，避免新增用户必须执行的 CLI 步骤）。

## 6.1 AT 落地与结果（GREEN）

- 新增 `docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py`（已登记入 `bin/test-all` CORE/CI_CORE）。
- 覆盖：`close_dropped` 评论先于关闭、GitHub 用 `--reason not planned` 关闭、Gitee 关闭带 `--comment`、评论失败不关任何平台；handler 签名向后兼容（`close_issue` 默认参数不影响既有调用）；`pull_raw_issue` 全 CLOSED 副本 fail-closed。
- 运行结果：**7/7 OK**。回归：`test-platform-adapter-raw-identity`、`test-command-lifecycle-raw-metadata`、`test-issue-sync-close-linked`、`test-wt-close-dryrun-safety` 全绿。
- `wt-close` 的 `--force` 分支编排已落地（`transition("dropped")` 瞬时本地态 → 组装关闭评论 → `close-dropped`），并加 `--dry-run` 守卫；`bash -n` 通过。

## 6. 自指防护（B0）

本 raw 是「修复 dropped 收口命令的实现」，不是「被 P0 评审后要 dropped 的功能」。P0 结论：**继续**。依据：6 条缺口经源码逐条核实、无既有 issue 覆盖（`065554Z` 只做未合并提交分诊、`031605Z` 只做 B0 审计、`#4652` 关键词广搜、`#4654` comment 的 PROJECT_ROOT bug、历史 `20260409T171500Z` 局部过期）。不得因「研究里看到很多 dropped 历史文档」误判 dropped。

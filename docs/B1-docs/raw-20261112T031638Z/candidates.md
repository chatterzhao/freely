---
candidate_id: C-20261112T031638Z-A
status: promoted
source_raw: raw-20261112T031638Z
created_at: 2026-11-12
milestone: M-20261112T031638Z-A
---

# Candidates

被否决方案见 brainstorms.md §3。两个 candidate 独立、可分别回滚，同一 milestone / 同一 PR。

## C-20261112T031638Z-A: 指引文案全域去幽灵名 + 补必填 --kind

- candidate_format_version: v2
- title: 把「零幽灵 skill 名」的扫描域从生成器/模板扩到全部活代码与文档，并把必填 `--kind` 补进所有 wt-create 指引
- status: promoted
- decision_reason: R33 的验收只覆盖生成器与模板，本轮普查在 `bin/issue-sync`、`pretests-gate`、`wt-close`、`runtime/freely`（5 处）、hooks 模板、2 份文档里仍找到幽灵名或缺 `--kind` 的指引；根因是扫描域定义太窄而非替换不彻底。同时证伪 raw 的「--skill 已废弃」说法——`--skill` 仍是合法可选覆盖参数，真正必填的是 `--kind`，因此修法是补 `--kind` 而非删 `--skill`。死备份 `.bak.py` 与两处测试 fixture 明确排除并写明理由，避免过度扩大改动面。
- next_action: AT-001（全域静态扫描 + 白名单 + 真实触发 guard 的行为断言 + 反向断言）→ develop `91473740c` 基线 RED → 修文案 → GREEN → 因触及 `runtime/freely` 同轮新增 `tests/unit/t-*.sh` 满足 Step 2.5 → PR。
- revisit_trigger: 新增任何面向用户的 wt-create / skill 指引载体（新命令、新 hook 模板、新文档）时，必须纳入 AT 扫描域；`--kind` 的取值集合变化时同步更新指引常量。
- acceptance_criteria:
  - RED：develop `91473740c` 基线 + 最终版 AT-001 → 全域扫描判红（列出全部残留位置），`--kind` 缺失断言判红，`test-wt-close-protected-branch-guard` 的反向断言判红。
  - GREEN：`bin/issue-sync` 的 protected guard 文案只引用真实 skill `freely-workflow-guarded-execution`，且 workflow 第 2 步含 `--source platform --kind <fix|feature|hotfix>`。
  - GREEN：`pretests-gate:570`、`wt-close:1155/1159/1163`、`hooks/reference-transaction.sh:118`、`pr-create-guarded:158` 注释、`AGENTS.md.example:146`、`three-loop-capability-lifecycle.md:206/359`、`runtime/freely:1110/10771/11361/11407/13430` 全部修正；`reference-transaction.sh` 不再出现两个完全相同的重复选项。
  - GREEN：AT-001 全域扫描 0 命中（白名单外），白名单逐条含理由；`commands.md` 保持不改（`--skill` 未废弃）。
  - GREEN：`test-wt-close-protected-branch-guard` 的 Test 6 改为**反向断言**（guard 不得含幽灵名、必须含真实 skill 名），且该测试整体 PASS。
  - GREEN：因触及 `docs/system/workspace/scripts/runtime/freely`，同轮新增 `docs/system/workspace/scripts/tests/unit/t-*.sh` 函数级单测，Step 2.5 判 pass。
  - 不退化：不删任何 guard、不放宽任何门禁判据、不改 `--skill` 的解析逻辑、不动 `.bak.py` 与两处 fixture；其余既有 AT 全绿；`check-runtime-size` / `check-bin-projection` / `check-epics-map` 仍 ok。
- promotion_gate: AT-001 RED → GREEN + Step 2.5 pass（runtime 改动带 unit test）+ 三门禁全过 + 既有 AT 全绿
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 全仓 grep 普查逐条定性 14 类命中；实测 `wt-create:22/109` 与 `commands.md:75/87` 证伪「--skill 已废弃」；实测 `bin/freely-package:188` 与零引用证伪 `.bak.py` 为活代码；本轮 wt-create 输出当场复现全部文案缺陷；四个方案逐一评估并否决 alias 造名与删提示两类方向性错误。
  - verdict: pass
- promoted_issue_id: I-20261112T031638Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/issues/I-20261112T031638Z-A.md
- milestone: M-20261112T031638Z-A
- session_refs: []

## C-20261112T031638Z-B: raw-issue-pull 显式传 --project 消除 protected-root 噪音

- candidate_format_version: v2
- title: `raw-issue-pull` 调 `issue-sync create` 时显式传 `--project <工位根>`，让分支判定基于调用方工位而非脚本物理位置
- status: promoted
- decision_reason: 逐层核实链路后确认根因是 ROOT_DIR 从脚本位置推导（`raw-issue-pull:53` → `issue-sync:36`），而 `wt-create:1002` 已 `cd` 进 dev 工位，导致必然撞主仓 develop guard。后果不止刷屏——`issue-sync create` 失败意味着 platform title 归一化与 platform_ids 补全被跳过，属真实功能缺失。`issue-sync:116` 注释本身就指明了正解（`--project`），只是调用方没照做。一处传参即可修好，不改任何 guard 判据。
- next_action: AT-002（静态断言传参 + 真实新建一次 fix 工位的行为断言）→ develop 基线 RED → 修传参 → GREEN（真实 wt-create 输出无 ERROR/WARN）→ PR。
- revisit_trigger: `raw-issue-pull` 的 ROOT_DIR 推导方式变化、或 `issue-sync` 的 `--project` 语义变化时，必须重跑 AT-002 的行为断言。
- acceptance_criteria:
  - RED：develop `91473740c` 基线上真实执行 `wt-create --source platform --kind fix`，输出含 `[ERROR] issue-sync refuses to run on protected branch: develop` 与 `[WARN] raw-issue-pull: issue-sync create failed`。
  - GREEN：`bin/raw-issue-pull` 调 `issue-sync create` 时显式传 `--project`，指向调用方所在工位根（由 `$(pwd)` 或 target 推导），不再依赖脚本物理位置。
  - GREEN：真实新建一次 fix 工位，输出**不含** `issue-sync refuses to run on protected branch`、**不含** `issue-sync create failed`，且 raw issue 正常物化。
  - GREEN：`issue-sync` 的 protected guard 本身**未被削弱**——在主仓 develop 上直接调 `issue-sync create` 仍必须 exit 1。
  - 不退化：不改 `issue-sync` 的 ROOT_DIR 默认推导、不改 `wt-create` 的 cd 逻辑、不放宽 guard；`raw-issue-pull` 的 exit 0/3/1 语义与 STDOUT 单 JSON 契约保持不变。
- promotion_gate: AT-002 RED → GREEN（真实 wt-create 自证）+ guard 未被削弱的反向验证 + 三门禁全过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐层读 wt-create:1002/519-526 → raw-issue-pull:53/133 → issue-sync:36/117 确认 ROOT_DIR 链路；本轮 wt-create 输出即为 RED 证据；四个方案评估后否决改 ROOT_DIR 默认值（blast radius 覆盖 14 个模块）、跳过 create（掩盖功能缺口）、降级 guard（削弱门禁）。
  - verdict: pass
- promoted_issue_id: I-20261112T031638Z-B
- promoted_issue_path: docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/issues/I-20261112T031638Z-B.md
- milestone: M-20261112T031638Z-A
- session_refs: []
# PRD: 修复 chat help 错误信息 shell 引号嵌套

- issue_id: I-20260720T023136Z-A

## Goal
让 `docs/system/workspace/scripts/runtime/freely` chat 命令在本地 raw issue 创建被禁用时输出的错误提示完整可读：不再出现 `line 6700: 描述: No such file or directory`，`<描述>`/`<详细描述>` 作为字面量占位符展示。

## Why Now
该 log_error 在每次 worker chat 触发本地 raw issue 创建路径时都会崩溃输出，用户（含 agent）看不到完整的 `freely feedback` / `freely wt-create` 使用指引，直接损害 chat intake 可用性。

## Product Surface
- `docs/system/workspace/scripts/runtime/freely` L6700 log_error 字符串字面量。
- 不涉及其他命令、不涉及运行时逻辑、不涉及文档。

## Non-Goals
- 不扫描、不改写其他 log_error 消息（包括 L15388/L15687 提示文本）。
- 不改 log_error 函数签名或调用约定。
- 不新增帮助命令或文档文件。

## Non-Negotiables
- bash 语法必须通过 `bash -n`。
- 渲染后 `<描述>`/`<详细描述>` 必须是字面量，不能被解释为重定向。
- 中文文本与消息内的双引号必须原样保留。
- 不改变 chat 命令本身的执行语义。

## Context Pack
- 复现：`bash -c 'log_error(){ echo "$*"; }; log_error "[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>""'` → `bash: 描述: No such file or directory`，EXIT=1。
- 修复验证：`log_error '[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"'` → 完整文本输出，EXIT=0。
- 相关代码：`docs/system/workspace/scripts/runtime/freely` 6697-6701（chat 命令 error branch）。

## Decomposition Tree
1. 修改 L6700 字符串：外层双引号改为单引号。
2. `bash -n` 语法验证。
3. 模拟执行 log_error 行，确认无重定向报错且文本完整。
4. grep 确认该字符串不再含裸 `<`/`>`。

## Prototype Path
无独立原型——单字符串修复，直接以 shell 模拟执行 + bash -n 作为最小验证。

## Eval Plan
- environment：feature worktree（dev） + test-pre-merge-*（GREEN）。
- evidence：`bash -n` 通过 + 模拟 log_error 输出无 `No such file` + grep 确认无裸尖括号。
- failure signal：`bash -n` 报错、输出含 `No such file`、中文被破坏。
- failure handling：回到 dev worktree 修正字符串，重新 RED→GREEN。
- 层级说明：
  - unit：对 log_error 行的 bash 模拟执行（覆盖脚本语法与字面量语义）。
  - integration / end-to-end：本 issue 为单个字符串字面量修复，不触达跨模块/用户流程行为，标记 not_applicable（change_not_touching_this_layer）并给出 replacement_evidence（bash -n + 模拟执行即覆盖语法与语义面）。
  - real-environment：不需要真实环境测试（not applicable，protected/纯静态字符串面）。

## Execution Slices
- slice-1：编辑 L6700 字符串为单引号包裹。
- slice-2：bash -n 验证。
- slice-3：模拟执行 + grep 证据采集。

## Revisit Triggers
- 若未来 chat help 消息重新引入需要插值变量或嵌套引号的内容，需重审引号策略。
- 若 log_error 签名变化，需回归本条消息。

## Dev-Loop Handoff
- 实现环按 pre-tests.md 的 AT-001~AT-003 逐条执行；先 RED（复现 `No such file`），后 GREEN。
- 最小引用：`docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/pre-tests.md`。

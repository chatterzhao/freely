# B1 Brainstorm — raw-20261112T131150Z

## 1. 触发场景（真机，develop 8ad2c2a83）

R33.6 / #4310 收口时按标准链路先跑 \`wt-close --raw-key 20261112T031638Z --dry-run\` 做预演，
输出里 \`git worktree remove\` / \`git branch -d\` 都带 \`[DRY-RUN]\` 前缀，看起来无害；
但紧接着出现：

    wt-close: cleaning up companion test-pre-merge: test-pre-merge-20261112T031638Z-...
    Deleted branch test-pre-merge-... (was 8ad2c2a83)
    wt-close: test-pre-merge cleaned ✓

预演结束后 \`git worktree list\` 里 test 工位消失、branch 也没了，即**唯一一份 test-gate.env 证据被删**。
随后正式 \`wt-close\` 拒绝执行：

    [wt-close] 找不到对应的测试工位 test-pre-merge-20261112T031638Z-*
    测试工位中的 test-gate.env 是测试已运行的唯一证据。

只能 \`wt-create\` 进入 resume 模式重建工位、重跑 2 分钟 test-gate 才继续。

同一轮紧接着的第二击：\`wt-create\` resume 输出首行

    [wt-create] raw-20261112T031638Z phase_state=absorbed → proposed (auto-reopen)

该 raw 早已合并、双平台 CLOSED；auto-reopen 之后主仓（develop 工作树）\`git status\` 变成
\` M docs/B1-docs/raw-20261112T031638Z/issue.md\`，需要人工 \`git checkout --\` 还原。

## 2. 代码定位

### 2.1 dry-run 泄漏（wt-close）

- \`wt-close:25\` \`DRY_RUN=false\`，\`wt-close:169\` \`--dry-run\` 置 true。
- Phase 5（删工位，1081）、Phase 6（删本地分支，1142）、Phase 7（同步 develop，1261）都正确包了 \`if [[ "$DRY_RUN" == true ]]\`。
- **Phase 6b（1189–1254）完全没有 DRY_RUN 分支**：直接
  \`git worktree remove "$_tp_wt"\`、\`git branch -D "$_tp_branch"\`，
  还会关 ACP 会话、\`agent_release_all()\`、清 \`agent-id.env\`。
- 因此 dry-run 的破坏面不止「删工位」：还会释放 agent 表、删 agent-id.env，属于**有状态副作用**。

### 2.2 auto-reopen 写错目标（wt-create）

- \`wt-create:443–458\`：「Raw issue state check」段落用相对路径
  \`_issue_file="docs/B1-docs/raw-20261112T131150Z/issue.md"\` 直接 \`sed -i\`。
- 该段在**建工位之前**执行，此时 CWD 是调用方目录 —— 正常是主仓（develop），
  resume 模式更是必然在主仓 → 注释写的 "never on develop" 与实际行为相反。
- resume 模式下 raw 已 absorbed 是**正常状态**（上一轮已合并），自动回退成 proposed 是语义错误。

## 3. 方案空间

| 方案 | 做法 | 评价 |
|---|---|---|
| A | Phase 6b 外层加 \`DRY_RUN\` 分支，dry 时只 \`_dry\` 打印 | 最小、与既有 Phase 5/6/7 一致 ✅ |
| B | 新增 \`--rehearse\` 独立参数，dry-run 只跑前置门禁 | 语义更清晰但要同时改 usage/文档/测试，超范围 |
| C | dry-run 时跳过整个 Phase 6b..7 | 会掩盖「Phase 7 已有 dry 分支」的既有设计，判据变模糊 |

auto-reopen：

| 方案 | 做法 | 评价 |
|---|---|---|
| A | resume 模式不改写；非 resume 且 raw 已终态时要求显式 \`--reopen\`，写入落在新建的 dev 工位内 | 符合 issue「显式开关 + 只写工位」要求 ✅ |
| B | 保留自动 reopen，只把路径改成主仓绝对路径 | 仍然在写受保护分支，治标不治本 |
| C | 彻底删掉 auto-reopen | 会砍掉「重开已关闭 raw 继续干」的正当用法 |
| D | 改成调用 \`issue-sync\` 做状态迁移 | 跨模块、语义耦合，超本轮范围 |

## 4. 结论

两处都是「预演/恢复路径产生不可逆副作用」，采用方案 A + A：
- dry-run 零副作用（含 agent 表 / agent-id.env）；
- reopen 必须显式 \`--reopen\`，且只写 dev 工位内的文档副本；resume 模式不动 phase。

## 5. 证伪记录

- 「dry-run 删工位是 pretests-retirement-gate 干的」→ 否：日志里该 gate 先打印 \`passed ✓\`，
  删除发生在 \`Phase 6b\` 之后，且 \`git branch -D\` 输出紧跟 \`cleaning up companion test-pre-merge\`。
- 「auto-reopen 只在非 resume 生效」→ 否：本轮正是 resume 模式触发（dev 分支存在、test 工位缺失）。
- 「这是本轮新引入」→ 否：Phase 6b 一直没有 DRY_RUN 分支；auto-reopen 段历史轮次同样会写主仓，只是此前无人用 dry-run。

# B1 Candidates — raw-20261112T131150Z

## C-20261112T131150Z-A：预演/恢复路径零副作用

- kind: fix
- 范围：
  1. \`wt-close\` Phase 6b（companion test-pre-merge 清理）纳入 \`DRY_RUN\` 分支：
     dry 时只打印 \`[DRY-RUN]\` 计划动作，不动 worktree / branch / agent_working 表 / agent-id.env。
  2. \`wt-create\` 的「Raw issue state check」不再隐式改写 phase：
     - resume 模式一律不改（中断残留的 raw 状态就是它应有的状态）；
     - 非 resume 且 raw 已是 \`absorbed|completed|dropped\` 时，必须显式 \`--reopen\`，
       否则拒绝并给出指引；
     - 允许 reopen 时，写入目标改为**新建的 dev 工位内**的文档副本，绝不写调用方（主仓）工作树。
- 验收：
  - AT-001 静态 + 行为：Phase 6b 的破坏性命令只在 \`DRY_RUN != true\` 分支内；
    抽取该段用 \`DRY_RUN=true\` 执行时，stub git 不收到 \`worktree remove\` / \`branch -D\`；
    负向控制（\`DRY_RUN=false\`）必须收到，证明测试能分辨两者。
  - \`wt-create\` 源码中不再存在对相对路径 \`docs/B1-docs/raw-<key>/issue.md\` 的无条件 \`sed -i\`；
    \`--reopen\` 出现在 usage 与参数解析；resume 路径显式跳过 phase 改写。
- 不退化边界：
  - 正式（非 dry-run）wt-close 的清理顺序、门禁强度、\`--force\` 语义不变；
  - 正常（非 resume）建工位行为不变；
  - reopen 只是把写入位置从「调用方工作树」搬到「工位」，不改 phase 语义与状态机；
  - 不引入新的 phase 枚举、不新增 CLI 子命令。

## 为什么合成一个 candidate

两个缺陷共享同一个根因模式（预演/恢复路径被当成真实路径执行而有副作用），
且修复点集中在同两条命令、同一批 AT 里；拆成两个 PR 会产生「先修 dry-run、再修 reopen」
的重复验证成本。raw 记录里也已把它们写成同一条（含两段现象）。

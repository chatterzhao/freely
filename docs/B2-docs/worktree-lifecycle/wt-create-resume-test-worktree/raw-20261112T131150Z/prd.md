# PRD: 预演与恢复路径不得产生不可逆副作用

- issue_id: I-20261112T131150Z-A
- source_raw: raw-20261112T131150Z
- workflow_kind: fix
- milestone: M-20261112T131150Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story，epics-map.svg 无需改动）

## 目标

让两条「本应只读」的路径真正只读：

1. \`freely wt-close --dry-run\` 全程零副作用（工作树、分支、agent_working 表、agent-id.env 都不动）。
2. \`wt-create\` 不再隐式把已终态的 raw 改回 proposed，也不再写调用方（受保护分支）的工作树；
   要重开工位必须显式 \`--reopen\`，写入只落在新建的 dev 工位内。

## 唯一改动范围

- \`docs/system/workspace/scripts/worktree/wt-close\`：Phase 6b（companion test-pre-merge 清理）纳入 \`DRY_RUN\` 分支。
- \`docs/system/workspace/scripts/worktree/wt-create\`：\`--reopen\` 参数 + resume 跳过 phase 改写 + reopen 写入工位内文档。
- 新增 AT：\`docs/system/workspace/scripts/tests/test-wt-close-dryrun-safety.py\`。
- 新增函数级单测：\`docs/system/workspace/scripts/tests/unit/t-worktree-preview-01.sh\`。
- \`bin/test-all\` 的 \`CORE\` / \`CI_CORE\` 各 +1。

## 不退化边界

- 正式（非 dry-run）wt-close 的清理顺序、closeout-gate / pretests-retirement-gate / dev-test 一致性判据不变。
- \`--force\` 与 \`--discard-unmerged\` 的语义、reason 要求不变。
- 正常（非 resume）建工位的四态幂等、legacy 补建、\`_init_test_worktree_state\` 单一真源不变。
- 不新增 phase 枚举；不改 \`issue-sync\` / 平台同步；不夹带 #4315 / #4316 的修复。

## 功能需求

- FR-1：\`DRY_RUN=true\` 时 Phase 6b 不执行任何 \`git worktree remove\` / \`git branch -D\` / agent 表写入，只打印 \`[DRY-RUN]\` 计划。
- FR-2：\`DRY_RUN=false\` 时 Phase 6b 行为与现状逐字一致（含 \`--force\` 分支）。
- FR-3：\`wt-create\` 对 \`absorbed|completed|dropped\` 的 raw，在 resume 模式不改写 phase_state。
- FR-4：\`wt-create\` 非 resume 且 raw 已终态时，未传 \`--reopen\` 拒绝执行并给出指引；传 \`--reopen\` 时把新 phase 写进 dev 工位内的文档，主仓 \`git status\` 保持干净。
- FR-5：usage 文本包含 \`--reopen\`，且 \`--reopen\` 仅在写开关语义下生效（不影响分支/kind 解析）。

## 验收

- AT-001：静态断言 + 真实执行抽取出的 Phase 6b 代码块（dry 与 non-dry 双跑，负向控制）。
- \`tests/unit/t-worktree-preview-01.sh\` 全 PASS（Step 2.5 的函数级证据）。
- \`bin/test-all --ci\` 全绿；三门禁（projections / runtime size / bin projection）不变。

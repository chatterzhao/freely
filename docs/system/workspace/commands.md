# Freely 封装命令参考

## 为什么必须用封装命令

Freely 的每条封装命令内部都执行了多个关键步骤。直接用 `git`/`gh` 命令会跳过这些步骤——不是"不推荐"，而是**直接跳过了完整流程**。

| 封装命令 | 封装了哪些步骤 |
|---------|--------------|
| `freely feedback` | 创建 raw issue → 双平台同步（GitHub + Gitee）→ 纳入扫描发现 |
| `freely wt-create` | 创建 dev worktree + test-pre-merge 工位 → 同步 tooling → cd 到工位 |
| `freely pr-create-guarded` | pull develop → 冲突处理 → dry-run gate → 双平台 push → 双平台创建 PR |
| `freely pr-review-guarded` | 6 维独立 review → verdict 文档 |
| `freely pr-merge-guarded` | PR gate → promotion gate → merge → develop-push → 双平台同步 |
| `freely wt-close` | 关闭 test-pre-merge + dev worktree → 双平台 close issue → 清理分支 |
| `freely develop-push` | 受控 develop push → 审计日志 |
| `freely issue-sync` | 双平台 issue 同步（create/update/comment/close/promote/batch） |
| `freely deploy-skills` | 部署 workspace skills 到 AI 工具目录 |

跳过任何一步 = 门禁拦截 = 必须回到正确命令重新走流程。

## 意图→命令速查

从你想做什么出发，找到正确命令：

| 你想做什么 | 用这个命令 | ❌ 不要用 |
|-----------|-----------|---------|
| 报告 bug / 提需求 | `freely feedback --title "..." --kind fix\|feature --body "..."` | gh issue create |
| 修改已有 issue 标题/内容 | `freely feedback edit --raw-key <key> --title "..." --body "..."` | gh issue edit |
| 开始修 bug / 做功能 | `freely wt-create --raw-key <key> --source platform --kind fix\|feature --slug <slug>` | git worktree add, git checkout -b |
| 代码写完想提交 | `freely pr-create-guarded` | gh pr create, git push |
| 请人 review | `freely pr-review-guarded <branch>` | — |
| review 通过想合并 | `freely pr-merge-guarded develop <branch>` | gh pr merge, git merge |
| 合并完了收工 | `freely wt-close --raw-key <key>` | git worktree remove, git branch -D |
| 只关平台 issue（无本地工位） | `freely wt-close --raw-key <key> --platform-only --reason "..."` | gh issue close |
| 强制丢弃一个 issue | `freely wt-close --raw-key <key> --force --reason "..."` | git branch -D |
| 同步 develop 到远程 | `freely develop-push attempt` | git push --no-verify, git push --force |
| 同步双平台 issue 状态 | `freely issue-sync <subcommand>` | gh issue close, gh issue edit |
| 部署 skills 到 AI 工具 | `freely deploy-skills` | 手动 cp |
| 查看当前项目状态 | `freely live-status` | — |
| 查看所有工位状态 | `freely fleet-status` | git worktree list |

## 每个命令的详细说明

### `freely feedback`

**语法**:

| 场景 | 命令 |
|------|------|
| 创建新 raw issue | `freely feedback [create] --title "..." --kind <fix\|feature> --body "..." [--severity P0\|P1\|P2]` |
| 编辑已有 raw issue | `freely feedback edit --raw-key <key> [--title "..."] [--body "..."]` |

**选项**:

| 选项 | 说明 |
|------|------|
| `--title <text>` | 标题（fix:/feat:/docs: 等前缀，<=72 字符） |
| `--kind <fix\|feature>` | 类型，决定分支前缀和 RED 策略 |
| `--body <text>` | 正文（>=50 有效字符，至少一个 `##` 章节） |
| `--severity <P0\|P1\|P2>` | 严重度（默认 P2） |
| `--raw-key <key>` | edit 时必填 |

**封装步骤**:
1. 创建 raw issue
2. 双平台同步（GitHub + Gitee）
3. 纳入扫描发现队列

**使用场景**: 发现 bug、有新功能需求时。已有 issue 描述不准确时用 `edit`。

---

### `freely wt-create`

**语法**: `freely wt-create --raw-key <key> --source platform --kind <fix|feature|hotfix> --slug <slug> [--base <branch>] [--skill <name>]`

**选项**:

| 选项 | 说明 |
|------|------|
| `--raw-key <key>` | 必填。raw issue key（YYYYMMDDTHHMM[SS]Z） |
| `--source platform` | 必填。只允许 `platform` |
| `--kind <fix\|feature\|hotfix>` | 必填。分支前缀和 RED 策略 |
| `--slug <slug>` | 必填。简短描述性 slug |
| `--base <branch>` | 可选。基分支（默认 develop） |
| `--skill <name>` | 可选。覆盖默认 workflow skill |

**封装步骤**:
1. 创建 dev worktree + test-pre-merge 测试工位
2. 同步 tooling（config、session-store、bootstrap）
3. 从平台拉取 raw issue 到本地 B1-docs
4. 输出工位路径

**使用场景**: 已有 raw issue，准备开始开发时。

---

### `freely pr-create-guarded`

**语法**: `freely pr-create-guarded [--title <title>] [--body <body>] [--base <branch>]`

**选项**:

| 选项 | 说明 |
|------|------|
| `--title <title>` | 可选。PR 标题（默认从分支名派生） |
| `--body <body>` | 可选。PR 正文 |
| `--base <branch>` | 可选。目标分支（默认 develop） |

**封装步骤**（自动执行的门禁链）:
1. 工位清洁检查 → phase_state 检查 → dev↔test 一致性
2. epics-map 对齐 → dry-run merge gate → IBM governance gate
3. pretests evidence check → comment resolution
4. rebase 到最新 develop → 双平台 push → 双平台创建 PR

**使用场景**: 开发完成、测试全部 GREEN 后。必须在 fix/raw-* 或 feature/raw-* 工位中执行。

---

### `freely pr-review-guarded`

**语法**: `freely pr-review-guarded <branch> [--reviewer <name>] [--slot <slot>] [--verdict pass|fail] [--reason <text>]`

**选项**:

| 选项 | 说明 |
|------|------|
| `<branch>` | 必填。要审查的分支 |
| `--reviewer <name>` | 可选。Reviewer 名称 |
| `--slot <slot>` | 可选。Reviewer AI slot |
| `--verdict <pass\|fail>` | 可选。手动覆盖 verdict |
| `--reason <text>` | 可选。覆盖为 pass 时必须提供理由 |

**封装步骤**:
1. 工位清洁检查
2. TDD Reviewer agent 四问审查（RED→GREEN→ADEQUACY→REFACTOR），最多 3 轮
3. 生成 verdict 文档，pass 时自动 commit + push
4. ACP 不可用时回退到人工审查

**使用场景**: PR 创建后需要独立评审时。

---

### `freely pr-merge-guarded`

**语法**:

| 场景 | 命令 |
|------|------|
| 正常合并 | `freely pr-merge-guarded <target-branch> <source-branch> [--dry-run]` |
| 完成冲突解决 | `freely pr-merge-guarded complete <target-branch> <source-branch>` |

**选项**:

| 选项 | 说明 |
|------|------|
| `<target-branch>` | 合并目标分支 |
| `<source-branch>` | 合并来源分支 |
| `--dry-run` | 只验证门禁，不执行合并 |

**封装步骤**:
1. 合并锁 → PR gate → PR review 检查 → local↔remote sync
2. issue-sync → 工位清洁检查 → 本地 git merge（含 receipt 注入）
3. semantic conflict 检测 → develop-push 到双平台 → 双平台 close PR

**使用场景**: PR review 通过后准备合并。**必须在 develop 分支执行。**

---

### `freely wt-close`

**语法**:

| 场景 | 命令 |
|------|------|
| 正常收口 | `freely wt-close --raw-key <key>` |
| 只关平台 issue | `freely wt-close --raw-key <key> --platform-only --reason "违规绕过门禁中，理由充分，是：<理由>"` |
| 强制丢弃 | `freely wt-close --raw-key <key> --force [--discard-unmerged] --reason "违规绕过门禁中，理由充分，是：<理由>"` |
| 跳过平台关闭 | `freely wt-close --raw-key <key> --skip-platform` |
| 试运行 | `freely wt-close --raw-key <key> --dry-run` |

**选项**:

| 选项 | 说明 |
|------|------|
| `--raw-key <key>` | 必填。支持 `raw-YYYYMMDDTHHMMSSZ`、`fix/raw-{key}-{slug}`、纯时间戳等格式 |
| `--reason <text>` | 绕过标记（--force/--discard-unmerged/--platform-only/--skip-platform）时必须填写 |
| `--force` | 永久丢弃（不可恢复）。有未合并提交时需同时 `--discard-unmerged` |
| `--discard-unmerged` | 确认丢弃未合并提交 |
| `--platform-only` | 仅通过 API 关闭双平台 issue。**不需要本地 docs** |
| `--skip-platform` | 跳过平台 issue 关闭 |
| `--dry-run` | 只打印操作不执行 |

**封装步骤**（正常收口）:
1. comment resolution → phase_state 检查 → pretests-retirement-gate
2. dev↔test 一致性 → 未合并提交守卫
3. 删除 test + dev 工位 → 双平台 close issue → 删除远程/本地分支

**使用场景**:
- **正常收口**: PR 已合并，清理工位和分支
- **只关平台**: 无本地工位或修复已在其他 PR 完成
- **强制丢弃**: 确定放弃全部工作

> **关键**: `gh issue close` 只关一个平台，`freely wt-close --platform-only` 确保双平台同步关闭。

---

### `freely develop-push`

**语法**:

| 场景 | 命令 |
|------|------|
| 查看状态 | `freely develop-push status` |
| 尝试推送 | `freely develop-push attempt` |
| 推迟推送 | `freely develop-push defer --reason <post_merge_acceptance\|cleanup_followthrough\|remote_delivery_hold> [--note <text>]` |
| 清除状态 | `freely develop-push clear` |

**选项**:

| 选项 | 说明 |
|------|------|
| `--project <path>` | 可选。项目根路径 |
| `--reason <value>` | defer 时必填 |
| `--note <text>` | defer 时可选 |

**使用场景**: 需要将 develop 同步到远程时用 `attempt`。有原因需推迟时用 `defer`。

---

### `freely issue-sync`

**语法**:

| 子命令 | 说明 |
|--------|------|
| `create <local_id>` | 创建平台 issue（幂等） |
| `update <local_id>` | 更新平台 issue（跳过未变更） |
| `comment <local_id>` | 推送未同步的评论 |
| `close <local_id> [reason]` | 关闭平台 issue |
| `promote <raw_id> <I_id>` | 关闭 raw，创建 I-* 并交叉引用 |
| `promote-finalize <local_id>` | 所有子 issue promote 后关闭 raw |
| `status <local_id>` | 显示同步状态 |
| `batch` | 批量同步所有变更 issue |
| `scan` | 显示变更的 issue |

**使用场景**: 手动管理双平台 issue 同步。通常由 `pr-merge-guarded` 和 `wt-close` 自动调用。

---

### `freely deploy-skills`

**语法**: `freely deploy-skills [--tools <name,...>] [--force] [--dry-run]`

**选项**:

| 选项 | 说明 |
|------|------|
| `--tools <name,...>` | 逗号分隔的工具名（默认自动检测） |
| `--force` | 强制覆盖 |
| `--dry-run` | 只显示不写入 |

**使用场景**: 修改任何 skill 文件后必须执行。

---

### `freely live-status` / `freely fleet-status`

**语法**: `freely live-status [--project <path>]` / `freely fleet-status [--project <path>]`

**功能**:
- **live-status**: 当前项目运行时状态（daemon、prompt、continuity、develop push 等）
- **fleet-status**: 所有 worktree 表格视图（branch、CLEAN/DIRTY、supervisor/AI PID、intent 等）

## 完整开发流程

```
freely feedback → freely wt-create → B1 预研 → B2 设计 → RED 测试先行 → dev 实现 → GREEN 验证 → freely pr-create-guarded → freely pr-review-guarded → freely pr-merge-guarded → freely wt-close
```

被 hook 拦截了？从你当前阶段对应的命令重新开始——不要绕过门禁。

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
| `freely develop-push attempt` | 受控 develop push → 审计日志 |

跳过任何一步 = 门禁拦截 = 必须回到正确命令重新走流程。

## 意图→命令速查

从你想做什么出发，找到正确命令：

| 你想做什么 | 用这个命令 | ❌ 不要用 |
|-----------|-----------|---------|
| 报告 bug / 提需求 | `freely feedback --title "..." --kind fix\|feature --body "..."` | gh issue create |
| 开始修 bug / 做功能 | `freely wt-create --raw-key <key> --source platform --kind fix\|feature --slug <slug>` | git worktree add, git checkout -b |
| 代码写完想提交 | `freely pr-create-guarded` | gh pr create, git push |
| 请人 review | `freely pr-review-guarded <branch>` | — |
| review 通过想合并 | `freely pr-merge-guarded develop <branch>` | gh pr merge, git merge |
| 合并完了收工 | `freely wt-close --raw-key <key>` | git worktree remove, git branch -D, gh issue close |
| 同步到远程 | `freely develop-push attempt` | git push --no-verify, git push --force |
| 查看当前状态 | `freely live-status`, `freely fleet-status` | — |

## 每个命令的详细说明

### `freely feedback`

**语法**: `freely feedback --title "..." --kind <fix|feature> --body "..."`

**封装步骤**:
1. 创建 raw issue
2. 双平台同步（GitHub + Gitee）
3. 纳入扫描发现队列

**使用场景**: 发现 bug、有新功能需求、有改进想法时。

---

### `freely wt-create`

**语法**: `freely wt-create --raw-key <key> --source platform --kind <fix|feature> --slug <slug>`

**封装步骤**:
1. 创建 dev worktree（feature/* 或 fix/*）
2. 创建 test-pre-merge 测试工位
3. 同步 tooling（config、session-store、bootstrap）
4. 输出工位路径，提示 cd 进入

**使用场景**: 已有 raw issue，准备开始开发时。

---

### `freely pr-create-guarded`

**语法**: `freely pr-create-guarded`

**封装步骤**:
1. pull develop 到最新
2. 冲突检测与处理
3. dry-run gate（governance-merge-gate）
4. 双平台 push
5. 双平台创建 PR（GitHub + Gitee）

**使用场景**: 开发完成、测试全部 GREEN 后，准备提 PR 时。

---

### `freely pr-review-guarded`

**语法**: `freely pr-review-guarded <branch>`

**封装步骤**:
1. 6 维独立 review（correctness、security、performance、maintainability、test-coverage、governance）
2. 生成 verdict 文档

**使用场景**: PR 创建后，需要独立评审时。

---

### `freely pr-merge-guarded`

**语法**: `freely pr-merge-guarded develop <branch>`

**封装步骤**:
1. PR gate（检查 PR 状态和审批）
2. promotion gate（governance 门禁）
3. merge 到 develop
4. develop-push 到双平台
5. 双平台 close PR

**使用场景**: PR review 通过、CI 通过后，准备合并时。

---

### `freely wt-close`

**语法**: `freely wt-close --raw-key <key>`

**封装步骤**:
1. 关闭 test-pre-merge 测试工位
2. 关闭 dev worktree
3. 双平台 close issue（GitHub + Gitee）
4. 清理本地分支

**使用场景**: PR 已合并到 develop，需要收工清理时。

---

### `freely develop-push attempt`

**语法**: `freely develop-push attempt`

**封装步骤**:
1. 受控的 develop push
2. 审计日志记录

**使用场景**: 需要在 develop 上同步远程时。

## 完整开发流程

```
freely feedback → freely wt-create → B1 预研 → B2 设计 → RED 测试先行 → dev 实现 → GREEN 验证 → freely pr-create-guarded → freely pr-review-guarded → freely pr-merge-guarded → freely wt-close
```

被 hook 拦截了？从你当前阶段对应的命令重新开始——不要绕过门禁。

# Brainstorm: Worker Launch 保护工位重定向

- 来源: raw-20260509T022152Z52Z (#264)
- 日期: 2026-05-09
- 基于: 2026-05-08 #256-#263 修复 + 7h daemon 运行数据

## 根因分析（完整版）

### 问题现象

daemon 运行 7 小时，17 个 worker prompt，0 个执行成功，20+ 次 restart storm。

### 根因链（四层）

```
第1层: AI 写 continuity → delegate worker
       选了 develop 作为 worker target（保护分支，不可 commit）

第2层: runtime 读 continuity → 生成 worker prompt
       Worktree header 直接写 develop 路径（L9519）
       不检查是否可写，不重定向

第3层: worker 在 develop 启动
       尝试 commit → hook 拦截 → 快速退出
       某些时候 worker 成功执行了 cleanup（不涉及 commit 的操作）

第4层: 快速退出 → bridge 重启 → 再次 launch → 3次/30s → storm
       Broken pipe (L11802) 是 launch pipeline 在快速重启中断开
```

### 为什么之前的修复不完整

| 修复 | 层级 | 效果 |
|------|------|------|
| #256 reference-transaction hook | — | 允许 branch -d |
| #258 wt-create pull defer | 工具 | 工位创建成功 |
| #259 raw-issue-pull target=pwd | 工具 | raw issue 写入工位 |
| #260 wt-create skill name | 工具 | 使用更友好 |
| #261 prompt companion info | 第2层 | AI 知道配对工位路径，但 runtime 不自动重定向 |
| #262 merge error guidance | 门禁 | AI 理解 IBM 阶段要求 |
| **#264 本 issue** | **第2+3层** | **runtime 自动重定向 + AI 工作流引导** |

#261 在 prompt 里加了 companion 信息，但只是"告诉 AI 有这么个工位"——AI 需要自己决定什么时候去。runtime 层没有强制重定向。

### 正确的工位使用契约（来自 fix-execution skill）

| 操作 | test-pre-merge | develop | fix/feature |
|------|---------------|---------|-------------|
| 读文件 | ✅ | ✅ | ✅ |
| 写文件（dirty） | fix: ✅, feat: ❌ | ❌ | ✅ |
| git add/commit | ❌ | ❌ | ✅ |
| stash → cd → pop → commit | — | — | ✅ |
| merge | ❌ | 只接受 merge commit | fix→test-pre-merge |

### Worker 应该的工作流

**fix-execution 模式**：
```
1. 在 test-pre-merge 快测（dirty only，不改 git）
2. 验证通过 → git stash
3. cd fix/raw-{key}-{slug}
4. git stash pop
5. 补全 IBM governance artifacts（若缺）
6. git add + commit
7. pr-merge-guarded fix→test-pre-merge→develop
```

**feat-execution 模式**：
```
1. 直接在 feature/raw-{key}-{slug} 工作
2. 不在 test-pre-merge 改任何文件
3. 正常 IBM 流程 + commit + merge
```

## 解决方案

### 设计原则

- **Manager（主管）** 运行在 test-pre-merge，做 patrol、写 continuity、写 worker prompt
- **Worker** 只能运行在 `fix/*` 或 `feature/*` 工位，不能是 develop/main/test-pre-merge
- Runtime 验证：worker target branch 必须是 fix/* 或 feature/*，否则 **报错拒绝**，让主管修正
- **不做自动重定向**——runtime 不应该猜测配对工位。主管应该明确指定正确的工位

### Phase 1: Runtime 拒绝非法 worker target（本 issue）

`worker_prompt_launchable_for_manager_project` (L9695) 增加检查：

```bash
target_branch="$(worker_prompt_target_branch "$prompt_file")"
case "$target_branch" in
  fix/*|feature/*) ;;  # OK
  *)
    # WORKER_PROMPTS_NOT_LAUNCHABLE + 明确错误原因
    return 1
    ;;
esac
```

报错信息告诉主管：worker 必须在 fix 或 feature 工位运行，当前 target 是 `$target_branch`（保护分支），请修改 continuity 中的 worker delegation target。

### Phase 2: Manager prompt 引导（后续）

Manager prompt 首跳指引中加入：
- 写 continuity 时，worker target 必须选 fix/* 或 feature/*
- 如何通过 `git worktree list` 找到配对可写工位
- fix-execution vs feat-execution 的工位使用规则

## 成功标准

- Worker 在 fix/feature 工位启动（`Worktree: fix/raw-...`）
- Worker commit 不再被保护分支 hook 拦截
- 连续运行 1h+ 无 restart storm
- Worker 产出能走完 fix→test-pre-merge→develop 合入

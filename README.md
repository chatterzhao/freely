# freely

## 项目意图

Freely 是一个自主项目循环运行器：
- AI 作为项目路径的活跃工作者运行
- AI 遵循项目意图 + 宪法作为硬性约束
- AI 通过监控/重启行为保持连续性

主要文档：
- 项目意图：`docs/PROJECT_INTENT.md`
- 宪法：`docs/CONSTITUTION.md`
- 法律：`docs/LAWS.md`
- pre-brainstorms 工作区：`docs/pre-brainstorms/README.md`

## 快速开始

```bash
chmod +x ./bin/freely

freely init \
  --project <项目绝对路径> \
  --intent <项目意图文件绝对路径> \
  --constitution <宪法文件绝对路径> \
  --ai codex:gpt-5-codex:auto

freely doctor --project <项目绝对路径>
freely start --project <项目绝对路径>
```

在另一个终端中：

```bash
freely status --project <项目绝对路径>
freely stop --project <项目绝对路径>
```

## 文档门禁

在实现或合并前运行基线文档检查：

```bash
chmod +x ./bin/governance-check
./bin/governance-check
```

## Hook 回归门禁

合并前验证本地推送策略：

```bash
chmod +x ./bin/test-pre-push-hook
./bin/test-pre-push-hook
```

功能交付分支策略：

- `feature/* → dev → test-pre-merge → pr-create-guarded → pr-merge-guarded → develop` 为标准开发集成路径（test-pre-merge 是进入 develop 的强制验证阶段）
- `feature/* → develop` 作为正常路径被阻止（CONSTITUTION.md §2）
- 直接推送/合并到 `develop` 被本地 hook 策略阻止

标准 worktree 创建方式（从项目根目录执行）：

```bash
cd <your-project-name-path>

git worktree add -b feature/<topic> \
  ../<your-project-name>-worktrees/feature-<topic> \
  develop

cd ../<your-project-name>-worktrees/feature-<topic>
```

这里不需要先 `git checkout develop`，因为命令最后的 `develop` 已经显式指定了新分支的基线。

合并完成后的标准清理方式：

```bash
git worktree remove ../<your-project-name>-worktrees/feature-<topic>
git branch -d feature/<topic>
```

`bin/wt-enter` / `bin/wt-add` 只是辅助命令；hooks 会在未按规范操作时兜底并给出友好提示。

# freely

## 项目意图

Freely 是一个自主项目循环运行器：
- AI 作为项目路径的活跃工作者运行
- AI 遵循项目意图 + 宪法作为硬性约束
- AI 通过监控/重启行为保持连续性

主要文档：
- 项目意图：`docs/PROJECT_INTENT.md`
- 宪法：`docs/CONSTITUTION.md`
- 文档地图：`docs/README.md`

## 快速开始

```bash
chmod +x ./bin/freely

./bin/freely init \
  --project <项目绝对路径> \
  --intent <项目意图文件绝对路径> \
  --constitution <宪法文件绝对路径> \
  --ai codex:gpt-5-codex:auto

./bin/freely doctor --project <项目绝对路径>
./bin/freely start --project <项目绝对路径>
```

在另一个终端中：

```bash
./bin/freely status --project <项目绝对路径>
./bin/freely stop --project <项目绝对路径>
```

## BMAD 文档门禁

在实现或合并前运行 BMAD 基线检查：

```bash
chmod +x ./bin/bmad-check
./bin/bmad-check
```

## Hook 回归门禁

合并前验证本地推送策略：

```bash
chmod +x ./bin/test-pre-push-hook
./bin/test-pre-push-hook
```

功能交付分支策略：

- `feature/* -> pre-develop` 用于测试集成
- `pre-develop -> develop` 仅在验证后
- 直接推送/合并到 `develop` 被本地 hook 策略阻止
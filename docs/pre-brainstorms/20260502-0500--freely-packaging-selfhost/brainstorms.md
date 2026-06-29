# Freely 打包与自举验证

## 目标

从 develop 打包出可独立运行的 Freely 版本，用打包版本开发 Freely 自己，打包后验证通过才能 merge 到 develop。

## 版本号

```
nightly:  YYYYMMDD-nightly    (每天从 develop 出，一天一个)
stable:   YYYY.MM.DD-stable   (从 main 出)
```

test-pre-merge 批次是一次性验证容器，不产生持久版本。

## 打包清单

```
打包（Freely 产品能力，随版本发布）：

  docs/system/workspace/agents/           agent 角色定义
  docs/system/workspace/skills/           skill 定义
  docs/system/workspace/hooks/            git gate 脚本
  docs/system/workspace/scripts/          运行时脚本
  docs/system/workspace/ibm-framework.md
  docs/system/workspace/three-loop-capability-lifecycle.md
  docs/system/workspace/three-loop-trace-contract.md
  docs/system/workspace/tools.md
  docs/system/workspace/acp-session-architecture.md
  docs/system/workspace/session-lifecycle-protocol.md
  docs/system/workspace/project-agents-contract.md
  docs/system/workspace/README.md
  docs/system/workspace/scan-lifecycle-design.md

  bin/                                    入口脚本（所有）
  .githooks/                              git hook 包装层
  templates/                              freely init 模板
  .freely/tool-boundary-bootstrap.md

不打包（仅 Freely 开发仓库内使用）：
  CONSTITUTION.md / LAWS.md              开发笔记本
  AGENTS.md                              项目治理入口
  PROJECT_INTENT.md                      产品方向
  milestones.md / pre-brainstorms/        开发计划
  issues/ / progress/                    开发状态
  .freely/config.env                     项目配置
  .freely/intake/ / .freely/logs/        运行时数据
```

## 打包脚本

`freely-package --version <ver> [--output <dir>]`

1. 读取 workspace 下的 allowlist（`install-lifecycle-allowlist.txt` 扩展为 `package-allowlist.txt`）
2. 复制 allowlist 中的文件到输出目录
3. 写入版本文件 `FREELY_VERSION=<ver>`
4. 验证打包完整性（所有引用的文件都存在）

## 自举验收流程

```
feature → PR → test-pre-merge-YYYYMMDD（从 develop 新建）
  → 从 test-pre-merge 打包 → Freely YYYYMMDD-NNN-dev
  → 用打包版本启动 daemon，开发 Freely 自己
  → 能正常完成一个 Manager cycle（patrol → 判断 → 产出）
  → 通过？→ merge 到 develop
  → 失败？→ 丢弃 test-pre-merge，修 feature
```

## 夜间发布

每天定时从 develop HEAD 打包 `YYYYMMDD-nightly`，放到 `~/.freely/versions/` 供 Freely 开发自己使用。

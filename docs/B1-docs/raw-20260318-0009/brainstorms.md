# 20260318-0009 Multi-Worktree Supervision Control Plane

## 背景

Freely 自举时已经不是单工位开发，而是同时存在 runtime/control-plane、frontend probe、architecture synthesis、evolver 等多个 worktree。现有治理能约束 branch/worktree 合法性，但还没有把“项目负责人如何同时监督多个工位”做成正式 CLI 能力。

当前暴露的问题是：

- 主监督者只能从聊天和零散命令里拼当前盘面
- checkpoint 压力能在单 worktree 状态里看见，但缺少项目级视图
- 多工位并行时，哪些该继续、哪些该先 checkpoint、哪些只该 doc-loop，不够稳定

## 收敛结论

Freely 应把 `multiple worktrees as supervised workcells` 收成 control-plane 能力，而不是临时经验：

1. 项目级 CLI 必须能展示所有 mounted worktree 的 branch、dirty state、supervisor/ai pid、最近运行态。
2. dirty/checkpoint 压力必须进入 supervisor/state，而不是只在人工合并前才看 `wt-status-all`。
3. 多账号恢复也属于 control-plane；当所有账号都不可立即使用时，应切换到最早 reset 的账号并 sleep，到点后继续自举。
4. 这套方法应形成可复用 skill，供 Freely 自己和未来托管项目复用。

## 落点

- `docs/LAWS.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/README.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`

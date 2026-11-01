---
audit_id: AUD-20261101T231000Z
phase_state: completed
subject: README architecture diagram
created_at: 2026-11-01
---

# README 架构图审计：旧图为什么不准确

## 1. 旧图表达了什么

旧图的主线是：

```
人 → CLI/TUI/GUI → Freely core → Manager/Gates → Worker/Reviewer/A2A → Worktrees/Harness/Platforms
```

它没有说错，但它只表达了“控制面 + 执行面”的一半：

- Manager 派工、Gate 检查、Worker 执行、Reviewer 审查、worktree 隔离、ACP harness、GitHub/Gitee。
- 对不熟悉 Freely 的人，这张图看起来像“另一个多 agent 编排器”，和普通 agent framework 没有本质区别。

## 2. 旧图漏了什么

| 漏掉的面 | 为什么重要 | 旧图后果 |
| --- | --- | --- |
| 规格面（SDD） | Freely 的第一真相是 docs，不是 DB：Intent/Constitution/LAWS、B1/B2、PRD/pre-tests/tasks | 看起来像 prompt-driven，而不是 document-driven |
| TDD | pre-tests → RED → 实现 → GREEN → test-pre-merge 证据 | 看起来像“Worker 写完就算”，没有验收闭环 |
| scan / platform 隔离 | 平台只是界面；scan 下载、sync 上传，本地 docs 是唯一真相 | 容易误解为 AI 直接读 GitHub/Gitee |
| 工具面 | command/script/skill/MCP 各有职责，不是同一层 | 容易把 skill 当权限、把 command 当 git 糖 |
| harness 的位置 | ACP harness 是执行提供层，可替换，不是宿主 | 容易误解为 Freely 绑定某个 AI CLI |
| 人的插话入口 | issue/comment、chat、PR review 是三种不同入口 | 容易只画成“CLI” |

## 3. 修正后的模型：五个平面

```
界面面：issue/comment/chat + CLI/TUI/GUI
   ↓
规格面（SDD）：Intent/Constitution/LAWS + B1/B2 + PRD/pre-tests/tasks/code-review
   ↓
控制面：scan → Manager(three-loop) → gates；A2A；watchdog；freely-db
   ↓
执行面（TDD）：Worker(dev) → RED → 实现 → test-pre-merge(GREEN) → Reviewer
   ↓
基座面：ACP harness（Claude/Codex/OpenCode/Cline）+ GitHub/Gitee
```

关键连线：

- 人 → 界面 → 规格：issue/chat 先变成 raw issue，不是直接派工。
- 规格 → scan：docs 是 scan 的输入，scan 产出 stage/next_action。
- 规格 → Manager/Worker：PRD/pre-tests 是任务与验收依据。
- 规格 → gates：IBM/TDD/review/merge 都检查文档与证据。
- Manager → Worker：A2A task 派工。
- Worker → tools → harness：命令/脚本/skill/MCP 最终落到 ACP 会话。
- Worker/测试 → gates：测试证据进入 PR/merge 门禁。
- gates → platform：PR/merge 是对外写侧。

## 4. 图的设计取舍

- 保留五个平面，但只画主路径；`scan`、`Manager`、`gates` 不展开内部步骤，避免变成流程图。
- `Reviewer` 与 `Test lane` 分开放：Reviewer 审产物，Test lane 跑验收，两者不是同一件事。
- `tools` 与 `harness` 分开：commands/scripts/skills/MCP 是工具面，ACP 是执行基座。
- `platforms` 与 `interfaces` 分开：平台是外部工作界面，interfaces 是 Freely 的入口抽象。
- 不把 A2A 画成中心：A2A 是协调协议，不是真相源；真相在 docs。

## 4.1 最终取舍：主图用交付闭环，五平面做分层辅图

只画五平面仍然回答不了“B1/B2 产出什么、谁读、怎么循环”。所以 README 主图改为**交付闭环**：

```
人 → issue/chat → B1-IBM → B2-IBM → SDD/TDD 文档
   → Manager 派工 → Worker 按文档实现 → Reviewer 独立验收
   → PR/merge/closeout → 回到 auto-loop
```

五平面图保留为“系统分层”辅图：

- 主图回答“交付怎么走、角色在哪”。
- 辅图回答“系统由哪些面组成、runtime/tools/harness 在哪”。

这样既不把 B1/B2 误画成 runtime 组件，也不让五平面图替代交付语义。

## 5. 仍需在后续轮次确认的问题

1. **已确认**：GUI 目前是 Tauri probe（`src-tauri/` 只暴露 probe bridge），README 已改为“CLI 主入口 / TUI / GUI（Tauri probe）”。
2. TUI 与 CLI 是否共享同一 core contract，还是 TUI 只是轻壳？需要看 `bin/freely tui` 与 `src/` 实现。
3. `scan` 是否所有来源都先落 docs，还是 chat/worktree 有例外？README 图用“docs 是真相”是规范目标，需确认实现一致性。
4. MCP 在 Freely 中是“可接”还是“已接”？README 只应写已支持的能力。
5. 多项目 fleet 是否属于产品面，还是内部运维工具？决定 README 是否把它放在架构图里。

这些不是 README 文案问题，是产品事实问题；后续轮次要用运行验证，而不是只读文档。

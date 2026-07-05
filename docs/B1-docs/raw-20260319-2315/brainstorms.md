# 研究：CLI TUI 人类插话输入框

## Context

- 日期：2026-03-19 23:15 PDT
- 触发：Freely 已经具备 `human interruption` 的 CLI-first intake 最小闭环，但实际人类入口仍然偏脚本化。当前需要一层真正可用的 CLI 应用 TUI，让用户启动后立刻看到输入框，输入内容即作为 interruption 进入 Freely。
- 当前已知事实：
  - `freely intake chat` 已可 durable 记录 raw interruption。
  - 主管已具备 `notice -> claim -> choose reaction -> delegate skill -> resolve` 的基本链路。
  - `human-interruption-handling` 已作为 skill 真源存在。
  - 但真实用户入口仍缺少一个“打开就能输入”的前台体验。

## 主问题

需要回答的不是“是否要做 TUI”，而是：

1. TUI 在 Freely 中属于什么角色边界，如何保持 `CLI first` 而不绕过现有 intake 能力。
2. 第一个最小可用界面应长什么样，才能让“输入一句话就当插话”成立。
3. 中文输入、中文展示、终端宽度与光标编辑需要满足什么最低要求。
4. TUI 应只做输入与状态展示，还是也允许处理 claim / resolution / worker handoff。

## 已形成的判断

### 1. TUI 不是第二套入口系统，而是 `freely intake chat` 的前端

TUI 的正确站位应是：

- 一个 CLI 应用形态
- 一个 `freely intake chat` / `freely intake status` / `freely baseline-status` 的交互壳
- 一个帮助人类稳定插话的前端

它不应成为：

- 绕过 `.freely/intake/**` 的特殊消息总线
- 直接向某个 AI 会话注入 prompt 的捷径
- 一个新的长期状态事实源

因此最小原则必须是：

- 所有人类输入最终仍调用同一条 intake 能力
- TUI 自己不发明新的持久化协议
- 主管仍然只看 `.freely/intake/**` 与相关 resolution artifacts

### 2. 第一版 TUI 应该极简，不要一上来做全屏 IDE

第一版最重要的是“插话可用”，不是“像 IDE 一样无所不能”。

建议第一版只做三块：

1. 顶部状态条
- 当前 project
- manager/supervisor 状态
- active intake 数量
- 最近一次 claim/resolve 摘要

2. 中间滚动视图
- 最近 intake items
- 最近 resolution 摘要
- 可选显示当前 manager 提示中的关键 supervision alerts

3. 底部输入框
- 默认聚焦
- 输入后按 Enter / Ctrl+Enter 提交为 interruption
- 支持多行编辑

若第一版没有一个稳定可用的底部输入框，TUI 就没有完成它的首要使命。

### 3. 中文支持不是附加项，而是第一版门槛

因为用户明确要在输入框直接输入中文，所以第一版必须满足：

- UTF-8 输入与显示
- 全角字符宽度正确计算
- 光标移动不因中文字符错位
- 多行换行时不破坏中文内容
- intake 持久化后仍保留原始中文内容

最低验收应包括：

- 在输入框输入纯中文
- 中英混排
- 标点与换行
- 提交后 `message.txt` 与 TUI 展示一致

### 4. 第一版 TUI 的输入语义应直接等价于“插话”

启动后，用户默认在做一件事：

- 向 Freely 插话

因此底部输入框默认应等价于：

`freely intake chat --project <project> --channel tui --author human --message <text>`

这带来两个直接好处：

- 用户不用先理解 `claim` / `resolve`
- TUI 不会因为“想做更多”而破坏现有 human interruption 架构

### 5. TUI 第一版不应让人类直接 claim / resolve

虽然技术上可以在 TUI 中加按钮，但第一版不应这样做。

原因：

- `claim` / `resolve` 属于主管与 specialized AI 的处理职责
- 若人类界面直接做这些动作，会模糊 manager contract
- 会让 TUI 同时变成“操控台”和“输入框”，增加语义混乱

因此建议第一版只允许：

- 输入 interruption
- 查看 queue / resolution / status

不允许直接：

- claim
- choose reaction
- resolve
- override absorption target

### 6. 第一版 TUI 的推荐布局

建议如下：

```text
+----------------------------------------------------------------------------------+
| Freely | project: freely | manager: running/down | intake: 3 pending            |
+----------------------------------------------------------------------------------+
| Intake Queue                                                                     |
| - [delegated][followup] 20260319-230648-cli-freely-cli-tui ...                  |
| - [new] ...                                                                      |
|                                                                                  |
| Recent Resolutions                                                               |
| - discovery -> docs/B1-docs/raw-...                                          |
| - continuation -> docs/epics/...                                                 |
|                                                                                  |
| Supervisor Snapshot                                                              |
| - expected running but down: none                                                |
| - current focus: workspace routing foundation                                    |
+----------------------------------------------------------------------------------+
| Interruption Input                                                               |
| >                                                                                |
|   现在需要设计 CLI，至少有个输入框...                                            |
|                                                                                  |
| Enter: submit  Alt+Enter: newline  Ctrl+C: quit                                  |
+----------------------------------------------------------------------------------+
```

关键点：

- 输入框必须始终明显可见
- 用户不必切屏或切模式才能插话
- 中间区只展示最必要的状态，不要抢输入框的注意力

### 7. 提交交互建议

建议第一版采用：

- `Enter`：提交单行或当前内容
- `Alt+Enter`：插入换行

若终端兼容性不稳定，可退化为：

- `Ctrl+S`：提交
- `Enter`：普通换行

但不建议把提交动作设计得太隐蔽，否则会直接损伤“插话感”。

### 8. TUI 技术实现边界

无论使用什么终端 UI 技术栈，第一版都必须遵守：

- UI 层只负责收集输入与展示状态
- 提交时调用现有 `freely intake chat`
- 队列显示来自 `freely intake status`
- 项目状态来自 `freely baseline-status`

更进一步的实现建议：

- 把 TUI 做成 `freely tui --project <abs_path>`
- 内部仍调用 runtime/freely 的既有子命令
- 不在 TUI 层复制业务规则

这样可以保持低耦合：

- runtime 是能力真源
- TUI 是 presentation shell

### 9. 第一版不需要先做全自动桥接聊天会话

当前的目标是：

- 有一个稳定输入框
- 输入后 durable 进入 Freely
- 主管能够看到

还不是：

- 自动接管外部聊天平台
- 自动在 TUI 内嵌完整 AI 对话会话

因此第一版更像：

- interruption terminal

而不是：

- fully interactive AI IDE

### 10. 与 human interruption 架构的对齐

这条 TUI 设计必须完全服从已经建立的人类插话架构：

- raw input -> `.freely/intake/**`
- manager notice / claim
- `skill:human-interruption-handling`
- resolution artifact
- canonical absorption

TUI 只替换“人怎么发出插话”，不替换后面的处理链。

## Open Questions

1. TUI 应该内嵌在 `./bin/freely` 下，还是单独做成 `./bin/freely-tui`，再复用 runtime 子命令？
2. 第一版是否需要显示 resolution artifact 摘要，还是只显示 intake queue 足够？
3. 中文输入框若使用现有 TUI 库，是否存在全角字符光标错位风险，需要单独验证哪一套库最稳？
4. 是否要为输入框增加“当前输入仅作为 interruption”这一显式提示，避免用户误以为这是直接对 AI 会话说话？
5. TUI 是否要支持 `--project` 外的项目切换，还是第一版先只服务当前已启动项目？

## 初步结论

- 这项需求应先 materialize 为一个新的 pre-brainstorm，而不是直接写 UI 代码。
- 第一版目标不是“大而全的 Freely 终端”，而是“有输入框的 interruption TUI”。
- 最小可交付应是：
  - `freely tui --project ...`
  - 顶部状态条
  - 中间 intake/status 列表
  - 底部输入框
  - 中文输入与展示正确
  - 提交后走现有 `freely intake chat`
- 第一版不应越权承担 manager 的 claim / resolve 职责。

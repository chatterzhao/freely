# 研究：Freely 管理用户项目时的 Git Hook 安装模式

## Context

- 日期：2026-03-06 00:16 UTC
- 触发：Freely 后续将负责管理用户项目，需要给用户项目安装并维护 Git hooks。
- 已确认方向：
  - 默认在用户项目下生成 `.freely/.githooks/`
  - 默认将 `core.hooksPath` 指向 `.freely/.githooks/`
  - Freely 前端提供开关，可关闭该模式并改用 `.git/hooks`
  - 用户若不满意 Freely 管理模式，可复制 hooks 到 `.git/hooks` 自行维护，且不再受 Freely 升级影响

## 要解决的问题

1. Freely 需要版本化、可升级、可审计地管理 hooks，但不能把用户永久锁死在 Freely 的托管模式里。
2. `.git/hooks` 不是版本化目录，适合用户自行接管；`.freely/.githooks/` 则更适合 Freely 生成和升级。
3. 需要明确：
   - 默认模式是什么
   - 切换开关的行为是什么
   - Freely 升级时会改哪些文件
   - 用户复制后哪些内容不再被 Freely 覆盖

## 初步分层

### 模式 A：Freely 托管模式（默认）

- hooks 实际文件位于：`<project>/.freely/.githooks/`
- Git 配置：`git config core.hooksPath .freely/.githooks`
- 特点：
  - Freely 可升级、覆盖、修复、审计
  - 与项目业务文件分离
  - 更适合产品化管理

### 模式 B：项目原生模式（用户接管）

- hooks 实际文件位于：`<project>/.git/hooks/`
- Git 配置恢复默认或指向 `.git/hooks`
- 特点：
  - 用户可直接修改
  - Freely 不再自动覆盖这些 hooks
  - 后续 Freely 升级不会影响用户自定义内容

## 关键语义

1. `.freely/.githooks/` 是 Freely 的托管资产目录，不等同于用户自定义目录。
2. 前端开关不是“简单换路径”，而是“切换托管责任”：
   - 开启：Freely 负责生成、更新、校验
   - 关闭：Freely 停止托管，用户自行负责
3. 如果用户希望基于 Freely 当前模板做二次修改，应提供“复制到 `.git/hooks` 并切换为用户接管模式”的明确指引。

## 候选方案

### 方案 A：单一托管模式

- 只允许 `.freely/.githooks/`
- 不提供切换到 `.git/hooks`

问题：
- 用户逃生路径弱
- 一旦对 Freely 生成的 hooks 不满意，只能直接改托管目录，升级时容易被覆盖

### 方案 B：默认托管 + 可切换到用户接管

- 默认使用 `.freely/.githooks/`
- UI 提供“切换为项目原生 hooks”开关
- 切换时提供复制或迁移指引

优点：
- 兼顾产品化升级与用户主权
- 行为边界清晰
- 容易解释给用户和 AI

### 方案 C：双写同步

- Freely 同时维护 `.freely/.githooks/` 和 `.git/hooks`

问题：
- 容易出现双源漂移
- 用户难以判断哪个是事实源
- 升级覆盖风险更高

## 初步倾向

倾向方案 B：
- `.freely/.githooks/` 作为 Freely 默认事实源
- `.git/hooks` 作为显式退出托管后的用户事实源
- 两者不做长期双写同步

## 需要进一步明确的点

1. 切换到 `.git/hooks` 时是否自动复制当前 Freely hooks 模板。
2. Freely 是否需要在 `.freely/` 下记录当前 hooks 模式，如 `managed` / `user-owned`。
3. `doctor` / 前端设置页是否需要提示：
   - 当前 hooks 来源
   - 是否受 Freely 升级影响
   - 如何切回托管模式
4. 当用户切到 `.git/hooks` 后，Freely 是否仍做只读检查而不自动修复。

## 结论

该议题需要进入后续治理与产品设计收敛，已具备 issue-ready 条件。

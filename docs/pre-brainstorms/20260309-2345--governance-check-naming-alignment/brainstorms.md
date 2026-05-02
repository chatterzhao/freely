# 研究：治理检查命名与残留收敛

## Context

- 日期：2026-03-09 23:45 UTC
- 触发：仓库主流程已经切换到 `pre-brainstorm -> IBM -> dev-loop`，但仍保留 `bmad-check` 命令名、脚本文案与部分旧目录测试夹具，命名与当前项目语义不一致。
- 用户判断：当前应用里已经不再使用 `bmad`；工作路径更接近 “pre-b 产出 issue，再进入 IBM/issue-bound brainstorm 分析并产出 map” 的两次 brainstom 闭环，不应再让遗留缩写污染入口命名。
- 约束：本次改动属于治理/命名收敛，不只是字符串替换。需要同时处理命令名、脚本真源、README/AGENTS 入口文案、测试夹具以及文档中对旧概念的误导性表述。

## 现状观察

1. 正式流程名已经不是 BMAD
- `docs/PROJECT_INTENT.md`、`docs/LAWS.md` 与 workspace skills 的主路径均使用 `pre-brainstorm`、`IBM`、`dev-loop`。
- `bmad` 未作为当前正式方法论术语存在，只在 `bmad-check` 这一治理脚本名和少量历史记录中残留。

2. `bmad-check` 的职责其实是治理检查，不是流程执行
- 当前脚本检查的是：核心治理文档存在、`pre-brainstorms/**` 结构完整、candidate 关键字段齐全。
- 这类职责跨越 pre-brainstorm/IBM/dev-loop，不属于某一阶段本身，因此不应拿阶段名来命名。

3. `bibm` 不适合作为替代名
- 它试图把两段流程强行压成一个内部缩写，但缺乏自解释性。
- 对命令入口、README、人类协作与 AI 工具提示都不够清晰。

4. 旧目录残留仍在测试中
- 部分测试仍构造 `docs/brainstorms`、`docs/planning`、`docs/validation`、`docs/continuity`。
- 这类残留比历史 pre-brainstorm 文档里提到 `bmad-check` 更危险，因为它会继续为未来实现提供过时夹具。

## 命名目标

新名称应同时满足：

1. 表达“治理一致性检查”，而非某个执行阶段。
2. 能覆盖当下的文档完整性检查，也能覆盖未来部分下沉到 hook 的门禁。
3. 与项目现有层次一致：
- 流程阶段：`pre-brainstorm` / `IBM` / `dev-loop`
- 技能层：`skills`
- 门禁层：`check` / `gate`
4. 对人类与 AI 都足够直白，不依赖内部黑话。

## 候选比较

### 1. `governance-check`

优点：
- 直接表达“治理检查”
- 不与任何单一流程阶段冲突
- 可以自然延伸到 `governance-gate`
- 与宪法/法律/skills/hooks 的分层一致

缺点：
- 语义比 “文档检查” 更宽，但这其实符合当前脚本真实职责

结论：
- 作为首选名

### 2. `workspace-check`

优点：
- 和 `docs/system/workspace/**` 分层贴近
- 暗示这不是单纯文档检查

缺点：
- 容易被理解为环境/依赖/worktree 健康总检查，边界过宽

结论：
- 可作备选，但不如 `governance-check` 准确

### 3. `route-check`

优点：
- 强调流程路由一致性

缺点：
- 太窄，覆盖不了核心文档存在性与字段契约检查

结论：
- 不采用

## 收敛结论

1. `bmad-check` 正式重命名为 `governance-check`。
2. 相关脚本真源、bin 包装、README/AGENTS 文案、脚本输出文案全部改为 `governance-check` / `governance gate` 语义。
3. 历史 pre-brainstorm 中作为“当时记录”的 `bmad-check` 提及可以保留，但若用于描述当前事实，应改写为“现已收敛为 `governance-check`”。
4. 测试夹具中旧目录结构应一并迁移，避免继续为未来开发提供过时基线。
5. 不引入 `bibm` 作为新正式术语；正式流程仍使用 `pre-brainstorm -> IBM -> dev-loop`。

## 本次实施边界

- 改命令：`./bin/bmad-check` -> `./bin/governance-check`
- 改脚本真源文件名与成功/失败文案
- 更新 README、AGENTS、脚本说明中的入口命名
- 迁移直接依赖旧目录结构的测试夹具
- 仅保留历史记录性质的 `bmad-check` 文本；如某处在陈述当前机制，则同步更新为新名

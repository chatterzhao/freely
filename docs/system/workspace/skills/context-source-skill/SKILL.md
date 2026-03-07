---
name: context-source-skill
description: 对调用方传入的当前输入包做来源适配、上下文判定、usable issue 判断与下一跳提示词组装，为 lead-agent 产出自治编排结果。
---

# skill:context-source-skill

## 适用边界

- 处理首跳来源识别、需求池扫描、优先级判断、路由判定与下一跳提示词组装。
- 不直接执行业务型 doc/dev-loop。
- 不替代 milestone、issue、progress 的长期状态维护，只产出当前回合的判定结果、建议更新与下一跳编排输出。
- 输入包由调用方传入；本 skill 只消费传入输入，不在 skill 内凭空生成新的起始任务。

## 输入

- 调用方传入的 `input_context`
- 调用方显式附带或指向的：
  - `docs/PROJECT_INTENT.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - `workspace/tools.md`
- 按需读取调用方已指明的补充证据：
  - `docs/pre-brainstorms/**`
  - issue / progress / recovery 证据
  - chat 或 session evidence

## 调用约定

- `lead-agent` 必须把当前回合需要处理的输入包交给本 skill。
- 输入包至少应包含：
  - `source_input`
  - `source_type` 或可推断来源
  - `milestone_path`
  - `tools_path`
  - 当前已知的 issue / progress / recovery 指针
- 本 skill 可以在传入路径范围内继续读取上下文，但不负责自己决定“本轮要处理哪个新输入”。

## 工作流

1. 从调用方传入的 `input_context` 开始，识别当前这一轮要处理的来源。
2. 在调用方给定的上下文范围内扫描需求池：
   - `docs/milestones.md`
   - progress / recovery
   - story-scoped `code-reviews` / test
   - chat / github-issue
   - `docs/PROJECT_INTENT.md`
3. AI 基于当前输入包自主判断此刻优先查看哪个池，而不是由脚本硬编码固定顺序。
4. 识别当前输入来源：
   - 新问题输入：intent / code-review / test / chat / github-issue
   - 延续输入：milestone / issue / progress / recovery
5. 先从 `docs/milestones.md` 查找是否已有匹配条目。
6. 对命中的条目判定是否为 usable issue：
   - `committed_issues` 中且顺序明确 -> usable
   - `candidate_issues` 中仍需研究或排序 -> not usable
   - `completed_issues` 中 -> 不重复执行，转 completion verification 或回流
7. 若 milestone 未命中，再检查：
   - 是否已有 issue path
   - 是否已有 progress / recovery 记录
   - 是否只是 pre-brainstorm candidate
8. 先做边界判定，再决定路径：
   - 无稳定 issue 边界 -> `pre-brainstorm`
   - 已有关联 issue，但需要在既有 issue 边界内继续脑暴 -> `issue-bound brainstorm`
   - 已有稳定 issue 且可继续推进 -> `issue continuation`
9. 结合 `tools.md` 判断当前任务强度与工具适配：
   - 路由/预研/文档收敛优先考虑更适合长 prompt 编排的工具
   - 命中 usable issue 后的仓库实现优先考虑更适合工程执行的工具
   - 不在规则中硬编码唯一工具，而是让 AI 基于当前输入做解释性选择
10. 组装下一跳 prompt，prompt 至少包含：
   - `<source input>`
   - `docs/milestones.md` 路径
   - 需要阅读的 workspace 相对路径，例如 `workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
   - 当前为何选择该工具
   - 进入 doc-loop / dev-loop / pre-brainstorm 的边界要求
11. 产出下一跳：
   - `pre-brainstorm` -> `skill:doc-pre-brainstorm-execution`
   - `issue-bound brainstorm` -> `skill:doc-ibm-execution`
   - `issue continuation`
     - 若当前缺文档 / 缺 `PRE_TEST` / 缺 mapping -> `skill:doc-ibm-execution`
     - 若 issue 已 ready/in-progress 且文档足够 -> `skill:dev-loop-execution`
12. 如发现治理口径漂移，要求在下一跳中补齐对应治理资产。

## 输出

- `source_type`
- `matched_milestone`
- `usable_issue: true|false`
- `route_kind`
- `selected_tool`
- `why_selected`
- `next_skill`
- `recommended_route`
- `next_prompt`
- `required_updates`

## 判定原则

- milestone 是主动扫描层，不是纯报表。
- `pending://milestone-binding` 只能是短暂过渡态。
- 已有 issue path 不代表直接进入 dev-loop；仍要结合文档完整度、状态和证据决定。
- chat / code-review / test 这类外部输入，若尚未进入正式 issue 体系，先回到 pre-brainstorms 收敛。
- 核心产出是“提示词组装与工具选择建议”，不是 shell 里的硬编码路由。
- AI 应理解后路由，而不是按脚本分支表机械跳转。
- `test` / `code-review` / `chat` 不得因为来源名直接硬编码路径，必须先判断 issue 边界。

## 完成

- `lead-agent` 获得可执行的下一跳决定。
- 当前回合需要更新的 candidate / milestone / issue 状态已被显式指出。
- 下一跳外部 AI 工具与 prompt 已被组装出来。
- 若进入 `doc-pre-brainstorm-execution`，主产物应是 candidate + milestone 同步。
- 若进入 `doc-ibm-execution`，主产物应是 issue-bound `IBM+G` 产物与 milestone 同步。
- 若进入 `dev-loop-execution`，主产物应是代码 / 测试 / progress / milestone 回写。

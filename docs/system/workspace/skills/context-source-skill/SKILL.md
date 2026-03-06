---
name: context-source-skill
description: 对当前输入做来源适配、上下文读取、usable issue 判定与下一跳提示词组装，为 lead-agent 产出 AI 自治编排结果。
---

# skill:context-source-skill

## 适用边界

- 处理首跳来源识别、路由判定与下一跳提示词组装。
- 不直接执行业务型 doc/dev-loop。
- 不替代 milestone、issue、progress 的长期状态维护，只产出当前回合的判定结果、建议更新与下一跳编排输出。

## 输入

- `input_context`
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/milestones.md`
- `workspace/tools.md`
- 按需读取：
  - `docs/pre-brainstorms/**`
  - issue / progress / recovery 证据
  - chat 或 session evidence

## 工作流

1. 识别当前输入来源：
   - 新问题输入：intent / review / test / chat / github-issue
   - 延续输入：milestone / issue / progress / recovery
2. 先从 `docs/milestones.md` 查找是否已有匹配条目。
3. 对命中的条目判定是否为 usable issue：
   - `committed_issues` 中且顺序明确 -> usable
   - `candidate_issues` 中仍需研究或排序 -> not usable
   - `completed_issues` 中 -> 不重复执行，转 completion verification 或回流
4. 若 milestone 未命中，再检查：
   - 是否已有 issue path
   - 是否已有 progress / recovery 记录
   - 是否只是 pre-brainstorm candidate
5. 结合 `tools.md` 判断当前任务强度与工具适配：
   - 路由/预研/文档收敛优先考虑更适合长 prompt 编排的工具
   - 命中 usable issue 后的仓库实现优先考虑更适合工程执行的工具
   - 不在规则中硬编码唯一工具，而是让 AI 基于当前输入做解释性选择
6. 组装下一跳 prompt，prompt 至少包含：
   - `<source input>`
   - `docs/milestones.md` 路径
   - 需要阅读的 workspace 相对路径，例如 `workspace/skills/no-usable-issue-skill/SKILL.md`
   - 当前为何选择该工具
   - 进入 doc-loop / dev-loop / pre-brainstorm 的边界要求
7. 产出下一跳：
   - 无 usable issue -> `skill:no-usable-issue-skill`
   - 有 usable issue 但文档未完备 -> `skill:has-usable-issue-skill` 并优先导向 `doc-loop-execution`
   - 有 usable issue 且已具备执行条件 -> `skill:has-usable-issue-skill` 并导向 `dev-loop-execution`
8. 如发现治理口径漂移，要求在下一跳中补齐对应治理资产。

## 输出

- `source_type`
- `matched_milestone`
- `usable_issue: true|false`
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
- chat / review / test 这类外部输入，若尚未进入正式 issue 体系，先回到 pre-brainstorms 收敛。
- 核心产出是“提示词组装与工具选择建议”，不是 shell 里的硬编码路由。
- AI 应理解后路由，而不是按脚本分支表机械跳转。

## 完成

- `lead-agent` 获得可执行的下一跳决定。
- 当前回合需要更新的 candidate / milestone / issue 状态已被显式指出。
- 下一跳外部 AI 工具与 prompt 已被组装出来。
- 若进入 `no-usable-issue-skill`，主产物应是 candidate + milestone 同步。
- 若进入 `has-usable-issue-skill`，主事实源应切换到 milestone + issue + progress。

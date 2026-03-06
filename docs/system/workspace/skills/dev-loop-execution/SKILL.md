---
name: dev-loop-execution
description: 执行 `DDD` 开发环，负责在已完成 docs 收敛的 issue/story 上下文中实现、测试，并把状态回写给 auto-loop。
---

# skill:dev-loop-execution

## 职责

- 负责在已完成 docs 收敛的 issue/story 上下文中实现、测试并回写状态。
- 负责把代码、测试、progress、milestone、issue 状态保持一致。
- 负责在测试或评审暴露问题时，判断是否仍留在当前 issue 边界内。
- 不负责重新发明 issue 边界；边界失稳时应回流给 `auto-loop` 重判。

## 进入条件

- 当前 issue 已有完整或足够完整的 `doc-loop` 产物。
- 当前回合主要工作是实现、测试、评审修复和状态回写。

## 输入上下文

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`
- `docs/milestones.md`
- 按需读取：
  - `docs/progress/{epic}/p-{issue}.md`
  - recovery 记录
  - review / test 结果

## 工作产物

- `src/**`
- `tests/**`
- `docs/progress/{epic}/p-{issue}.md`
- `docs/milestones.md`
- 对应 issue 状态文档
- 按需更新：
  - 恢复记录
  - review / test 证据

## 工作步骤
1. 阅读治理文档和 issue 上下文。
2. 实现前，定义当前周期的语义范围，避免在单次提交中混合不相关关注点。
3. 在正确的功能 worktree 中实现变更。
4. 如果代码和文档不一致，优先代码/测试修正路径。
5. 开发和评审期间，持续根据实现和发现的缺陷添加/调整测试用例。
6. push/merge 前，执行语义提交边界复查；如仍有混合关注点则拆分提交。
7. 运行必需的测试，包括集成验收测试，将 `TEST` 结果作为合并/提升证据。
8. 用测试证据更新：
   - `docs/progress/{epic}/p-{issue}.md`
   - `docs/milestones.md`
   - 对应 issue 状态文档
9. 用 `skill:laws-enforcer` 和 `skill:constitution-guard` 验证闭环。

## 不负责

- 不直接承担 issue-bound brainstorm、mapping、`PRE_TEST` 重建等 docs 主工作。
- 不把超出当前 issue 边界的新问题伪装成当前 issue 的实现细节。

## 状态回流给 auto-loop

当出现以下任一情况时，应把状态交还 `auto-loop`：

- 当前实现已完成
- 当前仍需继续 dev work
- 当前被阻塞
- 测试 / review / chat 暴露的问题已超出当前 issue 边界
- 当前 issue 需要补 docs，必须回到 `doc-ibm-execution`

回流时最少应提供：
- `status`: `in_progress | blocked | reroute_required | completed`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`

语义要求：
- 若缺 docs 或 `PRE_TEST`，`next_recommended_route` 设为 `doc-ibm-execution`
- 若发现是新问题或边界外问题，`next_recommended_route` 设为 `doc-pre-brainstorm-execution` 或标记为 `reroute_required`
- 若只是未完成实现，则保持 `dev-loop-execution`

## 完成判定
- 代码、测试和文档状态更新已对齐且可验证。

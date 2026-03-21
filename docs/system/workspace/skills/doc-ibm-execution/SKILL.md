---
name: doc-ibm-execution
description: 在法律和宪法下执行 milestone-owned issue 的 `IBM+G` 文档收敛。
---

# skill:doc-ibm-execution

## 职责

- 只处理 milestone 已接纳的 issue。
- 先确定正式目录归属，再把 issue 从“docs 不足”推进到“ready for dev”或“明确阻塞”。
- 同步 issue、milestone 与治理资产。
- `IBM + G` 作为 doc-loop 的一部分，其循环归宿与生命周期细节以 `docs/system/workspace/three-loop-capability-lifecycle.md` 为准。

## 不负责

- 不把 raw problem 直接当作 IBM issue。
- 不直接承担实现代码、测试与 progress 主回写。

## 工作流

1. 先读取 [issue-materialization-checklist.md](references/issue-materialization-checklist.md) 确认当前输入已经是 milestone-owned issue，且正式目录归属稳定。
2. 补齐 IBM 产物时，`prd.md` 不得只停留在人类摘要；必须按 [prd-quality-bar.md](references/prd-quality-bar.md) 达到 AI-ready 的最小结构。
3. 若 IBM 产物缺失或不完整，按 [ibm-completion-gate.md](references/ibm-completion-gate.md) 补齐 issue、brainstorm、`prd.md`、`pre-tests.md`、`tasks.md` 与 milestone 回写。
4. `pre-tests.md` 和 `tasks.md` 必须从 `prd.md` 自然派生；若三者之间仍需大量口头补充，视为 IBM 未收口。
5. 在 IBM 中继续深化验收边界：
   - 把 candidate-level acceptance 转成 issue-level acceptance
   - 让 `pre-tests.md`、`tasks.md` 和 issue-bound brainstorm 体现这层深化
6. 若文档已经足够驱动实现，按同一 gate 把 `phase_state` 切到 `done_ibm`，并返回最小实现上下文。
7. 若在 IBM 中发现边界外新问题，停止扩写当前 issue，返回 `next_recommended_route=doc-pre-brainstorm-execution`。

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`
- `execution_base`
- `integration_target`
- `depends_on`

## 完成判定

- 当前 issue 已明确属于 milestone-owned issue。
- 关键 IBM 产物完整，或已明确为什么必须 reroute。
- `prd.md` 已达到 AI-ready quality bar，且 `pre-tests.md`、`tasks.md` 与之对齐。
- candidate acceptance 已被深化为 issue-level acceptance。
- 进入 dev-loop 所需的最小上下文已备齐。

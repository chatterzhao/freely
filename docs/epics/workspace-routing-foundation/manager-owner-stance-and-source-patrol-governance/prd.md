# PRD: manager-owner-stance-and-source-patrol-governance

## Problem

Freely 当前已经有 manager / worker / interruption / patrol 的分散真源，但仍缺少一条更高层的一致表达：

- 开发 Freely 的治理输入不能直接充当产品化后的运行期角色真源
- 产品能力真源里还没有把 manager owner stance、advisory interruption semantics 与 source-patrol completeness 一起写清

结果是 AI 容易把开发期治理文档误读成运行期角色合同，或在面对插话和 source drift 时回退成“继续问人”而不是主管自己做项目级判断。

## Goal

让 Freely 的产品能力真源能够独立表达：

1. manager 是项目主人
2. worker 是受委派的核实/执行者
3. human interruption 是 advisory signal
4. standing-source patrol 需要覆盖 interruption、milestone、progress、pre-brainstorm
5. source drift 的默认处理是补账、核实、重排、委派

## Non-goals

- 不改写开发 Freely 的治理输入来充当运行期角色真源
- 不新增第四层 loop
- 不实现新的 runtime / watchdog / dispatcher 机制
- 不重复定义已有的 restart-point routing 或 delegation threshold

## Required Outcome

1. `manager-agent` 明确项目主人姿态与默认决策方式。
2. `worker-agent` 明确只负责核实 / 执行 / 回证，不接管项目级裁决。
3. interruption 相关 skill 明确 advisory signal semantics。
4. patrol / routing 相关 skill 或 reference 明确 source-patrol completeness contract。
5. 各文件之间的 wording 保持一致，不再需要靠读者自行拼接。

## Eval Plan

- Truth-source review:
  - 是否明确区分治理输入与产品能力真源
  - 是否明确写出 manager / worker / interruption / patrol 的新边界
  - 是否仍与已有 issue 的真源发生重叠或冲突
- Dogfood acceptance:
  - 后续使用 `freely chat` / manager patrol 思考这类问题时，主管能更稳定地把插话视为 signal，并按 source completeness 做补账或委派

# Pre-Tests: manager-owner-stance-and-source-patrol-governance

## Pre-merge acceptance

1. `manager-agent` 单独阅读时，能看出：
   - manager 是项目主人
   - manager 默认自己做全局判断
   - 只有高风险缺少外部事实时才追问人
2. `worker-agent` 单独阅读时，能看出：
   - worker 只负责核实 / 执行 / 带回 evidence
   - worker 不接管项目级方向裁决
3. interruption 相关 skill 单独阅读时，能看出：
   - human interruption 是 advisory signal
   - 是否打断、并行、排队、冻结由 manager 判断
4. patrol / routing 相关 skill 或 reference 单独阅读时，能看出：
   - standing-source patrol 至少覆盖 interruption、milestone、progress、pre-brainstorm
   - source drift 的默认动作是补账、核实、重排、委派
5. 单独阅读这些产品能力真源时，不会再把 `PROJECT_INTENT / CONSTITUTION / LAWS` 误当成运行期角色真源。

## Post-merge acceptance

1. 在 `develop` 上继续通过 `freely chat` 观察 manager 处理插话时，检查其默认 reasoning 是否更接近：
   - 先自行理解与全局安排
   - 再决定 direct answer / queue / freeze / worker delegation
2. 在巡检 stale source 时，检查 manager 是否更自然地把 interruption / milestone / progress / pre-brainstorm 一并视为 standing-source completeness 面，而不是只盯单一 source。

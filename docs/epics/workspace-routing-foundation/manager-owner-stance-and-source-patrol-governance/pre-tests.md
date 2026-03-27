# Pre-Tests: manager-owner-stance-and-source-patrol-governance

## Acceptance Structure

### Pre-merge focused regression / smoke

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

### Post-merge integration acceptance

1. 在 `develop` 上继续通过 `freely chat` 观察 manager 处理插话时，检查其默认 reasoning 是否更接近：
   - 先自行理解与全局安排
   - 再决定 direct answer / queue / freeze / worker delegation
2. environment:
   - `develop`
   - protected verification worktree
3. evidence:
   - 新 continuity / prompt / reply wording 能体现主管先做全局判断
4. failure signal:
   - 主管仍默认把项目级不确定性直接回抛给插话者
5. failure handling / replay expectation:
   - 若失败，回到来源 feature worktree 或新 feature worktree 修正真源，不在 protected verification worktree 直接修实现

### Post-merge application-native real-environment acceptance

1. 在真实 Freely runtime 下观察 manager patrol / reactivation / interruption handling，检查 manager 是否更自然地把 interruption / milestone / progress / pre-brainstorm 一并视为 standing-source completeness 面，而不是只盯单一 source。
2. environment:
   - live Freely runtime on `develop`
3. evidence:
   - manager continuity、patrol reasoning、或 runtime-visible handoff wording 能恢复四类 source completeness 面
4. failure signal:
   - patrol reasoning 仍只盯单一 source，或把 source drift 当成默认追问用户的问题
5. failure handling / replay expectation:
   - 若失败，回到 feature worktree 修正文档真源，并重新在 `develop` runtime replay

### Post-merge end-to-end dogfood acceptance

1. 用一条真实 human interruption / continuation 场景观察 manager 是否把插话视为 advisory signal，并由主管自己决定 absorption、queue、freeze 或 worker delegation，而不是把用户原话当成调度命令。
2. environment:
   - `freely chat` against the canonical `develop` runtime
3. evidence:
   - continuity / response / delegated next step 体现 advisory-signal semantics 与 owner stance
4. failure signal:
   - 主管把插话者当成项目调度者，或直接要求插话者负责项目级澄清
5. failure handling / replay expectation:
   - 若失败，回到来源 feature worktree 或新 feature worktree 继续修正 truth source，再重新用 interruption 场景 replay

### Non-goals

1. 不在本 issue 中引入新的 runtime 机制或 watchdog 实现。
2. 不在本 issue 中把 source completeness 事务 machine-readable 化。

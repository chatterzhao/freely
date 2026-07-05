# Pre-tests: agent-ready-prd-for-freely-flow

1. 当前 IBM 产物明确区分 `B` 与 `PRD`：`B` 负责收敛与比较，`PRD` 负责执行控制面
2. `prd.md` 不只包含目标与产品面，还必须包含：
   - non-goals
   - non-negotiables
   - context pack
   - decomposition tree
   - prototype path
   - eval plan
   - execution slices
   - revisit triggers
3. 不依赖额外口头解释，AI 也能从 `prd.md` 派生本 story 的 `tasks.md`
4. `prd.md` 明确说明何时应该因模型、工具或用户行为变化而重判
5. 当前 IBM 产物足够让后续治理 issue 直接进入 dev-loop，而不需要重新做一轮大型研究

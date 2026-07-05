# Brainstorm: agent-execution-safety-review-and-security-decision-support

## Focus

把 execution-boundary review 与 security decision support 收成一条最小 capability owner。

## Key Ideas

1. 运行时不应只依赖单 agent 直觉判断执行边界。
2. 也不应因为存在风险就默认回退到人工逐步批准。
3. 更合适的能力是：
   - 先检查 tool flags / project config / injected policy / observed posture 是否一致
   - 再在需要时拉起一个或多个 reviewer agents
   - 形成内部 decision committee

## Intended Output

- a reusable execution-boundary review contract
- a reusable security decision support contract
- reviewer-backed continuation guidance
- non-blocking safeguard recommendations

## Boundary

本 issue 不拥有：

- Freely default autonomy posture
- product-facing activation consent wording
- global security umbrella decomposition

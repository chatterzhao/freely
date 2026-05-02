# 预研：legacy promoted candidate normalization

## Context

- 日期：2026-03-21
- 触发：在当前 sweep 做最终 review 时，发现一批 legacy pre-brainstorm candidate 仍写着 `status: promoted`，但 `promoted_issue_path` 仍是 `pending://issue-materialization`。
- 当前风险不在实现，而在治理真源：
  - 主管或 skill 读取到 `promoted` 时，会默认它已经进入 issue-bound 生命周期
  - 但 `pending://...` 又说明它从未真正 materialize
  - 这会制造“假 promotion”，让里程碑 / candidate / issue 生命周期出现伪闭环

## Problem

这批 legacy candidate 大多来自早期格式与方法论尚未稳定的阶段，问题主要分两类：

1. 方向被后续主线吸收，但从未回写为正式 issue path
2. 方向仍值得保留，但并没有真正达到 promotion gate

这两类都不该继续保留为：

```text
status: promoted
promoted_issue_path: pending://issue-materialization
```

因为这既不是已 materialize，也不是诚实的待研究状态。

## Normalization Principle

本轮采用保守规范化，不做大规模历史重写：

1. 只修“假 promotion”
- 若 candidate 没有真实 `promoted_issue_path`，就不再保留 `status: promoted`

2. 不伪造 issue 绑定
- 不因为想让表面更干净，就临时给它绑一个并不准确的 issue

3. 不在 promote-ready sweep 中重写整批 legacy 研究语义
- 这轮只做 lifecycle honesty 修复
- 若后续要真正做 legacy research reconciliation，应开独立治理线

## Proposed Action

- 对 legacy candidate 执行逐条 disposition，而不是一刀切：
  - 已被后续 issue / skill / constitution / laws 吸收：改为 `status: dropped`，并用 `adoption_type: superseded` 留痕
  - 方向仍可能有效但尚未达到 materialization gate：改为 `needs_research`
  - 仅在仍值得保留且尚无更好归宿时，回到 `proposed`

这样处理的好处：

- 不丢历史研究内容
- 不伪造 materialization
- 不会把已被主线吸收的候选错误地重新打开
- `governance-check`、milestone 审核与主管监督读取到的状态会更诚实

## Why Not Materialize Everything Now

不适合在当前 sweep 里把这些历史 candidate 全部物化成新 issue：

- 它们跨越多个早期主题和旧格式
- 其中不少已经被后续 issue / skill / laws 吸收
- 强行一次性 materialize 会制造新的重复 issue 和新的生命周期噪音

所以这轮最优解是：

- 先把假 promotion 去掉
- 后续如果需要，再单独做 legacy candidate reconciliation

## Expected Result

- 当前仓库中不再存在：
  - `status: promoted`
  - 且 `promoted_issue_path: pending://issue-materialization`

- 所有真正 promoted 的 candidate，都应该：
  - 指向真实 issue
  - 或已经在 milestone / issue 生命周期中可追踪

- 对历史候选的 disposition 更准确：
  - `status: dropped + adoption_type: superseded` 表示已被主线吸收
  - `needs_research` 表示还值得保留但不能假装已 materialize

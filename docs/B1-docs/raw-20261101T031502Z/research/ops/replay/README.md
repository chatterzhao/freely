# 研究回放证据

这些脚本是 B1 研究 spike，不接 runtime，不修改产品代码。

| 脚本 | 验证 | 运行 |
| --- | --- | --- |
| `intake_replay.py` | 六类事件归一化 + `event_id` 幂等 | `python3 intake_replay.py` |
| `handoff_replay.py` | 五类后续消息 owner/handback/停止/恢复 + 真实 issue #4070 两条评论 | `python3 handoff_replay.py` |
| `prompt_manifest.py` | 11 段 manifest、prefix hash 稳定、usage/cache 三态 | `python3 prompt_manifest.py` |
| `../spike/dsh-plugin-contract.ts` | DSH 插件 `inject`/`apply`/session API 静态编译 | 见 `dsh-freely-plugin-design.md` §2.4 |

## 结果摘要

- intake：10 行输入（5 事件 × 2 次）→ 5 行，`dedupe_ok=true`；真实 issue #4070 评论、`cli/cli#14879` PR review/CI 形状。
- handoff：new/active/completed/expired/cross-ticket/stop/worker-death/reviewer-3 轮全部断言通过；真实线程两条评论同一 Task。
- prompt：prefix hash `262d1e...` 在 tail 变化时不变；reported 80/20 → 0.8，estimated/absent → null。
- DSH：`pnpm typecheck` 通过；最小插件编译通过；未跑真实 host E2E。

## 限制

- 真实数据只用于事件形状/幂等；不是 Freely runtime 的端到端集成。
- PR review/CI 真实样本来自 `cli/cli#14879`，因为本 repo 历史 PR 无 review 数据。
- B2 必须用产品代码重跑这些场景，研究脚本不能替代验收。

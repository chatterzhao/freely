---
name: freely-mem9-continuity-bridge
description: >- 评估并约束 mem9 作为 Freely 可选连续性后端的接入边界。确保本地
  `docs/` 治理事实源始终优先于外部后端。

  Use when: 配置或排查 mem9 连续性后端，或本地与远端状态不一致。
  触发词："mem9"、"continuity backend"、"连续性后端"、"state sync"。
---

# skill:freely-mem9-continuity-bridge

## 职责

- 评估 mem9 是否适合作为 Freely 的可选 continuity backend。
- 明确哪些内容可以外部化，哪些必须继续保留在本地治理事实源。
- 给出 `local-only` 与 `local + mem9` 两种模式的切换边界。
- 为未来 runtime / doc-loop 集成提供最小、可追溯的接入约束。

## 不负责

- 不把 mem9 提升为 Freely 的正式治理事实源。
- 不替代 `docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/PROJECT_INTENT.md` 或 `docs/B1-docs/`。
- 不直接实现网络调用、鉴权或同步代码。

## 工作流

1. 先读取对应 issue 与 pre-brainstorm，确认这条研究到底是在评估什么边界。
2. 先列出本地权威事实源，再决定哪些 continuity artifact 可以外发。
3. 给出清晰的 `local-only` / `local + mem9` 运行边界。
4. 若后续要进入实现，继续把结果交给 `freely-doc-B2_IBM-execution` 或 `freely-dev-loop-execution`，不要在 skill 内偷跑实现。

## 完成判定

- mem9 的角色被明确限定为可选连续性增强层。
- 本地治理事实源优先级没有被削弱。
- 后续 runtime/bridge 是否接入 mem9 的决策路径已经稳定。

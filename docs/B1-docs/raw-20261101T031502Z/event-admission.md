---
analysis_id: EA-20261101T231000Z
phase_state: in_progress
topic: Freely 事件准入放在哪一层
created_at: 2026-11-01
---

# 事件准入：Freely 应该学 Super-agent 的哪一段

## 0. 问题

Super-agent 的入口是：

```
Source → Trigger → gate（代码）→ assessment（模型）→ Decision → Ticket
```

Freely 的入口是：

```
platform → scan → raw issue → B1（模型判断价值）→ candidate → B2 → ...
```

Freely 没有 per-event 的“谁可以发起、强度是什么、这条事件是否已处理”的代码 gate。问题不是“要不要抄 Mandate”，而是：

1. 权威判断（谁能发起）应该放在哪一层？
2. 价值判断（值不值得做）应该放在哪一层？
3. 两者混在一起会发生什么？

## 1. 先拆两个判断

| 判断 | 内容 | 适合谁做 | 失败后果 |
| --- | --- | --- | --- |
| 权威判断 | 发送者是否被允许、来源是否可信、是不是机器人、强度是 explicit 还是 inferred | 代码 gate | 不该做的工作进入流程，浪费注意力/越权 |
| 价值判断 | 这件事值不值得做、边界是什么、优先级如何 | B1 模型 + 人 | 该做的事被误杀，或范围失控 |

Super-agent 把两者都做了（gate + assessment），但 gate 是代码，assessment 是模型。Freely 目前把两者都交给 scan + Manager/B1，没有代码 gate。

## 2. 四种放置方式

### Option A：scan 时准入（平台 → 本地 raw issue 之前）

- 在 `task-lifecycle-scan` / `platform-adapter` 拉取后，先判发送者/来源/是否机器人。
- 通过才落 `docs/B1-docs/` 或进入 chat intake；不通过只记 disposition。
- 优点：最早、最便宜；不让噪音进入文档与 Manager 上下文。
- 缺点：scan 是批量/异步，可能丢失“事件上下文”；会与 B1 的价值判断重复；需要 actor/event id。

### Option B：Manager 派工前准入

- Manager 拿到 scan/chat 后，先用代码 gate 判“这条能不能派”，再决定是否 B1/建工位。
- 优点：有上下文；可与 scan 的 stage 结合。
- 缺点：Manager 已经消耗了上下文；gate 仍在模型循环里，不是真正的 pre-model；难以阻止噪音进入 prompt。

### Option C：raw issue 创建时准入（wt-create/feedback）

- `freely feedback` / `wt-create` 时检查 actor/来源。
- 优点：实现简单，所有工作都要经过 wt-create。
- 缺点：太晚；raw issue 已经创建，平台已经可见；无法阻止 Manager 先读它。

### Option D：混合（推荐研究方向）

- **代码 gate 只做权威判断**，放在 scan/intake 边界：发送者是否在白名单、来源是否允许、是否机器人、强度 explicit/inferred；通过后记录 `admission` 元数据（source、actor、event id、policy version、reason）。
- **B1 只做价值判断**：值不值得做、边界、优先级。
- Manager 只派“已准入”的 item；未准入的只在 panel/日志可见，不进入 prompt 上下文。
- 不引入 Mandate 的运行时 scope 凭证；admission 只是审计/路由事实，不是授权 token。

## 3. 为什么推荐 D，而不是照抄 Mandate

- Freely 的授权核心在“合并/交付”，不是“单条事件”。Mandate 的 scope/strength/revalidation 会把 B1 的价值判断前置成运行时规则，破坏 SDD 的“先收敛再决定”。
- 但 Freely 确实缺“谁可以发起”的代码边界：现在任何能写 issue/chat 的人/机器人都能让 Manager 读入上下文。至少要有 allowlist/bot 分类/来源校验。
- admission 记录能让审计回答“这条工作凭什么进来”，而不需要复制 Mandate 的完整状态机。

## 4. 实现前必须补的数据（当前没有）

看 `platform-adapter.py` 的 GitHub `fetch_issue`，只取：

```
title, body, createdAt, updatedAt, labels, state, comments[body]
```

**没有 author、authorAssociation、comment author/id/time、issue id（内部）、event id。** 因此现在即使想加 gate，也无法回答：

- 这条 issue/comment 是谁发的？
- 评论是哪一条、什么时候发的？
- 是不是同一个人重复发？

要做 admission，平台 adapter 至少要补：

- issue: `id`, `number`, `author`, `authorAssociation`, `createdAt`, `updatedAt`
- comment: `id`, `author`, `authorAssociation`, `createdAt`, `body`
- 事件级 id（用于幂等）

否则只能做“来源级”粗判，不能做“发送者级”准入。

## 5. 与 Super-agent 的对照

| 维度 | Super-agent | Freely（若做 Option D） |
| --- | --- | --- |
| 权威判断 | 代码 gate + 准入表 + 机器人列表 | 代码 gate + allowlist/来源/机器人分类 |
| 价值判断 | assessment（模型） | B1（模型 + candidate） |
| 授权凭证 | Mandate（scope/strength/policy version） | admission 记录（审计，不是 token） |
| 默认姿态 | observe | B1 照常，但未准入不进入 Manager 上下文 |
| 复活 | 按当前 Policy 重校验 | 重新 scan + 重新 B1 |

## 6. 风险与未解

1. **actor 数据缺失**：不补 adapter，gate 只能做来源级；需要先补字段。
2. **allowlist 维护成本**：谁来维护？项目配置还是平台 team？需要产品决定。
3. **误杀**：代码 gate 误判会把合法请求挡在 B1 之外；需要 observe 模式先记录“would admit”，再逐步 enforce。
4. **与 B1 重复**：gate 不能判断价值，否则 B1 变成橡皮图章；边界要写死。
5. **多平台身份**：GitHub/Gitee 账号不映射；同一个人两个平台可能被当成两个人。暂时按平台各自 allowlist，不做跨平台身份。

## 7. 结论

Freely 应该补的是**scan/intake 边界的权威 gate + admission 记录**，不是 Mandate 运行时。它解决“谁可以发起、这条事件是否已处理”，把“值不值得做”留给 B1。前提是先补平台 adapter 的 actor/event 字段；否则这个设计只能停在纸面。

---
analysis_id: AM-20261101T231000Z
phase_state: in_progress
topic: 注意力成本如何度量
created_at: 2026-11-01
---

# 注意力度量：先有数据，再谈谁更省人

## 0. 为什么需要这个

两边都在说“把人的注意力上移”，但都没有给出可复现的指标。没有指标时，“Freely 更自主”或“Super-agent 更安静”都只是叙事。

## 1. 现有数据源

### Freely

| 数据 | 位置 | 能回答 |
| --- | --- | --- |
| 人插话 | `freely.db chats`（chat_type/author/issue/consumed） | 人主动说了多少次 |
| agent 求人 | `a2a_tasks.state=input-required` + reason | agent 什么时候需要人/Reviewer |
| 工单状态 | issue `phase_state` / milestone | 卡在哪个阶段 |
| review | `reviews` 表 / code-review 文件 | 审查轮次与 verdict |
| 测试证据 | test-gate.env / pre-tests | 返工/失败 |
| PR 评论 | 平台，未入 runtime | 目前不可用（缺口） |

### Super-agent

| 数据 | 位置 | 能回答 |
| --- | --- | --- |
| Decision/reason | DB `decisions` | 为什么接/忽略 |
| Report/Attention | Ticket/Relay | agent 何时求人 |
| Panel 操作 | 面板 | 人实际做了什么 |
| IM 消息 | 渠道 | 打扰次数/长度 |

## 2. 一次真实采样（Freely 主项目，2026-11-01）

只读查询 `.freely/freely.db`：

- `a2a_tasks` 共 55 条：manager completed 29、worker failed 17、worker input-required 4、manager submitted 3、worker working 2。
- `input-required` 的 reason 全是 `needs-review:b1/red/test`，没有“human question”类。
- `chats` 表 0 条；`reviews` 表 0 条；`sessions` 里 manager active 5 条。

这说明：

- 这个项目的“求人”主要是**agent→Reviewer**，不是 agent→human；人的直接插话样本为 0。
- worker failed 17 条偏高，但可能是历史/僵尸任务，不能直接当失败率。
- review 表为空，说明 review 证据主要落在文件，不在 DB；要度量 review 轮次得读文件。

**结论：现有数据不足以计算“人工动作数/issue”或“打断精度”。** 需要先补事件级记录（谁、什么时候、因为什么求人/回复）。

## 3. 建议指标

| 指标 | 定义 | 数据来源 | 用途 |
| --- | --- | --- | --- |
| 人工动作数/issue | chat + issue comment + PR review + approval 次数 | chats、平台、PR | 衡量总打扰 |
| 打断精度 | agent 主动消息中“人必须行动”的比例 | chats/attention/PR | 衡量噪音 |
| 决策时延 | attention 发出 → 人回复 | 时间戳 | 衡量响应成本 |
| 升级率 | 每 issue input-required/blocked 次数 | a2a_tasks | 衡量 agent 自决能力 |
| 返工率 | review fail / 总 review | reviews/code-review | 衡量自检 |
| 漏报率 | 人主动补 issue/comment 的比例 | chats/issue | 衡量发现能力 |
| 静默失败率 | 无 report/无 close 的 issue 比例 | a2a_tasks/phase | 衡量可靠性 |

## 4. 最小埋点

不要求一次做全：

1. 每次 `input-required` 记录 `reason` + `requested_at` + `requested_by`。
2. 每次人 `chat`/PR review 记录 `issue_id` + `actor` + `at`。
3. 每次 review verdict 记录 `round` + `verdict` + `required_fixes` 数。
4. 每次 close 记录 `human_actions` 计数（从上述事件聚合）。

没有这四类事件，任何“注意力优化”都无法验证。

## 5. 与 Super-agent 的对比

- Super-agent 有结构化 Decision/Report/Attention，但也没有面板外的注意力指标；它的优势是**消息长度/默认沉默**这类可执行约束。
- Freely 有 chat/issue/PR 三个入口，但 PR 评论未入 runtime，review 未入 DB；它的优势是**入口宽、可审计**。
- 结论：**当前无法证明谁更省注意力。** 只能说 Super-agent 在设计上更克制，Freely 在入口上更宽。下一步应先把事件记全，再谈优化。

## 6. 未解

- 人工动作如何跨平台去重（同一个人 GitHub/Gitee/chat）？
- “必要决策”和“噪音”如何判定？需要人工标注样本。
- 是否把 Reviewer 的 input-required 算作“人的注意力”？它消耗的是另一个 agent，不是人。

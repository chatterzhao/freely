---
analysis_id: FM-20261101T231000Z
phase_state: in_progress
topic: Freely vs Super-agent failure modes
created_at: 2026-11-01
---

# 失效模式对比：两边分别怎么坏

> 这一篇不看“功能有没有”，只看“坏了会怎样、能不能发现、能不能恢复”。每个失效模式都按“预防 / 检测 / 恢复 / 残余风险”四段看。

## 0. 方法

- Super-agent 侧：读 `docs/001-008`、`prompts/*`、`src/app/{tools,notices,effects,assessment}.ts`、关键测试 `tests/followups.spec.ts`、`tests/effects.spec.ts`、`tests/core-engine.spec.ts`。
- Freely 侧：读 `task-lifecycle-scan.py`、`a2a_task.py`、`pr-*-guarded`、`pretests-gate`、`wt-*`、`three-loop`、`scan-lifecycle`、相关测试。
- 判定只针对“机制是否存在/是否可验证”，不评价模型能力。

## 1. 失效模式总表

| 失效模式 | Super-agent | Freely | 谁更强 |
| --- | --- | --- | --- |
| 漏掉一条请求 | gate 过滤 + observe 记录；被过滤的 Trigger 可能不可见 | scan 下载 + chat snapshot；PR review/CI 不进自动路径 | Super-agent |
| 重复做同一件事 | accept 以 trigger ID 幂等；disposition 记录 | a2a list 查询防重复；无事件级账本；实测同一 raw 因 dev/test 工位重复 | Super-agent |
| 越权/范围蔓延 | Policy + 准入表 + Mandate；运行时拒绝 | 阶段/门禁/分支保护；无 per-event 准入 | Super-agent（运行时） |
| 交接后消息丢失 | followupOwners + handback + 未读 Input 重投 | A2A 状态 + summary；无消息级 ownership | Super-agent |
| 人的注意力被淹没 | 默认沉默、IM ≤100 词、结构化 attention | Manager 主动汇报；入口多；无注意力指标 | Super-agent |
| 上下文丢失/串味 | 每 Ticket 独立 Session；inline/spill；Worker 冷启动 | session resume/fork + 文档；fork 可能带无关上下文 | 分裂 |
| 缓存误判 | 前缀稳定但无 cache 指标 | 有 `[CACHE]` 但 input 常为估算，hit/miss=0 | 分裂/都不足 |
| 外部副作用重复 | effect 队列 + 重试/退避；恢复提示先核对 | platform-adapter/issue-sync；无通用 effect 队列 | Super-agent |
| 文档/状态漂移 | 无文档层；Engine 单写 DB | phase 多写者、I-* 双解析、scan station/next_action 不一致 | Freely 风险更高 |
| Reviewer 走形式 | 无内建 Reviewer（不是“走形式”，是缺失） | 独立 Reviewer + 四层/六维；但 review gate 依赖 agent 身份 | Freely |
| TDD 被绕过 | 无 TDD | GREEN 硬门禁；RED 流程；全 not_applicable 仅 skill 约束 | Freely（但没有想象中硬） |
| harness 能力不匹配 | 绑定 DSH，不存在“换 harness”问题 | ACP 多 CLI；能力靠分支兜底，缺 probe | Freely（方向对，契约弱） |
| 平台不可用 | Source 报错，Ticket/Policy 仍在本地 | scan platform_health degraded；本地 docs 仍在 | 平手（都可降级） |

## 2. 逐项细看

### 2.1 漏掉一条请求

Super-agent：

- Source 先把 bot 自己的消息、范围外消息过滤；gate 再判发送者/准入表。
- 被过滤的 Trigger 仍留 disposition；`observe` 模式会记录“would accept”，但不通知人。
- 风险：**过滤错了没人知道**。没有抽样复核/漏报指标；文章也承认“不确定就安静忽略”。

Freely：

- 平台 issue 由 scan 下载；chat 由 `chats` 表进 Manager prompt。
- PR review comment/CI 反馈没有自动入口（见 `research.md` 7.11）。
- 风险：**入口缺失 + scan 降级**。平台 adapter 缺失时 scan 只能 degraded，本地 docs 仍可读，但新请求可能进不来。

判定：Super-agent 的“漏”是**判定层漏**（有记录但没人看）；Freely 的“漏”是**入口层漏**（根本没进入 runtime）。前者可用抽样/指标补，后者需要补入口与 ownership。

### 2.2 重复做同一件事

Super-agent：

- accept 以 trigger ID 幂等；同一 Trigger 接受两次只产生一个 Ticket。
- `dispositions` 记录每条 Trigger 的去向；重复决策可识别。
- 测试覆盖 follow-up 不触发新 Eval、handback 后才可重新路由。

Freely：

- Manager 派工前查 `a2a_task list --raw-key`；没有事件级幂等账本。
- 实测 scan 对同一 raw 因 dev/test 两个工位各出一条；`收口` station 与 `wt-create` next_action 不一致。
- 风险：**重试/重启/多工位**都可能重复；没有“这条消息已处理”的账本。

判定：Super-agent 更强。Freely 需要事件级幂等键或 ownership 账本，不能只靠“查一下”。

### 2.3 越权与范围蔓延

Super-agent：

- Mandate 记录 Policy 版本、scope、strength、matched rules、发送者身份。
- 运行时 gate 拒绝越权；Policy 变化会让在途 Eval 失效。
- 风险：Policy 变化不立即吊销 Mandate；复活才重校验；Worker 仍以 operator 身份跑命令，不是安全边界。

Freely：

- 授权是流程：角色 + phase + IBM/测试/PR/merge gate + 分支保护。
- 没有 per-event 准入；Manager 可能被长上下文说服，Worker 可能做超范围改动。
- 风险：**越权只能在 review/merge 时发现**，不是运行时拒绝。

判定：单条事件的“能不能做”，Super-agent 更强；组织级“能不能合并”，Freely 更强。两者防守点不同。

### 2.4 交接后消息丢失

Super-agent：

- `followupOwners` 决定哪些 Ticket 拥有消息；Worker 可 handback 一次；未读 Input 在 Assignment 结束时释放。
- `reportRelay` 用稳定 key 去重；Attention 是单问题 + 目标会话。
- 测试覆盖：人 follow-up 直达 Worker、不触发 Eval；guest 的 stop 不生效；handback 后才可 attach/accept。

Freely：

- A2A 有状态机与 summary/evidence；Reviewer verdict 通过 SSE 广播。
- 没有消息级 ownership；PR/Issue 后续讨论没有“归谁”的运行时事实。
- 风险：**后续讨论被重复开单或漏接**；Manager 上下文丢失后无法恢复归属。

判定：Super-agent 明显更强。这是 Freely 最该补的协作 primitive。

### 2.5 人的注意力被淹没

Super-agent：

- 默认沉默；只有可验收结果、必须决策、确实做不了才说话；IM 单条 ≤100 词。
- Panel 先列“需要人”的项；健康状态不占空间。
- 风险：没有注意力指标；被过滤的请求不可见。

Freely：

- Manager 主动汇报；scan needs_human；chat/issue/PR 多渠道。
- 没有“消息长度/打扰频率”的硬约束；没有注意力指标。
- 风险：**主动汇报多、入口多**，人可能被淹没；但漏报也少。

判定：设计上 Super-agent 更强；两者都没有可复现指标，不能量化“省了多少”。

### 2.6 上下文丢失/串味

Super-agent：

- 每 Ticket 独立 Session；Router 不读代码；inline/spill 有界；Worker 冷启动。
- 风险：Worker 没有 Router 的全局上下文；跨月记忆未解决；订阅多 Thread 可能串。

Freely：

- Worker/Reviewer fork Manager session；文档长期记忆；session resume。
- 风险：**fork 把无关上下文带进 Worker**；prompt 有 STABLE/SEMI-STABLE/DYNAMIC 排序，但只是注释约定，改动可能破坏顺序；文档可能过期。

判定：单会话隔离 Super-agent 更强；跨会话/跨项目长期记忆 Freely 更强。两者都需要“上下文预算/契约”。

### 2.7 缓存误判

Super-agent：

- 段序固定、Policy 置尾、revision 绑定；没有 cache 指标，无法知道命中多少。
- 风险：Worker 冷启动；provider 缓存不可见。

Freely：

- `[CACHE]` 日志；但 input 常为 `prompt_bytes//4` 估算，hit/miss=0；fork/resume 策略没有前后对照。
- 风险：**以为命中了，其实上下文不对**；指标是假的。

判定：都不足。Freely 有排序与观测入口，但数据不可信、顺序无校验；Super-agent 有纪律但不可见。优先补“usage vs estimated + 排序校验”。

### 2.8 外部副作用重复

Super-agent：

- effect 队列持久化、重试/退避、health；Outbox 保 receipt。
- 恢复提示要求先核对目录/git/GitHub 再重做。
- 风险：外部 API 不幂等时仍可能重复；恢复靠提示词。

Freely：

- platform-adapter/issue-sync 有 retry/状态；没有通用 effect 队列。
- PR/issue 写侧没有 receipt/去重账本。
- 风险：**重试可能重复评论/重复开 PR**；靠脚本自己处理。

判定：Super-agent 更强。Freely 需要外部副作用 receipt/idempotency key。

### 2.9 文档/状态漂移

Super-agent：没有文档层，不存在“文档漂移”；但 Ticket 状态与外部现实可能不一致（PR 被外部合并/关闭时靠 subscription 更新）。

Freely：

- phase 多写者；I-* 双解析；scan station/next_action 不一致；平台 adapter 降级。
- 风险：**文档看起来是真相，但字段可能过期**；scan/gate 只能对账一部分。

判定：Freely 风险更高。这是 SDD 的代价，必须用 schema/单写者/派生规则治理。

### 2.10 Reviewer 走形式

Super-agent：没有内建 Reviewer；Worker 自审 + 外部自动 bot（可错输入，最多三轮）。不是“走形式”，是**角色缺失**。

Freely：独立 Reviewer + 四层/六维审查 + verdict；但 review gate 依赖 `agent_working` 身份，手工工位会 fail-closed。

判定：Freely 更强；风险在“Reviewer 是否真的独立/有证据”，不是“有没有角色”。

### 2.11 TDD 被绕过

Super-agent：没有 TDD。

Freely：GREEN/pretests gate 硬；RED 流程；全 not_applicable 只由 skill 约束。

判定：Freely 更强，但“全 not_applicable”是可见的绕过面；下一轮应设计 scope-aware 规则。

### 2.12 harness 能力不匹配

Super-agent：绑定 DSH，不存在换 harness；但 `engines.dsh` 钉版本，升级/换宿主是重写。

Freely：ACP 多 CLI；能力差异靠分支兜底，缺 probe；DSH 没有 ACP。

判定：Freely 方向更对，但契约弱；P0 `harness-status` 只是第一步。

## 3. 跨切面结论

1. **Super-agent 的强项集中在“事件 → 决策 → 交接”链路**：幂等、ownership、attention、effect queue。这是 Freely 最该借的。
2. **Freely 的强项集中在“规格 → 测试 → 审查 → 合并”链路**：SDD、TDD、Reviewer、gates。这是 Super-agent 最缺的。
3. **两边都缺“注意力/漏报”的度量**：没有指标，就无法证明谁更省人。
4. **Freely 的独有风险是“分域真相的对账成本”**：文档、A2A、git、test-gate、平台各有一份真相；scan/gate 是唯一对账层，但它自己也会降级。
5. **Super-agent 的独有风险是“单仓/单宿主/单写者”**：更精确，但扩展边界硬。

## 4. 对下一轮设计的意义

- 事件准入/幂等/ownership 应该作为一组设计，而不是三个独立 feature。
- 状态 schema/单写者应该优先于“再加一个 gate”。
- TDD 的 not_applicable 需要 scope-aware 规则。
- HarnessPort 的能力契约要能表达 native/degraded/unknown，而不是布尔。
- 注意力指标要先定义，再谈优化。

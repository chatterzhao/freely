---
audit_id: DEBT-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 研究债台账：还有哪些没研究透

> 标准：acceptance_criteria 的每一条都要有“研究证据/实现证据”。没有证据的，不能 promote；不能用“应该可以”代替。

## 0. 总表

| Candidate | 研究缺口 | 实现/验证缺口 | 关闭证据 | 当前状态 |
| --- | --- | --- | --- | --- |
| C-F 讨论入口 | ✅ `intake.md` 六类 schema/准入/选型；✅ 真实 issue/PR/CI 回放 | platform-adapter 方法、events 表、scan 读取 | `intake.md` + `replay/intake_replay.py` 输出 | needs_research（实现待 B2） |
| C-B ownership/handoff | ✅ `handoff.md` §2.1 五类现状/目标矩阵；✅ 协议 v0 | new/fork 丢 message 修复、handoff 表/真实回放 | 行为矩阵 + 回放日志（B2） | needs_research（实现待 B2） |
| C-C report/attention/prompt | ✅ report/attention/批量决策 schema；✅ A2A 映射；✅ prompt manifest/三态 | usage/cache 基线、真实 patrol 对照 | `runtime-contracts.md` §3.1-3.2 + 基线日志（B2） | needs_research（测量待 B2） |
| C-D HarnessPort | ✅ HarnessPort Protocol；✅ RoleHarnessConfig；✅ per-role probe/JSON 契约 | 角色级选择/探测实现 | `harness-strategy.md` §1.1-1.4 + probe 输出（B2） | needs_research（实现待 B2） |
| C-E DSH 插件 | 服务 API 可用性、插件骨架/桥协议 | P0/P1 spike、首次 session 消息、gate 阻断 | spike 报告 + 代码 | needs_research |

## 1. C-F 讨论入口

acceptance：

1. 六类来源都有入口、event_id、thread_key、actor、去重规则。
2. issue comment/PR review 进入 Manager 的 scan/queue。
3. CI 结果能进入，不依赖人转述。
4. 同一事件重复拉取不产生重复任务。

研究缺口：

- 六类来源具体是：issue body、issue comment、PR review comment、PR review（approve/request changes）、CI check、chat。
- 每类当前可用字段不同：`fetch_issue` 有 comments 但只有 body；`list_open_issue_records` 只有 number/title/body/state；PR review/CI 无 adapter 方法。
- 需要决定：扩展 scan 轮询，还是新增 events 表/事件流；推荐“scan 保留生命周期 + events 表存增量事件 + event_id 去重”。
- 需要明确 actor 来源：GitHub `author.login`/`authorAssociation`；Gitee 对应字段；chat `author`。
- 需要真实回放：一个 issue comment、一个 PR review、一个 CI fail。

## 2. C-B ownership/handoff

acceptance：

1. 五类后续消息 owner 规则可回答“归谁”。
2. 越界消息 handback 一次，带理由/目标。
3. 已停止/关闭工单不被自动复活。
4. 幂等键/超时释放可验证。

研究缺口：

- `handoff.md` 有目标规则，但没有“现状行为 vs 目标行为”矩阵；需要逐类列：新建请求、活跃 Thread 后续、已完成 Thread 后续、跨工单、人 stop。
- 需要确认当前 scan/Manager 对每类消息的实际行为（漏接/重复/新开单）。
- new/fork 丢 message 是已确认 bug；修复方案要写到函数级（new/fork 后显式 prompt + 角色定义）。
- 需要回放：同一 PR 两条评论、跨工单评论、人 stop、Worker 死亡后 fail 反馈。

## 3. C-C report/attention/prompt

acceptance：

1. Manager 每轮上下文成本基线（字符/token/文档数）与 cache hit/miss 基线。
2. Manager 可读/不可读边界可检查。
3. 路由支持批量决策 + 单条拒绝，拒绝原因可追溯。
4. report 六态、attention 含问题/目标/动作。
5. relay 幂等键；prompt 稳定前缀/可变尾部，有 cache 对照。

研究缺口：

- report/attention 目前只有散文，需要 JSON schema 与 A2A 字段映射（message data vs task row）。
- 批量决策/逐条拒绝没有协议；需要定义 Manager 输出结构（accept/stop/ignore/unavailable + reason）。
- prompt 有 STABLE/SEMI/DYNAMIC 顺序，但没有 manifest（段名/顺序/hash/bytes）；需要固定段名并记录。
- 没有 usage/cache 基线；21 条日志全是 estimated，不能当命中率。需要先建立“reported/estimated/absent”三态。
- 真实 patrol 对照需要运行 Manager（实现/测试阶段），研究阶段先给采样方案。

## 4. C-D HarnessPort

acceptance：

1. ACP CLI 能力矩阵（有/无/降级/需探测）。
2. HarnessPort 覆盖 probe/session/prompt/interrupt/usage/cache/tools/skills。
3. 三角色可选 harness，有 probe/fallback。
4. DSH 可行性结论。
5. 明确 DSH 插件边界。

研究缺口：

- `harness-strategy.md` 有能力矩阵和原则，但没有可实现的接口签名/类型。
- RoleHarnessConfig 只有字段名，没有 schema（role/tool/slot/adapter/model/preset）。
- per-role probe 没有输出样例；`harness-status --role` 未实现。
- UI/CLI 后端只有命令草案，没有 JSON contract。
- DSH 可行性已结论“不做 adapter、做 Freely-host 插件”，但服务 API 是否稳定仍未 spike。

## 5. C-E DSH 插件

acceptance：

1. 插件注入所需 DSH services，不加载 dsh-superagent。
2. Manager/Worker/Reviewer 独立 DSH preset/session。
3. 首次 session 收到 task+role prompt；handoff append-only。
4. 一个真实 issue 从 Manager 到 PR，全程无 ACP。
5. gate exit code 阻断；usage reported/estimated。

研究缺口：

- DSH 服务注入面有代码依据（`src/index.ts` 的 inject），但没有实际插件骨架验证。
- `sessionController` 的 create/prompt/stop API 需要 spike 验证；fork 不存在，需 context pack。
- Python runtime 与 plugin 的 bridge 协议只有设计，没有最小 echo/spike。
- 首次 session 消息丢失 bug 未修；C-E 依赖 C-B。
- 真实 issue E2E 是实现阶段验收，不是纯研究。

## 6. 跨切面债

| 债 | 说明 | 关闭方式 |
| --- | --- | --- |
| I-* canonical 格式 | YAML vs bullet 双写 | 选 YAML；parser 修改或脚本生成 bullet |
| phase 单写者 | wt-create/pr-review/pr-merge 各写 | transition 表 + 显式命令 |
| TDD `change_surface` | 未定义字段/校验 | schema + gate 规则 |
| 注意力度量 | 无基线 | 最小埋点 + 采样 |
| MCP | `mcpServers: []` | 明确“不编排”或接 harness MCP |
| 语义 Watchdog | 只有进程/SSE | 定义轻量 supervisor reviewer 范围 |
| raw issue absorbed | C-B~F 在 absorbed raw 下 | 确认 promote 路径或新 raw |

## 7. 关闭顺序

1. C-F 来源/事件 schema + 回放（研究）。
2. C-B 行为矩阵 + new/fork 修复方案 + 回放（研究/修复）。
3. C-C schema/manifest + 基线方案（研究）。
4. C-D 接口/配置/probe 契约（研究）。
5. C-E 插件 spike（需代码）。
6. 跨切面 schema/transition/TDD/attention（研究+实现）。
7. B1 acceptance review → promote → B2 → TDD 实现。

## 8. 规则

- 每条债必须有“关闭证据”链接/日志/代码；没有就保持 needs_research。
- 研究阶段不写产品代码；C-E spike 例外，必须在独立 spike 目录/分支，不接主路径。
- 发现新债就加进本表，不静默跳过。

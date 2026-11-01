---
analysis_id: OBS-20261101T231000Z
phase_state: in_progress
topic: 可观测性对比
created_at: 2026-11-01
---

# 可观测性：DSH 实时强，Freely 审计强，但 Freely 的只读面会 fail-closed

## 0. 实测（2026-11-01，主项目）

| 命令 | 结果 | 说明 |
| --- | --- | --- |
| `freely live-status --project <main>` | **ERROR**：unable to resolve agent identity；agent_working has no entry | 只读状态命令依赖 Manager 身份，runtime 停止/身份缺失时不可用 |
| `freely baseline-status` | **ERROR**：同上 | 同上 |
| `freely status` | **ERROR**：同上 | 同上 |
| `freely fleet-status` | 正常输出 worktree/branch/sup/ai/dirty/checkpoint | 不依赖 agent identity |
| `freely harness-status` | 正常输出角色/能力/binary/cache | 只读探针，不启动会话 |
| `freely task-source-scan --json` | 正常输出，但 platform_health=degraded | 依赖 platform_adapter |
| `reviews` 表 | 0 行 | review 证据在文件，不在 DB |
| `chats` 表 | 0 行 | 该项目没有人工 chat 样本 |
| `a2a_tasks` | 55 条（completed 29 / failed 17 / input-required 4 / submitted 3 / working 2） | 可看任务状态，但 failed 高需结合历史 |

## 1. Freely 的可观测面

| 面 | 数据 | 优点 | 缺点 |
| --- | --- | --- | --- |
| docs | B1/B2、phase、milestone、code-review | 可审计、可交接、长期 | 不是实时；容易漂移 |
| CLI | live/baseline/fleet/harness-status | 人可读 | live/baseline 依赖 agent identity，停了就看不了 |
| DB | a2a_tasks、sessions、chats、agent_working | 结构化、可查询 | reviews 空；cache 不在 DB；多表关联 |
| 日志 | cycle log、`[CACHE]`、watcher log | 细节多 | 非结构化；重复行；估算值混入 |
| 平台 | issue/PR/CI | 对外真实 | AI 不直接读；scan 只拉一部分 |

## 2. Super-agent 的可观测面

- 单写 DB：Trigger/Thread/Ticket/Decision/Report/Attention 都在一个状态存储。
- Health board + Panel：runtime/组件健康、需要人的项、Ticket 详情。
- Decision/reason：为什么接/忽略可查。
- Relay/Notice：对外消息与归属可查。
- 缺点：没有文档审计链；Panel 之外的指标也有限。

## 3. 对比判定

| 维度 | Super-agent | Freely | 判定 |
| --- | --- | --- | --- |
| 实时健康 | health board/panel，单 DB | live-status 依赖 identity，停了就 ERROR | **DSH 更强** |
| 任务状态 | Ticket/Decision | a2a_tasks/sessions | 平手；DSH 更集中 |
| 审计 | Decision/Report | 文档 + review + phase | **Freely 更强** |
| 错误定位 | health/effect/recovery | 日志分散、scan 可能 degraded | **DSH 更强** |
| 人工可读 | Panel | CLI + docs | 平手；Freely 更依赖命令行 |
| 数据一致性 | 单写者 | 多源、多写者 | **DSH 更强** |

结论：**DSH 更像“运行中的控制台”，Freely 更像“事后的审计卷宗”。** 对长跑系统，两者都需要：Freely 缺的是“不依赖 Manager 身份的只读健康面”。

## 4. 建议（研究结论）

1. **只读状态要能降级**：`live-status`/`baseline-status` 在 agent_working 空时，至少输出 scan/fleet/DB 的可用部分，而不是整体 ERROR。
2. **health surface 独立于 runtime 身份**：像 `harness-status` 一样，先报组件可用性，再报 agent 状态。
3. **review 入 DB 或结构化索引**：现在 `reviews` 空、证据在文件；查询“review 轮次/失败原因”很难。
4. **cache/usage 结构化**：不要只写 `[CACHE]` 日志；至少 event 表 + `usage_reported`。
5. **scan 的 platform_health 要显式展示**：degraded 时告诉人“哪些源没扫到”，而不是只给 stage。

## 5. 未解

- 是否要把 `live-status` 的 fail-closed 改成“部分可用”？会不会掩盖身份问题？
- review 文件与 DB 谁是权威？是否双写？
- 多项目下 health 如何聚合？`fleet-status` 只是单项目 worktree。
- 日志/DB/docs 三套观测如何做统一 ID（raw_key/task_id/issue_id）？

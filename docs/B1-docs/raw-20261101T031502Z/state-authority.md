---
analysis_id: SA-20261101T231000Z
phase_state: in_progress
topic: Freely 状态权威与单写者
created_at: 2026-11-01
---

# 状态权威：Freely 需要的是 schema，不是更多门禁

## 0. 问题

Freely 的很多 bug 不是“功能没做”，而是“同一件事有多个写法/多个写者”：

- I-*：`pretests-gate` 只认 bullet，`pr-merge-guarded` 只认 YAML frontmatter。
- `phase_state`：`wt-create`、`pr-review-guarded`、`pr-merge-guarded` 各写一段；`wt-close` 只检查。
- scan：从 docs/A2A/worktree 推导 stage，但 station 与 next_action 可能不一致。
- milestone：由 B1/B2 的 agent 手工更新，没有脚本校验。

这不是“再加一个 gate”能解决的；需要**字段级权威表 + 派生规则 + 单写者**。

## 1. 每个字段回答什么问题

| 字段/文件 | 回答的问题 | 当前写者 | 读者 | 建议权威 |
| --- | --- | --- | --- | --- |
| `docs/B1-docs/raw-*/issue.md` `phase_state` | raw 是否已吸收/丢弃 | wt-create（改回 proposed）、pr-merge（absorbed）、人 | scan、gates | 单一终态写者（merge/closeout），人工只读 |
| `docs/B2-docs/**/issues/I-*` `phase_state` | 正式 issue 到哪一步 | 人/agent、pr-review、pr-merge | scan、gates、pretests | 单一状态机写者（建议 pr-merge + 显式 transition CLI） |
| `docs/milestones.md` candidate/committed 状态 | 规划队列 | B1/B2 skill（手工） | scan、gates | B1/B2 脚本化写入；禁止自由编辑 |
| `.freely/run/test-gate.env` | 测试是否在 HEAD 跑过 | daemon stop | pretests-retirement | 只由测试运行器写 |
| `a2a_tasks` / `sessions` | 谁在做、做到哪 | A2A server/runtime | Manager、scan | A2A server 单写者 |
| git worktree/branch | 环境是否存在 | git/wt-create/wt-close | scan、fleet | git 本身 |
| 平台 issue/PR | 对外状态 | issue-sync/platform-adapter | 人、scan（下载副本） | 平台是外部权威；本地是副本 |
| scan `stage/next_action` | 下一步建议 | scan 派生 | Manager | 纯派生，不写回 |

## 2. 关键原则

### 2.1 一个字段一个写者

不是“一个文件一个写者”，而是“一个字段一个写者”。例如 I-* 的 `phase_state` 只能由状态机写，`title/body` 可以由 B2 skill 写；`milestones.md` 的队列只能由 B1/B2 脚本写。

### 2.2 派生视图不写回

scan 的 `stage/next_action` 是派生视图，不能写回 issue；否则会出现“scan 改了 phase”的循环。`live-status`/`fleet-status` 同理。

### 2.3 冲突时按域裁决

- 规格/验收冲突：docs 赢（平台副本以本地为准）。
- 执行中冲突：A2A 赢（“谁在做”以活跃 session 为准）。
- 环境冲突：git 赢（worktree 不存在就是不存在）。
- 测试冲突：test-gate 赢（HEAD 没跑就是没跑）。
- 规划冲突：milestone 赢（candidate 是否入队）。

### 2.4 一个 canonical 格式，其他是镜像

I-* 目前必须 YAML + bullet 双写才能过两个门禁。长期应选一个 canonical（建议 YAML frontmatter，因为机器可解析、可校验），然后：

- 修改 `pretests-gate` 读 YAML；或
- 由脚本从 YAML 生成正文 bullet，禁止手写两份。

在没改之前，双写必须由脚本生成并校验一致，不能靠人记。

## 3. 与 Super-agent 的对照

| 维度 | Super-agent | Freely 现状 | Freely 应有 |
| --- | --- | --- | --- |
| 写者 | Engine 唯一写 Ticket/Trigger/Decision | 多脚本/多 agent 各写一段 | 字段级单写者 |
| 状态查询 | 运行时对象，精确 | 文档+DB+git+平台，多源 | 权威表 + 派生 |
| 冲突 | 不存在（单写） | 常见（phase/scan/milestone） | 域裁决规则 |
| 迁移 | schema migration | 无统一 schema | 显式 schema + 校验 |

Super-agent 的单写者更可靠，但绑定运行时；Freely 不可能把所有状态塞进一个 DB（会丢文档审计），所以正确方向不是“抄单写 DB”，而是“**分域权威 + 字段级单写者 + 派生视图**”。

## 4. 落地顺序（研究结论，不是实现）

1. 先写一张权威表（本文件 §1），所有脚本/skill 引用同一张表。
2. 选 I-* canonical 格式，改一个 parser 或生成镜像；停止手写双份。
3. 给 `phase_state` 加显式 transition 命令（who → what → why），禁止 sed 直改。
4. 给 `milestones.md` 加 schema 校验（candidate status 与 issue phase 对齐）。
5. 让 scan 只输出派生视图，并在输出中标注 `source_of_truth`，不写回。
6. 最后才考虑事件准入/幂等；否则 gate 会建在流沙上。

## 5. 未解

- canonical 格式选 YAML 还是 bullet？取决于哪个 parser 更容易统一。
- `phase_state` 的 transition 表由谁维护？skill 还是 runtime？
- milestone 是否应该从 issue/phase 自动派生，而不是手工维护？
- 多项目/多工位下，权威表是否需要 project-scoped 版本？

---
analysis_id: RUNTIME-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 运行时契约与实证：状态、准入、上下文、注意力、可观测、TDD

## 0. 结论

Freely 的运行时问题不是“功能少”，而是**契约不显式**：

- 状态是分域真相，但没有字段级单写者；
- 事件没有准入层，discussion 没入口；
- prompt 有排序但无 manifest，cache 多为估算；
- 注意力没有指标；
- 只读状态会 fail-closed；
- TDD 的 GREEN 硬、RED 软。

下面每节只保留结论、证据、最小改动。

## 1. 状态权威：分域真相，不是一份真相

| 问题 | 权威源 | 谁写 | 说明 |
| --- | --- | --- | --- |
| 做什么/为什么/怎么验/边界 | docs（Intent/Constitution/LAWS、B1/B2、PRD/pre-tests） | B1/B2、人、Worker | 规格与生命周期真相 |
| 现在有没有 agent 在做 | A2A `sessions`/`a2a_tasks` | runtime/A2A server | scan 明确写“A2A is the arbiter of in progress” |
| 生命周期到哪一步 | issue `phase_state` + milestone | wt-create、pr-review、pr-merge | 多写者，易漂移 |
| 代码/工位是否存在 | git worktree/branch | git、wt-create/wt-close | 环境真相 |
| 测试是否在 HEAD 跑过 | `.freely/run/test-gate.env` + evidence | daemon stop、test-lane | 证据真相 |
| 对外平台状态 | GitHub/Gitee | issue-sync/platform-adapter | 对外副本；AI 只读本地 |
| 下一步 | scan stage/next_action | scan 派生 | 派生视图，不写回 |

原则：

- 一个字段一个写者；派生视图不写回。
- 冲突按域裁决：规格 docs 赢，执行 A2A 赢，环境 git 赢，测试 test-gate 赢，规划 milestone 赢。
- I-* 目前必须 YAML frontmatter + 正文 bullet 双写：`pretests-gate` 只认 bullet，`pr-merge-guarded` 只认 YAML。长期应选一个 canonical（建议 YAML），另一个由脚本生成。
- `phase_state` 没有单一写者：wt-create、pr-review、pr-merge 各写一段；应引入显式 transition 命令，禁止 sed 直改。

## 2. 事件准入：放在 scan/intake 边界，只做权威判断

| 判断 | 内容 | 适合谁 |
| --- | --- | --- |
| 权威判断 | 发送者是否允许、来源是否可信、是否机器人、explicit/inferred | 代码 gate |
| 价值判断 | 值不值得做、边界、优先级 | B1 模型 + 人 |

四种放置：

- A：scan 时准入（最早，但批量/丢上下文）。
- B：Manager 派工前（已进 prompt，太晚）。
- C：raw issue 创建时（raw 已可见，太晚）。
- D（推荐）：scan/intake 边界做权威 gate + admission 记录；B1 只做价值判断；不引入 Mandate。

当前数据缺口：`platform-adapter.fetch_issue` 只取 title/body/dates/labels/state/comments[body]，**没有 author、comment id/time、event id**。要做 actor 级准入，先补：

- issue: id/number/author/association/created/updated
- comment: id/author/association/created/body
- 事件级 id（幂等）

否则只能做来源级粗判。

## 3. Prompt 顺序与 cache

`freely` 的组装顺序：

1. STABLE：Agent 角色定义
2. `start-lead-agent.sh`（intent/constitution 路径、任务）
3. SEMI-STABLE：fleet
4. STABLE：exit contract（resume 跳过）
5. DYNAMIC：scan/chat/continuation/context warning/checkpoint/supervision
6. DYNAMIC：auto-retry hint
7. MANAGER-ONLY：thread history/unconsumed workers
8. DYNAMIC：session handoff/continuity（最后）

`fresh_with_handoff` 在 context 超阈值时只发 handoff（几 KB），是正确方向。

ACP 传输事实：

- `session/new|resume|fork` 参数只有 cwd/mcpServers/sessionId；没有 systemPrompt。
- 完整 prompt 通过 `session/prompt` 发送；每次发全文，不是 delta。
- cache 是否命中取决于 ACP agent/provider，不是 Freely 保证。

Cache 日志：

- 从 usage 取 cache_hit/miss/input/output；无 usage 时 `input=prompt_bytes//4` 估算。
- 没有 `usage_reported`；只能靠 `input==bytes//4` 反推。
- hit/miss=0 可能是没缓存，也可能是没上报。
- 主项目最近 50 cycle 的 21 条 `[CACHE]` 全是 estimated、hit=0/miss=0。

结论：Freely 有排序，没有 manifest/校验；cache 不可回归。应加：段名/顺序/hash、usage_reported/cache_reported、prefix hash。

## 3.1 Report / Attention / 批量决策 schema

### Report

```json
{
  "report_state": "progress|waiting|ready|blocked|failed|dropped",
  "summary": "一句话进展",
  "next_action": "下一步",
  "evidence_paths": ["docs/...", "test/..."],
  "attention": {
    "needed": true,
    "question": "只问一个问题",
    "target_role": "manager|worker|reviewer|human",
    "target_session": "session-id-or-null",
    "human_action": "需要人做什么",
    "for_trigger_id": "event-id"
  }
}
```

规则：

- `attention.needed=false` 时其余 attention 字段为空；true 时只能有一个问题。
- `report_state` 六态；`dropped` 表示不做/丢弃，不是失败。
- `summary` 不替代 evidence；verdict 必须是 artifact。
- `target_role` 与 `target_session` 至少一个；human action 必须可执行。

### A2A 映射

| report_state | A2A state/字段 | 说明 |
| --- | --- | --- |
| progress | `working` + progress | 不新增行；更新进度 |
| waiting | `input-required` + reason | 缺输入，不结束 |
| ready | `submitted`/`completed` 候选 | 等 Reviewer/Manager |
| blocked | `input-required` + reason=blocked | 需人/上游 |
| failed | `failed` + reason | 可重试 |
| dropped | `canceled` + reason | 不做 |

持久化：优先放 `handoff_messages.parts[].data`；A2A 旧字段做兼容镜像，不把 JSON 塞进 `message` 文本。

### 批量决策

```json
{
  "decisions": [
    {"trigger_id": "event-1", "decision": "accept|stop|ignore|unavailable", "reason": "..."},
    {"trigger_id": "event-2", "decision": "ignore", "reason": "duplicate"}
  ]
}
```

- 一条失败不影响其他；每条有 reason。
- `accept` 必须带 candidate/issue 目标；`stop` 必须带停谁；`ignore` 必须去重/不处理理由。
- 以 `trigger_id` 幂等；重复决策只生效一次。

## 3.2 Prompt manifest

固定段名/顺序；每段记录 `bytes`、`sha256`、`kind`（stable/semi/dynamic）、`source`。

| # | 段 | kind | 说明 |
| --- | --- | --- | --- |
| 1 | `agent_role` | stable | 角色定义 |
| 2 | `bootstrap` | stable | intent/constitution 路径、任务 |
| 3 | `fleet` | semi | 工位/分支状态 |
| 4 | `exit_contract` | stable | resume 时跳过 |
| 5 | `scan` | dynamic | scan summary |
| 6 | `chat` | dynamic | unconsumed chats |
| 7 | `continuation` | dynamic | 续跑 |
| 8 | `context_warning` | dynamic | 上下文告警 |
| 9 | `checkpoint` | dynamic | 检查点 |
| 10 | `thread_history` | dynamic | Manager only |
| 11 | `session_handoff` | dynamic | 最后 |

规则：

- 前 4 段是 prefix；5-11 是 tail。tail 变化不能改变 prefix 字节。
- 每次 prompt 写 `prompt_manifest` 日志；`prefix_hash` 用于 cache 对照。
- 不要把 fleet/scan/chat 插到 prefix；不要把 Policy/LAWS 放尾部（会破坏 prefix 且授权应在前）。
- 角色不同 manifest 可不同，但段名/顺序固定。

### usage/cache 三态

| 字段 | 值 | 说明 |
| --- | --- | --- |
| `usage_source` | reported/estimated/absent | reported=provider usage；estimated=bytes//4；absent=无 |
| `cache_source` | reported/estimated/absent | reported=cache 字段；estimated=推断；absent=无 |
| `prefix_hash` | sha256 | 前 4 段 |
| `cache_hit_tokens`/`cache_miss_tokens` | int/null | 只有 reported 才算命中率 |

没有 `usage_source=reported` 时，禁止把 `hit=0` 当“缓存没命中”；只能报“未知”。

## 4. 注意力度量：当前没有基线

现有数据（主项目）：

- `a2a_tasks` 55 条：manager completed 29、worker failed 17、input-required 4、submitted 3、working 2。
- input-required 的 reason 全是 needs-review:b1/red/test，没有 human question。
- chats 0、reviews 0、manager active 5。
- 结论：现有数据不足以算“人工动作数/打断精度”。

建议指标：

| 指标 | 定义 | 数据 |
| --- | --- | --- |
| 人工动作数/issue | chat + issue comment + PR review + approval | chats/平台/PR |
| 打断精度 | agent 主动消息中“人必须行动”的比例 | chats/attention/PR |
| 决策时延 | attention 发出→人回复 | 时间戳 |
| 升级率 | 每 issue input-required/blocked 次数 | a2a_tasks |
| 返工率 | review fail/总 review | reviews/code-review |
| 漏报率 | 人主动补 issue/comment 的比例 | chats/issue |

最小埋点：input-required 记录 reason/requested_at/by；人 chat/PR review 记录 issue/actor/time；review verdict 记录 round/required_fixes；close 聚合 human_actions。

## 5. 可观测性：DSH 实时强，Freely 审计强，但只读面 fail-closed

实测（2026-11-01，主项目）：

| 命令 | 结果 |
| --- | --- |
| `live-status` / `baseline-status` / `status` | **ERROR**：unable to resolve agent identity（agent_working empty） |
| `fleet-status` | 正常（worktree/branch/sup/ai/dirty） |
| `harness-status` | 正常（角色/能力/binary/cache） |
| `task-source-scan --json` | 正常，但 platform_health=degraded |
| `reviews` 表 | 0 行；review 证据在文件 |
| `chats` 表 | 0 行 |

结论：

- DSH 像“运行中的控制台”（单 DB/health/panel）；Freely 像“事后审计卷宗”（docs/review/phase）。
- Freely 缺“不依赖 Manager 身份的只读健康面”。
- 建议：live-status 降级输出 scan/fleet/DB 可用部分；health surface 独立于 runtime 身份；review 入 DB 或结构化索引；cache/usage 结构化；scan platform_health 显式展示。

## 6. TDD 政策：GREEN 硬、RED 软

现状：

- `pretests-gate` 要求每个 Acceptance Item `red-green-status=green` 或合法 `not_applicable`。
- 它检查 not_applicable reason/explanation/replacement_evidence，但不检查至少一个真实 test_command/pass，也不检查 actual_RED_output。
- “全部 not_applicable 是糊弄”只写在 `freely-test-execution` skill；gate 没有硬拦截。
- 历史：431 份 pre-tests，327 份有 not_applicable，247 份无 test_command（含旧 schema/docs-only）。

建议：按改动面分级：

| 改动面 | 最低验收 |
| --- | --- |
| docs/spec | 链接/结构/引用校验；可 not_applicable 可执行测试 |
| config/metadata | 解析/一致性校验 |
| script/runtime | 至少一个可执行测试 |
| agent/skill/prompt | 行为回放/结构校验 |
| UI/GUI | 交互验证/截图/端到端 |

硬约束：代码类至少一个 test_command/passed；docs/config 允许全 not_applicable 但必须有可执行替代校验；全 not_applicable 不能覆盖整个代码类 issue。

## 7. 未解

- canonical 格式选 YAML 还是 bullet？
- 事件准入数据（actor/event id）谁补？
- 注意力指标先采样哪个项目？
- live-status 降级会不会掩盖身份问题？
- `change_surface` 由谁声明/校验？

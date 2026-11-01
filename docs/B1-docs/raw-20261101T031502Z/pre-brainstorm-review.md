---
review_id: B1-REV-20261101T231000Z
phase_state: completed
reviewer: subagent:2db58fae-5163-4307-b247-9564ffea4416
mode: subagent
verdict: pass-with-gaps
created_at: 2026-11-01
---

# B1 预研达标评审

## 0. 结论

**verdict: pass-with-gaps。**

预研包已经足以进入 **B1 candidate 起草**，但不能直接 promote，也不应直接开 PR/merge。它不是“B1 完成”，而是“B1 的输入已经足够扎实”。

独立评审（subagent，未修改文件）的核心判断：

- 强项：问题层优先、证据四分层（文章/原型/代码/实测）、敢于自我纠错、替代方案与代价齐全。
- 无阻断性缺口：actor/event id、canonical 格式、DSH 宿主所有权都已显式列为未解，属于下一阶段设计决策，不是本轮漏项。
- 条件：先修两条 major（DSH 路线表述、循环口径），把 adopt 清单收敛为 1–2 个 candidate，并补 DSH 快照 SHA/量化复现命令。

## 1. 评审范围

- 预研文档：`research-index.md`、`synthesis.md`、`delivery-model.md`、`research.md`、`super-agent-article.md`
- 分面：`failure-modes.md`、`event-admission.md`、`state-authority.md`、`tdd-policy.md`、`attention-metrics.md`、`context-cache.md`、`observability.md`、`harness-port.md`、`dsh-adapter-decision.md`
- 根 `README.md` 与 `docs/assets/freely-delivery-loop.{svg,html}`
- 抽查代码：`pretests-gate`、`pr-merge-guarded`、`run-acp-prompt.py`、主项目 `[CACHE]`

## 2. 评审标准与结果

| 标准 | 结果 | 说明 |
| --- | --- | --- |
| 问题/意图/痛点清楚 | pass | 六个子需求 + 逐项判定表 |
| 关键事实可复核 | pass-with-gaps | Freely 侧抽查成立；DSH 侧原缺 SHA/URL，已补 |
| 替代方案/代价 | pass | A/B/C/D、adopt/adapt/reject |
| 边界/non-goals/未解 | pass | 索引明确“未解是设计决策，不是漏研究” |
| 足以支撑 B1 candidate | pass-with-gaps | 可起草，但需收敛 scope |
| README/图与结论一致 | pass-with-gaps | 已修 DSH 路线、循环口径、图例/后缀 |
| DSH 取舍依据 | pass | adapter vs 插件矩阵 + 重评条件 |

## 3. Findings 与处理

| severity | finding | 状态 | 处理 |
| --- | --- | --- | --- |
| major | README 仍可能被读成“DSH 需要 adapter”，与 DSH 决策相反 | fixed | README 改为“DSH 不做 harness adapter；方向是 @freely/dsh-freely 插件”；新增 `dsh-adapter-decision.md` |
| major | `delivery-model` 标题“四个循环”与表内 5 行、README“三个 loop + 门禁”不一致 | fixed | 统一为“3 个常驻 loop + 2 段交付门禁”，表加类型列 |
| major | “AI 是项目所有者/人只在需要时出现”是收益断言，缺指标 | fixed | 改为“目标态”，并注明注意力度量尚无基线 |
| major | 静态图图例仍是 archify 模板（前端/后端/云服务/安全/消息总线），节点带“· 架构组件” | fixed | 图例改为入口/控制/基座/规格门禁/工具/外部；删除模板后缀 |
| minor | DSH 来源缺 repo URL/commit SHA | fixed | 补 `6337fc823ce20251c8de8085948165c81aaa701e` 与 URL |
| minor | 431/327/247、55 条 A2A、21 条 CACHE 缺复现命令 | fixed | `research.md` §7.8 补 find/grep/sqlite/harness-status 命令 |
| minor | “issue-sync 是唯一出口”过强 | fixed | 改为“出站写平台统一走封装命令（issue-sync/platform-adapter）” |
| minor | scan 与 Manager 并列，未标派生视图 | fixed | README 标注“scan（派生视图，不写回）” |
| minor | “四问/四层/六维”术语混用 | fixed | 阶段评审=四层；PR 评审=四问；failure-modes 对齐 |
| minor | 文章实验数字易被误读 | accepted | 文章文档明确“合成负载，只评调度，不评单任务能力”；不参与判定 |

## 4. 是否进入 B1 candidate

**yes，带条件。**

建议先把 adopt 清单收敛为 1–2 个 candidate，不要一次承接 16 个维度：

1. **C-A：状态权威 + 字段级单写者**（`state-authority.md` 先行）
   - 目标：I-* canonical 格式、phase transition、scan 派生不写回。
   - 这是其他 runtime 协作 primitive 的地基；event-admission 依赖它。
2. **C-B：运行时协作 primitive**（`event-admission.md` + `failure-modes.md`）
   - 目标：事件准入（权威判断）、消息级 ownership/handback、幂等键。
   - **前置依赖**：平台 adapter 先补 actor/event id；否则只能做来源级 gate。

DSH 相关不进入本轮 candidate：

- 不做 DSH-as-harness adapter。
- 若要进 DSH 生态，单独立项做 `@freely/dsh-freely` 插件 spike（Source + skill + CLI），验收条件见 `dsh-adapter-decision.md` §6。

## 5. 下一步

1. 按 B1 skill 起草 `candidates.md`（C-A/C-B），写 scope/non-goals/acceptance_criteria/promotion_gate/open_questions。
2. 对 C-A 先做 acceptance review，再决定是否 promote。
3. 本预研只提交、不 PR、不 merge；B1 candidate 阶段再按完整 B1→B2→实现生命周期走。

## 6. 验证

- README 链接检查通过。
- `pretests-gate` 通过。
- 交付图静态 SVG 可渲染，图例/后缀已清理。
- 独立评审报告已落盘（见上）。

## 7. 2026-11-01 二次复审：新证据推翻“可进入 candidate”

在 `agent-handoff.md`、`deployment-forms.md`、`harness-selection.md`、`dsh-freely-plugin-design.md` 完成后，对 C-B/C/C-D 的 promotion readiness 重审：

- **C-B**：A2A 实际是 task 行，不是 message/artifact 历史；`acp_session_connect` 在 new/fork 丢 message；原 acceptance “五类消息 owner + 真实回放”未做。→ `needs_research`。
- **C-C**：Freely 已有 STABLE/SEMI/DYNAMIC 排序，但无 manifest/校验；report/attention 字段契约与基线未做。→ `needs_research`。
- **C-D**：原 candidate 把“DSH adapter”混进 HarnessPort；新研究拆成 C-D（HarnessPort/角色级选择）与 C-E（Freely-host 插件）。→ `needs_research`。
- **C-E**：插件架构有代码级依据（DSH 注入 services），但无 P0/P1 spike。→ `needs_research`。

二次 verdict：**needs_more_research**，不是 promote。下一步按 C-B/C 的行为盘点与协议草案、C-D 的接口/探测、C-E 的 P0/P1 spike 分别补证据，再走 acceptance review。

这与第一次 `pass-with-gaps` 不矛盾：第一次评的是“研究包是否足以起草 candidate”；第二次评的是“candidate 是否能进入 B2”。结论是：可以起草，但不能 promote。

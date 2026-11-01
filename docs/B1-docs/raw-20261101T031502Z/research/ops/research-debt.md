---
audit_id: DEBT-20261101T031502Z
phase_state: research_closed
created_at: 2026-11-01
---

# 研究债台账：还有哪些没研究透

> 标准：acceptance_criteria 的每一条都要有“研究证据/实现证据”。没有证据的，不能 promote；不能用“应该可以”代替。

## 0. 总表

| Candidate | 研究缺口 | 实现/验证缺口 | 关闭证据 | 当前状态 |
| --- | --- | --- | --- | --- |
| C-F 讨论入口 | ✅ `intake.md` 六类 schema/准入/选型；✅ 真实 issue/PR/CI 回放 | platform-adapter 方法、events 表、scan 读取 | `intake.md` + `replay/intake_replay.py` 输出 | needs_research（实现待 B2） |
| C-B ownership/handoff | ✅ 五类现状/目标矩阵；✅ 协议 v0；✅ 状态机回放 | new/fork 丢 message 修复、handoff 表/真实回放 | `handoff.md` §2.1 + `handoff_replay.py` | needs_research（实现待 B2） |
| C-C report/attention/prompt | ✅ schema/A2A 映射/manifest；✅ prefix/cache 回放；✅ 可观测性基线 | 真实 patrol 对照 | `runtime-contracts.md` §3.1-3.2 + `prompt_manifest.py` | needs_research（对照待 B2） |
| C-D HarnessPort | ✅ Protocol/RoleConfig/JSON 契约；✅ 主项目三角色 probe 输出 | 角色级选择/`--role` 实现 | `harness-strategy.md` §1.1-1.5 | needs_research（实现待 B2） |
| C-E DSH 插件 | ✅ 服务注入/插件骨架静态 spike；✅ create/resolveAgent API 编译验证 | 真实 host 加载、Python bridge、首次 session、gate E2E | `dsh-freely-plugin-design.md` §2.4 + `spike/dsh-plugin-contract.ts` | needs_research（实现待 B2） |

## 1. 研究关闭明细

| Candidate | 已关闭的研究债（证据） | 剩余 B2 债 |
| --- | --- | --- |
| C-F | 六类来源/event schema/准入/scan-vs-events 选型：`intake.md` §1-§6；真实 issue #4070 comment、`cli/cli#14879` PR review/CI 形状 + 幂等：`replay/intake_replay.py`（10→5，dedupe_ok） | adapter 方法、events 表、scan/queue 读取、runtime 回放 |
| C-B | 五类现状/目标矩阵：`handoff.md` §2.1；protocol v0：§6；状态机 + 真实 #4070 两条评论回放：`replay/handoff_replay.py` | new/fork 发 message + 角色 prompt、handoff 表、runtime E2E |
| C-C | report/attention/批量决策 schema + A2A 映射：`runtime-contracts.md` §3.1；11 段 manifest/三态：§3.2；prefix/cache 回放：`replay/prompt_manifest.py`；可观测性基线：21 条全 estimated、hit_rate=null | A2A 字段落库、manifest 日志、真实 patrol 对照 |
| C-D | HarnessPort Protocol、RoleHarnessConfig、per-role probe/JSON 契约：`harness-strategy.md` §1.1-§1.4；主项目三角色 probe（reviewer fork degraded）：§1.5 | `--role`、apply/validate、UI/CLI 后端、运行中 session 处理 |
| C-E | DSH 插件静态契约 spike：`dsh-freely-plugin-design.md` §2.4；`spike/dsh-plugin-contract.ts` 在 DSH 类型环境编译通过 | 真实 host 加载、Python bridge、首次 session、gate/usage E2E |

## 2. 研究债关闭规则

- 每行“已关闭”必须有文档/脚本/日志链接；没有就保持 needs_research。
- “剩余 B2 债”不是研究债，进入 B2 的 `b2_acceptance`；B1 promotion gate 不再要求 runtime E2E。
- C-E 的 runtime P0/P1 spike 仍是 B1 未关闭项：插件能否真实加载/调用是可行性，不是实现验收；没跑不 promote。

## 6. 跨切面债

| 债 | 说明 | 关闭方式 |
| --- | --- | --- |
| I-* canonical 格式 | YAML vs bullet 双写 | ✅ ADR-001：YAML canonical，bullet 投影 |
| phase 单写者 | wt-create/pr-review/pr-merge 各写 | ✅ ADR-002：phase transition 命令 + 转移表 |
| TDD `change_surface` | 未定义字段/校验 | ✅ ADR-003：面级最低证据 |
| 注意力度量 | 无基线 | ✅ ADR-007：先埋点，后算指标 |
| MCP | `mcpServers: []` | ✅ ADR-004：harness 拥有，Freely 传递 |
| 语义 Watchdog | 只有进程/SSE | ✅ ADR-005：Manager 调用的轻量 reviewer |
| raw issue absorbed | C-B~F 在 absorbed raw 下 | ✅ ADR-006：直接 promote，不重开 raw |

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

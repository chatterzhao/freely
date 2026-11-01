# Tasks: Super-agent 架构对比、实现质量评估与方向立项

- issue_id: I-20261101T031502Z-A
- owner: I-20261101T031502Z-A

| # | 任务 | 产出 | 状态 |
| --- | --- | --- | --- |
| T1 | 读取文章要点与原型 9 篇设计文档、prompts、核心 src | 事实清单与证据分级 | done |
| T2 | 读取 Freely 三角色、A2A、three-loop、scan、session 协议 | Freely 现状清单 | done |
| T3 | 逐维比较并识别结构性差异 | `brainstorms.md` §4–§5 | done |
| T4 | 评估路由、交接、缓存的实现质量 | `brainstorms.md` §4.12 | done |
| T5 | 建立 Super-agent → Freely 全量概念映射 | `concept-map.md` | done |
| T6 | 评估 harness 抽象、ACP/A2A/插件边界 | `brainstorms.md` §4.13 | done |
| T7 | 登记三个 needs_research candidate 并绑定 milestone | `candidates.md`、`milestones.md` | done |
| T8 | 用 archify 生成协作拓扑图与 HarnessPort 边界图 | 两张 `.html` + `.svg` | done |
| T9 | 写 PRD / pre-tests / IDN 并跑门禁 | 本目录产物 + 证据日志 | done |
| T10 | 实现 P0：能力矩阵 + 角色读取 + 二进制探针 + cache 聚合 | `harness_status.py`、`bin/harness-status`、`freely harness-status` | done |
| T11 | 写 5 项单测（角色/能力、cache 去重、require 失败、缺表、未知工具） | `scripts/tests/test-harness-status.py` | done |
| T12 | 在 test 工位跑单测与 CLI 验收 | 2 条新证据日志 | done |

## 后续（不在本 issue 内）

- C-B follow-up ownership：先做五类后续消息的行为盘点，再决定是否进入 B2。
- C-C 路由/交接/cache：先做 patrol 成本与 cache 基线，再决定改 prompt/skill 还是 runtime。
- C-D HarnessPort：先做 ACP 能力矩阵与 DSH adapter spike，再决定接口与插件边界。

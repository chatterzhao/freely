---
review_id: B1-REV-20261101T031502Z
phase_state: completed
reviewer: subagent:2db58fae-5163-4307-b247-9564ffea4416 + session desk review
mode: subagent / desk-review
verdict: needs_more_research
created_at: 2026-11-01
---

# B1 预研评审：结论与 readiness

## 0. Verdict

**C-F/B/C/D promoted；C-E 仍 needs_more_research。** 研究级 gate 已通过独立 review；运行时验收转入 B2 `b2_acceptance`。

第一次独立评审的 `pass-with-gaps` 评的是“研究包是否足以起草 candidate”；新证据（A2A task 行、new/fork 丢消息、scan 无讨论入口、DSH 服务注入面）出来后，第二次评审的结论是“candidate 还不能 promote”。

## 1. 已修问题

| 问题 | 处理 |
| --- | --- |
| DSH 路线表述矛盾 | README 改为“不做 adapter；方向是 @freely/dsh-freely 插件”；`research/harness/harness-strategy.md` 区分 A/B1/B2/C |
| 循环口径不一致 | 统一为“3 常驻 loop + 2 段交付门禁” |
| “AI 是项目所有者”是收益断言 | 改为“目标态”；注意力度量无基线 |
| 图例模板残留 | 重叠图/交付图改为实际分类，删除“架构组件”后缀 |
| DSH 缺 SHA/URL | 补 `6337fc8...` 与 repo URL |
| 量化事实缺复现命令 | `research/delivery/runtime-contracts.md` 保留数据与命令 |
| issue-sync “唯一出口”过强 | 改为“出站统一走封装命令” |
| scan 未标派生视图 | README 标注“派生、不写回” |
| 四问/四层/六维混用 | 阶段评审=四层；PR 评审=四问 |
| 过程稿重复 | 合并为 16 份结论文档；删除 research/synthesis/article/harness-port/deployment/adapter 等重复过程稿 |

## 2. Readiness matrix

| Candidate | 已有 | 仍缺 | 下一跳 |
| --- | --- | --- | --- |
| C-F 讨论入口 | `research/delivery/intake.md`、`replay/intake_replay.py` | promoted；B2 做 adapter/events/scan | — |
| C-B ownership/handback | `research/delivery/handoff.md`、`replay/handoff_replay.py` | promoted；B2 修 new/fork + 表 | — |
| C-C report/attention/prompt | `research/delivery/runtime-contracts.md` §3.1-3.2、`replay/prompt_manifest.py` | promoted；B2 做真实 patrol 对照 | — |
| C-D HarnessPort/角色选择 | `research/harness/harness-strategy.md` §1.1-1.5 | promoted；B2 做 --role/apply/UI | — |
| C-E DSH 插件 | `research/dsh-plugin/dsh-freely-plugin-design.md` §2.4 | needs_research：真实 host/Python bridge/E2E 未跑 | P0/P1 spike → review |

C-F/B/C/D 已 promoted；C-E 仍待 runtime spike。

## 3. B1 loop

```
研究 → acceptance_criteria 自检 → 缺口 → 回研究
     → promotion_gate → 独立 acceptance review → B2
```

优先级：**C-F 讨论入口 → C-B/C 交接 → C-D harness → C-E 插件**。这是主意图顺序，不是实现偏好。

## 4. 验证

- candidates/milestone 状态一致（A promoted；B/C/D/E/F needs_research）。
- README/文档链接 0 缺失。
- `pretests-gate` 通过。
- 已知仓库既有 `governance-check` 5 个缺陷，见 `research/ops/docs-directory-audit.md`；不是本轮引入，未绕过。

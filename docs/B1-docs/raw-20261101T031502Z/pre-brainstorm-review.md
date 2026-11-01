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

**needs_more_research。** 研究包足以起草 candidate，但 C-F/C-B/C/C-D/C-E 都未达到 promotion gate；不能进入 B2/实现。

第一次独立评审的 `pass-with-gaps` 评的是“研究包是否足以起草 candidate”；新证据（A2A task 行、new/fork 丢消息、scan 无讨论入口、DSH 服务注入面）出来后，第二次评审的结论是“candidate 还不能 promote”。

## 1. 已修问题

| 问题 | 处理 |
| --- | --- |
| DSH 路线表述矛盾 | README 改为“不做 adapter；方向是 @freely/dsh-freely 插件”；`harness-strategy.md` 区分 A/B1/B2/C |
| 循环口径不一致 | 统一为“3 常驻 loop + 2 段交付门禁” |
| “AI 是项目所有者”是收益断言 | 改为“目标态”；注意力度量无基线 |
| 图例模板残留 | 重叠图/交付图改为实际分类，删除“架构组件”后缀 |
| DSH 缺 SHA/URL | 补 `6337fc8...` 与 repo URL |
| 量化事实缺复现命令 | `runtime-contracts.md` 保留数据与命令 |
| issue-sync “唯一出口”过强 | 改为“出站统一走封装命令” |
| scan 未标派生视图 | README 标注“派生、不写回” |
| 四问/四层/六维混用 | 阶段评审=四层；PR 评审=四问 |
| 过程稿重复 | 合并为 16 份结论文档；删除 research/synthesis/article/harness-port/deployment/adapter 等重复过程稿 |

## 2. Readiness matrix

| Candidate | 已有 | 仍缺 | 下一跳 |
| --- | --- | --- | --- |
| C-F 讨论入口 | `intent-alignment.md` §4.1、scan 代码证据 | 六类来源 event schema；真实 issue 评论/PR review 回放 | 来源盘点 → 回放 → acceptance review |
| C-B ownership/handback | `handoff.md` 五类 owner、幂等/超时 | 行为盘点；真实 PR/issue 评论回放；new/fork 修复 | 回放 → acceptance review |
| C-C report/attention/prompt | `handoff.md` 字段、`runtime-contracts.md` 排序 | prompt manifest/校验；cache/usage 基线；patrol 对照 | 补 manifest/基线 → 对照 |
| C-D HarnessPort/角色选择 | `harness-strategy.md`、`harness-selection.md` | 接口草案；per-role probe 证据 | 接口 → probe |
| C-E DSH 插件 | `dsh-freely-plugin-design.md` | P0/P1 spike（首次 session 消息、handoff、gate） | spike → review |

任一“仍缺”未关闭，status 保持 `needs_research`，不得 promote。

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
- 已知仓库既有 `governance-check` 5 个缺陷，见 `docs-directory-audit.md`；不是本轮引入，未绕过。

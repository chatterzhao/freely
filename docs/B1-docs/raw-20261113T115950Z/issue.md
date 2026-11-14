---
schema_version: '1'
local_id: raw-20261113T115950Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T115950Z-A
platform_ids:
  github:
    issue_id: '4342'
    url: https://github.com/chatterzhao/freely/issues/4342
    synced_at: ''
  gitee:
    issue_id: IKV7I4
    url: https://gitee.com/zhaoquan/freely/issues/IKV7I4
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T115950Z/issues/I-20261113T115950Z-A.md
last_synced_comment_at:
  github: '2026-11-14T02:41:17Z'
  gitee: '2026-11-14T02:41:17Z'
hash: ''
created_at: '2026-11-13T11:59:50Z'
updated_at: '2026-11-14T02:41:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T115950Z-A
source_candidate: ''
completed_at: '2026-11-14T02:41:17Z'
closeout_note: ''
severity: P1
---

# docs: pr-review-guarded 的执行引导未包含 L0，规则无法落地

workflow_kind: feature

## docs: pr-review-guarded 的执行引导未包含 L0，规则无法落地

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T115950Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T11:59:50Z |
| updated | 2026-11-13T11:59:50Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T115950Z`。实现前请用 `wt-create --raw-key 20261113T115950Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

R33.14 / #4339 只把 L0 写进了 freely-tdd-review/SKILL.md，但 pr-review-guarded 的**执行引导**没有同步：

1. ACP reviewer prompt（docs/system/workspace/scripts/worktree/pr-review-guarded 约 535 行）仍只写 "Follow skill:freely-tdd-review (TDD four-question review)"，要求的 JSON 只有 red / green / adequacy / refactor 四个维度，**没有 L0 / intent / drift 维度**。
2. 人工回退提示（同文件约 746 行）的步骤 3 仍是「每级检查：下层是否忠实消化了上层？」——完全没有 L0。
3. 结果是：reviewer 可以只跑四层就给出 verdict: pass，L0 规则形同虚设；R33.8–R33.10 那类「四层全绿但整体漂移」仍可通过。

## 设计意图（已核实）

- freely-tdd-review/SKILL.md 已明确「L0 先于四层；L0 不通过直接 fail」「四层自洽不能替代项目一致」。
- pr-review-guarded 是评审的唯一执行入口（ACP 与人工回退都走它），引导必须与 skill 一致，否则规则不落地。

## 期望

1. ACP prompt 的 Instructions 增加 L0 段：要求先引用外部锚点原文（设计文档 / 既有验收测试 / 门禁源码注释 / 既有同类实现），再回答 Q1–Q5；有门禁改动时必须给四段证据。
2. 评审 JSON 增加 intent 维度（status: pass|fail + note），或在 summary 中强制包含 L0 五问结论——**先确认 review_verdict 的解析面**：若只解析顶层 verdict，新增维度是安全的；若会校验维度集合，则改用 summary 约束，避免破坏契约。
3. 人工回退步骤加入「先做 L0，再逐层」，并要求 review 文档包含 "## L0：项目意图一致性" 段。
4. AT：断言 prompt 与人工提示都含 L0 关键词与五项必答；负向控制断言基线（当前 develop）不含；同时断言 review_verdict 的现有解析行为不变（避免改了引导却破坏门禁）。

## 边界

- 不改 L0 的五项内容与失败判据（那是 #4339 已定的）；
- 不放宽任何门禁；若新增 JSON 维度，必须保证 pr-merge-guarded 读取 verdict 的逻辑不变；
- 不把「review 文档有没有 L0 段」做成可补字段通过的门禁——L0 的价值在于引用外部锚点，不在于字段存在。

### comment-20261114T024117Z
- source: system
- event: promote_finalized
- children: ["I-20261113T115950Z-A"]

拆解为以下任务:
1. [I-20261113T115950Z-A](will-be-updated)

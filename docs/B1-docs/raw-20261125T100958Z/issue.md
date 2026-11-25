---
schema_version: '1'
local_id: raw-20261125T100958Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261125T100958Z-A
platform_ids:
  github:
    issue_id: '4704'
    url: https://github.com/chatterzhao/freely/issues/4704
    synced_at: ''
  gitee:
    issue_id: IKXZ80
    url: https://gitee.com/zhaoquan/freely/issues/IKXZ80
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T10:09:58Z'
updated_at: '2026-11-25T10:10:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: 2026-11-25T12:35:00Z
closeout_note: ''
severity: P1
---

# fix: feedback edit 应脱离 wt-create 按 raw key 直接改平台单

workflow_kind: fix

## fix: feedback edit 应脱离 wt-create 按 raw key 直接改平台单

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T100958Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `none` |
| created | 2026-11-25T10:09:58Z |
| updated | 2026-11-25T10:10:07Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T100958Z`。实现前请用 `wt-create --raw-key 20261125T100958Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
`freely feedback edit --raw-key <key> --title|--body` 要求本地已存在 `docs/B1-docs/raw-<key>/issue.md`，否则报 `local issue file not found`（runtime/freely:25179）。但 `feedback create` 只在平台建单、**不生成本地文档**（设计如此，本地文档由 `wt-create` 物化）。于是 create 后无法直接 edit，形成命令链断裂。

## 边界澄清（用户 2026-11-25 明确）
- **feedback 不创建本地文档是有意设计**：本地文档是 `wt-create` 的职责（wt-create 代表「要实现这条 raw issue」）。
- **修改 raw issue 不等于要实现它**：`feedback edit` 必须与 `wt-create` 完全解耦；不得要求先建工位、不得依赖本地 issue.md 存在。
- 本次修的是「编辑平台单」能力，不触碰 wt-create 的物化语义。

## 根因
`cmd_feedback` 的 edit 分支无条件读取本地 issue.md 来提取三样东西：platform_ids、kind、body 前缀（`workflow_kind:`）。缺本地文件时这三项全拿不到，于是直接 return 1——即使平台单完全可以通过 raw key 定位。

## 现成能力（无需改底层 adapter）
platform-adapter.py 已具备全部所需只读/写能力：
1. `search <raw_key>`（顶层 `search_raw_issue`，:1121）：双平台按 raw key 枚举，返回每平台 `issue_number/title/url/matches`（GitHub 按 title+body 搜索，Gitee 分页全量本地匹配），只读。
2. `discover-raw <raw_key>`（:1183）：按 `[RAW-<key>]` 前缀解析身份。
3. `update-issue <local_id> <platform_ids_json> <title> <body>`（顶层 `update_issue`，:1106）：逐 configured platform 写，已汇总双平台结果（#4671 修过部分成功）。
4. 两个 handler 的 `update_issue`（:686 GitHub / :344 Gitee）都只在 title/body **非空**时才加对应参数——空字段不覆盖，天然支持只改标题或只改正文。

## 期望
`feedback edit --raw-key <key>` 支持两条路径，行为一致：
1. **本地文档存在**（既有行为，保持兼容）：从 issue.md 取 platform_ids / kind / body 前缀；调用 update-issue 后同步更新本地 body。
2. **本地文档不存在**（新增）：用 `search <raw_key>` 从平台按 raw key 发现各平台 issue_id，组装 platform_ids JSON，再调 `update-issue`；**不写本地文件**（无本地文档可写，也不创建）。
   - 内容来源：**仅显式参数**——`--title`/`--body` 由调用方给出，空字段传空串由 adapter 跳过（不覆盖、不回读平台）。语义与 `comment` 一致：纯平台写命令，不依赖本地状态。
   - 平台发现失败（0 匹配 / 多义 / 不可读）→ fail-closed，给出可操作报错（含 `freely feedback --help` 与平台搜索命令），不得静默跳过或伪装成功。
   - 双平台写结果汇总：任一失败 → 非零退出 + 完整回执（沿用 #4671 语义），不得部分成功伪装整体成功。
   - 标题需 canonical：有 title 时用 `canonical_raw_title` 规范化（复用既有逻辑，:25120 附近）。

## 验收建议（TDD，最小可复现）
- RED：在只有平台单、无本地 issue.md 的情况下 `feedback edit --raw-key <k> --title ...` → 现状 rc=1（local issue file not found）。
- GREEN：同一场景 → 平台按 raw key 发现 ids → update-issue 成功，双平台回执 success；本地仍无 issue.md（证明未创建本地文档、未耦合 wt-create）。
- 兼容回归：有本地文档时 edit 行为不变（含本地 body 同步）。
- 只改标题：`--title` 单独给出 → 平台 body 保持原样（空 body 不覆盖）。
- 只改正文：`--body` 单独给出 → 平台 title 保持原样。
- fail-closed：raw key 在平台 0 匹配 → 非零 + 可操作报错；双平台部分失败 → 非零 + 完整回执。
- 回归：现有 feedback/issue-sync AD 与 test-all 全绿。

## 非目标
- 不改 `feedback create` 不生成本地文档的设计；不改 `wt-create` 物化语义；不改变平台写必须经 adapter 的纪律；不夹带 #4702（push 吞错）、#4703（证据沿袭）、#4698、#4687。

## 与既有 raw 的关系
raw-20261125T094413Z（#4703）覆盖 test 工位证据 stale 判据；本条覆盖 feedback edit 的平台单编辑入口解耦，边界不重叠。

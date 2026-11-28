---
schema_version: '1'
local_id: raw-20261113T141456Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T141456Z-A
platform_ids:
  github:
    issue_id: '4435'
    url: https://github.com/chatterzhao/freely/issues/4435
    synced_at: ''
  gitee:
    issue_id: IKV85U
    url: https://gitee.com/zhaoquan/freely/issues/IKV85U
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/issues/I-20261113T141456Z-A.md
last_synced_comment_at:
  github: '2026-11-28T10:15:59Z'
  gitee: '2026-11-28T10:15:59Z'
hash: ''
created_at: '2026-11-13T14:14:56Z'
updated_at: '2026-11-28T10:16:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T141456Z-A
source_candidate: ''
completed_at: '2026-11-28T10:15:58Z'
closeout_note: ''
severity: P1
---

# fix: 跨 raw 只允许走 governance-only lane，但机制未接线且 GATE 1 不给指引

workflow_kind: fix

## fix: 跨 raw 只允许走 governance-only lane，但机制未接线且 GATE 1 不给指引

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T141456Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T14:14:56Z |
| updated | 2026-11-13T14:14:56Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T141456Z`。实现前请用 `wt-create --raw-key 20261113T141456Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：跨 issue 的既有机制（已核实历史讨论）

raw-20261103T091157Z（platform issue-parity）的 prd / IDN / code-review 明确写过：

> GATE 1（一个工位一个 raw issue）下，跨 raw key 的文档物化/回填不能混入本 lane，**必须单独 governance-only lane + FREELY_SKIP_IBM_GATE**。

也就是说项目**已经设计**了跨 issue 的放行机制，只是它没有被文档化到可执行层，也没有接进 GATE 1 的报错与工具链。

## 现象（R33.18 真机）

用户要求「同步本地与平台 issue 状态并对齐」，执行 `issue-sync batch` 改了 108 个跨 raw 的 B2 文档；随后 `pr-create-guarded` 的 `governance-merge-gate` GATE 1 报：

    GATE 1: timestamp mismatch ... issue raw-20260612T000223Z ...
    诊断步骤: ... 一个工位处理了多个 raw issue → 违反一个工位一个 issue

**报错只教人「拆工位」，没有指出 governance-only lane**。结果是执行者（本会话）为了让流程走通，短暂删掉了 `wt-close` 的 `platform_state` 前置检查——把门禁冲突转嫁成了实现语义退化。这正是「跨 issue 机制不可执行」导致的次生事故。

## 四个具体缺口

1. **GATE 1 报错不带放行指引**：只列「拆工位 / 迁移 / 移除」，不提 `FREELY_SKIP_IBM_GATE` + governance-only lane。
2. **两处白名单真源不一致**：`governance-merge-gate.is_governance_only_path()` 硬编码默认含 `docs/system/workspace/skills/`、`docs/system/workspace/scripts/quality/`、`hooks/*.md`；而 `.freely/config.toml [skip_ibm_gate].allowed_paths` 覆盖后只含 `templates/`、`docs/B1-docs/`、`docs/B2-docs/`、4 个 md。config 优先 → 默认值与实际行为脱节，读代码的人会误判。
3. **没有「跨 raw 状态同步」的明确入口**：`issue-sync batch` 无范围参数时天然跨 raw，在任何 raw 工位里跑都会撞 GATE 1；有范围参数时又只能同步一个 raw。缺少「全量同步 = governance-only lane」的官方说法与命令。
4. **没有测试覆盖放行边界**：没有任何 AT 断言「哪些路径可以跨 raw、哪些必须拒绝」，所以 GATE 1 与 skip 路径都没有回归保护。

## 期望：两条 lane 的显式契约

| lane | 允许的变更 | 是否允许跨 raw | 判定 |
|---|---|---|---|
| **issue lane**（默认） | 实现 / 能力 / 契约 / 测试（`bin/`、`docs/system/scripts`、`contracts/`、`src/` 等） | **禁止**（GATE 1 准确拒绝） | 无 skip |
| **governance-only lane** | 纯治理/状态同步（`docs/B1-docs/`、`docs/B2-docs/`、`docs/milestones.md`、`epics-map.svg`、`templates/`） | **允许** | `FREELY_SKIP_IBM_GATE` + `is_governance_only_path` |

具体：
1. `is_governance_only_path` 与 config 单一真源：删掉硬编码默认（或由 config 生成），避免两套白名单。
2. GATE 1 的报错追加：`如果这是跨 raw 的纯文档/状态同步，请走 governance-only lane：FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<理由>"`。
3. `issue-sync batch` 显式化范围：`--raw-key <key>`（本 raw 工位用）与默认全量（打印「全量同步跨 raw，必须走 governance-only lane」）。
4. AT：
   - issue lane 改其他 raw 的 `docs/B2-docs/**` → GATE 1 拒绝；
   - governance-only lane 改同样路径 + `FREELY_SKIP_IBM_GATE` → 允许；
   - `bin/` 或 `docs/system/scripts/` 在两种 lane 下都拒绝；
   - 白名单与 config 完全一致（差集为空）。

## 边界

- 不放宽 implementation 路径的跨 raw 限制；不改 `docs/LAWS.md` 的「一个工位一个 issue」；
- 不放宽 reason 前缀校验；不新增第三种 lane；
- 不把「补字段/造数据」当作放行手段。

### comment-20261128T101559Z
- source: system
- event: promote_finalized
- children: ["I-20261113T141456Z-A"]

拆解为以下任务:
1. [I-20261113T141456Z-A](will-be-updated)

---
schema_version: '1'
local_id: raw-20261111T083905Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261111T083905Z-A
platform_ids:
  github:
    issue_id: '4291'
    url: https://github.com/chatterzhao/freely/issues/4291
    synced_at: ''
  gitee:
    issue_id: IKULWN
    url: https://gitee.com/zhaoquan/freely/issues/IKULWN
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/skills/skill-merge-compat/raw-20261111T083905Z/issues/I-20261111T083905Z-A.md
last_synced_comment_at:
  github: '2026-11-11T09:12:11Z'
  gitee: '2026-11-11T09:12:11Z'
hash: ''
created_at: '2026-11-11T08:39:05Z'
updated_at: '2026-11-11T09:26:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261111T083905Z-A
source_candidate: ''
completed_at: '2026-11-11T09:12:10Z'
closeout_note: ''
severity: P2
---

# refactor: 为 skill 删并建索引兼容期并收敛总数

workflow_kind: feature

## refactor: 为 skill 删并建索引兼容期并收敛总数

| Field | Value |
|-------|-------|
| local_id | `raw-20261111T083905Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-11T08:39:05Z |
| updated | 2026-11-11T08:39:05Z |

---

> **Freely 治理**：这是 raw issue `raw-20261111T083905Z`。实现前请用 `wt-create --raw-key 20261111T083905Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 根因

#4164（收敛 37 个 skill 的重叠分组）的验收标准 2 要求「至少 2 组完成合并、skill 总数 ≤25」。R28 前置评审逐个读了 9 个 SKILL.md，结论是三组并非重复实现，而是同一链路的不同阶段/owner：执行流程组是 workflow 明确区分的 RED→dev→GREEN 三阶段；人类中断组是 triage（首次 reaction 路由）/ handling（manager 深度解释）/ direct-answer（runtime dispatcher 直接 claim）；worktree 组分别判脏树阈值、merge 顺序退役、fleet 批次。直接删并会破坏 dispatcher 的 claim 路径与 TDD 顺序。

但「37 个 skill 首跳要读多个文件」的成本确实存在，且删并会牵动 AGENTS.md、freely-workflow-guarded-execution、hooks、skill 索引、路由测试与打包白名单，需要独立的兼容期，不能夹带在 R28 的零语义变更 PR 里。R28 已落地 skill-map.yaml（37 条 loop/owner + 3 组判定 + 12 loop 唯一入口）、37 份 frontmatter 的 supersedes 预留字段与 bin/check-skill-frontmatter 的孤儿检查，本 issue 承接真正的删并。

## 影响

- 37 个 SKILL.md 首跳阅读量与误路由概率偏高，矩阵只能固定真源、不能减少文件数。
- 没有索引兼容期就删 skill 会留下悬空引用（AGENTS.md 的全链路、workflow skill 的 [skill] 节点、hooks 的 skill 名、打包白名单）。
- supersedes 目前全为 []，删并后不回填会让历史引用不可追溯。

## 修复方案

1. 先做引用普查：全仓 grep 每个待删 skill 名，列出 AGENTS.md / workflow / hooks / skill 索引 / tests / packaging 的全部引用点，做成清单。
2. 建索引兼容期：保留被删 skill 名为 skill-map.yaml 的 alias 条目（指向保留入口），lint 支持 alias 且对未迁移引用 fail-closed；所有引用点先改读矩阵入口。
3. 按组逐个删并：每组保留一个入口 skill，其余正文合并为子章节或删除；总数目标 ≤25；每删一个同步 skill-map.yaml 的 skills/routing/overlap_groups 与保留 skill 的 supersedes。
4. 补 AT：路由测试按 loop 断言唯一入口可达；lint 断言无孤儿、无悬空 alias、supersedes 目标存在；新增回归比较 develop 基线。
5. 打包与安装态验证：确认删除的 skill 不残留在 package-allowlist 与已激活版本。

## 验收标准

- RED：在 develop 基线上，引用普查清单/alias 兼容层/supersedes 回填/删除后的路由测试均不存在。
- GREEN：≥2 组完成删并、skill 目录数下降且 ≤25；lint 0/1/2 三态仍成立且真实语料 rc=0。
- GREEN：全仓无被删 skill 名的悬空引用；AGENTS.md 与 workflow 全链路仍可执行。
- GREEN：matrix 的 routing 每个 loop 仍唯一可达；supersedes 记录被合并 skill；epics-map 与 milestone 同步。
- 不退化：freely-workflow-guarded-execution 的 RED→dev→GREEN 顺序不变；dispatcher 的 triage/handling/direct-answer 三条 claim 路径不变。

## 排期

由 R28 拆出，排入 goal v5 队列 R28.5，紧跟 R28 之后、R29 之前。

### comment-20261111T091210Z
- source: system
- event: promote_finalized
- children: ["I-20261111T083905Z-A"]

拆解为以下任务:
1. [I-20261111T083905Z-A](will-be-updated)

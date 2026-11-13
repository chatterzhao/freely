---
schema_version: '1'
local_id: raw-20261113T113100Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T113100Z-A
platform_ids:
  github:
    issue_id: '4339'
    url: https://github.com/chatterzhao/freely/issues/4339
    synced_at: ''
  gitee:
    issue_id: IKV7ES
    url: https://gitee.com/zhaoquan/freely/issues/IKV7ES
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T113100Z/issues/I-20261113T113100Z-A.md
last_synced_comment_at:
  github: '2026-11-13T11:35:58Z'
  gitee: '2026-11-13T11:35:58Z'
hash: ''
created_at: '2026-11-13T11:31:01Z'
updated_at: '2026-11-13T11:44:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T113100Z-A
source_candidate: ''
completed_at: '2026-11-13T11:35:57Z'
closeout_note: ''
severity: P1
---

# docs: 评审 skill 缺 L0 项目意图一致性锚点，设计漂移无法被发现

workflow_kind: feature

## docs: 评审 skill 缺 L0 项目意图一致性锚点，设计漂移无法被发现

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T113100Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T11:31:01Z |
| updated | 2026-11-13T11:31:01Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T113100Z`。实现前请用 `wt-create --raw-key 20261113T113100Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：一次真实的评审失效

2026-11-13，用户人工复核发现 R33.8 / R33.9 / R33.10 三处实现虽然**全部通过了现有评审**，但都违背项目整体设计意图：

1. R33.8 新增 `close-linked`：只校验 `kind` + `platform_ids` 就关平台，不检查 `phase_state`，绕开了 `issue-sync batch` 的状态驱动收口与 raw 的 Phase 1 严格校验；还引入 `status: closed` 作为第二套收口语义。
2. R33.9 给 `_resolve_branch_from_raw_key` 加 `test-pre-merge-*` 回退；R33.10 又给 `_is_protected_branch` 开 `--force --discard-unmerged` 例外——两者都与 `test-wt-close-protected-branch-guard` Test 1–3「test-pre-merge-* 一律 blocked」直接冲突，并让丢弃型沙箱跑了完整 raw 生命周期（平台关单 + Phase 7 develop 同步）。
3. R33.8 在 raw 副本一致性判红时手工补 `### comment-` 块凑过门禁。

这些问题的共同点：**在评审当时，B1/B2 文档完全自洽、AT 全绿、四层 fidelity 审查全部通过**。漂移发生在「上层本身错了」，而现有评审只审「下层有没有忠实于上层」。

## 缺口定位（已读源码确认）

`docs/system/workspace/skills/freely-tdd-review/SKILL.md` 的核心方法只有一条主线：
「相邻节点之间有没有忠实消化」——raw→B1→candidate→milestone→B2→实现→测试，逐层检查 fidelity。
它**没有**任何以「本轮之外的项目资产」为锚的检查：
- 项目设计文档（`docs/system/workspace/scripts/README.md`、contracts、AGENTS.md）
- 既有验收测试（尤其是断言「必须拒绝 / 必须阻止」的测试）
- 既有门禁的源码注释与设计理由
- 既有实现（是否已有同类能力、是否在造第二套）

也没有明确要求评审回答：
- 本轮是否在**放宽**或**绕过**门禁？强度是否下降？
- 是否与既有验收契约**冲突**？
- 是否造成**能力降级**（删除、放宽、强制变可选、fail-closed 变 fail-open）？
- 是否引入**第二套语义/真源**？
- 若确需改门禁，证据链是否包含「当初为什么这样设计 → 现在为什么必须改 → 是设计错误还是实现不达标 → 强度不降」？

## 期望：给评审加一层「L0 项目意图一致性」锚点

1. 在 `freely-tdd-review/SKILL.md` 的核心方法之前新增 **L0：项目意图一致性 / 设计漂移检测**，明确：
   - 外部锚点优先于本轮自证（B1/B2 不能自己证明自己）；
   - 必须读的锚点清单（README/contracts/既有验收测试/门禁源码注释/既有同类实现）；
   - 五个必答问题（冲突、门禁强度、能力降级、第二套语义、设计漂移）；
   - 门禁改动的举证责任与「强度不降」判定；
   - 明确的失败判据（出现任一即不得 pass，即使测试全绿）。
2. `pr-review-guarded` 的人工审查提示与 `code-reviews` 模板同步加入 L0 章节要求，使 verdict 必须显式回答这五项（缺项视为未完成评审）。
3. 增加一条 AT：断言 skill 与 review 模板包含 L0 的五项必答与「外部锚点优先」；负向控制断言缺失 L0 的旧文档必须判红。
4. 回填证据：用 R33.8 / R33.9 / R33.10 三个真实案例作为「L0 应命中」的样例写进 skill（不虚构）。

## 边界

- 只改评审规则文档与模板，不改 `pr-merge-guarded` 的 verdict 判定逻辑（除非 L0 缺项必须 fail-closed，需单独评估）；
- 不放宽任何现有门禁；不引入新的评审轮次机制；
- 不把 L0 做成「又一份可自证的 checklist」——它必须强制引用外部锚点原文。

## 为什么要求走完整流程而不是 doc-only

`.freely/config.toml [skip_ibm_gate].allowed_paths` 不含 `docs/system/workspace/skills/`，因此 `FREELY_SKIP_IBM_GATE` 的 governance-only 快速路径不适用于本改动。这是项目**有意**把 skill 当系统真源：评审规则变更必须走完整 IBM 链路（本 raw 的 B1/B2/AT/PR 本身即为第一次实践）。

### comment-20261113T113558Z
- source: system
- event: promote_finalized
- children: ["I-20261113T113100Z-A"]

拆解为以下任务:
1. [I-20261113T113100Z-A](will-be-updated)

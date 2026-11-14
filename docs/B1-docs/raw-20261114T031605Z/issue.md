---
schema_version: '1'
local_id: raw-20261114T031605Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T031605Z-A
platform_ids:
  github:
    issue_id: '4526'
    url: https://github.com/chatterzhao/freely/issues/4526
    synced_at: ''
  gitee:
    issue_id: IKV9KO
    url: https://gitee.com/zhaoquan/freely/issues/IKV9KO
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261114T031605Z/issues/I-20261114T031605Z-A.md
last_synced_comment_at:
  github: '2026-11-14T08:13:29Z'
  gitee: '2026-11-14T08:13:29Z'
hash: ''
created_at: '2026-11-14T03:16:05Z'
updated_at: '2026-11-14T08:13:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T031605Z-A
source_candidate: ''
completed_at: '2026-11-14T08:13:28Z'
closeout_note: ''
severity: P1
---

# feat: B1 缺设计意图审计，导致拿到 raw 不看设计就局部开干

workflow_kind: feature

## feat: B1 缺设计意图审计，导致拿到 raw 不看设计就局部开干

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T031605Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T03:16:05Z |
| updated | 2026-11-14T03:16:05Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T031605Z`。实现前请用 `wt-create --raw-key 20261114T031605Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：这一课是真实代价换来的

本轮（R33.18 / R33.16）连续出现三次「拿到 raw 就局部开干」：

1. 为了让跨 raw 的对齐通过 GATE 1，短暂**删掉 `wt-close` 的 `platform_state` 前置检查**——把门禁冲突转嫁成实现退化。
2. 为回滚跨 raw 文档执行 `git reset --hard`，**把同分支上已提交的 `cmd-create` 改动一起丢掉**，但 review 文档仍写着 FR-1 已完成（实现与陈述偏离）。
3. 见到「batch 没关链接」就直接改 `cmd-batch` 的关闭判据，事后才去读 `ibm-framework.md` 确认「sync 由确定性生命周期事件驱动」——顺序反了。

共同点：**没有在动手前先判定「这是设计错、设计不完整、实现未完成、实现偏差，还是 bug」**。

## 现行 B1 skill 的缺口（已读源码）

`docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md`：

- B 阶段只有 step 0「审视 issue 价值与时效性」（是否值得做），step 2「读取边界文档 CONSTITUTION/LAWS/PROJECT_INTENT」（只读，不产出判定）。
- 没有要求读**既有验收测试**（尤其「必须拒绝/必须阻止」类断言）。
- 没有要求读**门禁源码注释与理由**、**既有同类实现**、**配置约束**。
- 没有要求给出**四/五分类判定**与**引用原文的锚点**。
- 「完成自检」只查三件套存在性，不查判定质量。

结果：candidate 可以在「没判定过」的情况下产出；到 review 才由 L0 兜底，但那时实现已经写完，返工成本最大。

## 期望：在设计意图审计放进 B1，并在 candidate 上留下可核对的证据

### 1. B1 skill 新增 **B0：设计意图审计**（先于发散，晚于价值审视）

brainstorms.md 必须新增一节（顺序在最前）：

```markdown
## 0. 设计意图审计（先于方案）
- 外部锚点（引用原文，至少两类）:
  - 设计文档: <文件路径>「<原文>」
  - 既有验收测试: <文件名>「<断言原文>」
  - 门禁源码注释/理由: <文件:行>「<原文>」
  - 既有同类实现: <路径>
- 判定（五选一，必须给证据）: 设计正确 / 设计不完整 / 实现未完成 / 实现偏差 / bug
- 与既有断言的冲突: 有/无；有则写「为什么必须冲突、谁该改」
- 影响面: 会被这个判定改变的契约/门禁/文档
```

五分类的理由：这四类问题的修法完全不同——
- 设计正确 + 实现未完成 → 补实现（不是改设计）；
- 设计不完整 → 先补契约/字段，再实现；
- 实现偏差 → 改实现使其符合设计；
- bug → 直接修，但要在锚点里证明「设计本来就要求这样」。

### 2. candidate 带判定，让 M 阶段可核对

candidates.md 每个 candidate 增加两个字段：

```markdown
- design_verdict: <上述五选一>
- anchor_refs: <brainstorms.md#0 里引用过的锚点，至少两条>
```

B1 的「完成自检」增加两项：§0 存在且锚点 ≥2；每个 candidate 的 design_verdict 与 §0 一致。

### 3. 机器校验（防回退，不新增硬门禁）

新增 AT `test-b1-design-intent-audit.py`：
- 断言 skill 含 B0 段、五分类、四类锚点、§0 模板；
- 断言 candidates 模板含 design_verdict / anchor_refs；
- 断言「完成自检」含这两项；
- 负向控制：基线（develop）不含 → 红。

**刻意不做成 pr-create-guarded 的硬门禁**：L0 的教训是「强制字段」会被「补一段空文本」绕过；先靠 skill + 模板 + 自检落地，观察若干轮后再决定是否升级为门禁（若升级，必须校验锚点能在被引用文件里逐字命中，而不是只查字段存在）。

### 4. 与 review L0 的分工（避免重复）

| 层 | 回答的问题 | 时机 | 成本 |
|---|---|---|---|
| B1 §0 | 这个 raw 到底是哪一类问题？该改设计还是改实现？ | 动手前 | 最低 |
| review L0 | 实现有没有偏离项目意图、有没有降级/第二套语义？ | 合并前 | 兜底 |

两者引用同一套锚点，但 B1 是**决策**，review 是**核对**。review 不能替代 B1：到了 review，返工成本已经付过。

## 边界

- 不改 L0 的五问与失败判据（R33.14 / R33.16 已定）；
- 不新增硬门禁；不改 verdict 契约；

### comment-20261114T081329Z
- source: system
- event: promote_finalized
- children: ["I-20261114T031605Z-A"]

拆解为以下任务:
1. [I-20261114T031605Z-A](will-be-updated)

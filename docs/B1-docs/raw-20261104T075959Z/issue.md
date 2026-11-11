---
schema_version: '1'
local_id: raw-20261104T075959Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T075959Z-A
platform_ids:
  github:
    issue_id: '4164'
    url: https://github.com/chatterzhao/freely/issues/4164
    synced_at: ''
  gitee:
    issue_id: IKSW9K
    url: https://gitee.com/zhaoquan/freely/issues/IKSW9K
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/skills/skill-overlap-matrix/raw-20261104T075959Z/issues/I-20261104T075959Z-A.md
last_synced_comment_at:
  github: '2026-11-11T08:40:30Z'
  gitee: '2026-11-11T08:40:30Z'
hash: ''
created_at: '2026-11-04T07:59:59Z'
updated_at: '2026-11-11T08:40:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T075959Z-A
source_candidate: ''
completed_at: '2026-11-11T08:40:29Z'
closeout_note: ''
---

# refactor: 收敛 37 个 skill 的重叠分组

workflow_kind: feature

## 根因
37 个 skill 中存在职责重叠组：执行流程、人类中断、Worktree 治理各有 3 个近似 skill；agent 需要先读多个 skill 才能确定路由，token 成本与误路由概率都上升。

## 证据
- `docs/system/workspace/skills/` 下 37 个 skill 目录（另有 README.md）。
- 重叠组：
  - 人类中断：`freely-human-interruption-direct-answer` / `-handling` / `-manager-triage`
  - Worktree 治理：`freely-worktree-hygiene-supervision` / `-maintenance-governance` / `freely-multi-worktree-supervision`
  - 执行流程：`freely-dev-loop-execution` / `freely-test-execution` / `freely-test-RED-execution`
- 单个 SKILL.md 平均约 100 行，37 个合计约 3,833 行。

## 影响
- agent 路由需要读多个 skill 才能判定，token 成本高。
- 同一规则在多份 SKILL.md 中各写一遍，漂移无检测。
- 新用户难以判断该用哪个 skill。

## 修复方案
1. 先做 skill 依赖/重叠矩阵：输入、输出、触发词、所属 loop、owner。
2. 合并同组：每组保留一个入口 skill，其余降为子章节或引用；合并后目标 ≤25 个。
3. 每个 skill 的 frontmatter 增加 `loop`、`owner`、`supersedes` 字段，供路由使用。
4. 加 lint：SKILL.md 不得重复定义同一枚举/命令表（引用真源）。

## 验收标准
- GREEN：给出 37 个 skill 的重叠矩阵与合并建议表。
- GREEN：至少 2 组完成合并，skill 总数下降且路由测试通过。
- GREEN：每个 SKILL.md frontmatter 含 `loop`/`owner`。
- GREEN：`grep -r "从 gate 源码提取" docs/` 为 0。

### comment-20261111T084030Z
- source: system
- event: promote_finalized
- children: ["I-20261104T075959Z-A"]

拆解为以下任务:
1. [I-20261104T075959Z-A](will-be-updated)

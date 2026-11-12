---
schema_version: '1'
local_id: raw-20261112T031638Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T031638Z-A
platform_ids:
  github:
    issue_id: '4310'
    url: https://github.com/chatterzhao/freely/issues/4310
    synced_at: ''
  gitee:
    issue_id: IKUSRE
    url: https://gitee.com/zhaoquan/freely/issues/IKUSRE
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/issues/I-20261112T031638Z-A.md
last_synced_comment_at:
  github: '2026-11-12T05:48:09Z'
  gitee: '2026-11-12T05:48:09Z'
hash: ''
created_at: '2026-11-12T03:16:38Z'
updated_at: '2026-11-12T12:49:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T031638Z-A
- I-20261112T031638Z-B
source_candidate: ''
completed_at: '2026-11-12T05:48:08Z'
closeout_note: ''
severity: P2
---

# fix: issue-sync 保护分支提示仍引用幽灵 skill 名与过时 --skill 参数

workflow_kind: fix

## fix: issue-sync 保护分支提示仍引用幽灵 skill 名与过时 --skill 参数

| Field | Value |
|-------|-------|
| local_id | `raw-20261112T031638Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/command-wrapper/guidance-text-single-source/raw-20261112T031638Z/issues/I-20261112T031638Z-A.md` |
| created | 2026-11-12T03:16:38Z |
| updated | 2026-11-12T05:48:14Z |

---

> **Freely 治理**：这是 raw issue `raw-20261112T031638Z`。实现前请用 `wt-create --raw-key 20261112T031638Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

R33（#4179）宣称已修「生成器 6 处 + 模板 3 处幽灵 skill 名」，AT-001 也有「生成器与模板零幽灵名」断言。但本轮（R33.5 / #4307）执行 wt-create 时，输出里仍真实打印：

```
[ERROR] issue-sync refuses to run on protected branch: develop
  Bug fix:   skill:freely-fix-execution
  Feature:   skill:freely-feature-execution
  2. wt-create --raw-key <key> --skill <freely-fix-execution|freely-feature-execution> --slug <slug>
```

真源位置：bin/issue-sync 第 126/127/131 行；另有 docs/system/workspace/AGENTS.md.example 第 146 行仍写 `wt-create --raw-key <key> --source <source> --skill <skill> --slug <slug>`。

## 根因

R33 的验收只检查了 AGENTS 生成器与模板的特定位置，没覆盖 bin/issue-sync 的运行时错误文案与 AGENTS.md.example 模板本身。三个名字（fix / feature / feat-execution）在 R33 已证实根本不存在；`--skill` 参数也已被 `--kind fix|feature` 取代。因此每次在 protected root 触发这条 guard 时，都会把后续 agent 引向不存在的 skill 与不存在的参数。

## 伴随的第二个面（B1 阶段评估是否拆 candidate）

同一轮 wt-create 还输出 `[WARN] raw-issue-pull: issue-sync create failed for raw-... (platform title normalization may be incomplete)`，随后 `pull: materialized ... from platform`。即 wt-create 从主仓 develop 调 issue-sync create，必然被 protected-branch guard 拒绝。raw 仍能物化（平台 issue 已由 feedback 创建），但每建一个工位就稳定产生一条 ERROR + WARN 噪音，且平台标题归一化可能不完整。这与文案问题同属「issue-sync 在 protected root 的边界」，但一个是文案、一个是调用路径，B1 需判断是否拆成两个 candidate。

## 影响

误导性中等但持续：这条消息出现在每次新建工位的启动输出里，正是 agent 读取流程指引的时刻。与 R33「生成器/模板零幽灵名」的验收结论直接矛盾，说明该验收的覆盖面不足。

## 建议方向（供 B1 预研）

1. 把 bin/issue-sync 三处改为真实入口 `skill:freely-workflow-guarded-execution` 与 `--source platform --kind fix|feature --slug <slug>`；AGENTS.md.example 第 146 行同步。
2. 把「零幽灵 skill 名」断言从生成器/模板扩展到 bin/ 运行时文案与 AGENTS.md.example，避免再次漏网（R33 的 AT 可复用）。
3. 单独核查 wt-create 的 raw-issue-pull 调用路径：若平台 issue 已存在，应跳过不必要的 create，或改从 dev 工位内调用 issue-sync，消除 protected-root ERROR 噪音。
4. 验收：新建一次 fix 工位，输出中不再出现任何 `freely-*-execution` 幽灵名、不再出现 `--skill`、不再出现 `issue-sync refuses to run on protected branch`。

## 评审结论

真实、可复现（本轮 wt-create 输出即为证据）、与既有验收结论矛盾，应作为独立 fix raw 登记。R33.5 已合并收口，本条不回灌其代码。

### comment-20261112T054808Z
- source: system
- event: promote_finalized
- children: ["I-20261112T031638Z-A", "I-20261112T031638Z-B"]

拆解为以下任务:
1. [I-20261112T031638Z-A](will-be-updated)
2. [I-20261112T031638Z-B](will-be-updated)

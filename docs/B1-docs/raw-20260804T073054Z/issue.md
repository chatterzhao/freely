---
schema_version: '1'
local_id: raw-20260804T073054Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4076'
    url: https://github.com/chatterzhao/freely/issues/4076
    synced_at: ''
  gitee:
    issue_id: IK6EH2
    url: https://gitee.com/zhaoquan/freely/issues/IK6EH2
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-04T07:30:54Z'
updated_at: '2026-08-04T07:31:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

## 现象
codex 启动时批量告警 `⚠ Skipped loading 30 skill(s) due to invalid SKILL.md files`，30 个部署在 `~/.codex/skills/freely-*/SKILL.md`（及部分非前缀目录）的 skill 全部无法加载，报错一致：
`invalid YAML: did not find expected comment or line break at line 2 column 17, while scanning a block scalar at line 2 column 14`

## 根因
`docs/system/workspace/skills/**/SKILL.md` 的 frontmatter 中 `description: >-` 块标量写法错误：`>-` 之后同行直接跟内容（如 `description: >- 内容`），而 YAML 块标量要求 `>-` 后必须换行、内容缩进。该错误由 2026-06-29 批量 commits（`docs: freely-XXX — add use-when triggers to description`，如 44ba1b09b）引入，30/39 个 skill 受影响。
`bin/deploy-skills` 部署时只校验 `name:` 字段存在，未做 frontmatter YAML 解析校验；pre-commit hook 也未对 `docs/system/workspace/skills/**` 做 YAML 校验，因此坏文件一路通过门禁并部署。

## 影响
- codex 每次启动跳过 30 个 skill，freely workflow/B1/B2/RED/dev/test 等核心 skill 全部不可用，治理流程名存实亡
- `freely deploy-skills` 无法拦截，问题会持续扩散到新 skill

## 附带问题
- 部署目录 `~/.codex/skills/`（及 `~/.claude/skills/`）混存 39 个 `freely-*` 前缀 skill 与 32 个旧非前缀版本（如 feature-execution、fix-execution），造成双份/过时定义
- `docs/system/workspace/skills/feature-execution/`、`fix-execution/` 源目录只剩 `SKILL.md.bak`，无 `SKILL.md` 真源

## 建议
1. 修复 30 个源 `SKILL.md` 的 `description: >-` 换行缩进
2. `bin/deploy-skills` 增加 frontmatter YAML 校验，坏文件 fail
3. pre-commit hook 增加 `docs/system/workspace/skills/**` 的 YAML 校验
4. 处理 `feature-execution`/`fix-execution` 的 `.bak`（恢复或正式退役），清理部署目录非前缀旧版
5. 修复后 `freely deploy-skills --tools claude,codex --force` 重新部署并验证

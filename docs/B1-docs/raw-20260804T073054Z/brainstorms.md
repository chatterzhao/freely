---
b1_id: B1-20260804T073054Z
phase_state: completed
source_raw: raw-20260804T073054Z
source_url: https://github.com/chatterzhao/freely/issues/4076
produced_candidate: C-20260804T073054Z-A
created_at: 2026-08-04T08:50:00Z
---

# B1_IBM: 30 个 workspace skill 的 SKILL.md frontmatter YAML 无效

## Input

- 来源：`raw-20260804T073054Z`（GitHub #4076 / Gitee IK6EH2）。
- 现象：codex 启动报 `⚠ Skipped loading 30 skill(s) due to invalid SKILL.md files`，错误统一为 `did not find expected comment or line break at line 2 column 17, while scanning a block scalar`。

## Discovery

- 实测：`docs/system/workspace/skills/` 下 37 个 `SKILL.md`，30 个无法通过 PyYAML 解析（与 codex 报错数量一致）。
- 根因：2026-06-29 批量 commits（`docs: freely-XXX — add use-when triggers to description`）把 frontmatter 写成 `description: >- 内容...`，块标量指示符 `>-` 后必须换行，内容需缩进；同行走内容非法。
- 链路缺口：`bin/deploy-skills` 部署时只校验 `name:` 字段，不做 YAML 解析；pre-commit hook 未校验 `docs/system/workspace/skills/**`，坏文件一路通过并部署到 `~/.codex/skills/`、`~/.claude/skills/`。
- 附带：部署目录混存 39 个 `freely-*` 前缀 skill 与旧非前缀版本；源目录 `feature-execution/`、`fix-execution/` 只剩 `SKILL.md.bak`。

## Brainstorm

### Option A：仅批量修复 30 个 frontmatter

快，但 deploy-skills / pre-commit 仍无校验，同类问题会复发。拒绝。

### Option B：修复文件 + 部署链加 YAML 校验（治本）

修复 30 个 `description: >-` 换行缩进；`bin/deploy-skills` 增加 frontmatter YAML 解析校验（坏文件 fail）；pre-commit hook 增加 `docs/system/workspace/skills/**` 的 YAML 校验；修复后重新部署并验证 codex 可加载。附带项（部署目录旧版清理、`.bak` 处理）作为同一 issue 的清理子项。采用。

## Decision

采用 Option B。修复与防复发同步落地，附带清理部署目录与 `.bak` 源目录。

## Candidate

- candidate_id: `C-20260804T073054Z-A`
- status: promoted
- milestone: `M-20260804T073054Z-A`
- next_action: B2 物化修复设计与测试方案（frontmatter 解析校验 + 部署验证）。

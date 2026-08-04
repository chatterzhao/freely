---
candidate_id: C-20260804T073054Z-A
status: promoted
source_raw: raw-20260804T073054Z
created_at: 2026-08-04
milestone: M-20260804T073054Z-A
---

# Candidates

## C-20260804T073054Z-A: SKILL.md frontmatter YAML 修复 + 部署链校验

- candidate_format_version: v2
- title: 修复 30 个 SKILL.md frontmatter 并给部署链加 YAML 校验
- status: promoted
- decision_reason: 根因是块标量写法错误 + 部署链无校验；只修文件会复发，须同时补 deploy-skills 与 pre-commit 校验。
- next_action: B2 物化 I-20260804T073054Z-A，设计 frontmatter 解析校验测试与部署验证。
- revisit_trigger: 无（已 promote）。
- acceptance_criteria:
  - 30 个坏 `SKILL.md` frontmatter 通过 YAML 解析（`description: >-` 换行缩进）
  - `bin/deploy-skills` 对坏 frontmatter 拒绝部署并给出明确错误
  - pre-commit hook 校验 `docs/system/workspace/skills/**` 的 frontmatter YAML
  - 重新部署后 codex 启动无 `Skipped loading` 告警（30 个 skill 全部加载）
  - 部署目录旧非前缀 skill 与 `.bak` 源清理（feature-execution/fix-execution 恢复或退役）
- promotion_gate: B2 明确测试矩阵（YAML 解析单测、部署拦截测试、全量加载验证）并物化 I-* issue。
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: independent-readonly-review
  - summary: 复核坏文件数量（30/37）、根因 commit 与部署链缺口，方向正确
  - verdict: pass
- promoted_issue_id: I-20260804T073054Z-A
- milestone: M-20260804T073054Z-A
- session_refs: []

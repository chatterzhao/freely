---
candidate_id: C-20261124T054145Z-A
status: promoted
source_raw: raw-20261124T054145Z
created_at: 2026-11-24
milestone: M-20261124T054145Z-A
---

## C-20261124T054145Z-A: CI 合并保护链 fail-closed 收口

- candidate_format_version: v2
- title: CI 合并保护链三处失效——权限、分支保护、自签 check
- status: promoted
- design_verdict: 实现未完成 + 实现偏差（复合）
- anchor_refs:
  - `.github/workflows/pr-merge-guard.yml:1-7`「Branch protection on develop REQUIRES this check to pass / Only pr-merge-guarded sets it to success」
  - `.github/workflows/pr-merge-guard.yml:9-31`「enforce_admins: true — prevents gh pr merge --admin bypass」
  - `CONSTITUTION.md:49`「hook/gate bypass 永久禁止」
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded:296-329`（自签 fallback 源码）
  - CI run 43827151395 与 `branches/develop/protection` API 实测结果
- decision_reason: Option C。三处断点互相掩盖，只修任两处都无法使「禁止绕过门禁」成为可验证事实；统一采用 fail-closed。
- next_action: 进入 B2_IBM 物化 I-* issue，设计覆盖 workflow 权限、pr-merge-guarded 自签移除、分支保护配置验证的 RED/GREEN 测试。
- revisit_trigger: 若 GitHub 平台改为 Ruleset 且现有 check 机制被替代，重新评估本 candidate 的单一语义前提。
- acceptance_criteria:
  - CI guard job 能成功创建 `governance/pr-merge-guard` check（工作显式声明 checks: write）
  - develop 分支保护强制该 check 且 enforce_admins 为真（有 API 读取证据）
  - `pr-merge-guarded` 在 check 缺失 / API 失败时非零退出，不再自行创建 success check
  - 三处均有可复现的 RED → GREEN 证据
- promotion_gate: 三处改动面均已有 RED 测试设计且无既有门禁可绕过；B0 判定与 brainstorms §0 一致。
- open_questions:
  - 是否需要把分支保护一次性设置从 workflow 注释提升为可执行的封装命令（本轮只要求结果可验证，不强制命令化）
  - Option D（GitHub Ruleset / 第三方 CI）作为后续演进，不在本 candidate scope
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: B0 判定、四问、三方案对比、fail-closed 决策与证据链完整；decision 与 anchor 一致，无绕过门禁建议。
  - verdict: pass
- promoted_issue_id: I-20261124T054145Z-A
- promoted_issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/issues/I-20261124T054145Z-A.md
- milestone: M-20261124T054145Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker

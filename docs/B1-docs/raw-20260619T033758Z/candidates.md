# Candidates

## C-20260619T033758Z-A: legacy issue

- candidate_format_version: v2
- title: login claude 交互式 slot 命名与 alias 创建
- status: promoted
- decision_reason: 问题边界清晰，根因明确（tool_login_generic 被错误复用），实现方案参照 login codex 既有模式，代码已完成且 6 场景测试通过
- next_action: 转入 freely-doc-B2_IBM-execution 产出 I-issue，然后 dev-loop 验证→pr-create-guarded→pr-review-guarded→pr-merge-guarded→wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `freely ai login claude` 先提示 auth_mode (account/apikey)，再提示 slot name，空输入终止
  - `freely ai login claude apikey --name foo` 非交互创建 slot + settings.json + alias
  - `freely ai login claude account --name foo` 非交互创建 slot + alias（无 settings override）
  - settings.json 模板为 Anthropic 官方完整骨架（model, env, permissions, hooks, statusLine 等全部字段）
  - `--yes` 无 `--name` 时报错退出
  - opencode/cc/cc-use-codex-cli/kiro-cli 同样适用
- promotion_gate: 6 个测试场景全部通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4-8
  - mode: subagent
  - summary: 审查 ai-cli 修改，确认：1) _prompt_generic_login_mode 与 codex_prompt_login_mode 模式一致，2) _login_account_slot 正确处理 slot name 交互+alias 创建，3) cmd_login 路由逻辑正确（apikey/account 分支无遗漏），4) _login_apikey_alias 空 LOGIN_PROVIDER_NAME 改为交互提示且空输入终止，5) settings.json 骨架包含 Anthropic 最新全部字段
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260619T033758Z-A/issue.md
- milestone: M-20260619T033758Z-A
- session_refs: []

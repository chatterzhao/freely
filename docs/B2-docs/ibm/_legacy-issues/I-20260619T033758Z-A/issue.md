---
local_id: I-20260619T033758Z-A
kind: linked
status: completed
phase_state: completed
completion_evidence: docs/epics/login-claude-interactive-slot/code-reviews/test-log.md
promoted_from: raw-20260619T033758Z
source_candidate: docs/pre-brainstorms/20260619T033758Z--login-claude-interactive-slot/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-19T03:37:58Z
updated_at: 2026-06-19T03:37:58Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/login-claude-interactive-slot/pre-tests.md
verification_artifact_dir: docs/epics/login-claude-interactive-slot/code-reviews
---

# I-20260619T033758Z-A: login claude 交互式 slot 命名与 alias 创建

- source_candidate: `docs/pre-brainstorms/20260619T033758Z--login-claude-interactive-slot/candidates.md`
- pre_tests_path: `docs/epics/login-claude-interactive-slot/pre-tests.md`
- verification_artifact_dir: `docs/epics/login-claude-interactive-slot/code-reviews`

## 实现

修改 `docs/system/workspace/scripts/runtime/ai-cli`：

1. **新增 `_prompt_generic_login_mode`** — 为 claude/opencode/cc/cc-use-codex-cli/kiro-cli 提供 account/apikey 交互选择，参照 `codex_prompt_login_mode` 模式
2. **新增 `_login_account_slot`** — account 模式 slot 创建：提示 slot name（空输入终止）→ 创建 `~/.ai-auth/{tool}-account-{name}/` → 添加 `alias {tool}-account-{name}="{tool}"` 到 `~/.zshrc`
3. **修改 `cmd_login` claude 分支** — 替换 `tool_login_generic`，增加 auth_mode 交互提示 + account/apikey 路由
4. **修改 `_login_apikey_alias`** — `LOGIN_PROVIDER_NAME` 为空时交互提示 slot name，空输入终止；`--yes` 模式无 `--name` 时报错
5. **更新 settings.json 骨架** — 从 3 行简陋模板替换为 Anthropic 官方完整骨架（含 model, env.*, permissions.allow/deny, apiKeyHelper, hooks, statusLine 等全部字段）

## 测试

6 个场景全部通过：
- `login claude apikey --name foo` → 非交互创建 ✅
- `login claude apikey` → 提示 slot name → 创建 ✅
- `login claude apikey` + 空输入 → 终止 exit 2 ✅
- `login claude account --name foo` → 非交互创建 ✅
- `login claude` → 提示 auth_mode → 提示 slot name → 创建 ✅
- `--yes` 无 `--name` → 报错 ✅

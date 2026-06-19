# Test Log: login claude 交互式 slot

- owner_issue: `docs/issues/I-20260619T033758Z-A/issue.md`
- source_candidate: `docs/pre-brainstorms/20260619T033758Z--login-claude-interactive-slot/candidates.md`

Test date: 2026-06-19
Test worktree: test-pre-merge-20260619T033758Z-login-claude-interactive-slot

## Test 1: Non-interactive apikey (--name)

```
$ ./bin/ai login claude apikey --name test-slot
[INFO] Slot created: /Users/zhaoyu/.ai-auth/claude-apikey-test-slot
[INFO] Active slot: claude-apikey-test-slot
[INFO] Alias added: claude-apikey-test-slot
```

Result: ✅ PASS — slot dir + settings.json + alias created

## Test 2: Interactive apikey (prompt for slot name)

```
$ echo "my-custom-slot" | ./bin/ai login claude apikey
[INFO] Slot created: /Users/zhaoyu/.ai-auth/claude-apikey-my-custom-slot
[INFO] Active slot: claude-apikey-my-custom-slot
[INFO] Alias added: claude-apikey-my-custom-slot
```

Result: ✅ PASS — prompted for name, used custom name

## Test 3: Empty input terminates

```
$ echo "" | ./bin/ai login claude apikey
[ERROR] Slot name is required — cannot be empty
EXIT CODE: 2
```

Result: ✅ PASS — exit 2 on empty input

## Test 4: Account mode --name

```
$ ./bin/ai login claude account --name my-account
[INFO] Alias added: claude-account-my-account
[INFO] Account slot created successfully!
[INFO]   Alias:  claude-account-my-account
[INFO]   Run 'claude-account-my-account' to use claude with default auth.
```

Result: ✅ PASS — account slot + alias created

## Test 5: Full interactive account mode

```
$ printf "account\nmy-interactive-slot\n" | ./bin/ai login claude
[INFO] Alias added: claude-account-my-interactive-slot
[INFO] Account slot created successfully!
```

Result: ✅ PASS — two-step prompt (auth_mode + slot name)

## Test 6: Full interactive apikey mode

```
$ printf "apikey\nmy-apikey-interactive\n" | ./bin/ai login claude
[INFO] Slot created: /Users/zhaoyu/.ai-auth/claude-apikey-my-apikey-interactive
[INFO] Alias added: claude-apikey-my-apikey-interactive
[INFO] Config: .../settings.json
```

Result: ✅ PASS — apikey path through full interactive flow

## Test 7: --yes without --name

```
$ ./bin/ai login claude apikey --yes
[ERROR] --name is required in non-interactive (--yes) mode for claude apikey login
EXIT: 2
```

Result: ✅ PASS — clear error, exit 2

## Test 8: settings.json schema validation

```json
{
  "model": "claude-opus-4-8",
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "",
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_MODEL": "claude-opus-4-8",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-4-6"
  },
  "permissionMode": "bypassPermissions",
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": [...],
    "deny": [...]
  },
  "apiKeyHelper": { "enabled": true, "storage": "keychain" },
  "hooks": { "pre": {}, "post": {}, "onFailure": {} },
  "statusLine": { "enabled": true, ... },
  "autoUpdatesChannel": "latest",
  "skipDangerousModePermissionPrompt": true,
  "theme": "dark",
  "editor": "vim"
}
```

Result: ✅ PASS — valid JSON, all Anthropic fields present

## Summary

| # | Scenario | Status |
|---|----------|--------|
| 1 | apikey --name (non-interactive) | ✅ |
| 2 | apikey prompt (interactive) | ✅ |
| 3 | empty input → exit 2 | ✅ |
| 4 | account --name (non-interactive) | ✅ |
| 5 | full interactive account | ✅ |
| 6 | full interactive apikey | ✅ |
| 7 | --yes without --name → error | ✅ |
| 8 | settings.json schema | ✅ |

All 8 tests pass. 6 acceptance items (AI-01 through AI-06) covered.

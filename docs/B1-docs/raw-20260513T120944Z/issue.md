---
local_id: raw-20260513T120944Z44Z
kind: raw
- phase_state: absorbed
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
- phase_state: absorbed
platform_ids:
  github:
    issue_id: '336'
    url: https://github.com/chatterzhao/freely/issues/336
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-13T12:09:58Z'
updated_at: 2026-05-17T04:47:25Z
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260513T120944Z44Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260513T120944Z44Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-13T12:09:44Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260513T120944Z44Z`。实现前请用 `wt-create --raw-key 20260513T120944Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-13T12:09:44Z"
title: "governance: unify gate bypass — remove break-glass, keep FREELY_SKIP_IBM_GATE=1 as single legitimate bypass"

## Problem

Currently there are three parallel gate bypass mechanisms, creating confusion and enabling illegitimate bypasses:

| Mechanism | Legitimate? | Reality |
|-----------|------------|---------|
| `FREELY_SKIP_IBM_GATE=1` | ✅ Designed correctly | Skips IBM doc gate only, keeps all other gates, requires pr-merge-guarded |
| break-glass (`verified_false_negative`/`tooling_unavailable`) | ❌ De facto illegitimate | Used as label to bypass gates without fixing root cause. Gate false positives should be fixed, not bypassed |
| `--no-verify` | ❌ Always illegal | CONSTITUTION/LAWS/AGENTS all forbid it, yet `pre-commit.sh:92` actively suggests it |

## Solution

Unify to a single bypass: `FREELY_SKIP_IBM_GATE=1`. Remove break-glass entirely.

### Remove (break-glass mechanism)

- `docs/system/workspace/hooks/pre-merge-commit.sh`: delete break-glass env var reads (lines 49-53) + break-glass validation block (lines 118-176)
- `docs/system/workspace/hooks/commit-msg.sh`: delete `Freely-Break-Glass-Reason`, `Freely-Blocked-Gate`, `Freely-Operation-Scope`, `Freely-Evidence-Ref`, `Freely-Follow-On-Issue` trailer validation (lines 135-213)
- `docs/system/workspace/hooks/reference-transaction.sh`: remove `pr-merge-guarded-break-glass` pattern
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`: remove `--break-glass` flag, break-glass validation, break-glass receipt trailers
- `docs/system/workspace/scripts/quality/governance-check`: remove break-glass audit functions
- `docs/system/workspace/hooks/protected-branch-breakglass-receipts.md`: delete entire file
- `docs/LAWS.md` §2D: remove break-glass whitelist, receipt fields, follow-on duty
- `docs/CONSTITUTION.md` lines 49-50, 94-95: remove break-glass references
- `AGENTS.md` line 151: remove break-glass references
- Skill files (4): remove break-glass references
- Test scripts (8): remove break-glass test cases

### Fix (--no-verify elimination)

- `docs/system/workspace/hooks/pre-commit.sh:92`: replace `git commit --no-verify` with guidance to use `FREELY_SKIP_IBM_GATE=1` through pr-merge-guarded
- `docs/system/workspace/hooks/README.md`: update --no-verify references
- `docs/system/workspace/AGENTS.md.example`: clarify --no-verify permanently forbidden

### Keep (FREELY_SKIP_IBM_GATE=1)

- `pre-merge-commit.sh` lines 14-46: keep `FREELY_SKIP_IBM_GATE=1` check as-is
- `pre-push.sh` lines 25-26: keep as-is
- `AGENTS.md.example` lines 104, 111: keep, emphasize as only bypass

## Not changing

- AI runtime flags (`--dangerously-bypass-approvals-and-sandbox`, `bypassPermissions`, `--skip-git-repo-check`) — not git governance
- `core.hooksPath` config — not a bypass mechanism
- Historical docs (pre-brainstorms, epics, progress, milestones) — historical records

## Files to change (definitive list)

### Code changes (8 files)
1. `docs/system/workspace/hooks/pre-commit.sh` — line 92 text fix
2. `docs/system/workspace/hooks/pre-merge-commit.sh` — remove break-glass
3. `docs/system/workspace/hooks/commit-msg.sh` — remove break-glass trailer validation
4. `docs/system/workspace/hooks/reference-transaction.sh` — remove break-glass pattern
5. `docs/system/workspace/scripts/worktree/pr-merge-guarded` — remove --break-glass
6. `docs/system/workspace/scripts/quality/governance-check` — remove break-glass audit

### File deletion (1 file)
7. `docs/system/workspace/hooks/protected-branch-breakglass-receipts.md`

### Doc changes (6 files)
8. `docs/LAWS.md` §2D
9. `docs/CONSTITUTION.md` lines 49-50, 94-95
10. `AGENTS.md` line 151
11. `docs/system/workspace/hooks/README.md` — --no-verify references
12. `docs/system/workspace/AGENTS.md.example`

### Skill changes (4 files)
13-16. Four skills referencing break-glass

### Test changes (8 files)
17-24. Test scripts with break-glass test cases

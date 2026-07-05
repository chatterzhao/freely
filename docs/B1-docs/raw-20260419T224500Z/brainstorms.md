# Brainstorms - 20260419-2245--runtime-claude-launch-and-session-evidence

## Context

Protected-root replay on `2026-04-19` showed the tool switch was not failing because `iflow` had merely stopped serving. The narrower seam was that Freely switched to a Claude-family tool path whose non-interactive print-mode contract had drifted.

Manual replay proved the difference:

1. `printf 'say hi\n' | codex exec --skip-git-repo-check -C /Users/zhaoyu/Downloads/code/my-freely/freely --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees --dangerously-bypass-approvals-and-sandbox -` returned `hi`.
2. `claude -p --permission-mode bypassPermissions "say hi"` returned `Hi.`
3. `claude -p --permission-mode bypassPermissions --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees "say hi"` failed with `Input must be provided either through stdin or as a prompt argument when using --print`.

The same replay also showed a second seam: Freely could mint a Claude session id and later treat it as resumable even when no Claude session evidence existed for the project.

## Decision

Materialize one bounded owner that repairs Claude-family non-interactive launch semantics and resume-target truth without hard-coding behavior to `codex` or reopening generic runtime lifecycle work.

## Boundaries

- keep scope on Claude-family print-mode launch contract and verified session-evidence gating only
- do not reopen the broader worker/supervisor self-heal redesign
- do not treat `iflow` retirement as the root cause for this owner
- preserve tool-agnostic recovery semantics so other short-lived non-interactive tools keep working under the same model

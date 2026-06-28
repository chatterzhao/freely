#!/usr/bin/env bash
set -euo pipefail

# ── Hook integrity: core.hooksPath must be .githooks ──
_hooks_path="$(git config --local core.hooksPath 2>/dev/null || echo ".githooks")"
if [[ "$_hooks_path" != ".githooks" ]]; then
  cat >&2 <<MSG
[HOOK] BLOCKED: git hooks disabled (core.hooksPath=$_hooks_path).
  Hooks enforce the canonical workflow. Restore with:
    git config core.hooksPath .githooks
MSG
fi


# ── Fleet audit: detect orphaned managed branches ──
_fleet_audit_orphans() {
  local branch worktree_path issue_count=0
  while IFS= read -r branch; do
    [[ -n "$branch" ]] || continue
    # Check if branch has an active worktree
    worktree_path=$(git worktree list --porcelain 2>/dev/null | awk -v br="refs/heads/$branch" '
      $1=="worktree" {wt=$2}
      $1=="branch" && $2==br {print wt; exit}
    ')
    if [[ -z "$worktree_path" ]]; then
      if [[ $issue_count -eq 0 ]]; then
        echo "[freely] WARNING: Orphaned managed branches detected (no active worktree):" >&2
      fi
      echo "  - $branch (use wt-close or wt-close --force to clean up)" >&2
      ((issue_count++))
    fi
  done < <(git branch --list 'fix/*' 'feature/*' 'hotfix/*' 'test-pre-merge-*' 2>/dev/null | sed 's/^[* ]*//')
  if [[ $issue_count -gt 0 ]]; then
    echo "" >&2
  fi
}
_fleet_audit_orphans

# ── Secret detection gate ──────────────────────────────────────
# Scans staged files for API keys, tokens, and credentials before commit.
# Patterns: Anthropic/OpenAI/DeepSeek keys, generic high-entropy tokens.
_scan_staged_for_secrets() {
  local staged_files found=0
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
  [[ -n "$staged_files" ]] || return 0

  # Patterns that indicate secrets
  local patterns=(
    'sk-[a-zA-Z0-9]{32,}'           # Anthropic/OpenAI/DeepSeek API keys
    'sk-[a-zA-Z0-9_-]{32,}'         # Alternative key format
    'ANTHROPIC_AUTH_TOKEN[[:space:]]*=[[:space:]]*[^[:space:]]{20,}'  # env var
    'DEEPSEEK_API_KEY[[:space:]]*=[[:space:]]*[^[:space:]]{20,}'
    'OPENAI_API_KEY[[:space:]]*=[[:space:]]*[^[:space:]]{20,}'
    'api_key[[:space:]]*=[[:space:]]*["'"'"']?[a-zA-Z0-9_-]{20,}'  # generic
    'secret[[:space:]]*=[[:space:]]*["'"'"']?[a-zA-Z0-9_-]{20,}'
  )

  while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    [[ -f "$file" ]] || continue
    # Skip binary files and generated files
    case "$file" in
      *.png|*.jpg|*.gif|*.ico|*.woff*|*.ttf|*.eot|*.lock|*.sum) continue ;;
    esac
    for pattern in "${patterns[@]}"; do
      if grep -qE "$pattern" "$file" 2>/dev/null; then
        # Check for false positives: file paths in .md docs
        # (e.g. task-source-scan-*) can match sk-* key patterns.
        # If every match is inside quoting or part of a file-path line, skip.
        local false_positive=0
        if [[ "$file" == *.md ]]; then
          local matches matched_text
          matches="$(grep -oE "$pattern" "$file" 2>/dev/null || true)"
          false_positive=1
          while IFS= read -r matched_text; do
            [[ -n "$matched_text" ]] || continue
            # Check backtick quoting
            if grep -qE "\`[^\`]*${matched_text}[^\`]*\`" "$file" 2>/dev/null; then
              continue
            fi
            # Check double-quote quoting
            if grep -qE "\"[^\"]*${matched_text}[^\"]*\"" "$file" 2>/dev/null; then
              continue
            fi
            # Check if match is only on lines that look like file path refs
            # (unquoted YAML values like field: docs/.../file.md)
            local match_lines
            match_lines="$(grep -n "${matched_text}" "$file" 2>/dev/null | cut -d: -f1 || true)"
            local all_path_lines=1
            while IFS= read -r line_no; do
              [[ -n "$line_no" ]] || continue
              local line_content
              line_content="$(sed -n "${line_no}p" "$file" 2>/dev/null || true)"
              if ! echo "$line_content" | grep -qE "(docs/|\.md|\.py|\.sh|\.json)"; then
                all_path_lines=0
                break
              fi
            done <<< "$match_lines"
            if [[ "$all_path_lines" -eq 1 ]]; then
              continue
            fi
            false_positive=0
            break
          done <<< "$matches"
        fi
        if [[ "$false_positive" -eq 1 ]]; then
          continue
        fi
        echo "[SECURITY] Possible secret detected in: $file"
        echo "  Pattern matched: $pattern"
        found=1
      fi
    done
  done <<< "$staged_files"

  if [[ "$found" -eq 1 ]]; then
    cat <<'MSG'

┌─────────────────────────────────────────────────────────────┐
│  COMMIT BLOCKED: Possible secrets detected in staged files  │
│                                                             │
│  API keys, tokens, and credentials must NOT be committed.   │
│  Remove secrets and use environment variables or .gitignore │
│  protected config files instead.                             │
│                                                             │
│  False positives should be fixed by excluding the file or        │
│  refining the pattern. Hooks must not be bypassed.              │
└─────────────────────────────────────────────────────────────┘
MSG
    return 1
  fi

  # Also check for .claude/settings.json specifically
  if echo "$staged_files" | grep -q '.claude/settings.json'; then
    echo "[SECURITY] .claude/settings.json may contain API keys and is gitignored"
    return 1
  fi

  return 0
}

_scan_staged_for_secrets || exit 1

[[ -f "./bin/worktree-common.sh" ]] || exit 0
# shellcheck disable=SC1091
source ./bin/worktree-common.sh

branch="$(freely_wt_current_branch)"
[[ -n "$branch" ]] || exit 0

guarded_state_path="$(git rev-parse --git-dir 2>/dev/null || true)"
if [[ -n "$guarded_state_path" ]]; then
  guarded_state_path="$guarded_state_path/freely-guarded-merge-state"
fi

load_guarded_state() {
  [[ -n "$guarded_state_path" && -f "$guarded_state_path" ]] || return 1
  guarded_state_target=""
  guarded_state_source=""
  guarded_state_bypass=""
  while IFS='=' read -r key value; do
    case "$key" in
      target_branch) guarded_state_target="$value" ;;
      source_branch) guarded_state_source="$value" ;;
      bypass_mode) guarded_state_bypass="$value" ;;
    esac
  done <"$guarded_state_path"
  [[ -n "$guarded_state_target" && -n "$guarded_state_source" && -n "$guarded_state_bypass" ]] || return 1
}

require_valid_guarded_completion_state() {
  load_guarded_state || {
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion state is missing or malformed.
Re-run the merge through ./bin/pr-merge-guarded so hooks can verify a canonical completion handshake.
MSG
  }

  if [[ "$guarded_state_target" != "$branch" ]]; then
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion target '$guarded_state_target' does not match current branch '$branch'.
MSG
  fi

  merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null || true)"
  source_sha="$(git rev-parse "$guarded_state_source" 2>/dev/null || true)"
  if [[ -z "$merge_head" || -z "$source_sha" || "$merge_head" != "$source_sha" ]]; then
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion source '$guarded_state_source' does not match MERGE_HEAD.
MSG
  fi
}

run_guarded_merge_followthrough_hook() {
  local hook_path="./docs/system/workspace/hooks/pre-merge-commit.sh"
  [[ -x "$hook_path" ]] || return 0
  "$hook_path"
}

if freely_wt_is_test_pre_merge_branch "$branch"; then
  # test-pre-merge is a discardable testing sandbox — commits and merges INTO it are allowed.
  # Only block: pr-merge-guarded complete path (develop merge with receipt injection).
  if git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
    if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" == "1" ]]; then
      require_valid_guarded_completion_state
      exit 0
    fi
    # Normal merges from fix/feature for testing: allowed
  fi
  # Direct commits for test evidence: allowed
fi

case "$branch" in
  main|develop)
    # Allow governance-automated commits (wt-close frontmatter, issue-sync,
    # lifecycle closeout, etc.) via FREELY_SKIP_IBM_GATE with valid reason.
    if [[ -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
      # --reason gate: env var bypass must carry valid business reason
      if ! echo "${FREELY_SKIP_IBM_GATE}" | grep -q "^违规绕过门禁中，理由充分，是："; then
        cat >&2 <<'REASON_GATE'
[GATE] 检测到你试图通过 FREELY_SKIP_IBM_GATE 违规绕过门禁

  如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。

  只有确实有合理的业务理由（仅文档/清理/格式化变更等），才允许绕过。
  FREELY_SKIP_IBM_GATE 的值必须匹配格式:
    FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"

  示例: FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：仅文档类变更不含实现代码" git commit
REASON_GATE
        exit 1
      fi
      echo "[HOOK] FREELY_SKIP_IBM_GATE — validating governance-only paths"
      if [[ -x "./bin/governance-merge-gate" ]]; then
        set +e
        gate_output="$(./bin/governance-merge-gate --staged --target-branch "$branch" --skip-ibm-gate 2>&1)"
        gate_rc=$?
        set -e
        if [[ "$gate_rc" -ne 0 ]]; then
          cat >&2 <<'GUIDE'
[HOOK] FREELY_SKIP_IBM_GATE=1 blocked: non-governance changes detected.

  FREELY_SKIP_IBM_GATE=1 only allows docs/cleanup/format changes.
  For implementation changes, complete IBM lifecycle FIRST:

    skill:freely-doc-B1_IBM-execution  → raw → brainstorm → candidate → milestones.md
    skill:freely-doc-B2_IBM-execution  → I-* issue → PRD → tasks → code-review → milestones.md

  Then commit via proper worktree flow (not directly on develop).
GUIDE
          echo "$gate_output" >&2
          exit "$gate_rc"
        fi
        echo "$gate_output"
      fi
      echo "[HOOK] IBM governance gate skipped (governance-only changes confirmed)"
      exit 0
    fi
    if git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
      if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" == "1" ]]; then
        require_valid_guarded_completion_state
        if [[ "$branch" == "develop" ]]; then
          run_guarded_merge_followthrough_hook
        fi
        exit 0
      fi
      cat <<MSG
[HOOK] Commit blocked: raw merge completion on '$branch' is forbidden.
Use the guarded completion path instead:

  ./bin/pr-merge-guarded complete "$branch" <source-branch>

Do not finish protected-branch merges with bare 'git commit' or equivalent bypass.
MSG
    fi
    cat <<MSG
[HOOK] Commit blocked: direct development on '$branch' is forbidden.

Read AGENTS.md §核心开发流程, then invoke the correct skill:

  Bug fix  → skill:freely-fix-execution   (Fix first, govern later)
  Feature  → skill:freely-feat-execution  (Govern first, then code)

Quick start:
  cd <project-root>
  ./bin/wt-create --raw-key <key> --source <platform|chat-inbox> --skill <skill> --slug <slug>
  cd ../<project>-worktrees/<branch-dir>

Do NOT work around this hook. Bypass attempts (skip-worktree, --no-verify,
removing remotes, etc.) violate CONSTITUTION.md §5.
The skills enforce the full IBM lifecycle:
  feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create → pr-merge → wt-close
MSG
    ;;
esac

if ! freely_wt_is_primary_worktree; then
  if [[ -x "./bin/checkpoint-guard" ]]; then
    set +e
    checkpoint_output="$(./bin/checkpoint-guard --staged-only  2>&1)"
    checkpoint_rc=$?
    set -e
    if [[ "$checkpoint_rc" -eq 2 ]]; then
      cat <<MSG
[HOOK] ⚠ scope note: staged change set spans multiple scopes.

$checkpoint_output

MSG
    elif [[ "$checkpoint_rc" -ne 0 ]]; then
      echo "$checkpoint_output" >&2
      exit "$checkpoint_rc"
    fi
  fi
  if [[ -x "./bin/pretests-gate" ]]; then
    set +e
    pretests_output="$(./bin/pretests-gate --staged-only 2>&1)"
    pretests_rc=$?
    set -e
    if [[ "$pretests_rc" -ne 0 ]]; then
      cat <<MSG
[HOOK] Commit blocked: staged issue completion does not satisfy bound pre-tests evidence.

$pretests_output

Keep the issue in a non-completed phase until its bound pre-tests acceptance items are backed by real test execution, lawful non-test waivers, and traceable evidence. Do not clear this gate by only filling metadata.
MSG
      exit "$pretests_rc"
    fi
  fi
  exit 0
fi

if ! freely_wt_validate_branch_base "$branch"; then
  cat <<MSG
[HOOK] Commit blocked: branch '$branch' base check failed.
Expected:
  feature/* from develop
  feature/premerge-* from the active test-pre-merge-* batch (or develop when no test batch is active)
  release/* from develop
  hotfix/* from main
MSG
fi

existing_for_branch="$(freely_wt_existing_dedicated_for_branch "$branch")"
if [[ -n "$existing_for_branch" ]]; then
  rel_target="$(freely_wt_relative_target_for_branch "$branch")"
  cat <<MSG
[HOOK] Commit blocked in primary worktree.
Branch '$branch' has dedicated sibling worktree:
  $existing_for_branch

Start work in worktree:
  cd "$existing_for_branch"

Standard cleanup after merge:
  ./bin/wt-close "$branch"
MSG
  git worktree list
  exit 1
fi

rel_target="$(freely_wt_relative_target_for_branch "$branch")"
cat <<MSG
[HOOK] Commit blocked in primary worktree.
No dedicated sibling worktree found for '$branch'.

Create it from the project root with the standard command:
  cd <your-project-name-path>
  ./bin/wt-create "$branch"
  cd ${rel_target}

If you must create it manually instead:
  git worktree add ${rel_target} "$branch"
  ./bin/freely sync-tooling --source-project <your-project-name-path> --project ${rel_target}

When the work is finished and merged:
  ./bin/wt-close "$branch"
MSG

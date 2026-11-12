#!/usr/bin/env bash
# Function-level unit test (Step 2.5): the Phase 6b cleanup block of wt-close
# must be a no-op when DRY_RUN=true, and must still clean when DRY_RUN=false.
# It executes the real source block against a stub git, so a future refactor
# that drops the guard fails here even if the indentation still "looks" right.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
WT_CLOSE="$ROOT/docs/system/workspace/scripts/worktree/wt-close"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-preview.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

_extract_block() {
  awk '/Phase 6b/{flag=1} /Phase 7/{flag=0} flag' "$WT_CLOSE"
}

_block="$(_extract_block)"
[[ -n "$_block" ]] && ut_ok "Phase 6b block extracted" || ut_bad "Phase 6b block missing"
printf '%s\n' "$_block" | grep -q 'DRY_RUN' && ut_ok "Phase 6b consults DRY_RUN" || ut_bad "Phase 6b ignores DRY_RUN"

_run_block() {
  local dry="$1" sandbox="$2"
  mkdir -p "$sandbox/bin" "$sandbox/wts/test-pre-merge-20261112T131150Z-probe" "$sandbox/root"
  cat > "$sandbox/bin/git" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$GIT_LOG"
case "$1" in show-ref) exit 0 ;; esac
exit 0
STUB
  chmod +x "$sandbox/bin/git"
  {
    printf 'set -uo pipefail\n'
    printf '_dry() { printf "[DRY-RUN] %%s\n" "$*"; }\n'
    printf 'DRY_RUN=%s\n' "$dry"
    printf 'FORCE=false\nDISCARD_UNMERGED=false\n'
    printf "branch='fix/raw-20261112T131150Z-probe'\n"
    printf "PROJECT_WORKTREES_ROOT='%s/wts'\n" "$sandbox"
    printf "PROJECT_ROOT='%s/root'\n" "$sandbox"
    printf '%s\n' "$_block"
    printf 'exit 0\n'
  } > "$sandbox/block.sh"
  GIT_LOG="$sandbox/git.log" PATH="$sandbox/bin:/usr/bin:/bin" HOME="$sandbox" \
    bash "$sandbox/block.sh" >/dev/null 2>&1 || true
}

_run_block true "$tmp/dry"
if grep -qE 'worktree remove|branch -D' "$tmp/dry/git.log" 2>/dev/null; then
  ut_bad "DRY_RUN=true still sent a destructive verb to git"
else
  ut_ok "DRY_RUN=true leaves worktree and branch alone"
fi

_run_block false "$tmp/real"
if grep -qE 'worktree remove|branch -D' "$tmp/real/git.log" 2>/dev/null; then
  ut_ok "DRY_RUN=false still performs the cleanup (negative control)"
else
  ut_bad "DRY_RUN=false no longer cleans up — the harness is blind"
fi

WT_CREATE="$ROOT/docs/system/workspace/scripts/worktree/wt-create"
if grep -E 'sed -i.*phase_state' "$WT_CREATE" | grep -qv '_reopen_file'; then
  ut_bad "wt-create still rewrites phase_state on a non-worktree path"
else
  ut_ok "wt-create phase rewrite is confined to the dev worktree copy"
fi

ut_report

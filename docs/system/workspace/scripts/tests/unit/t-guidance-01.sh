#!/usr/bin/env bash
# Guidance text invariants (raw-20261112T031638Z / #4310).
#
# Function-level checks for the runtime change: every wt-create hint the runtime
# prints must carry the REQUIRED --kind, and no guidance may quote a skill name
# that does not exist. These are the invariants the 27k-line runtime must keep
# when it refuses a launch or prints usage — the exact moments an agent reads to
# decide what to do next.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime/freely"
ISSUE_SYNC="$ROOT/bin/issue-sync"
RAW_PULL="$ROOT/bin/raw-issue-pull"
SKILLS="$ROOT/docs/system/workspace/skills"
REAL_SKILL="freely-workflow-guarded-execution"

# ── the real skill must exist; the ghosts must not ──────────────────────────
[[ -f "$SKILLS/$REAL_SKILL/SKILL.md" ]] \
  && ut_ok "referenced workflow skill exists on disk" \
  || ut_bad "referenced workflow skill missing: $REAL_SKILL"

for ghost in freely-fix-execution freely-feature-execution freely-feat-execution; do
  [[ ! -d "$SKILLS/$ghost" ]] \
    && ut_ok "ghost skill is indeed absent: $ghost" \
    || ut_bad "ghost skill unexpectedly exists: $ghost"
done

# ── every runtime wt-create hint carries --kind ─────────────────────────────
missing="$(python3 - "$RUNTIME" <<'PY'
import sys
from pathlib import Path
bad = []
for i, ln in enumerate(Path(sys.argv[1]).read_text(errors="replace").splitlines(), 1):
    if "wt-create" in ln and "--raw-key" in ln and "--kind" not in ln:
        bad.append(str(i))
print(",".join(bad))
PY
)"
assert_eq "" "$missing" "every runtime wt-create hint includes required --kind"

# ── runtime guidance quotes no ghost name ───────────────────────────────────
if grep -qE "freely-fix-execution|freely-feature-execution|freely-feat-execution" "$RUNTIME"; then
  ut_bad "runtime still quotes a ghost skill name"
else
  ut_ok "runtime quotes no ghost skill name"
fi

# ── issue-sync guard: real skill + --kind, no ghosts ────────────────────────
if grep -qE "freely-fix-execution|freely-feature-execution|freely-feat-execution" "$ISSUE_SYNC"; then
  ut_bad "issue-sync guard still quotes a ghost skill name"
else
  ut_ok "issue-sync guard quotes no ghost skill name"
fi
grep -q "skill:$REAL_SKILL" "$ISSUE_SYNC" \
  && ut_ok "issue-sync guard references the real workflow skill" \
  || ut_bad "issue-sync guard does not reference the real workflow skill"

guard_hint="$(grep -E "wt-create --raw-key" "$ISSUE_SYNC" || true)"
case "$guard_hint" in
  *--kind*) ut_ok "issue-sync guard hint includes required --kind" ;;
  *)        ut_bad "issue-sync guard hint missing --kind: $guard_hint" ;;
esac

# ── raw-issue-pull must pass --project so the guard sees the caller's worktree ─
call="$(grep -E 'issue-sync" .*create "\$local_id"' "$RAW_PULL" || true)"
case "$call" in
  *--project*) ut_ok "raw-issue-pull passes --project to issue-sync create" ;;
  *)           ut_bad "raw-issue-pull does not pass --project: $call" ;;
esac
grep -q 'caller_root="$(git rev-parse --show-toplevel' "$RAW_PULL" \
  && ut_ok "caller_root derived from the caller's worktree, not the script path" \
  || ut_bad "caller_root derivation missing"

# ── the guard itself must NOT be weakened ───────────────────────────────────
grep -qE 'main\|develop\|test-pre-merge-\*\)' "$ISSUE_SYNC" \
  && ut_ok "protected-branch guard still covers main/develop/test-pre-merge" \
  || ut_bad "protected-branch guard pattern was weakened"

ut_report
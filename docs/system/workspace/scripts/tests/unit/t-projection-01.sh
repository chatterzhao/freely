#!/usr/bin/env bash
# Projection consistency, function level (#4179): the verifier must distinguish
# a delegation from a byte copy, refuse drift on either side, and never treat a
# missing lock as a pass.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
VERIFIER="$ROOT/docs/system/workspace/scripts/quality/projection_verify.py"
LOCK="$ROOT/projection.lock"

[[ -f "$VERIFIER" ]] && ut_ok "verifier exists" || ut_bad "verifier missing"
[[ -f "$LOCK" ]] && ut_ok "projection.lock exists" || ut_bad "projection.lock missing"

# ── .githooks is wrappers only ──
stale="$(find "$ROOT/.githooks" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.bak*' -o -name '*.debug' \) | wc -l | tr -d ' ')"
assert_eq "0" "$stale" ".githooks carries no dead copies or backups"

wrappers=0
for hook in commit-msg post-checkout post-rewrite pre-commit pre-merge-commit \
            pre-push pre-rebase reference-transaction; do
  if [[ -f "$ROOT/.githooks/$hook" ]] && grep -q "exec bash" "$ROOT/.githooks/$hook"; then
    wrappers=$((wrappers + 1))
  else
    ut_bad "wrapper missing or not delegating: $hook"
  fi
  [[ -f "$ROOT/docs/system/workspace/hooks/$hook.sh" ]] \
    || ut_bad "truth script missing for $hook"
done
assert_eq "8" "$wrappers" "all eight wrappers exec their truth script"

# ── lock shape ──
kinds="$(python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
print(','.join(sorted(d.get('kinds',[]))))" "$LOCK")"
assert_eq "agents,bin,hooks,skills" "$kinds" "lock declares all four projection kinds"

modes="$(python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
print(','.join(sorted({e.get('mode','copy') for e in d['entries']})))" "$LOCK")"
assert_eq "copy,delegate" "$modes" "lock records both copy and delegate modes"

# Every recorded hash must equal the current truth hash.
bad="$(python3 -c "
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[2]); d=json.load(open(sys.argv[1]))
bad=[]
for e in d['entries']:
    if e.get('mode')!='delegate': continue
    p=root/e['source']
    if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:
        bad.append(e['source'])
print(len(bad))" "$LOCK" "$ROOT")"
assert_eq "0" "$bad" "every delegate entry pins the current truth hash"

# ── verify: consistent tree passes ──
python3 "$VERIFIER" verify --project "$ROOT" >/dev/null 2>&1
assert_eq "0" "$?" "verify passes on the consistent tree"

# ── verify: missing lock is a refusal, not a pass ──
empty="$(ut_sandbox)"
python3 "$VERIFIER" verify --project "$empty" >/dev/null 2>&1
assert_eq "2" "$?" "verify refuses a missing lock with 2"

# ── verify: breaking a delegation is drift ──
sandbox="$(ut_sandbox)"
python3 - "$LOCK" "$ROOT" "$sandbox" <<'PY'
import json, shutil, sys
from pathlib import Path
lock, root, dst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
doc = json.loads(lock.read_text(encoding='utf-8'))
for item in doc['entries']:
    for rel in (item['source'], item['target']):
        if rel.startswith('/'):
            continue
        src, target = root / rel, dst / rel
        if not src.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            if not target.exists():
                shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)
shutil.copy2(lock, dst / 'projection.lock')
hook = next(e for e in doc['entries'] if e['kind'] == 'hooks')
(dst / hook['target']).write_text('#!/usr/bin/env bash\nexit 0\n', encoding='utf-8')
PY
python3 "$VERIFIER" verify --project "$sandbox" >/dev/null 2>&1
assert_eq "1" "$?" "verify refuses a broken delegation with 1"

# ── the runtime exposes the command through bin/projections ──
# BSD grep has no \s; use the POSIX class (same trap as #4162).
grep -qE '^[[:space:]]+projections\) exec bash "\$SELF_ROOT/bin/projections"' \
  "$ROOT/docs/system/workspace/scripts/runtime/freely" \
  && ut_ok "runtime dispatches projections to bin/projections" \
  || ut_bad "runtime does not dispatch projections"
grep -q "projection_verify.py" "$ROOT/bin/projections" \
  && ut_ok "bin/projections points at the verifier" \
  || ut_bad "bin/projections does not point at the verifier"

# ── deploy-skills writes the hash back ──
grep -q "projection_verify.py" "$ROOT/bin/deploy-skills" \
  && ut_ok "deploy-skills records projection hashes" \
  || ut_bad "deploy-skills does not record projection hashes"

ut_report

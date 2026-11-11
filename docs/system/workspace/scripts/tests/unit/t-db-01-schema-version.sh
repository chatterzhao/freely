#!/usr/bin/env bash
# Schema contract (#4281): the DB records its schema version in
# PRAGMA user_version, and a database written by a newer build is refused
# instead of being silently downgraded.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

db_manager="$UT_PROJECT_ROOT/docs/system/workspace/scripts/runtime/freely_db_manager.py"
if [[ ! -f "$db_manager" ]]; then
  printf '  [FATAL] db manager not found: %s\n' "$db_manager" >&2
  exit 2
fi

sb="$(ut_sandbox)"
out="$(python3 - "$db_manager" "$sb" <<'PY'
import importlib.util
import pathlib
import sqlite3
import sys
import traceback

path, project = sys.argv[1], sys.argv[2]
# The DB manager imports its sibling helpers by bare module name.
sys.path.insert(0, str(pathlib.Path(path).parent))
spec = importlib.util.spec_from_file_location("freely_db_manager_probe", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("SCHEMA=%s" % getattr(mod, "SCHEMA_VERSION", "missing"))

daemon = mod.DbDaemon(project)
daemon._open_db()
daemon._ensure_tables()
version = daemon.conn.execute("PRAGMA user_version").fetchone()[0]
print("VERSION=%s" % version)
db_path = daemon.db_path
daemon.conn.close()

# A newer database must be refused, not re-interpreted by this build.
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA user_version = %d" % (int(version) + 1))
conn.commit()
conn.close()

newer = mod.DbDaemon(project)
newer._open_db()
try:
    newer._ensure_tables()
except RuntimeError as exc:
    print("REFUSED=1")
    print("REASON=%s" % str(exc)[:80])
except Exception:
    print("REFUSED=0")
    traceback.print_exc()
else:
    print("REFUSED=0")
PY
)" || { printf '  [FATAL] probe crashed:\n%s\n' "$out" >&2; exit 2; }

assert_contains "$out" "SCHEMA=1" "schema version constant is 1"
assert_contains "$out" "VERSION=1" "a fresh database records user_version=1"
assert_contains "$out" "REFUSED=1" "a newer database is refused"
assert_contains "$out" "newer than this build" "refusal names the version mismatch"
ut_report

#!/usr/bin/env bash
# Function-level contract for gitee-issue.py repo_path_branch (#4137).
# Gitee v5 deletes branches at /repos/{owner}/{repo}/branches/{branch};
# a GitHub git-ref path yields HTTP 404 for every branch.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

ROOT="$(git rev-parse --show-toplevel)"
MODULE="$ROOT/docs/system/workspace/scripts/runtime/gitee-issue.py"
[[ -f "$MODULE" ]] && ut_ok "gitee-issue module exists" || ut_bad "gitee-issue module missing"

path="$(python3 - "$ROOT" <<'PY'
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1])
mod_dir = root / "docs/system/workspace/scripts/runtime"
sys.path.insert(0, str(mod_dir))
spec = importlib.util.spec_from_file_location("gitee_issue_unit", mod_dir / "gitee-issue.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print(mod.repo_path_branch("zhaoquan/freely", "fix/raw-20261103T083757Z-demo"))
PY
)"
assert_eq "/repos/zhaoquan/freely/branches/fix/raw-20261103T083757Z-demo" "$path" "canonical Gitee branch endpoint"

source_has_ref="$(grep -c '/git/refs/heads/' "$MODULE" || true)"
assert_eq "0" "$source_has_ref" "no GitHub git-ref path remains"

ut_report

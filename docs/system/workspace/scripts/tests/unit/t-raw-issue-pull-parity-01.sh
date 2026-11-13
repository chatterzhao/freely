#!/usr/bin/env bash
# Function-level unit test (Step 2.5): pull_raw_issue mirrors platform comments
# and never demotes a local terminal phase. Uses the real adapter with only
# transport functions stubbed - no network, no hand-edited fixture data.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"

grep -qF 'details.get("comments")' "$ROOT/docs/system/workspace/scripts/sync/platform-adapter.py" \
  && ut_ok "pull reads the platform comments field" \
  || ut_bad "pull ignores platform comments"

grep -qF 'existing_terminal' "$ROOT/docs/system/workspace/scripts/sync/platform-adapter.py" \
  && ut_ok "pull detects an existing terminal raw" \
  || ut_bad "pull has no terminal-state guard"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-pull-parity.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

python3 - "$ROOT" "$tmp" <<'PY' > "$tmp/out" 2> "$tmp/err"
import importlib.util, sys, tempfile
from pathlib import Path
from unittest import mock

root = Path(sys.argv[1]); tmp = Path(sys.argv[2])
sys.path.insert(0, str(root / "docs/system/workspace/scripts/lifecycle"))
sys.path.insert(0, str(root / "docs/system/workspace/scripts/sync"))
spec = importlib.util.spec_from_file_location(
    "adapter_unit", root / "docs/system/workspace/scripts/sync/platform-adapter.py")
mod = importlib.util.module_from_spec(spec); sys.modules["adapter_unit"] = mod
spec.loader.exec_module(mod)

from raw_metadata_contract import RAW_METADATA_FIELDS
import yaml
defaults = {
    "schema_version": "1", "local_id": "raw-20261113T084851Z", "kind": "raw",
    "phase_state": "proposed", "absorbed_into": "", "platform_ids": {},
    "primary_platform": "github", "canonical_issue_path": "",
    "last_synced_comment_at": {}, "hash": "", "created_at": "2026-11-13T08:48:51Z",
    "updated_at": "2026-11-13T08:48:51Z", "intake_id": "", "author": "platform",
    "channel": "github", "session_refs": [], "platform_state": "open",
    "promoted_children": [], "source_candidate": "", "completed_at": "",
    "closeout_note": "",
}
fm = yaml.safe_dump({k: defaults.get(k, "") for k in RAW_METADATA_FIELDS},
                    default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
key = "20261113T084851Z"
comment = "拆解为以下任务:\n1. [I-20261113T084851Z-A](will-be-updated)"
title = "[RAW-" + key + "] " + mod.local_heading_title(key, "unit parity")
replica = {
    "status": "ok", "raw_key": "raw-" + key, "issue_id": "9001", "url": "https://example.invalid/issues/9001",
    "title": title, "body": "---\n" + fm + "\n---\n\nunit body\n",
    "created_at": "2026-11-13T08:48:51Z", "updated_at": "2026-11-13T08:48:51Z",
    "labels": ["kind/raw", "phase/proposed"], "comments": [comment], "state": "OPEN",
}
target = tmp / ("docs/B1-docs/raw-" + key)
with mock.patch.object(mod, "discover_raw_replicas", return_value={"github": replica}), \
     mock.patch.object(mod, "check_and_claim_assignee", return_value=(True, "ok")), \
     mock.patch.object(mod, "severity_from_replicas", return_value=(None, [])):
    mod.pull_raw_issue(key, target)
doc = (target / "issue.md").read_text(encoding="utf-8")
assert "### comment-platform-1" in doc, "comment block missing"
assert "拆解为以下任务" in doc, "comment text missing"
print("COMMENT_OK")
PY
rc=$?
if [[ $rc -eq 0 && "$(cat "$tmp/out")" == "COMMENT_OK" ]]; then
  ut_ok "pull mirrors platform comments into the local document"
else
  ut_bad "pull did not mirror comments (rc=$rc err=$(tail -3 "$tmp/err"))"
fi

# Terminal phase must survive a second materialization.
python3 - "$ROOT" "$tmp" <<'PY' > "$tmp/out2" 2> "$tmp/err2"
import importlib.util, sys
from pathlib import Path
from unittest import mock
root = Path(sys.argv[1]); tmp = Path(sys.argv[2])
sys.path.insert(0, str(root / "docs/system/workspace/scripts/lifecycle"))
spec = importlib.util.spec_from_file_location(
    "adapter_unit2", root / "docs/system/workspace/scripts/sync/platform-adapter.py")
mod = importlib.util.module_from_spec(spec); sys.modules["adapter_unit2"] = mod
spec.loader.exec_module(mod)
from raw_metadata_contract import RAW_METADATA_FIELDS
import yaml
key = "20261113T084851Z"
d = {
    "schema_version": "1", "local_id": "raw-" + key, "kind": "raw",
    "phase_state": "absorbed", "absorbed_into": "I-" + key + "-A", "platform_ids": {},
    "primary_platform": "github", "canonical_issue_path": "x",
    "last_synced_comment_at": {}, "hash": "", "created_at": "2026-11-13T08:48:51Z",
    "updated_at": "2026-11-13T08:48:51Z", "intake_id": "", "author": "platform",
    "channel": "github", "session_refs": [], "platform_state": "closed",
    "promoted_children": ["I-" + key + "-A"], "source_candidate": "",
    "completed_at": "2026-11-13T08:50:00Z", "closeout_note": "",
}
fm = yaml.safe_dump({k: d.get(k, "") for k in RAW_METADATA_FIELDS},
                    default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
title = "[RAW-" + key + "] " + mod.local_heading_title(key, "unit parity")
replica = {
    "status": "ok", "raw_key": "raw-" + key, "issue_id": "9001", "url": "https://example.invalid/issues/9001",
    "title": title, "body": "---\n" + fm + "\n---\n\nunit body\n",
    "created_at": "2026-11-13T08:48:51Z", "updated_at": "2026-11-13T08:48:51Z",
    "labels": ["kind/raw", "phase/proposed"], "comments": [], "state": "CLOSED",
}
target = tmp / ("term/docs/B1-docs/raw-" + key)
target.mkdir(parents=True, exist_ok=True)
(target / "issue.md").write_text("---\n" + fm + "\n---\n\n# unit parity\n\nunit body\n", encoding="utf-8")
with mock.patch.object(mod, "discover_raw_replicas", return_value={"github": replica}), \
     mock.patch.object(mod, "check_and_claim_assignee", return_value=(True, "ok")), \
     mock.patch.object(mod, "severity_from_replicas", return_value=(None, [])):
    mod.pull_raw_issue(key, target)
front = (target / "issue.md").read_text(encoding="utf-8").split("---", 2)[1]
assert "phase_state: absorbed" in front, "absorbed was demoted"
assert "platform_state: closed" in front, "platform_state lost"
print("TERMINAL_OK")
PY
rc=$?
if [[ $rc -eq 0 && "$(cat "$tmp/out2")" == "TERMINAL_OK" ]]; then
  ut_ok "re-materialization preserves absorbed / platform_state closed"
else
  ut_bad "terminal state was demoted (rc=$rc err=$(tail -3 "$tmp/err2"))"
fi

ut_report

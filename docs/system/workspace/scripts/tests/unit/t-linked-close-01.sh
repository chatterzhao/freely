#!/usr/bin/env bash
# Function-level unit test (Step 2.5): linked retirement is batch-only and
# guarded by phase_state == completed, with zero platform writes on refusal.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
CLOSE_SH="$ROOT/bin/issue-sync.d/cmd-close.sh"
BATCH_SH="$ROOT/bin/issue-sync.d/cmd-batch.sh"
EFFECTS="$ROOT/docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py"

grep -qF "linked issues are retired by 'issue-sync batch'" "$CLOSE_SH" \
  && ut_ok "direct cmd_close refuses linked documents" \
  || ut_bad "cmd-close still allows a direct linked close"

grep -qF 'cmd_close_linked() {' "$CLOSE_SH" \
  && ut_ok "batch-only linked close action exists" \
  || ut_bad "cmd_close_linked missing"

grep -qF 'cmd_close_linked "$local_id"' "$BATCH_SH" \
  && ut_ok "batch linked branch drives the retirement" \
  || ut_bad "batch does not call cmd_close_linked"

grep -qF 'phase != "completed"' "$EFFECTS" \
  && ut_ok "close_linked enforces completed phase" \
  || ut_bad "close_linked has no phase guard"

grep -qF 'metadata["platform_state"] = "closed"' "$EFFECTS" \
  && ut_ok "retirement writes platform_state" \
  || ut_bad "retirement does not write platform_state"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-linked-close.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/docs/system/workspace/scripts/sync" "$tmp/art" "$tmp/verification"
printf '# pre-tests\n' > "$tmp/verification/pre-tests.md"
printf 'import sys, json, os\nwith open(os.environ["ADAPTER_LOG"], "a") as f: f.write(sys.argv[1] + "\\n")\nprint(json.dumps({"github": {"status": "closed"}, "gitee": {"status": "closed"}}))\nsys.exit(0)\n' \
  > "$tmp/docs/system/workspace/scripts/sync/platform-adapter.py"
: > "$tmp/adapter.log"

make_doc() {
  local phase="$1"
  cat > "$tmp/linked.md" <<DOC
---
schema_version: '1'
issue_id: I-20261113T084729Z-A
kind: linked
status: completed
phase_state: $phase
promoted_from: raw-20261113T084729Z
source_candidate: docs/B1-docs/raw-20261113T084729Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '9001'
  gitee:
    issue_id: 'IKTEST1'
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-11-13T08:47:29Z
updated_at: 2026-11-13T08:47:29Z
intake_id: ''
author: platform
channel: freely-workflow-guarded-execution
session_refs: []
pre_tests_path: verification/pre-tests.md
verification_artifact_dir: art
---

# fixture
DOC
}

make_doc in_dev
ADAPTER_LOG="$tmp/adapter.log" PYTHONPATH="$ROOT/docs/system/workspace/scripts/lifecycle" \
  python3 "$EFFECTS" close-linked "$tmp/linked.md" "$tmp" >/dev/null 2>&1 \
  && ut_bad "close-linked accepted an in_dev linked issue" \
  || ut_ok "close-linked refuses an in_dev linked issue"
[[ ! -s "$tmp/adapter.log" ]] \
  && ut_ok "refusal performed zero platform writes" \
  || ut_bad "refusal still called the platform adapter"

make_doc completed
ADAPTER_LOG="$tmp/adapter.log" PYTHONPATH="$ROOT/docs/system/workspace/scripts/lifecycle" \
  python3 "$EFFECTS" close-linked "$tmp/linked.md" "$tmp" >/dev/null 2>&1 \
  && ut_ok "completed linked issue is retired" \
  || ut_bad "completed linked issue was refused"
grep -qF 'platform_state: closed' "$tmp/linked.md" \
  && ut_ok "platform_state: closed is written back" \
  || ut_bad "platform_state not written back"
grep -qF 'status: closed' "$tmp/linked.md" \
  && ut_bad "second status semantic reappeared" \
  || ut_ok "no second status semantic"

ut_report

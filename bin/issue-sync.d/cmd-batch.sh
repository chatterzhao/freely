#!/usr/bin/env bash
# cmd-batch.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync batch` — sync every changed issue.

cmd_batch() {
  local filter_key="${1:-}"
  local last_scan total=0 synced=0 batch_size=10 batch_count=0
  last_scan=$(_scan_state_get "last_sync_at")
  echo "[issue-sync] batch: last sync = ${last_scan:-never} scope=${filter_key:-ALL}"

	  # Collect all issue files into an array first (use temp file to preserve null bytes)
	  # Filter: skip issues where local platform_state is already closed
	  # (fully synced — no action needed). This reduces scan volume from ~200
	  # to ~10-20 inconsistent issues.
	  local _tmp _skipped=0
	  _tmp=$(mktemp /tmp/issue-sync-batch.XXXXXX)
	  { find "$ISSUES_DIR" -name "issue.md" -print0 2>/dev/null; find "$ROOT_DIR/docs/B2-docs" -name "I-*.md" -print0 2>/dev/null; } > "$_tmp"
	  while IFS= read -r -d '' issue_file; do
	    [[ -n "$issue_file" ]] || continue
	    local dir local_id
	    dir=$(dirname "$issue_file")
	    # raw docs are <key>/issue.md (id = parent dir); linked docs are
	    # <...>/issues/<I-id>.md (id = file name). Using basename(dirname) for
	    # both yielded "issues", so EVERY linked document was filtered out by
	    # the raw-*/I-* guard below and never processed (raw-20261113T130925Z).
	    case "$issue_file" in
	      */issues/I-*.md) local_id=$(basename "$issue_file" .md) ;;
	      *) local_id=$(basename "$dir") ;;
	    esac
	    [[ "$local_id" == raw-* || "$local_id" == I-* ]] || continue
	    # Scope filter: a raw-owning worktree may only sync its own issue and
	    # children (GATE 1). Cross-raw sync belongs to the governance-only lane
	    # (raw-20261103T091157Z established that mechanism).
	    #
	    # Compare the path BELOW /docs/, never the absolute path: the worktree
	    # directory itself is named fix-raw-<key>-<slug>, so an absolute-path match
	    # made every document in the tree look like "this lane" and the filter was
	    # a no-op (raw-20261114T031043Z).
	    if [[ -n "$filter_key" ]]; then
	      case "${issue_file#*/docs/}" in
	        *"$filter_key"*) ;;
	        *) continue ;;
	      esac
	    fi
	    # Skip fully-synced: platform_state=closed means both sides agree
	    local _pstate; _pstate=$(_fm_get "$issue_file" "platform_state")
	    if [[ "$_pstate" == "closed" ]]; then
	      _skipped=$((_skipped + 1))
	      continue
	    fi
	    issue_files+=("$issue_file")
	    total=$((total + 1))
	  done < "$_tmp"
	  rm -f "$_tmp"

	  if [[ "$total" -eq 0 ]]; then
	    echo "[issue-sync] batch: no issues to sync (skipped $_skipped already closed)"
	    return 0
	  fi

	  echo "[issue-sync] batch: $total issue(s) to process ($_skipped skipped as closed), batch_size=$batch_size"

  for issue_file in "${issue_files[@]}"; do
    local dir local_id
    dir=$(dirname "$issue_file")
    case "$issue_file" in
      */issues/I-*.md) local_id=$(basename "$issue_file" .md) ;;
      *) local_id=$(basename "$dir") ;;
    esac

    local kind
    kind=$(_fm_get "$issue_file" "kind")

    case "$kind" in
      raw)
        local phase_state; phase_state=$(_fm_get "$issue_file" "phase_state")
        if [[ "$phase_state" == "absorbed" || "$phase_state" == "dropped" ]]; then
          echo "[issue-sync] batch: close $local_id (phase_state=$phase_state)"
          cmd_close "$local_id" "completed" || true
        elif ! _already_on_platform "$issue_file" "github" 2>/dev/null; then
          echo "[issue-sync] batch: create $local_id (raw, not on platform)"
          cmd_create "$local_id" || true
        fi
        ;;
      linked)
        # Create on platform if missing (e.g. I-* items with no github.issue_id)
        if ! _already_on_platform "$issue_file" "github" 2>/dev/null; then
          echo "[issue-sync] batch: create $local_id (linked, not on platform)"
          cmd_create "$local_id" || true
        fi
        # Terminal closure is a STATE predicate, not a change predicate: a
        # completed I-* must close even on its first sync (no hash yet). Close is
        # idempotent, so it does not need the anti-spam gate that update has
        # (raw-20261113T130925Z).
        local phase; phase=$(_fm_get "$issue_file" "phase_state")
        local pstate; pstate=$(_fm_get "$issue_file" "platform_state")
        if [[ "$phase" == "completed" && "$pstate" != "closed" ]]; then
          echo "[issue-sync] batch: close $local_id (completed, platform=$pstate)"
          cmd_close_linked "$local_id" || true
        fi
        if _changed_since_last_sync "$local_id" "$issue_file"; then
          echo "[issue-sync] batch: update $local_id (phase=$phase)"
          cmd_update "$local_id" || true
        fi
        # Always check for unsynced comments
        cmd_comment "$local_id" || true
        ;;
    esac
    synced=$((synced + 1))
    batch_count=$((batch_count + 1))

    # Progress output every batch_size issues (keeps stream alive for Terminal)
    if [[ $((batch_count % batch_size)) -eq 0 ]]; then
      echo "[issue-sync] progress: $synced/$total"
    fi
  done

  # Final progress if not at batch boundary
  if [[ $((synced % batch_size)) -ne 0 ]]; then
    echo "[issue-sync] progress: $synced/$total"
  fi

  # Update scan state
  python3 -c "
import json, os, datetime
state = {}
if os.path.exists('$SCAN_STATE'):
  with open('$SCAN_STATE') as f: state = json.load(f)
state['last_scan_at'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
with open('$SCAN_STATE', 'w') as f: json.dump(state, f, indent=2, default=str)
" 2>/dev/null || true
}

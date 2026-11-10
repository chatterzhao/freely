#!/usr/bin/env bash
# cmd-batch.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync batch` — sync every changed issue.

cmd_batch() {
  local last_scan total=0 synced=0 batch_size=10 batch_count=0
  last_scan=$(_scan_state_get "last_sync_at")
  echo "[issue-sync] batch: last sync = ${last_scan:-never}"

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
	    local_id=$(basename "$dir")
	    [[ "$local_id" == raw-* || "$local_id" == I-* ]] || continue
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
    local_id=$(basename "$dir")

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
        if _changed_since_last_sync "$local_id" "$issue_file"; then
          local phase; phase=$(_fm_get "$issue_file" "phase_state")
          echo "[issue-sync] batch: update $local_id (phase=$phase)"
          cmd_update "$local_id" || true
          if [[ "$phase" == "completed" ]]; then
            cmd_close "$local_id" "completed" || true
          fi
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

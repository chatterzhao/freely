#!/usr/bin/env bash
# cmd-update.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync update` — refresh title/body/labels.

cmd_update() {
  local local_id="$1" file title body labels gh_id gitee_id
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  # No de-duplication here. `update` is an explicit, single-issue operator
  # command — the caller's intent IS the change. The batch paths (`scan`,
  # `batch`) keep the change-detection heuristic so they do not rewrite every
  # healthy replica. (#4653: gating this command made it a permanent no-op, so
  # a platform title or body could never be normalised.)

  title=$(_platform_title "$local_id" "$file")
  body=$(_issue_body "$file" "$local_id")
  labels=$(_labels "$file")

  # Aggregate both platform write results (raw-20261124T054217Z / #4671).
  # A partial success must never be reported as overall success — the runtime
  # consumes this exit code to decide whether replicas are consistent.
  local gh_result="skipped" gitee_result="skipped" write_failed=0

  gh_id=$(_gh_issue_number "$file")
  if [[ -n "${GH_REPO:-}" && -n "$gh_id" ]]; then
    echo "[issue-sync] GitHub: updating #$gh_id"
    if _gh_update "$gh_id" "$title" "$body" "$labels"; then
      gh_result="success"
    else
      gh_result="failure"
      write_failed=1
      echo "[issue-sync] GitHub: update FAILED" >&2
    fi
  fi

  gitee_id=$(_gitee_resolve_issue_number "$file" "$local_id")
  if [[ -n "${GITEE_REPO:-}" && -n "$gitee_id" ]]; then
    echo "[issue-sync] Gitee: updating $gitee_id"
    if _gitee_update "$gitee_id" "$title" "$body" >/dev/null; then
      gitee_result="success"
    else
      gitee_result="failure"
      write_failed=1
      echo "[issue-sync] Gitee: update FAILED" >&2
    fi
  fi

  local overall="success"
  [[ "$write_failed" -ne 0 ]] && overall="partial_failure"
  echo "[issue-sync] result: github=$gh_result gitee=$gitee_result overall=$overall"

  if [[ "$write_failed" -ne 0 ]]; then
    echo "[issue-sync] update FAILED (partial): $local_id" >&2
    return 1
  fi

  echo "[issue-sync] update complete: $local_id"
  return 0
}

#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
# Protected branches that only accept merge: develop, main
[[ "$branch" == "develop" || "$branch" == "main" ]] || exit 0

project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
guarded_state_path="$(git rev-parse --git-dir 2>/dev/null || true)"
if [[ -n "$guarded_state_path" ]]; then
  guarded_state_path="$guarded_state_path/freely-guarded-merge-state"
fi

# FREELY_SKIP_IBM_GATE: skip IBM governance gate with valid reason, keep merge state check
if [[ -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
  # --reason gate: env var bypass must carry valid business reason
  if ! echo "${FREELY_SKIP_IBM_GATE}" | grep -q "^违规绕过门禁中，理由充分，是："; then
    cat >&2 <<'REASON_GATE'
[GATE] 检测到你试图通过 FREELY_SKIP_IBM_GATE 违规绕过门禁

  如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。

  只有确实有合理的业务理由（仅文档/清理/格式化变更等），才允许绕过。
  FREELY_SKIP_IBM_GATE 的值必须匹配格式:
    FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"

  示例: FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：仅文档类变更不含实现代码" git merge
REASON_GATE
    exit 1
  fi
  load_guarded_state() {
    [[ -n "$guarded_state_path" && -f "$guarded_state_path" ]] || return 1
    guarded_state_target=""
    guarded_state_source=""
    guarded_state_bypass=""
    while IFS='=' read -r key value; do
      case "$key" in
        target_branch) guarded_state_target="$value" ;;
        source_branch) guarded_state_source="$value" ;;
        bypass_mode) guarded_state_bypass="$value" ;;
      esac
    done <"$guarded_state_path"
    [[ -n "$guarded_state_target" && -n "$guarded_state_source" && -n "$guarded_state_bypass" ]] || return 1
  }
  load_guarded_state || {
    cat <<MSG
[HOOK] Merge blocked: canonical guarded merge state is missing or malformed.
Re-run the merge through ./bin/pr-merge-guarded.
MSG
    exit 1
  }
  if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" != "1" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion handshake marker missing.
MSG
    exit 1
  fi
  cat <<'GATE_WARN' >&2
[HOOK] ⚠️  FREELY_SKIP_IBM_GATE=1 — IBM governance gate SKIPPED.

  仅以下 2 种情况允许绕过 IBM governance gate:
    1. docs-only 变更（agent 文档、skills、治理文档——不改运行时代码）
    2. 批量 closeout / 数据迁移 / YAML 规范化（机械操作，不改变行为）

  代码修改（含紧急修复）必须走完整流程:
    wt-create → skill:freely-fix-execution → B1 → B2 → dev → test → pr-merge-guarded

  本次绕过已记录。如非上述 2 种情况，请立即回退并走正常流程。
GATE_WARN

  # Delegate to governance-merge-gate with --skip-ibm-gate for path validation.
  # The gate has canonical path definitions (is_governance_only_path) that
  # work for both Freely and non-Freely projects via env var configuration.
  if [[ ! -x "./bin/governance-merge-gate" ]]; then
    cat <<MSG
[HOOK] FREELY_SKIP_IBM_GATE=1 but governance-merge-gate not found at ./bin/governance-merge-gate.
Install the gate or remove FREELY_SKIP_IBM_GATE=1 to use the full governance path.
MSG
    exit 1
  fi

  set +e
  gate_output="$(./bin/governance-merge-gate --staged --target-branch "$branch" --source-branch "$guarded_state_source" --skip-ibm-gate 2>&1)"
  gate_rc=$?
  set -e

  if [[ "$gate_rc" -ne 0 ]]; then
    cat <<MSG
[HOOK] FREELY_SKIP_IBM_GATE 拒绝：governance-merge-gate 检测到实现代码变更，不可绕过 IBM gate。

$gate_output

  FREELY_SKIP_IBM_GATE=1 仅限 document|cleanup|format 等治理型变更。
  实现变更必须走完整 raw→C→M→I 治理链。
MSG
    exit "$gate_rc"
  fi

  echo "$gate_output"
  echo "[HOOK] IBM governance gate skipped (FREELY_SKIP_IBM_GATE)"
  exit 0
fi

load_guarded_state() {
  [[ -n "$guarded_state_path" && -f "$guarded_state_path" ]] || return 1
  guarded_state_target=""
  guarded_state_source=""
  guarded_state_bypass=""
  while IFS='=' read -r key value; do
    case "$key" in
      target_branch) guarded_state_target="$value" ;;
      source_branch) guarded_state_source="$value" ;;
      bypass_mode) guarded_state_bypass="$value" ;;
    esac
  done <"$guarded_state_path"
  [[ -n "$guarded_state_target" && -n "$guarded_state_source" && -n "$guarded_state_bypass" ]] || return 1
}

require_valid_guarded_merge_state() {
  load_guarded_state || {
    cat <<MSG
[HOOK] Merge blocked: canonical guarded merge state is missing or malformed.
Raw develop merges are not an allowed entrypoint. Re-run the merge through ./bin/pr-merge-guarded so hooks can verify the canonical handshake.
MSG
    exit 1
  }

  if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" != "1" ]]; then
    cat <<MSG
[HOOK] Merge blocked: canonical guarded merge handshake marker is missing.
Raw develop merges are not an allowed entrypoint. Re-run the merge through ./bin/pr-merge-guarded.
MSG
    exit 1
  fi

  if ! git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
    cat <<MSG
[HOOK] Merge blocked: guarded completion requires an active MERGE_HEAD.
MSG
    exit 1
  fi

  if [[ "$guarded_state_target" != "$branch" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion target '$guarded_state_target' does not match current branch '$branch'.
MSG
    exit 1
  fi

  merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null || true)"
  source_sha="$(git rev-parse "$guarded_state_source" 2>/dev/null || true)"
  if [[ -z "$merge_head" || -z "$source_sha" || "$merge_head" != "$source_sha" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion source '$guarded_state_source' does not match MERGE_HEAD.
MSG
    exit 1
  fi
}

require_valid_guarded_merge_state

if git diff --cached --quiet --diff-filter=ACMR --; then
  exit 0
fi

if [[ ! -x "./bin/governance-merge-gate" ]]; then
  exit 0
fi

set +e
gate_output="$(./bin/governance-merge-gate --staged --target-branch "$branch" --source-branch "$guarded_state_source" 2>&1)"
gate_rc=$?
set -e

if [[ "$gate_rc" -ne 0 ]]; then
  cat <<MSG
[HOOK] Merge blocked: protected-branch governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain in the source writable worktree before rerunning the guarded merge.
MSG
  exit "$gate_rc"
fi

echo "$gate_output"

if [[ ! -x "./bin/governance-promotion-gate" ]]; then
  exit 0
fi

set +e
promotion_output="$(./bin/governance-promotion-gate --project "$project_root" --target-branch "$branch" 2>&1)"
promotion_rc=$?
set -e

if [[ "$promotion_rc" -ne 0 ]]; then
  cat <<MSG
[HOOK] Merge blocked: protected-branch promotion ownership gate failed.

$promotion_output

Let the current promotion owner finish or reclaim ownership through manager arbitration before merging to develop.
MSG
  exit "$promotion_rc"
fi

[[ -n "$promotion_output" ]] && echo "$promotion_output"
exit 0

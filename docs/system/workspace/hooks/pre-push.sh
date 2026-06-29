#!/usr/bin/env bash
set -euo pipefail

policy_ref='docs/CONSTITUTION.md §2'

while read -r local_ref local_sha remote_ref remote_sha; do
  [[ -z "${local_ref:-}" ]] && continue

  # Remote branch deletion (git push --delete): only allowed via wt-close.
  # git sends all-zero local_sha for delete operations.
  if [[ "$local_sha" == "0000000000000000000000000000000000000000" ]]; then
    # Walk process ancestry to check if wt-close is in the parent chain
    _pid=$PPID
    _is_wt_close=0
    while [[ "$_pid" -gt 1 ]]; do
      _cmd=$(ps -o comm= -p "$_pid" 2>/dev/null || true)
      case "$_cmd" in
        wt-close|bash*)
          _full_cmd=$(ps -o args= -p "$_pid" 2>/dev/null || true)
          case "$_full_cmd" in
            *wt-close*) _is_wt_close=1; break ;;
          esac
          ;;
      esac
      _ppid=$(ps -o ppid= -p "$_pid" 2>/dev/null | tr -d ' ' || true)
      [[ -n "$_ppid" && "$_ppid" -gt 0 ]] || break
      _pid=$_ppid
    done
    if [[ "$_is_wt_close" -eq 1 ]]; then
      continue
    fi
    cat >&2 <<'DELETE_BLOCK'
[HOOK] 远程分支删除被拦截。

  删除远程分支必须通过 wt-close 收口。
  直接执行 git push --delete 是违规操作。

  Usage: freely wt-close <branch>

  这是硬性门禁，无法绕过。
DELETE_BLOCK
    exit 1
  fi

  # Allow tag pushes (git push <remote> <tagname>)
  if [[ "$local_ref" == refs/tags/* ]]; then
    continue
  fi

  local_branch="${local_ref#refs/heads/}"
  remote_branch="${remote_ref#refs/heads/}"

  # Audit log for FREELY_SKIP usage
  if [[ -n "${FREELY_SKIP_CREATE_GATE:-}" || -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
    mkdir -p .freely/logs
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SKIP_GATE branch=$local_branch reason=${FREELY_SKIP_CREATE_GATE:-IBM_GATE}" >> .freely/logs/skip-gate.log
  fi

  if [[ "$local_branch" == test-pre-merge-* ]]; then
    cat >&2 <<MSG
[HOOK] Push blocked: test pre-merge batch '$local_branch' is local-only.
Create the batch from current develop, use it for temporary verification, then delete it.
Do not publish test-pre-merge branches to remote.
MSG
    exit 1
  fi

  case "$local_branch" in
    main|develop)
      # ── Force-push detection: block history rewrite on protected branches ──
      if [[ -n "${remote_sha:-}" && "$remote_sha" != "0000000000000000000000000000000000000000" ]]; then
        if ! git merge-base --is-ancestor "$remote_sha" "$local_sha" 2>/dev/null; then
          cat >&2 <<MSG
[HOOK] Push blocked: force push to protected branch '$local_branch' is forbidden.

  git push --force / --force-with-lease 会重写受保护分支的提交历史，
  导致不同平台 commit SHA 不一致，破坏多平台同步。

  正确流程:
    - 所有改动通过 pr-merge-guarded 合并
    - pr-merge-guarded 会同时推送到所有平台，保证一致性
    - 如果遇到 governance gate 阻塞，按报错修复后重新执行 pr-merge-guarded

  永远不要对 main/develop 使用 --force 或 --force-with-lease。

MSG
          exit 1
        fi
      fi
      if [[ "$local_branch" == "develop" && -x "./bin/governance-merge-gate" ]]; then
        if [[ -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
          if ! echo "${FREELY_SKIP_IBM_GATE}" | grep -q "^违规绕过门禁中，理由充分，是："; then
            cat >&2 <<'REASON_GATE'
[GATE] 检测到你试图通过 FREELY_SKIP_IBM_GATE 违规绕过门禁

  如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。

  只有确实有合理的业务理由（仅文档/清理/格式化变更等），才允许绕过。
  FREELY_SKIP_IBM_GATE 的值必须匹配格式:
    FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"

  示例: FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：仅文档类变更不含实现代码" git push
REASON_GATE
            exit 1
          fi
          echo "[HOOK] FREELY_SKIP_IBM_GATE — validating governance-only paths via governance-merge-gate --skip-ibm-gate"
          set +e
          gate_output="$(./bin/governance-merge-gate --range "develop..HEAD" --skip-ibm-gate 2>&1)"
          gate_rc=$?
          set -e
          if [[ "$gate_rc" -ne 0 ]]; then
            cat >&2 <<MSG
[HOOK] Push blocked: FREELY_SKIP_IBM_GATE=1 but governance-merge-gate detected implementation changes.

$gate_output

FREELY_SKIP_IBM_GATE=1 is only allowed for governance-only changes.
MSG
            exit "$gate_rc"
          fi
          echo "$gate_output"
        elif [[ -n "${remote_sha:-}" && "$remote_sha" != "0000000000000000000000000000000000000000" ]]; then
          set +e
          gate_output="$(./bin/governance-merge-gate --range "${remote_sha}..${local_sha}" 2>&1)"
          gate_rc=$?
          set -e
          if [[ "$gate_rc" -ne 0 ]]; then
            cat >&2 <<MSG
[HOOK] Push blocked: develop-bound governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain before pushing develop.
MSG
            exit "$gate_rc"
          fi
        fi
      fi
      continue
      ;;
    feature/*|hotfix/*|fix/*)
      # Validate naming convention: must contain raw-xxx or I-xxx key
      if ! echo "$local_branch" | grep -qoE 'raw-[0-9]{8}[-T][0-9]{4,6}Z?' && \
         ! echo "$local_branch" | grep -qoE 'I-[0-9]{8}[-T][0-9]{4,6}Z?(-[A-Z0-9]+)?'; then
        cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' must contain an issue key.
Format: fix|feature/raw-{YYYYMMDD}-{HHMM[SS]}-{slug} or feature/raw-{YYYYMMDDTHHMM[SS]Z}-{slug}
Each worktree/branch must correspond to an issue (docs/LAWS.md §2).
Use 'git branch -m' to rename.
MSG
        exit 1
      fi
      # Check if pr-create-gate has passed on this branch
      if [[ -z "${FREELY_SKIP_CREATE_GATE:-}" ]]; then
        if [[ ! -f ".freely/run/pr-create-gate-passed" ]]; then
          cat >&2 <<MSG
[HOOK] Push blocked: pr-create-gate has not been run on branch '$local_branch'.

  All fix/feature/hotfix branches must pass pr-create-guarded before pushing.
  Run pr-create-guarded in your worktree:
    freely pr-create-guarded

  The ONLY valid way to push is:
    freely pr-create-guarded
MSG
          exit 1
        fi
      else
        # FREELY_SKIP_CREATE_GATE: only allowed for docs-only changes with valid reason.
        if ! echo "${FREELY_SKIP_CREATE_GATE}" | grep -q "^违规绕过门禁中，理由充分，是："; then
          cat >&2 <<'REASON_GATE'
[GATE] 检测到你试图通过 FREELY_SKIP_CREATE_GATE 违规绕过门禁

  如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。

  只有确实有合理的业务理由（纯文档变更、治理文档更新等），才允许绕过。
  FREELY_SKIP_CREATE_GATE 的值必须匹配格式:
    FREELY_SKIP_CREATE_GATE="违规绕过门禁中，理由充分，是：<业务理由>"

  示例: FREELY_SKIP_CREATE_GATE="违规绕过门禁中，理由充分，是：纯治理文档更新不含代码变更" git push
REASON_GATE
          exit 1
        fi
        # Code files MUST go through pr-create-guarded.
        local _base; _base="$(git merge-base origin/develop HEAD 2>/dev/null || echo "origin/develop")"
        if git diff --name-only "$_base..HEAD" 2>/dev/null | grep -qE '\.(sh|py|rs|ts|js|tsx|jsx|go|java|c|cpp|h|toml)$'; then
          cat >&2 <<MSG
[HOOK] FREELY_SKIP_CREATE_GATE rejected: code files must use pr-create-guarded.
  Run: freely pr-create-guarded
MSG
          exit 1
        fi
      fi
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}
MSG
      exit 1
      ;;
    release/*)
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}
MSG
      exit 1
      ;;
    *)
      cat >&2 <<MSG
[HOOK] Push blocked: unsupported branch type '$local_branch'.
Use fix/*, feature/*, release/*, hotfix/* or protected integration branches.
MSG
      exit 1
      ;;
  esac
done

exit 0

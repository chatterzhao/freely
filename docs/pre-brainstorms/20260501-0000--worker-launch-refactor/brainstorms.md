# Brainstorms — Worker Launch Refactor

## Context

Manager AI delegates workers via `EXIT_KIND=delegate_workers` but workers never complete:
- Worker prompts pile up (6-14 observed)
- `worker_auto_recovered` fires every ~30s (supervisor crash loop)
- `manager-watchdog.sh` processes accumulate (9+ concurrent)
- Worktree cleanup never executes

Root cause traced to `launch_worker_from_manager_prompt_if_needed` (freely line 11367):
`start_workcell_supervisor_async` — starts a **full freely daemon** for each worker worktree.

## Current Architecture

```
Manager AI cycle
  ↓  writes: manager-exit-contract.env (EXIT_KIND=delegate_workers)
  ↓         manager-continuity-*.md (worker prompt references)
  ↓         worker-prompts/*.txt (worker task descriptions)
  ↓
Supervisor loop (line 18306)
  ↓  manager_runtime_launch_workers_after_ai_cycle_if_needed
  ↓  → manager_runtime_launch_workers_from_latest_handoff
  ↓     → reads continuity → gets worker prompt paths
  ↓     → for each worker: launch_worker_from_manager_prompt_if_needed
  ↓
launch_worker (line 11347)
  ├─ worker worktree has supervisor+AI → rebind/reentry (correct)
  └─ worker worktree has no runtime → start_workcell_supervisor_async
       ↓
       nohup freely daemon-run --project <worker_worktree> &
       ↓
       NEW freely daemon instance
         → own supervisor → own ACP bridge → own AI process
         → competes with manager daemon for resources
         → crashes or hangs → watchdog pile-up → prompts never consumed
```

## Problem

**`start_workcell_supervisor_async` launches a completely independent freely daemon.** 

This is unnecessary and harmful because:
1. Multiple freely instances compete for PID files, ACP bridge, and system resources
2. Worker daemon crashes trigger watchdog recovery loops
3. Worker prompts are never consumed because the worker daemon can't start properly
4. `manager-watchdog.sh --recover-expected-workers` processes accumulate

## Correct Architecture

Worker AI should run as a **managed sub-process of the manager runtime**, not an independent daemon:

```
Manager AI cycle completes → EXIT_KIND=delegate_workers
  ↓
Manager runtime (supervisor loop)
  ↓  for each worker_prompt:
  ↓    1. cd <worker_worktree> (or use --cwd)
  ↓    2. Set SESSION_PARENT_ID=<manager_session>
  ↓    3. Set FREELY_ROLE_HINT=worker
  ↓    4. Launch AI process directly:
  ↓       run-acp-prompt.py --bridge-socket <manager_bridge> \
  ↓         --cwd <worker_worktree> \
  ↓         --prompt-file <worker_prompt> \
  ↓         --launch-kind fork --session-id <new_uuid>
  ↓    5. Wait for AI to complete
  ↓    6. Read worker-exit-contract.env
  ↓    7. Update worker state (completed/blocked/handoff)
  ↓
Next manager cycle picks up worker results
```

Key differences:
- **No new daemon** — worker AI runs under the same runtime
- **Same ACP bridge** — worker uses the manager's bridge (through `--bridge-socket`)
- **Session fork** — worker gets its own ACP session via `session/new` (not `session/resume`)
- **Direct completion detection** — runtime waits for AI process exit, reads exit contract

## Implementation Plan

### Phase 1: Direct Worker Launch

Replace `start_workcell_supervisor_async` with `launch_worker_ai_directly`:

```bash
launch_worker_ai_directly() {
  local manager_project="$1" worker_project="$2" prompt_file="$3"
  
  # 1. Set worker session state
  write_worker_session_state "$worker_project" "${CLAUDE_SESSION_ID_CURRENT:-}"
  
  # 2. Build AI launch command
  local monitor_script cycle_log prompt_file
  # ... use existing monitor-ai-acp.sh but with worker role
  
  # 3. Launch and wait
  bash "$monitor_script" --project "$worker_project" --prompt-file "$prompt_file" \
    --launch-kind fork --role worker ...
  
  # 4. Read worker exit contract
  if [[ -f "$(worker_exit_contract_file "$worker_project")" ]]; then
    local kind=$(worker_exit_contract_kind "$worker_project")
    case "$kind" in
      worker_done) return 0 ;;
      worker_blocked) return 2 ;;
      worker_handoff_needed) return 3 ;;
    esac
  fi
}
```

### Phase 2: Worker State Management

- Track worker status in `manager-worker-launch-state.env`
- Detect completed/blocked/handoff workers
- Clean up worker state files on completion

### Phase 3: Manager Continuity Integration

- Manager AI reads worker results from exit contracts
- Updates milestone/progress based on worker completions
- Re-delegates blocked workers with updated context

## Continuity vs Exit Contract: 数据源分析

### Continuity (`manager-continuity-*.md`)

Manager 跨周期状态快照（markdown，AI 生成）：
- 项目状态：worktree fleet, scan results, governance checks
- Worker 委派历史：previous_worker_prompt, prompt_path
- 跨周期恢复上下文：下一个 manager cycle 读取

### Exit Contract (`manager-exit-contract.env`)

Manager 本轮决策的 machine-readable 合同（env 格式）：
```env
EXIT_KIND="delegate_workers"
WORKER_PROMPTS_CSV="/p1.txt,/p2.txt"
```

### 当前问题

Worker launch 走 continuity pipeline → 多层 gate + awk regex 解析 markdown → 脆弱。AI 输出格式微小偏差就导致 worker 不 launch。

### 修正方案

**保留 continuity 的 manager 上下文职能，worker launch 改从 exit_contract 读取。**

```
exit_contract (env, machine-readable)
  WORKER_PROMPTS_CSV=/p1.txt,/p2.txt
    ↓ 直接 split by comma → 逐个 launch_worker
    ↓ (不走 continuity pipeline)

continuity (markdown)
  保留给 manager 跨周期上下文
  不参与 worker launch 决策
```

## Files to Change

| File | Change |
|---|---|
| `freely` line 11591-11612 | `manager_runtime_launch_workers_after_ai_cycle_if_needed` — 从 exit_contract 读 WORKER_PROMPTS_CSV |
| `freely` line 11347-11367 | `launch_worker_from_manager_prompt_if_needed` — 已改 ✅ (直接 AI launch 替代 start_workcell_supervisor_async) |

## Success Criteria

1. **Worker executes**: Worker prompt consumed, AI process runs to completion
2. **Worker completes**: Worker exit contract written with valid EXIT_KIND
3. **No daemon proliferation**: Zero additional freely daemon instances
4. **Manager picks up results**: Next manager cycle reads worker exit contracts
5. **No worker prompt pile-up**: Prompts consumed within one supervisor loop iteration
6. **Worktree cleanup works**: Cleanup workers actually remove worktrees and branches

# Fix new-session FORCE_FRESH marker - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `cmd_new_session writes FORCE_FRESH=true to session-state.env. select_launch_kind checks it before JSONL fallback. After fresh launch, marker is stripped.`
- why_this: `new-session cleared state file but JSONL fallback still found old sessions and forced resume. When switching models (pro→flash), old sessions cannot be resumed.`
- alternatives_considered: `1) Clear JSONL dir: rejected, destructive. 2) Force fresh flag: chosen, minimal.`
- boundary_non_goals: `No change to resume enforcement logic.`
- residual_risk: `None — marker is one-shot, stripped after first launch.`

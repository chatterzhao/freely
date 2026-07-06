# Resume config - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add AI_RESUME_ON_RESTART config (default true). When set, select_launch_kind prefers resume even without verified session evidence.`
- why_this: `Stall-killed AI sessions lose session_id tracking but the tool session may still be alive. Resume saves token (deepseek cache) and time (skip re-reading docs).`
- alternatives_considered: `1) Always resume: rejected, need off switch for debugging. 2) Config only: chosen, simple and controllable.`
- boundary_non_goals: `No change to initial daemon start behavior (still fresh on first launch). No change to resume evidence verification.`
- residual_risk: `Resume without evidence may fail if tool session is actually gone. Tool handles this gracefully.`

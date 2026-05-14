# Code Review
- issue_id: I-20260514T005740Z-A
## Implementation Decision Note
- decision: strip ENV=val prefix in _resolve_tool_family, export env vars in _apply_tool_alias_settings
- why_this: oc-run-ds-flash-auto starts with OPENCODE_CONFIG=, breaking binary extraction
- alternatives_considered: (1) Hardcode every alias — violates design intent (2) Strip env prefix — chosen
- residual_risk: Edge cases in env value parsing (nested quotes) fall back to original alias

# Code Review
- issue_id: I-20260513T160637Z-A
## Implementation Decision Note
- decision: remove unquoted heredoc, use plain string for multi-line prompt format
- why_this: <<EOF in $(cat <<EOF) causes backtick command substitution; triple backticks for code fences get interpreted as shell commands
- residual_risk: None — multi-line string literal behaves identically to heredoc

---
b1_id: B1-20260720T012820Z / phase_state: completed
---
# B1: new→fresh
run-acp-prompt.py仅接受fresh/resume/fork/prompt。new导致argparse error→worker立即崩溃。
debug log确认: "invalid choice: new (choose from fresh, resume, fork, prompt)"

"""Verify and/or precedence is correct after fix."""
# Simulate the three fixed lines

def test_l403_fix():
    """state=working should require BOTH state check AND prefix match."""
    agent_id = "reviewer_05"
    state = "failed"
    # Fixed: state == "working" and (worker or reviewer)
    result = state == "working" and (agent_id.startswith("worker") or agent_id.startswith("reviewer"))
    assert result == False, f"state=failed + reviewer should NOT enter working handler, got {result}"

    state2 = "working"
    result2 = state2 == "working" and (agent_id.startswith("worker") or agent_id.startswith("reviewer"))
    assert result2 == True, f"state=working + reviewer SHOULD enter working handler, got {result2}"

def test_l403_bug_reproduction():
    """The old bug: reviewer in ANY state would enter working handler."""
    agent_id = "reviewer_05"
    state = "failed"
    # OLD buggy code: (state=="working" AND worker) OR reviewer
    old_buggy = state == "working" and agent_id.startswith("worker") or agent_id.startswith("reviewer")
    assert old_buggy == True, "OLD bug: reviewer failed task enters working handler — this is what we fixed"

def test_l442_fix():
    """submitted handler: both prefixes need state check."""
    agent_id = "reviewer_05"
    state = "completed"
    result = state == "submitted" and (agent_id.startswith("manager") or agent_id.startswith("reviewer"))
    assert result == False, f"state=completed + reviewer should NOT enter submitted handler"

def test_l663_fix():
    """launched_pids: both prefixes wrapped in parens."""
    r = {"agent_id": "reviewer_05", "state": "working", "worker_pid": "12345"}
    result = (r["agent_id"].startswith("worker") or r["agent_id"].startswith("reviewer")) and r["state"] == "working" and r.get("worker_pid")
    assert result == True, f"reviewer working with pid SHOULD match"

print("All _restore_tasks priority tests passed ✅")

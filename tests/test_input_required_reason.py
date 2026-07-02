"""Unit tests for InputRequiredReason enum."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "docs", "system", "workspace", "agents"))
from input_required_reason import InputRequiredReason

def test_all_values():
    assert len(list(InputRequiredReason)) == 12, f"Expected 12, got {len(list(InputRequiredReason))}"

def test_from_string_exact():
    assert InputRequiredReason.from_string("needs-review:b1") == InputRequiredReason.NEEDS_REVIEW_B1
    assert InputRequiredReason.from_string("needs-review:dev") == InputRequiredReason.NEEDS_REVIEW_DEV
    assert InputRequiredReason.from_string("needs-manager-decision") == InputRequiredReason.NEEDS_MANAGER_DECISION

def test_from_string_unknown():
    assert InputRequiredReason.from_string("garbage") == InputRequiredReason.UNKNOWN
    assert InputRequiredReason.from_string("") == InputRequiredReason.UNKNOWN
    assert InputRequiredReason.from_string(None) == InputRequiredReason.UNKNOWN

def test_from_string_trimmed():
    assert InputRequiredReason.from_string("  needs-review:b1  ") == InputRequiredReason.NEEDS_REVIEW_B1

def test_needs_role():
    assert InputRequiredReason.NEEDS_REVIEW_B1.needs_role == "reviewer"
    assert InputRequiredReason.NEEDS_REVIEW_GATE.needs_role == "reviewer"
    assert InputRequiredReason.NEEDS_MANAGER_DECISION.needs_role == "manager"
    assert InputRequiredReason.NEEDS_WORKER_RETRY.needs_role == "worker"
    assert InputRequiredReason.UNKNOWN.needs_role == "manager"

def test_fallback_coverage():
    """All unknown paths route to manager_01."""
    for v in ["", "nonexistent", "needs-unknown:xyz", None]:
        r = InputRequiredReason.from_string(v)
        assert r == InputRequiredReason.UNKNOWN
        assert r.needs_role == "manager"

def test_all_six_routes():
    """Verify 6 bidirectional routes + human + fallback all have needs_role."""
    routes = {
        "needs-review:b1": "reviewer", "needs-review:b2": "reviewer",
        "needs-review:dev": "reviewer", "needs-review:red": "reviewer",
        "needs-review:test": "reviewer", "needs-review:gate": "reviewer",
        "needs-manager-decision": "manager", "needs-worker-retry": "worker",
        "needs-manager-scope": "manager", "needs-worker-task": "worker",
        "needs-human-input": "manager", "unknown": "manager",
    }
    for reason, expected_role in routes.items():
        r = InputRequiredReason.from_string(reason)
        assert r.needs_role == expected_role, f"{reason} → {r.needs_role} != {expected_role}"

print("All InputRequiredReason tests passed ✅")

"""Logic tests for agent_working — test parsing without DB connection."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "docs", "system", "workspace", "scripts", "runtime"))
from agent_working import _parse_pairs, _format_pairs

def test_parse_pairs_normal():
    assert _parse_pairs("reviewer_05:ses_ghi,reviewer_08:ses_jkl") == {
        "reviewer_05": "ses_ghi", "reviewer_08": "ses_jkl"
    }

def test_parse_pairs_empty():
    assert _parse_pairs("") == {}
    assert _parse_pairs(None) == {}

def test_parse_pairs_single():
    assert _parse_pairs("worker_03:ses_def") == {"worker_03": "ses_def"}

def test_parse_pairs_no_session():
    """agent_id without session (no colon) is ignored."""
    assert _parse_pairs("worker_03") == {}

def test_format_pairs():
    d = {"reviewer_05": "ses_ghi", "reviewer_08": "ses_jkl"}
    result = _format_pairs(d)
    parts = result.split(",")
    assert len(parts) == 2
    assert "reviewer_05:ses_ghi" in parts
    assert "reviewer_08:ses_jkl" in parts

def test_format_pairs_empty():
    assert _format_pairs({}) == ""

def test_roundtrip():
    original = "reviewer_05:ses_ghi,reviewer_08:ses_jkl"
    assert _format_pairs(_parse_pairs(original)) == original

print("All agent_working logic tests passed ✅")

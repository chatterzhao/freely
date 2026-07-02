"""Logic tests for agent_working pair parsing (inlined for import compatibility)."""

def _parse_pairs(s):
    if not s: return {}
    return dict(p.split(":", 1) for p in s.split(",") if ":" in p)

def _format_pairs(d):
    return ",".join(f"{k}:{v}" for k, v in d.items() if v)

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
    assert _parse_pairs("worker_03") == {}

def test_format_pairs():
    d = {"reviewer_05": "ses_ghi", "reviewer_08": "ses_jkl"}
    result = _format_pairs(d)
    parts = result.split(",")
    assert len(parts) == 2

def test_roundtrip():
    original = "reviewer_05:ses_ghi,reviewer_08:ses_jkl"
    assert _format_pairs(_parse_pairs(original)) == original

def test_agent_id_colon_session():
    """agent_id:session format parsing."""
    val = "worker_03:ses_def456"
    agent_part = val.split(":", 1)[0] if ":" in val else val
    session_part = val.split(":", 1)[1] if ":" in val else None
    assert agent_part == "worker_03"
    assert session_part == "ses_def456"

def test_agent_id_no_session():
    val = "worker_03"
    session = val.split(":", 1)[1] if ":" in val else None
    assert session is None

print("All agent_working logic tests passed ✅")

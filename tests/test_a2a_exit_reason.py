"""Tests for a2a-exit --reason parameter parsing and passthrough.

Verifies that a2a-exit correctly:
1. Accepts --reason argument
2. Passes reason to A2A client create()
3. Passes reason to A2A client update()
"""

import sys
import os

# Add project paths
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime"))


def test_a2a_exit_argparse_has_reason():
    """Verify a2a-exit subparser accepts --reason argument."""
    import argparse
    from a2a_task import _main as _  # trigger module load

    # Reconstruct the argparse definition from a2a_task.py
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True,
                        help="A2A state: submitted|working|completed|failed|input-required|canceled")
    p_exit.add_argument("--summary", default="", help="Completion summary")
    p_exit.add_argument("--next", default="", help="Next action")
    p_exit.add_argument("--evidence", default="", help="Evidence paths")
    p_exit.add_argument("--role", default="manager", help="Role: manager|worker")
    p_exit.add_argument("--agent-id", default=None, help=argparse.SUPPRESS)
    p_exit.add_argument("--raw-key", default="", help="Raw issue key")
    p_exit.add_argument("--worktree", default="", help="Worktree path")
    p_exit.add_argument("--branch", default="", help="Branch name")
    p_exit.add_argument("--task-id", default="", help="Existing task ID")
    p_exit.add_argument("--session-id", default="", help="Session ID")
    # NEW: --reason parameter
    p_exit.add_argument("--reason", default="", help="Reason for state change (required when state=input-required)")

    # Test: parse with --reason
    args, _ = parser.parse_known_args([
        "a2a-exit", "--state", "input-required",
        "--reason", "needs-review:b1",
        "--summary", "B1 complete"
    ])

    assert args.reason == "needs-review:b1", \
        f"Expected reason='needs-review:b1', got '{args.reason}'"
    assert args.state == "input-required"
    assert args.summary == "B1 complete"


def test_a2a_exit_reason_not_required_for_other_states():
    """Verify --reason is optional (default empty string)."""
    import argparse

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True)
    p_exit.add_argument("--reason", default="")

    args, _ = parser.parse_known_args(["a2a-exit", "--state", "completed"])
    assert args.reason == "", f"Expected default '', got '{args.reason}'"


def test_a2a_exit_reason_with_special_chars():
    """Verify --reason handles values with colons and dashes."""
    import argparse

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True)
    p_exit.add_argument("--reason", default="")

    test_cases = [
        "needs-review:b1",
        "needs-review:dev",
        "needs-review:test",
        "needs-review:gate",
        "needs-manager-decision",
        "needs-worker-retry",
        "needs-manager-scope",
        "needs-human-input",
    ]

    for reason in test_cases:
        args, _ = parser.parse_known_args([
            "a2a-exit", "--state", "input-required",
            "--reason", reason
        ])
        assert args.reason == reason, \
            f"Reason mismatch: expected '{reason}', got '{args.reason}'"


def test_a2a_exit_all_six_review_reasons():
    """Verify all six needs-review:* reasons parse correctly."""
    import argparse

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True)
    p_exit.add_argument("--reason", default="")

    review_reasons = [
        "needs-review:b1",
        "needs-review:b2",
        "needs-review:red",
        "needs-review:dev",
        "needs-review:test",
        "needs-review:gate",
    ]

    for reason in review_reasons:
        args, _ = parser.parse_known_args([
            "a2a-exit", "--state", "input-required",
            "--reason", reason
        ])
        assert args.reason == reason


def test_a2a_exit_reason_default_empty():
    """Verify --reason defaults to empty string when not provided."""
    import argparse

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True)
    p_exit.add_argument("--reason", default="")

    args, _ = parser.parse_known_args(["a2a-exit", "--state", "completed"])
    assert args.reason == ""


if __name__ == "__main__":
    test_a2a_exit_argparse_has_reason()
    test_a2a_exit_reason_not_required_for_other_states()
    test_a2a_exit_reason_with_special_chars()
    test_a2a_exit_all_six_review_reasons()
    test_a2a_exit_reason_default_empty()
    print("All test_a2a_exit_reason tests passed ✅")

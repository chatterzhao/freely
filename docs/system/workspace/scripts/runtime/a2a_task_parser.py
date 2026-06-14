#!/usr/bin/env python3
"""a2a_task_parser.py — Parse A2A Task state from AI reply.

The AI's reply is an A2A Message (role/type/content). The structured state
block at the end provides the A2A Task state transition data.

A2A states: submitted, working, completed, failed, input-required, pending-input
"""
"""DEPRECATED: a2a_task_parser.py — text JSON extraction is now FALLBACK ONLY.

Primary exit path: a2a-exit tool (AI directly sets A2A Task state).
This parser is retained for backward compatibility during transition.

Deprecation schedule:
  Phase 4a (current): Fallback only, log deprecation warning on each use
  Phase 4b (2026-07-01): Prune STATE_ALIASES to minimal set
  Phase 4c (2026-07-14): Remove entirely (require >90% a2a-exit adoption)
"""

import json
import re

# ── A2A Task States ───────────────────────────────────────────────────────

VALID_STATES = {
    'submitted', 'working', 'completed', 'failed',
    'input-required', 'pending-input',
}

# Required fields per A2A state (summary is always required)
REQUIRED_FIELDS = {
    'submitted':      ['summary'],
    'working':        ['summary'],
    'completed':      ['summary'],
    'failed':         ['summary'],
    'input-required': ['summary'],
    'pending-input':  ['summary'],
}

# Natural language → A2A state aliases (AI may output NL variants)
STATE_ALIASES = {
    # submitted
    'delegate': 'submitted', 'delegated': 'submitted', 'dispatch': 'submitted',
    'working': 'submitted', 'active': 'submitted', 'in_progress': 'working',
    # working (worker)
    'in-progress': 'working', 'progress': 'working',
    # completed
    'done': 'completed', 'success': 'completed', 'finished': 'completed',
    'complete': 'completed', 'ok': 'completed', 'good': 'completed',
    'completed_no_op': 'completed', 'clean_success': 'completed',
    'completed_with_findings': 'completed', 'partial_success': 'completed',
    'completed_s_hint': 'completed', 'completed_with_evidence': 'completed',
    'completed_idle': 'completed', 'completed_independent': 'completed',
    'task_already_done': 'completed', 'noop': 'completed',
    'all_done': 'completed', 'finished_no_op': 'completed',
    'completed_no_changes': 'completed', 'normal': 'completed',
    # failed
    'stopped': 'failed', 'paused': 'failed', 'exit': 'failed',
    'nothing': 'failed', 'no_work': 'failed', 'idle': 'failed',
    'stop': 'failed', 'error': 'failed',
    # input-required
    'blocked': 'input-required', 'block': 'input-required',
    # pending-input
    'needs_manager': 'pending-input', 'needs_input': 'pending-input',
    'handoff': 'pending-input',
}


# ── Public API ────────────────────────────────────────────────────────────

def extract_state_block(reply_text: str) -> str:
    """Extract the A2A state JSON block from AI reply text.

    The AI reply IS an A2A Message. The structured state block at the end
    provides the Task state transition data for the A2A Server.
    """
    m = re.search(r'```(\S*)\s*\n(.*?)```', reply_text, re.DOTALL)
    return m.group(1).strip() if m else ""


def validate_state_json(fields: dict) -> tuple:
    """Validate A2A state fields. Returns (ok: bool, errors: list)."""
    errors = []
    state = fields.get("state", "")
    if not state:
        errors.append({"field": "state", "error": "missing"})
        return False, errors
    if state not in VALID_STATES:
        errors.append({"field": "state", "error": f"unknown A2A state: {state}"})
        return False, errors
    required = REQUIRED_FIELDS.get(state, [])
    for f in required:
        if not fields.get(f):
            errors.append({"field": f, "error": f"required for state={state}"})
    return len(errors) == 0, errors


def normalize_state_fields(fields: dict) -> None:
    """Normalize AI natural language → A2A state in place.

    Valid A2A states pass through. Non-A2A terms are mapped via aliases.
    """
    state = fields.get("state", "").strip().lower()
    if state not in VALID_STATES and state in STATE_ALIASES:
        fields["state"] = STATE_ALIASES[state]


def normalize_state(state: str) -> str:
    """Normalize AI natural language → canonical A2A state.

    Only applies aliases for non-A2A terms. Valid A2A states pass through unchanged.
    """
    s = state.strip().lower()
    if s in VALID_STATES:
        return s
    return STATE_ALIASES.get(s, s)


def extract_task_state(reply_text: str) -> dict:
    """Extract A2A state from AI reply without side effects."""
    block = extract_state_block(reply_text)
    if not block:
        return {"ok": False, "errors": [{"field": "block", "error": "no state JSON block found"}]}
    try:
        fields = json.loads(block)
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [{"field": "parse", "error": str(e)}]}
    normalize_state_fields(fields)
    ok, errors = validate_state_json(fields)
    if not ok:
        return {"ok": False, "errors": errors}
    return {"ok": True, "state": fields["state"], "fields": fields}

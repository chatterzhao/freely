#!/usr/bin/env python3
"""a2a_task_parser.py — Parse A2A Task JSON from AI reply.

Replaces handoff_parser.py. Extracts and validates A2A task state
from AI cycle logs. No DB dependencies.

Deprecated: handoff_parser.py — original parser, replaced 2026-06-12.
"""

import json
import os
import re

# ── Constants ─────────────────────────────────────────────────────────────

VALID_EXIT_KINDS = {
    'delegate_workers', 'resume_manager', 'stop_ai',
    'manager_working',
    'worker_done', 'worker_blocked', 'worker_handoff_needed',
    'worker_working',
}

REQUIRED_FIELDS = {
    'delegate_workers':       ['reason', 'worker_prompts_csv'],
    'resume_manager':         ['reason', 'restart_point', 'next_action'],
    'stop_ai':                ['reason'],
    'manager_working':        ['progress', 'next_action'],
    'worker_done':            ['completion_summary', 'evidence_paths'],
    'worker_blocked':         ['reason', 'next_action'],
    'worker_handoff_needed':  ['reason', 'next_action'],
    'worker_working':         ['progress', 'next_action'],
}

EXIT_KIND_ALIASES = {
    'delegate': 'delegate_workers', 'delegated': 'delegate_workers',
    'dispatch': 'delegate_workers',
    'working': 'manager_working', 'active': 'manager_working',
    'continue': 'resume_manager', 'resume': 'resume_manager',
    'analyzing': 'resume_manager', 'researching': 'resume_manager',
    'stopped': 'stop_ai', 'paused': 'stop_ai', 'exit': 'stop_ai',
    'finished': 'stop_ai', 'nothing': 'stop_ai', 'no_work': 'stop_ai',
    'done': 'stop_ai', 'idle': 'stop_ai',
    'completed': 'worker_done', 'success': 'worker_done',
    'partial': 'worker_done', 'normal': 'worker_done',
    'completed_no_op': 'worker_done', 'clean_success': 'worker_done',
    'completed_with_findings': 'worker_done', 'partial_success': 'worker_done',
    'completed_s_hint': 'worker_done', 'completed_with_evidence': 'worker_done',
    'completed_idle': 'worker_done', 'completed_independent': 'worker_done',
    'complete': 'worker_done', 'task_already_done': 'worker_done',
    'noop': 'worker_done', 'ok': 'worker_done', 'good': 'worker_done',
    'all_done': 'worker_done', 'finished_no_op': 'worker_done',
    'completed_no_changes': 'worker_done',
}


# ── Public API ────────────────────────────────────────────────────────────

def extract_task_block(reply_text: str) -> str:
    """Extract ```task JSON block from AI reply."""
    import re
    m = re.search(r'```(?:json)?\s*(?:task|handoff)?\s*\n?(.*?)\n?```', reply_text, re.DOTALL)
    if not m:
        m = re.search(r'```(?:json)\s*\n?(.*?)\n?```', reply_text, re.DOTALL)
    return m.group(1).strip() if m else ""


def validate_task_json(fields: dict, role: str = "manager") -> tuple:
    """Validate task JSON fields. Returns (ok: bool, errors: list)."""
    errors = []
    exit_kind = fields.get("exit_kind", "")
    if not exit_kind:
        errors.append({"field": "exit_kind", "error": "missing"})
        return False, errors
    if exit_kind not in VALID_EXIT_KINDS:
        errors.append({"field": "exit_kind", "error": f"unknown exit_kind: {exit_kind}"})
        return False, errors
    required = REQUIRED_FIELDS.get(exit_kind, [])
    for f in required:
        if not fields.get(f):
            errors.append({"field": f, "error": f"required for {exit_kind}"})
    return len(errors) == 0, errors


def normalize_fields(fields: dict) -> None:
    """Normalize field values in place."""
    exit_kind = fields.get("exit_kind", "").strip().lower()
    if exit_kind in EXIT_KIND_ALIASES:
        fields["exit_kind"] = EXIT_KIND_ALIASES[exit_kind]


def normalize_exit_kind(exit_kind: str) -> str:
    """Normalize AI natural language → canonical exit_kind."""
    ek = exit_kind.strip().lower()
    return EXIT_KIND_ALIASES.get(ek, ek)


def extract_task_json(reply_text: str) -> dict:
    """Extract and validate task JSON without DB side effects."""
    block = extract_task_block(reply_text)
    if not block:
        return {"ok": False, "errors": [{"field": "block", "error": "no JSON block found"}]}
    try:
        fields = json.loads(block)
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [{"field": "parse", "error": str(e)}]}
    normalize_fields(fields)
    return {"ok": True, "fields": fields}


# ── Legacy aliases (for backward compat during migration) ────────────────

extract_handoff_block = extract_task_block
validate_handoff_json = validate_task_json
extract_handoff_json = extract_task_json

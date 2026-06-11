#!/usr/bin/env python3
"""handoff_parser.py — Pure parsing/validation logic extracted from handoff.py.

No DB dependencies. Used by freely_db_manager.py (for handoff.parse),
and by freely bash (for handoff.extract via CLI).
"""

import json
import os
import re

# ── Constants (from handoff.py) ──────────────────────────────────────────

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

# AI natural-language → canonical exit_kind normalization
EXIT_KIND_ALIASES = {
    # ── Manager exit_kind 别名 ──
    # delegate_workers
    'delegate':              'delegate_workers',
    'delegated':             'delegate_workers',
    'dispatch':               'delegate_workers',  # 原有
    # manager_working
    'working':               'manager_working',
    'active':                 'manager_working',
    # resume_manager
    'continue':              'resume_manager',
    'resume':                 'resume_manager',
    'analyzing':              'resume_manager',
    'researching':            'resume_manager',
    # stop_ai
    'stopped':               'stop_ai',
    'paused':                'stop_ai',
    'exit':                  'stop_ai',
    'finished':              'stop_ai',
    'nothing':               'stop_ai',
    'no_work':               'stop_ai',
    'done':                  'stop_ai',
    'idle':                   'stop_ai',  # 原有

    # ── Worker exit_kind 别名 ──
    # worker_done
    'completed':              'worker_done',
    'success':                'worker_done',
    'partial':                'worker_done',
    'normal':                 'worker_done',
    'completed_no_op':        'worker_done',
    'clean_success':           'worker_done',
    'completed_with_findings': 'worker_done',
    'partial_success':        'worker_done',
    'completed_s_hint':        'worker_done',
    'completed_with_evidence': 'worker_done',
    'done':                    'worker_done',
    'completed_idle':          'worker_done',
    'completed_independent':  'worker_done',
    'complete':                'worker_done',
    'task_already_done':       'worker_done',
    'noop':                   'worker_done',
    'ok':                     'worker_done',
    'good':                   'worker_done',
    'all_done':               'worker_done',
    'finished':               'worker_done',
    'finished_no_op':         'worker_done',
    'completed_no_changes':    'worker_done',
    'no_changes_needed':      'worker_done',
    'skip':                   'worker_done',
    'skipped':                'worker_done',
    # worker_blocked
    'blocked':                'worker_blocked',
    'stuck':                  'worker_blocked',
    'cannot_proceed':         'worker_blocked',
    'waiting':                'worker_blocked',
    'waiting_on':             'worker_blocked',
    # worker_handoff_needed
    'awaiting_review':       'worker_handoff_needed',
    'needs_research':         'worker_handoff_needed',
    'transition':             'worker_handoff_needed',
    'needs_input':            'worker_handoff_needed',
    'requires_manager':       'worker_handoff_needed',
    'waiting_input':          'worker_handoff_needed',
    'needs_approval':         'worker_handoff_needed',
}

# AI field name aliases → canonical names
FIELD_ALIASES = {
    'summary': 'completion_summary',
    'artifacts': 'evidence_paths',
    'next_worker_suggestion': 'next_action',
}


# ── Parsing functions (from handoff.py) ──────────────────────────────────

def _strip_json_comments(text: str) -> str:
    """Strip // line comments from JSON/JSON5 text so json.loads can parse it."""
    result = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape:
            result.append(ch)
            escape = False
            i += 1
            continue
        if ch == '\\' and in_string:
            result.append(ch)
            escape = True
            i += 1
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            i += 1
            continue
        if not in_string and ch == '/' and i + 1 < len(text) and text[i + 1] == '/':
            i += 2
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
        result.append(ch)
        i += 1
    return ''.join(result)


def extract_handoff_block(text: str) -> str | None:
    """Extract the first handoff fenced block from AI reply text.

    Fence priority: ```json5 (canonical), ```json (compat), ```handoff (legacy).
    Returns the raw JSON text, or None if no block found.
    """
    # Strip ACP event lines that may be interleaved with the AI reply
    cleaned = re.sub(r'^\[ACP [^\n]*\n', '', text, flags=re.MULTILINE)
    cleaned = re.sub(r'\n\[(ACP|CACHE|TIMING)[^\n]*', '', cleaned)

    m = None
    # Try ```json5 (canonical) and ```json (compat), in order
    for fence in ('json5', 'json'):
        for json_m in re.finditer(rf'```{fence}\s*\n(\{{.*?\}})\n\s*```', cleaned, re.DOTALL):
            try:
                raw_block = json_m.group(1)
                candidate = json.loads(_strip_json_comments(raw_block))
                if 'exit_kind' in candidate:
                    m = json_m
                    break
            except Exception:
                continue
        if m:
            break

    # Fallback: ```handoff fence (legacy)
    if not m:
        m = re.search(r'```handoff\s*\n(.*?)\n\s*```', cleaned, re.DOTALL)
        if not m:
            m = re.search(r'```handoff\s*\n(.*)', cleaned, re.DOTALL)
    if not m:
        return None
    raw = m.group(1).strip()
    # Extract JSON object boundaries if raw contains extra trailing text
    brace_start = raw.find('{')
    brace_end = raw.rfind('}')
    if brace_start >= 0 and brace_end > brace_start:
        raw = raw[brace_start:brace_end + 1]
    return _strip_json_comments(raw).strip()


def normalize_fields(ai_fields: dict) -> dict:
    """Normalize AI field name aliases to canonical names. Mutates and returns."""
    for alias, canonical in FIELD_ALIASES.items():
        val = ai_fields.get(alias)
        if val is not None and val != '' and val != [] and not ai_fields.get(canonical):
            ai_fields[canonical] = ai_fields.pop(alias)
    return ai_fields


def normalize_exit_kind(ai_fields: dict, role: str = "") -> dict:
    """Normalize natural-language exit_kind to canonical values. Mutates and returns.

    Args:
        ai_fields: The handoff fields dict (will be modified in place)
        role: The agent role ("manager" or "worker"), used to resolve ambiguous aliases.
              If empty, defaults to manager semantics for ambiguous aliases.
    """
    exit_kind = ai_fields.get('exit_kind', '')

    # ── Handle ambiguous aliases with context awareness ──────────────────────
    AMBIGUOUS_ALIASES = {'finished', 'done', 'no_changes_needed'}
    if exit_kind in AMBIGUOUS_ALIASES:
        if role == 'worker':
            # Workers use 'finished'/'done' to indicate completion
            ai_fields['exit_kind'] = 'worker_done'
        else:
            # Managers use 'finished'/'done' to indicate stop/idle
            ai_fields['exit_kind'] = 'stop_ai'
        return ai_fields

    # ── Handle unambiguous aliases ─────────────────────────────────────────
    if exit_kind in EXIT_KIND_ALIASES:
        ai_fields['exit_kind'] = EXIT_KIND_ALIASES[exit_kind]
    return ai_fields


def validate_handoff_json(ai_fields: dict, role: str = "") -> tuple[bool, list[dict]]:
    """Validate AI-produced handoff JSON. Returns (ok, errors).

    Normalizes natural-language exit_kind to canonical values first.
    """
    errors = []
    exit_kind = ai_fields.get('exit_kind', '')
    normalize_exit_kind(ai_fields, role=role)
    exit_kind = ai_fields.get('exit_kind', '')

    if exit_kind not in VALID_EXIT_KINDS:
        errors.append({"field": "exit_kind", "error": f"invalid value '{exit_kind}'"})
        return False, errors

    for field in REQUIRED_FIELDS.get(exit_kind, []):
        val = ai_fields.get(field, '')
        if not val or val == '':
            # Fallback: AI often writes 'summary'/'completion_summary' for blocked/needed exits
            if field == 'reason' and exit_kind in ('worker_blocked', 'worker_handoff_needed'):
                fallback = ai_fields.get('completion_summary', '')
                if fallback and fallback != '':
                    ai_fields['reason'] = fallback
                    continue
            if field == 'next_action' and exit_kind in ('worker_blocked', 'worker_handoff_needed'):
                reason_text = ai_fields.get('reason', '')
                if reason_text and reason_text != '':
                    ai_fields['next_action'] = 'see reason'
                    continue
            errors.append({"field": field, "error": f"required for {exit_kind}, got '{val}'"})

    # Delegate: verify worker_prompts_csv paths exist
    if exit_kind == 'delegate_workers' and not errors:
        csv_val = ai_fields.get('worker_prompts_csv', '')
        for p in csv_val.split(','):
            p = p.strip()
            if not p or not os.path.isfile(p):
                errors.append({"field": "worker_prompts_csv", "error": f"path not found: '{p}'"})

    return len(errors) == 0, errors


def extract_handoff_json(reply_text: str) -> dict:
    """Extract and validate handoff JSON from reply text WITHOUT any DB side effects.

    Returns {"ok": true, "exit_kind": "...", "fields": {...}}
    or     {"ok": false, "errors": [...]}
    """
    block = extract_handoff_block(reply_text)
    if not block:
        return {"ok": False, "errors": [{"field": "handoff_block", "error": "no handoff block found"}]}
    try:
        ai_fields = json.loads(block)
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [{"field": "parse", "error": str(e)}]}
    normalize_fields(ai_fields)
    ok, errors = validate_handoff_json(ai_fields)
    if not ok:
        return {"ok": False, "errors": errors}
    return {"ok": True, "exit_kind": ai_fields.get('exit_kind', ''), "fields": ai_fields}

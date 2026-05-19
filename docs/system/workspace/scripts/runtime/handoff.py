#!/usr/bin/env python3
"""handoff.py: SQLite CRUD for manager-worker handoff state.

One table (handoffs), role field (manager|worker).
AI outputs ```handoff JSON → Runtime parses → writes DB → dispatches consume_*.
"""

import argparse
import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone


DB_PATH = None

# All 6 legal exit_kind values
VALID_EXIT_KINDS = {
    'delegate_workers', 'resume_manager', 'stop_ai',
    'worker_done', 'worker_blocked', 'worker_handoff_needed',
}

# Fields required per exit_kind (empty = not required)
REQUIRED_FIELDS = {
    'delegate_workers':       ['reason', 'worker_prompts_csv'],
    'resume_manager':         ['reason', 'restart_point', 'next_action'],
    'stop_ai':                ['reason'],
    'worker_done':            ['completion_summary'],
    'worker_blocked':         ['reason', 'next_action'],
    'worker_handoff_needed':  ['reason', 'next_action'],
}


def _now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=OFF")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.executescript("""
        DROP TABLE IF EXISTS worker_delegation;
        CREATE TABLE IF NOT EXISTS handoffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handoff_id TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('manager','worker')),
            raw_key TEXT NOT NULL,
            worktree TEXT DEFAULT '',
            branch TEXT DEFAULT '',
            prompt_file TEXT NOT NULL,
            parent_handoff_id TEXT DEFAULT '',
            previous_worker_handoff_id TEXT DEFAULT '',
            intent_kind TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK(status IN ('pending','launched','completed','rejected','blocked','consumed')),
            exit_kind TEXT DEFAULT '',
            reason TEXT DEFAULT '',
            restart_point TEXT DEFAULT '',
            next_action TEXT DEFAULT '',
            completion_summary TEXT DEFAULT '',
            evidence_paths TEXT DEFAULT '',
            worker_prompts_csv TEXT DEFAULT '',
            repair_target_role TEXT DEFAULT '',
            repair_target_handoff_id TEXT DEFAULT '',
            validation_errors_json TEXT DEFAULT '[]',
            session_id TEXT DEFAULT '',
            created_by TEXT DEFAULT '',
            consumed_by TEXT DEFAULT '',
            launched_at TEXT DEFAULT '',
            last_activity_at TEXT DEFAULT '',
            completed_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_handoffs_role_status ON handoffs(role, status);
        CREATE INDEX IF NOT EXISTS idx_handoffs_raw_key ON handoffs(raw_key);
        CREATE INDEX IF NOT EXISTS idx_handoffs_worktree ON handoffs(worktree);
        CREATE INDEX IF NOT EXISTS idx_handoffs_parent ON handoffs(parent_handoff_id);
        CREATE INDEX IF NOT EXISTS idx_handoffs_prev_worker ON handoffs(previous_worker_handoff_id);
        CREATE INDEX IF NOT EXISTS idx_handoffs_worktree_status ON handoffs(worktree, status);
        DELETE FROM handoffs WHERE status = 'pending' AND datetime(created_at) < datetime('now','-1 hour');
    """)
    # ── Schema migration: add columns missing in older DBs ──
    existing = {row[1] for row in conn.execute("PRAGMA table_info(handoffs)")}
    for col_name, col_def in [
        ("previous_worker_handoff_id", "TEXT DEFAULT ''"),
        ("last_activity_at", "TEXT DEFAULT ''"),
        ("repair_target_role", "TEXT DEFAULT ''"),
        ("repair_target_handoff_id", "TEXT DEFAULT ''"),
        ("validation_errors_json", "TEXT DEFAULT '[]'"),
        ("reason", "TEXT DEFAULT ''"),
    ]:
        if col_name not in existing:
            try:
                conn.execute(f"ALTER TABLE handoffs ADD COLUMN {col_name} {col_def}")
            except Exception:
                pass
    # Consolidate deprecated reason columns into unified reason
    if "blocked_reason" in existing and "reason" in existing:
        try:
            conn.execute(
                "UPDATE handoffs SET reason = blocked_reason "
                "WHERE reason = '' AND blocked_reason != ''")
        except Exception:
            pass
    if "handoff_reason" in existing and "reason" in existing:
        try:
            conn.execute(
                "UPDATE handoffs SET reason = handoff_reason "
                "WHERE reason = '' AND handoff_reason != ''")
        except Exception:
            pass
    conn.commit()
    conn.close()


# ── CRUD ──────────────────────────────────────────────────────────

def insert(role, raw_key, prompt_file, worktree="", branch="",
           parent_handoff_id="", previous_worker_handoff_id="",
           intent_kind="", created_by="", consumed_by="",
           exit_kind="", reason="", restart_point="", next_action="",
           completion_summary="", evidence_paths="",
           worker_prompts_csv=""):
    conn = _connect()
    hid = (_now_utc().replace("T", "").replace("Z", "").replace("-", "").replace(":", "")
           + "-" + uuid.uuid4().hex[:6])
    now = _now_utc()
    conn.execute(
        """INSERT INTO handoffs (handoff_id, role, raw_key, worktree, branch,
           prompt_file, parent_handoff_id, previous_worker_handoff_id,
           intent_kind, created_by, consumed_by,
           exit_kind, reason, restart_point, next_action,
           completion_summary, evidence_paths, worker_prompts_csv,
           status, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',?,?)""",
        (hid, role, raw_key, worktree, branch, prompt_file,
         parent_handoff_id, previous_worker_handoff_id,
         intent_kind, created_by, consumed_by, exit_kind,
         reason, restart_point, next_action,
         completion_summary, evidence_paths, worker_prompts_csv,
         now, now))
    conn.commit()
    conn.close()
    return hid


def _validate_terminal_fields(status, exit_kind, reason, consumed_by):
    """Validate mandatory fields for each terminal state transition.

    pending → launched:           no mandatory fields
    launched → completed:         exit_kind ✓
    launched → rejected:          exit_kind ✓  reason ✓
    launched → blocked:           exit_kind ✓  reason ✓
    completed/rejected/blocked → consumed:  consumed_by ✓
    """
    if status in ("rejected", "blocked") and not reason:
        return "{} handoff requires --reason (why?). e.g. 'develop rejected: only cleanup allowed' or 'stale_pid: worker died'".format(status)
    if status in ("rejected", "blocked", "completed") and not exit_kind:
        return "terminal status '{}' requires --exit-kind. e.g. launch_failed, stale_pid, completed".format(status)
    if status == "consumed" and not consumed_by:
        return "consumed handoff requires --consumed-by (who consumed?). e.g. 'manager'"
    return None


def update_status(handoff_id, status, expected_status, exit_kind="",
                  session_id="", reason="", restart_point="", next_action="",
                  completion_summary="", evidence_paths="",
                  worker_prompts_csv="", consumed_by=""):
    """Update status with mandatory optimistic locking.
    UPDATE always uses WHERE status=expected_status."""
    err = _validate_terminal_fields(status, exit_kind, reason, consumed_by)
    if err:
        sys.stderr.write("[handoff] VALIDATION ERROR: {}\n".format(err))
        sys.stderr.write("[handoff] handoff_id={} status={}\n".format(handoff_id, status))
    conn = _connect()
    now = _now_utc()
    cols = ["status=?", "updated_at=?"]
    params = [status, now]

    if status == "launched":
        cols.append("launched_at=?")
        params.append(now)
        cols.append("last_activity_at=?")
        params.append(now)
    if status in ("completed", "rejected", "blocked", "consumed"):
        cols.append("completed_at=?")
        params.append(now)

    # Track last activity
    if status not in ("pending",):
        cols.append("last_activity_at=?")
        params.append(now)

    for field, val in [("exit_kind", exit_kind), ("session_id", session_id),
                        ("reason", reason), ("restart_point", restart_point),
                        ("next_action", next_action),
                        ("completion_summary", completion_summary),
                        ("evidence_paths", evidence_paths),
                        ("worker_prompts_csv", worker_prompts_csv)]:
        if val:
            cols.append(f"{field}=?")
            params.append(val)

    where = "handoff_id=? AND status=?"
    params.append(handoff_id)
    params.append(expected_status)

    sql = f"UPDATE handoffs SET {', '.join(cols)} WHERE {where}"
    cur = conn.execute(sql, params)
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected


def update_last_activity(handoff_id):
    conn = _connect()
    now = _now_utc()
    conn.execute(
        "UPDATE handoffs SET last_activity_at=?, updated_at=? WHERE handoff_id=? AND status='launched'",
        (now, now, handoff_id))
    conn.commit()
    conn.close()


def get(handoff_id):
    conn = _connect()
    row = conn.execute("SELECT * FROM handoffs WHERE handoff_id=?", (handoff_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_by_role(role, status=None, limit=50):
    conn = _connect()
    if status:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE role=? AND status=? ORDER BY created_at DESC LIMIT ?",
            (role, status, limit)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE role=? ORDER BY created_at DESC LIMIT ?",
            (role, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_by_raw_key(raw_key, role=None):
    conn = _connect()
    if role:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE raw_key=? AND role=? ORDER BY created_at DESC",
            (raw_key, role)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE raw_key=? ORDER BY created_at DESC",
            (raw_key,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_by_raw_key_and_status(raw_key, statuses):
    """For scan filtering: find active workers by raw_key."""
    conn = _connect()
    placeholders = ','.join('?' * len(statuses))
    rows = conn.execute(
        f"SELECT * FROM handoffs WHERE raw_key=? AND role='worker' AND status IN ({placeholders})",
        [raw_key] + list(statuses)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def active_workers_for_worktree(worktree):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM handoffs WHERE worktree=? AND role='worker' AND status='launched'",
        (worktree,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def has_active_worker_for_worktree(worktree):
    """For scan filtering: check if worktree has launched worker."""
    conn = _connect()
    row = conn.execute(
        "SELECT 1 FROM handoffs WHERE worktree=? AND role='worker' AND status='launched' LIMIT 1",
        (worktree,)).fetchone()
    conn.close()
    return row is not None


def latest_manager():
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM handoffs WHERE role='manager' ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def children_of(parent_handoff_id):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM handoffs WHERE parent_handoff_id=? AND role='worker' ORDER BY created_at",
        (parent_handoff_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def latest_completed_worker(raw_key):
    """For previous_worker_handoff_id computation."""
    conn = _connect()
    row = conn.execute(
        "SELECT handoff_id, completion_summary, evidence_paths FROM handoffs "
        "WHERE raw_key=? AND role='worker' AND status='completed' "
        "ORDER BY created_at DESC LIMIT 1",
        (raw_key,)).fetchone()
    conn.close()
    return dict(row) if row else None


def mark_stale(inactivity_minutes=15):
    """Mark launched workers as blocked if last_activity_at exceeds threshold.
    Uses wall-clock INACTIVITY, not total runtime. Slow-but-active workers are safe."""
    conn = _connect()
    now = _now_utc()
    now_dt = datetime.now(timezone.utc)
    from datetime import timedelta
    cutoff = (now_dt - timedelta(minutes=inactivity_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute(
        "UPDATE handoffs SET status='blocked', exit_kind='worker_blocked',"
        " reason='Worker inactive > ' || ? || 'min (last_activity=' || last_activity_at || ')',"
        " next_action='Manager: check worker liveness. If worker is dead, re-dispatch or close.',"
        " updated_at=?, completed_at=? "
        "WHERE role='worker' AND status='launched' AND last_activity_at < ?",
        (str(inactivity_minutes), now, now, cutoff))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected


def auto_consume(raw_key):
    """Consume all unconsumed terminal workers for a raw_key.
    Called when manager creates a new handoff."""
    conn = _connect()
    now = _now_utc()
    cur = conn.execute(
        "UPDATE handoffs SET status='consumed', updated_at=?, completed_at=? "
        "WHERE raw_key=? AND role='worker' "
        "AND status IN ('completed','blocked','rejected')",
        (now, now, raw_key))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected


# ── JSON parse & dispatch ─────────────────────────────────────────

def extract_handoff_block(text):
    """Extract the first handoff fenced block from AI reply text.
    Fence is ```json (canonical); ```handoff accepted as legacy fallback."""
    # Strip ACP event lines that may be interleaved with the AI reply
    cleaned = re.sub(r'^\[ACP [^\n]*\n', '', text, flags=re.MULTILINE)
    # Strip trailing ACP/CACHE/TIMING metadata lines
    cleaned = re.sub(r'\n\[(ACP|CACHE|TIMING)[^\n]*', '', cleaned)
    # Try ```json fence (canonical) — AI writes json format with handoff content
    for json_m in re.finditer(r'```json\s*\n(\{.*?\})\n\s*```', cleaned, re.DOTALL):
        try:
            candidate = json.loads(json_m.group(1))
            if 'exit_kind' in candidate:
                m = json_m
                break
        except Exception:
            continue
    else:
        m = None
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
    return raw.strip()


def validate_handoff_json(ai_fields):
    """Validate AI-produced handoff JSON. Returns (ok, errors)."""
    errors = []
    exit_kind = ai_fields.get('exit_kind', '')
    # Natural-language alias: "completed" maps to worker_done
    ALIAS_MAP = {'completed': 'worker_done'}
    if exit_kind in ALIAS_MAP:
        ai_fields['exit_kind'] = ALIAS_MAP[exit_kind]
        exit_kind = ALIAS_MAP[exit_kind]
    if exit_kind not in VALID_EXIT_KINDS:
        errors.append({"field": "exit_kind", "error": f"invalid value '{exit_kind}'"})
        return False, errors

    for field in REQUIRED_FIELDS.get(exit_kind, []):
        val = ai_fields.get(field, '')
        if not val or val == '':
            errors.append({"field": field, "error": f"required for {exit_kind}, got '{val}'"})

    # Delegate: verify worker_prompts_csv paths exist
    if exit_kind == 'delegate_workers' and not errors:
        csv_val = ai_fields.get('worker_prompts_csv', '')
        for p in csv_val.split(','):
            p = p.strip()
            if not p or not os.path.isfile(p):
                errors.append({"field": "worker_prompts_csv", "error": f"path not found: '{p}'"})

    return len(errors) == 0, errors


def parse_handoff_json(reply_text, context):
    """Parse ```handoff JSON from AI reply, validate, merge Runtime fields,
    insert into DB, and return (record, consume_action)."""
    block = extract_handoff_block(reply_text)
    if not block:
        return None, "repair", [{"field": "handoff_block", "error": "no ```handoff block found"}]

    try:
        ai_fields = json.loads(block)
    except json.JSONDecodeError as e:
        return None, "repair", [{"field": "parse", "error": str(e)}]

    # Normalize common AI field name variants to protocol names
    FIELD_ALIASES = {
        'summary': 'completion_summary',
        'artifacts': 'evidence_paths',
        'next_worker_suggestion': 'next_action',
    }
    for alias, canonical in FIELD_ALIASES.items():
        val = ai_fields.get(alias)
        if val is not None and val != '' and val != [] and not ai_fields.get(canonical):
            ai_fields[canonical] = ai_fields.pop(alias)

    ok, errors = validate_handoff_json(ai_fields)
    if not ok:
        return None, "repair", errors

    # Build full record: Runtime fields + AI fields
    now = _now_utc()
    hid = (_now_utc().replace("T", "").replace("Z", "").replace("-", "").replace(":", "")
           + "-" + uuid.uuid4().hex[:6])

    record = {
        "handoff_id": hid,
        "role": context.get("role", "manager"),
        "raw_key": context.get("raw_key", ""),
        "worktree": context.get("worktree", ""),
        "branch": context.get("branch", ""),
        "prompt_file": context.get("prompt_file", ""),
        "parent_handoff_id": context.get("parent_handoff_id", ""),
        "previous_worker_handoff_id": context.get("previous_worker_handoff_id", ""),
        "intent_kind": context.get("intent_kind", ""),
        "status": "pending",
        "session_id": context.get("session_id", ""),
        "created_by": "runtime",
        "consumed_by": "",
        "launched_at": "",
        "last_activity_at": "",
        "completed_at": "",
        "created_at": now,
        "updated_at": now,
        **{k: v for k, v in ai_fields.items() if v != ''},
    }

    # Fill defaults for AI fields not present
    for f in ('exit_kind', 'reason', 'restart_point', 'next_action',
              'completion_summary', 'evidence_paths', 'worker_prompts_csv'):
        if f not in record:
            record[f] = ''

    # Insert
    conn = _connect()
    conn.execute(
        """INSERT INTO handoffs (handoff_id, role, raw_key, worktree, branch,
           prompt_file, parent_handoff_id, previous_worker_handoff_id,
           intent_kind, status, exit_kind, reason, restart_point, next_action,
           completion_summary, evidence_paths, worker_prompts_csv,
           session_id, created_by, consumed_by,
           launched_at, last_activity_at, completed_at, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (record["handoff_id"], record["role"], record["raw_key"],
         record["worktree"], record["branch"], record["prompt_file"],
         record["parent_handoff_id"], record["previous_worker_handoff_id"],
         record["intent_kind"], record["status"],
         record["exit_kind"], record["reason"],
         record["restart_point"], record["next_action"],
         record["completion_summary"], record["evidence_paths"],
         record["worker_prompts_csv"],
         record["session_id"], record["created_by"], record["consumed_by"],
         record["launched_at"], record["last_activity_at"],
         record["completed_at"], record["created_at"], record["updated_at"]))
    conn.commit()
    # Manager records auto-complete (patrol ended when JSON was output)
    if record["role"] == "manager":
        now = _now_utc()
        conn.execute(
            "UPDATE handoffs SET status='completed', completed_at=?, updated_at=? WHERE handoff_id=?",
            (now, now, record["handoff_id"]))
        conn.commit()
        record["status"] = "completed"
    conn.close()

    return record, record["exit_kind"], []


def insert_repair_handoff(repair_target_role, repair_target_handoff_id, validation_errors, raw_key):
    """Insert a structured repair handoff for Manager to consume.
    Stores repair_target_role, repair_target_handoff_id, validation_errors_json as structured columns,
    not buried in natural-language text. Manager reads the columns directly."""
    conn = _connect()
    hid = (_now_utc().replace("T", "").replace("Z", "").replace("-", "").replace(":", "")
           + "-" + uuid.uuid4().hex[:6])
    now = _now_utc()
    errors_json = json.dumps(validation_errors, ensure_ascii=False)
    reason = f"Agent [{repair_target_role}] 输出无效 handoff JSON。"
    next_action = f"检查 {repair_target_role} 的 prompt 和 JSON 格式。验证错误见 validation_errors_json 字段。"
    conn.execute(
        """INSERT INTO handoffs (handoff_id, role, raw_key, prompt_file,
           parent_handoff_id, status, exit_kind, restart_point, reason, next_action,
           repair_target_role, repair_target_handoff_id, validation_errors_json,
           created_by, created_at, updated_at)
           VALUES (?,?,'repair','',?,'pending','resume_manager','recovery',?,?,
           ?,?,?,'runtime',?,?)""",
        (hid, "manager", repair_target_handoff_id, reason, next_action,
         repair_target_role, repair_target_handoff_id, errors_json, now, now))
    conn.commit()
    conn.close()
    return hid


# ── CLI ────────────────────────────────────────────────────────────

def main():
    global DB_PATH
    parser = argparse.ArgumentParser(description="handoff.py — manager-worker handoff SQLite store")
    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init")
    p_init.add_argument("--db", required=True)

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--db", required=True)
    p_insert.add_argument("--role", required=True, choices=["manager", "worker"])
    p_insert.add_argument("--raw-key", required=True)
    p_insert.add_argument("--prompt-file", required=True)
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
    p_insert.add_argument("--parent", default="")
    p_insert.add_argument("--prev-worker", default="")
    p_insert.add_argument("--intent-kind", default="")
    p_insert.add_argument("--created-by", default="")
    p_insert.add_argument("--consumed-by", default="")
    p_insert.add_argument("--exit-kind", default="")
    p_insert.add_argument("--reason", default="")
    p_insert.add_argument("--restart-point", default="")
    p_insert.add_argument("--next-action", default="")
    p_insert.add_argument("--completion-summary", default="")
    p_insert.add_argument("--evidence-paths", default="")
    p_insert.add_argument("--worker-prompts-csv", default="")

    p_update = sub.add_parser("update")
    p_update.add_argument("--db", required=True)
    p_update.add_argument("--handoff-id", required=True)
    p_update.add_argument("--status", required=True)
    p_update.add_argument("--expected-status", default="")
    p_update.add_argument("--exit-kind", default="")
    p_update.add_argument("--session-id", default="")
    p_update.add_argument("--reason", default="")
    p_update.add_argument("--restart-point", default="")
    p_update.add_argument("--next-action", default="")
    p_update.add_argument("--completion-summary", default="")
    p_update.add_argument("--evidence-paths", default="")
    p_update.add_argument("--worker-prompts-csv", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("--db", required=True)
    p_get.add_argument("--handoff-id", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--db", required=True)
    p_list.add_argument("--role", default="worker")
    p_list.add_argument("--status", default="")

    p_list_key = sub.add_parser("list-key")
    p_list_key.add_argument("--db", required=True)
    p_list_key.add_argument("--raw-key", required=True)

    p_active = sub.add_parser("active-workers")
    p_active.add_argument("--db", required=True)
    p_active.add_argument("--worktree", required=True)

    p_has_active = sub.add_parser("has-active-worker")
    p_has_active.add_argument("--db", required=True)
    p_has_active.add_argument("--worktree", required=True)

    p_latest = sub.add_parser("latest-manager")
    p_latest.add_argument("--db", required=True)

    p_prev = sub.add_parser("latest-completed-worker")
    p_prev.add_argument("--db", required=True)
    p_prev.add_argument("--raw-key", required=True)

    p_stale = sub.add_parser("mark-stale")
    p_stale.add_argument("--db", required=True)
    p_stale.add_argument("--inactivity-minutes", type=int, default=15)

    p_auto_consume = sub.add_parser("auto-consume")
    p_auto_consume.add_argument("--db", required=True)
    p_auto_consume.add_argument("--raw-key", required=True)

    p_last_activity = sub.add_parser("update-last-activity")
    p_last_activity.add_argument("--db", required=True)
    p_last_activity.add_argument("--handoff-id", required=True)

    p_parse = sub.add_parser("parse")
    p_parse.add_argument("--db", required=True)
    p_parse.add_argument("--reply-text", required=True)
    p_parse.add_argument("--role", default="manager")
    p_parse.add_argument("--raw-key", default="")
    p_parse.add_argument("--prompt-file", default="")

    args = parser.parse_args()
    DB_PATH = args.db

    if args.cmd == "init":
        init_db()
        print("ok")
    elif args.cmd == "insert":
        hid = insert(args.role, args.raw_key, args.prompt_file,
                     args.worktree, args.branch, args.parent, args.prev_worker,
                     args.intent_kind, args.created_by, args.consumed_by,
                     args.exit_kind, args.reason, args.restart_point,
                     args.next_action, args.completion_summary,
                     args.evidence_paths, args.worker_prompts_csv)
        print(hid)
    elif args.cmd == "update":
        affected = update_status(
            args.handoff_id, args.status, args.expected_status or None,
            args.exit_kind, args.session_id, args.reason, args.restart_point,
            args.next_action, args.completion_summary, args.evidence_paths,
            args.worker_prompts_csv)
        print(f"ok affected={affected}")
    elif args.cmd == "get":
        r = get(args.handoff_id)
        print(json.dumps(r, indent=2, ensure_ascii=False) if r else "null")
    elif args.cmd == "list":
        rows = list_by_role(args.role, args.status or None)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.cmd == "list-key":
        rows = list_by_raw_key(args.raw_key)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.cmd == "active-workers":
        rows = active_workers_for_worktree(args.worktree)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.cmd == "has-active-worker":
        print("true" if has_active_worker_for_worktree(args.worktree) else "false")
    elif args.cmd == "latest-completed-worker":
        r = latest_completed_worker(args.raw_key)
        print(json.dumps(r, indent=2, ensure_ascii=False) if r else "null")
    elif args.cmd == "latest-manager":
        r = latest_manager()
        print(json.dumps(r, indent=2, ensure_ascii=False) if r else "null")
    elif args.cmd == "mark-stale":
        affected = mark_stale(args.inactivity_minutes)
        print(f"ok affected={affected}")
    elif args.cmd == "auto-consume":
        affected = auto_consume(args.raw_key)
        print(f"ok affected={affected}")
    elif args.cmd == "update-last-activity":
        update_last_activity(args.handoff_id)
        print("ok")
    elif args.cmd == "parse":
        context = {
            "role": args.role,
            "raw_key": args.raw_key,
            "prompt_file": args.prompt_file,
            "worktree": "", "branch": "", "parent_handoff_id": "",
            "previous_worker_handoff_id": "", "intent_kind": "", "session_id": "",
        }
        record, action, errors = parse_handoff_json(args.reply_text, context)
        if action == "repair":
            print(json.dumps({"action": "repair", "errors": errors}, ensure_ascii=False))
        else:
            print(json.dumps({"action": action, "handoff_id": record["handoff_id"]},
                             ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

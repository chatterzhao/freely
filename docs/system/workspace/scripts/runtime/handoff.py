#!/usr/bin/env python3
"""handoff.py: Manager-worker handoff state — DB ops via freely-db daemon.

One table (handoffs), role field (manager|worker).
AI outputs ```handoff JSON → Runtime parses → writes DB via daemon → dispatches.

All SQLite access goes through freely_db_manager daemon (Unix socket JSON-RPC).
Parse/validate logic imported from handoff_parser.
"""

import argparse
import hashlib
import json
import os
import socket
import sys
import uuid
from datetime import datetime, timezone

# ── Daemon socket RPC ────────────────────────────────────────────────────

PROJECT = None  # set by _resolve_project()


def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.sock"


def _resolve_project() -> str:
    """Derive project path from DB_PATH or current directory."""
    if DB_PATH and os.path.exists(DB_PATH):
        # DB_PATH is .freely/freely.db, project is two levels up
        db_dir = os.path.dirname(os.path.abspath(DB_PATH))
        return os.path.dirname(db_dir)
    return os.getcwd()


def _db_rpc(method: str, params: dict, timeout: float = 30.0) -> dict:
    """Send JSON-RPC to freely-db daemon, return result dict. Raises on error."""
    project = PROJECT or _resolve_project()
    socket_path = _socket_path(project)
    if not os.path.exists(socket_path):
        # Fallback: try starting daemon
        import subprocess
        daemon_py = os.path.join(os.path.dirname(__file__), "freely_db_manager.py")
        subprocess.run([sys.executable, daemon_py, "start", "--project", project, "--foreground"],
                       capture_output=True, timeout=10)
        for _ in range(50):
            if os.path.exists(socket_path):
                break
            import time
            time.sleep(0.1)

    request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(socket_path)
        sock.sendall((json.dumps(request, default=str) + "\n").encode())
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    finally:
        sock.close()

    response = json.loads(data.decode())
    if "error" in response:
        raise RuntimeError(response["error"].get("message", str(response["error"])))
    return response.get("result", {})


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Init (schema managed by daemon, this is a no-op for compat) ──────────

def init_db():
    """Ensure tables exist. Daemon auto-creates on first start."""
    try:
        _db_rpc("db.ping", {})
    except Exception:
        pass  # daemon will create tables on next start


# ── Public API (CLI-compatible) ──────────────────────────────────────────

def insert_handoff(
    role: str = "manager", raw_key: str = "", prompt_file: str = "",
    worktree: str = "", branch: str = "",
    parent: str = "", prev_worker: str = "", intent_kind: str = "",
    status: str = "pending", exit_kind: str = "", reason: str = "",
    restart_point: str = "", next_action: str = "",
    completion_summary: str = "", evidence_paths: str = "",
    worker_prompts_csv: str = "",
    session_id: str = "", created_by: str = "", consumed_by: str = "",
) -> str:
    result = _db_rpc("handoff.insert", {
        "role": role, "raw_key": raw_key, "prompt_file": prompt_file,
        "worktree": worktree, "branch": branch,
        "parent": parent, "prev_worker": prev_worker, "intent_kind": intent_kind,
        "status": status, "exit_kind": exit_kind, "reason": reason,
        "restart_point": restart_point, "next_action": next_action,
        "completion_summary": completion_summary, "evidence_paths": evidence_paths,
        "worker_prompts_csv": worker_prompts_csv,
        "session_id": session_id, "created_by": created_by, "consumed_by": consumed_by,
    })
    return result.get("handoff_id", "")


def update_status(handoff_id: str, status: str, expected_status: str = "",
                  exit_kind: str = "", session_id: str = "", reason: str = "",
                  restart_point: str = "", next_action: str = "",
                  completion_summary: str = "", evidence_paths: str = "",
                  worker_prompts_csv: str = "") -> int:
    params = {"handoff_id": handoff_id, "status": status}
    if exit_kind: params["exit_kind"] = exit_kind
    if session_id: params["session_id"] = session_id
    if reason: params["reason"] = reason
    if restart_point: params["restart_point"] = restart_point
    if next_action: params["next_action"] = next_action
    if completion_summary: params["completion_summary"] = completion_summary
    if evidence_paths: params["evidence_paths"] = evidence_paths
    if worker_prompts_csv: params["worker_prompts_csv"] = worker_prompts_csv
    result = _db_rpc("handoff.update", params)
    return result.get("affected", 0)


def update_last_activity(handoff_id: str) -> None:
    _db_rpc("handoff.update-last-activity", {"handoff_id": handoff_id})


def update_send_to_ai(handoff_id: str, send_to_ai_val: str) -> int:
    result = _db_rpc("handoff.update-send-to-ai",
                     {"handoff_id": handoff_id, "send_to_ai": send_to_ai_val})
    return result.get("affected", 0)


def update_worker_pid(handoff_id: str, worker_pid: str) -> int:
    result = _db_rpc("handoff.update-worker-pid",
                     {"handoff_id": handoff_id, "worker_pid": worker_pid})
    return result.get("affected", 0)


def get_handoff(handoff_id: str) -> dict | None:
    result = _db_rpc("handoff.get", {"handoff_id": handoff_id})
    return result.get("record")


def list_by_role(role: str = "worker", status: str | None = None) -> list[dict]:
    params = {"role": role}
    if status: params["status"] = status
    result = _db_rpc("handoff.list", params)
    return result.get("rows", [])


def list_by_key(raw_key: str, statuses: list[str] | None = None) -> list[dict]:
    result = _db_rpc("handoff.list-by-key", {"raw_key": raw_key})
    rows = result.get("rows", [])
    if statuses:
        rows = [r for r in rows if r.get("status") in statuses]
    return rows


def query_active_workers(worktree: str) -> list[dict]:
    result = _db_rpc("handoff.active-workers", {"worktree": worktree})
    return result.get("rows", [])


def has_active_worker(worktree: str) -> bool:
    result = _db_rpc("handoff.has-active-worker", {"worktree": worktree})
    return result.get("has_active", False)


def latest_manager() -> dict | None:
    result = _db_rpc("handoff.latest-manager", {})
    return result.get("record")


def latest_completed_worker(raw_key: str = "") -> dict | None:
    result = _db_rpc("handoff.latest-completed-worker", {"raw_key": raw_key})
    return result.get("record")


def mark_stale(inactivity_minutes: int = 15) -> int:
    result = _db_rpc("handoff.mark-stale", {"inactivity_minutes": inactivity_minutes})
    return result.get("affected", 0)


def auto_consume(raw_key: str, consumed_by: str = "manager") -> int:
    result = _db_rpc("handoff.auto-consume",
                     {"raw_key": raw_key, "consumed_by": consumed_by})
    return result.get("affected", 0)


def query_pending_delivery(consumed_by: str = "") -> list[dict]:
    result = _db_rpc("handoff.list-pending-delivery", {"consumed_by": consumed_by})
    return result.get("rows", [])


def get_launched_pids(raw_key: str = "") -> list[dict]:
    result = _db_rpc("handoff.get-launched-pids", {"raw_key": raw_key})
    return result.get("rows", [])


# ── Parse / Extract (delegates to handoff_parser) ────────────────────────

def parse_handoff_json(reply_text: str, context: dict):
    """Parse ```handoff JSON from AI reply, validate, insert via daemon."""
    from handoff_parser import extract_handoff_block, validate_handoff_json, normalize_fields
    block = extract_handoff_block(reply_text)
    if not block:
        return None, "repair", [{"field": "handoff_block", "error": "no ```handoff block found"}]

    try:
        ai_fields = json.loads(block)
    except json.JSONDecodeError as e:
        return None, "repair", [{"field": "parse", "error": str(e)}]

    normalize_fields(ai_fields)
    ok, errors = validate_handoff_json(ai_fields)
    if not ok:
        return None, "repair", errors

    # Insert via daemon
    result = _db_rpc("handoff.parse", {
        "reply_text": reply_text,
        "context": {
            "role": context.get("role", "manager"),
            "raw_key": context.get("raw_key", ""),
            "worktree": context.get("worktree", ""),
            "branch": context.get("branch", ""),
            "prompt_file": context.get("prompt_file", ""),
            "parent_handoff_id": context.get("parent_handoff_id", ""),
            "previous_worker_handoff_id": context.get("previous_worker_handoff_id", ""),
            "intent_kind": context.get("intent_kind", ""),
            "session_id": context.get("session_id", ""),
        },
    })
    if not result.get("ok"):
        return None, "repair", result.get("errors", [])
    record = {"handoff_id": result["handoff_id"], "exit_kind": result.get("exit_kind", ""),
              "status": "completed" if context.get("role") == "manager" else "pending"}
    return record, result.get("exit_kind", ""), []


def extract_handoff_json(reply_text: str):
    """Extract and validate handoff JSON without DB side effects. Delegates to handoff_parser."""
    from handoff_parser import extract_handoff_json as _extract
    return _extract(reply_text)


def insert_repair_handoff(repair_target_role: str, repair_target_handoff_id: str,
                          validation_errors: list, raw_key: str) -> str:
    """Insert a structured repair handoff for Manager to consume."""
    reason = f"Agent [{repair_target_role}] 输出无效 handoff JSON。"
    next_action = f"检查 {repair_target_role} 的 prompt 和 JSON 格式。"
    result = _db_rpc("handoff.insert", {
        "role": "manager", "raw_key": raw_key, "prompt_file": "",
        "status": "pending", "exit_kind": "manager_working",
        "reason": reason, "next_action": next_action,
        "repair_target_role": repair_target_role,
        "repair_target_handoff_id": repair_target_handoff_id,
        "validation_errors_json": json.dumps(validation_errors, ensure_ascii=False),
        "created_by": "runtime",
    })
    return result.get("handoff_id", "")


def query_by_issue(issue_id: str, consumed: int | None = None) -> list[dict]:
    """Legacy compat: handoffs are queried by raw_key, not issue_id."""
    return list_by_key(issue_id)


# ── CLI ───────────────────────────────────────────────────────────────────

def _main() -> int:
    parser = argparse.ArgumentParser(description="Handoff SQLite via freely-db daemon")
    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init")
    p_init.add_argument("--db")

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--db")
    p_insert.add_argument("--role", default="manager")
    p_insert.add_argument("--raw-key", default="")
    p_insert.add_argument("--prompt-file", required=True)
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
    p_insert.add_argument("--parent", default="")
    p_insert.add_argument("--prev-worker", default="")
    p_insert.add_argument("--intent-kind", default="")
    p_insert.add_argument("--created-by", default="")
    p_insert.add_argument("--consumed-by", default="")

    p_update = sub.add_parser("update")
    p_update.add_argument("--db")
    p_update.add_argument("--handoff-id", required=True)
    p_update.add_argument("--status")
    p_update.add_argument("--expected-status", default="")
    p_update.add_argument("--exit-kind")
    p_update.add_argument("--session-id")
    p_update.add_argument("--reason")
    p_update.add_argument("--restart-point")
    p_update.add_argument("--next-action")
    p_update.add_argument("--completion-summary")
    p_update.add_argument("--evidence-paths")
    p_update.add_argument("--worker-prompts-csv")

    p_get = sub.add_parser("get")
    p_get.add_argument("--db")
    p_get.add_argument("--handoff-id", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--db")
    p_list.add_argument("--role", default="worker")
    p_list.add_argument("--status", default=None)

    p_list_key = sub.add_parser("list-key")
    p_list_key.add_argument("--db")
    p_list_key.add_argument("--raw-key", required=True)

    p_active = sub.add_parser("active-workers")
    p_active.add_argument("--db")
    p_active.add_argument("--worktree", required=True)

    p_has_active = sub.add_parser("has-active-worker")
    p_has_active.add_argument("--db")
    p_has_active.add_argument("--worktree", required=True)

    p_latest = sub.add_parser("latest-manager")
    p_latest.add_argument("--db")

    p_prev = sub.add_parser("latest-completed-worker")
    p_prev.add_argument("--db")
    p_prev.add_argument("--raw-key", default="")

    p_stale = sub.add_parser("mark-stale")
    p_stale.add_argument("--db")
    p_stale.add_argument("--timeout-minutes", type=int, default=15)

    p_auto_consume = sub.add_parser("auto-consume")
    p_auto_consume.add_argument("--db")
    p_auto_consume.add_argument("--raw-key", required=True)
    p_auto_consume.add_argument("--consumed-by", default="manager")

    p_last_activity = sub.add_parser("update-last-activity")
    p_last_activity.add_argument("--db")
    p_last_activity.add_argument("--handoff-id", required=True)

    p_parse = sub.add_parser("parse")
    p_parse.add_argument("--db")
    p_parse.add_argument("--reply-text", required=True)
    p_parse.add_argument("--role", default="manager")
    p_parse.add_argument("--raw-key", default="")
    p_parse.add_argument("--prompt-file", default="")
    p_parse.add_argument("--worktree", default="")
    p_parse.add_argument("--branch", default="")
    p_parse.add_argument("--parent-handoff-id", default="")
    p_parse.add_argument("--previous-worker-handoff-id", default="")
    p_parse.add_argument("--intent-kind", default="")
    p_parse.add_argument("--session-id", default="")

    p_extract = sub.add_parser("extract")
    p_extract.add_argument("--reply-text", required=True)

    p_pending = sub.add_parser("list-pending-delivery")
    p_pending.add_argument("--db")
    p_pending.add_argument("--consumed-by", default="")

    p_send_ai = sub.add_parser("update-send-to-ai")
    p_send_ai.add_argument("--db")
    p_send_ai.add_argument("--handoff-id", required=True)
    p_send_ai.add_argument("--send-to-ai", required=True)

    p_update_pid = sub.add_parser("update-worker-pid")
    p_update_pid.add_argument("--db")
    p_update_pid.add_argument("--handoff-id", required=True)
    p_update_pid.add_argument("--worker-pid", required=True)

    p_launched = sub.add_parser("get-launched-pids")
    p_launched.add_argument("--db")
    p_launched.add_argument("--raw-key", default="")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1

    # Set DB_PATH for project resolution
    global DB_PATH, PROJECT
    DB_PATH = getattr(args, 'db', None)
    if DB_PATH:
        PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(DB_PATH)))

    if args.cmd == "init":
        init_db()
        print("ok")
        return 0

    if args.cmd == "insert":
        hid = insert_handoff(
            role=args.role, raw_key=args.raw_key,
            prompt_file=args.prompt_file, worktree=args.worktree,
            branch=args.branch, parent=args.parent,
            prev_worker=args.prev_worker, intent_kind=args.intent_kind,
            created_by=args.created_by, consumed_by=args.consumed_by,
        )
        print(hid)
        return 0

    if args.cmd == "update":
        kwargs = {}
        if args.status: kwargs["status"] = args.status
        if args.expected_status: kwargs["expected_status"] = args.expected_status
        if args.exit_kind: kwargs["exit_kind"] = args.exit_kind
        if args.session_id: kwargs["session_id"] = args.session_id
        if args.reason: kwargs["reason"] = args.reason
        if args.restart_point: kwargs["restart_point"] = args.restart_point
        if args.next_action: kwargs["next_action"] = args.next_action
        if args.completion_summary: kwargs["completion_summary"] = args.completion_summary
        if args.evidence_paths: kwargs["evidence_paths"] = args.evidence_paths
        if args.worker_prompts_csv: kwargs["worker_prompts_csv"] = args.worker_prompts_csv
        affected = update_status(args.handoff_id, **kwargs)
        print(f"ok affected={affected}")
        return 0

    if args.cmd == "get":
        rec = get_handoff(args.handoff_id)
        if rec:
            print(json.dumps(rec))
        else:
            print("null")
        return 0

    if args.cmd == "list":
        rows = list_by_role(args.role, args.status)
        print(json.dumps(rows))
        return 0

    if args.cmd == "list-key":
        rows = list_by_key(args.raw_key)
        print(json.dumps(rows))
        return 0

    if args.cmd == "active-workers":
        rows = query_active_workers(args.worktree)
        print(json.dumps(rows))
        return 0

    if args.cmd == "has-active-worker":
        result = has_active_worker(args.worktree)
        print("true" if result else "false")
        return 0

    if args.cmd == "latest-manager":
        rec = latest_manager()
        if rec:
            print(json.dumps(rec))
        else:
            print("null")
        return 0

    if args.cmd == "latest-completed-worker":
        rec = latest_completed_worker(args.raw_key)
        if rec:
            print(json.dumps(rec))
        else:
            print("null")
        return 0

    if args.cmd == "mark-stale":
        affected = mark_stale(args.timeout_minutes)
        print(f"done affected={affected}")
        return 0

    if args.cmd == "auto-consume":
        affected = auto_consume(args.raw_key, args.consumed_by)
        print(f"{affected}")
        return 0

    if args.cmd == "update-last-activity":
        update_last_activity(args.handoff_id)
        print("ok")
        return 0

    if args.cmd == "parse":
        context = {
            "role": args.role, "raw_key": args.raw_key,
            "prompt_file": args.prompt_file, "worktree": args.worktree,
            "branch": args.branch, "parent_handoff_id": args.parent_handoff_id,
            "previous_worker_handoff_id": args.previous_worker_handoff_id,
            "intent_kind": args.intent_kind, "session_id": args.session_id,
        }
        record, exit_kind, errors = parse_handoff_json(args.reply_text, context)
        if record is None:
            print(json.dumps({"action": "repair", "errors": errors}))
            return 1
        print(json.dumps({"action": exit_kind, "handoff_id": record["handoff_id"]}))
        return 0

    if args.cmd == "extract":
        result = extract_handoff_json(args.reply_text)
        print(json.dumps(result))
        return 0 if result.get("ok") else 1

    if args.cmd == "list-pending-delivery":
        rows = query_pending_delivery(args.consumed_by)
        print(json.dumps(rows))
        return 0

    if args.cmd == "update-send-to-ai":
        affected = update_send_to_ai(args.handoff_id, args.send_to_ai)
        print(f"ok affected={affected}")
        return 0

    if args.cmd == "update-worker-pid":
        affected = update_worker_pid(args.handoff_id, args.worker_pid)
        print(f"ok affected={affected}")
        return 0

    if args.cmd == "get-launched-pids":
        rows = get_launched_pids(args.raw_key)
        print(json.dumps(rows))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(_main())

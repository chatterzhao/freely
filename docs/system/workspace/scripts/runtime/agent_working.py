"""agent_working table CRUD — uses freely-db-cli socket RPC (not direct SQLite).

Identity file tracking is retired. Table managed by freely_db_manager.py.
All production callers must treat RPC failures as hard errors (fail-closed).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
from typing import Optional

from raw_key_canon import canonicalize_raw_key, try_canonicalize_raw_key
from agent_identity_value import format_agent_entry


class AgentWorkingError(RuntimeError):
    """Raised when agent_working DB/RPC fails. Callers must fail-closed."""


def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.sock"


def _db_rpc(project: str, method: str, params: dict, timeout: float = 5.0) -> dict:
    """Send JSON-RPC to freely_db_manager daemon via Unix socket.

    Fail-closed: any transport, protocol, or application error raises AgentWorkingError.
    Never returns a silent empty success that would look like "no row / no agent".
    """
    sp = _socket_path(project)
    req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, default=str) + "\n"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        try:
            sock.connect(sp)
        except OSError as e:
            raise AgentWorkingError(f"agent_working RPC connect failed ({sp}): {e}") from e
        try:
            sock.sendall(req.encode())
            sock.shutdown(socket.SHUT_WR)
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
        except OSError as e:
            raise AgentWorkingError(f"agent_working RPC transport failed: {e}") from e
    finally:
        sock.close()

    if not data:
        raise AgentWorkingError(f"agent_working RPC empty response for {method}")
    try:
        payload = json.loads(data.decode())
    except json.JSONDecodeError as e:
        raise AgentWorkingError(f"agent_working RPC invalid JSON: {e}") from e

    if "error" in payload and payload["error"]:
        err = payload["error"]
        msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
        raise AgentWorkingError(f"agent_working RPC error for {method}: {msg}")

    if "result" not in payload:
        raise AgentWorkingError(f"agent_working RPC missing result for {method}: {payload!r}")

    result = payload["result"]
    if result is None:
        raise AgentWorkingError(f"agent_working RPC null result for {method}")
    if not isinstance(result, dict):
        raise AgentWorkingError(f"agent_working RPC non-dict result for {method}: {type(result)}")
    return result


def _canon(raw_key: str) -> str:
    return canonicalize_raw_key(raw_key)


def agent_assign(project: str, raw_key: str, role: str, agent_id: str,
                 worktree: str = "", branch: str = "", session_id: str = "",
                 test_worktree: str = "", test_branch: str = "",
                 slot: str = ""):
    """ACP session/new|fork 时写入。通过 DB RPC。

    All roles use UPSERT (INSERT OR UPDATE). Fail-closed on RPC error.
    """
    raw_key = _canon(raw_key)
    if role == "worker":
        if not agent_id:
            raise AgentWorkingError("agent_id required for worker role")
        if not re.match(r"^worker_\d{2}$", agent_id):
            raise AgentWorkingError(
                f"agent_id '{agent_id}' invalid, expected 'worker_NN' format"
            )
    col = f"{role}_id"
    val = format_agent_entry(agent_id, session_id)
    return _db_rpc(project, "agent_working.upsert", {
        "raw_key": raw_key, "col": col, "val": val,
        "worktree": worktree, "branch": branch,
        "test_worktree": test_worktree, "test_branch": test_branch,
        "slot": slot, "role": role, "agent_id": agent_id,
    })


def acp_session_register(project: str, raw_key: str, role: str, agent_id: str,
                         session_id: str = "", slot: str = "",
                         worktree: str = "", branch: str = "",
                         test_worktree: str = "", test_branch: str = ""):
    """统一 session 注册入口。"""
    return agent_assign(project, raw_key, role, agent_id,
                        session_id=session_id, slot=slot,
                        worktree=worktree, branch=branch,
                        test_worktree=test_worktree, test_branch=test_branch)


def acp_session_connect(project: str, raw_key: str, role: str, agent_id: str,
                        slot: str, message: str = None,
                        force_new: bool = False) -> tuple:
    """统一 ACP session 操作选择。active detection + fallback safety net."""
    import sys
    raw_key = _canon(raw_key)

    base_tool = slot.split("-")[0] if "-" in slot else slot
    bridge_socket = _resolve_bridge_socket(project, base_tool)

    if force_new:
        result = _acp_bridge_call(project, base_tool, "session/new",
                                  {"role": role, "agentId": agent_id})
        sid = _session_id_from_result(result)
        acp_session_register(project, raw_key, role, agent_id, sid, slot)
        _prompt_after_connect(project, base_tool, sid, role, message)
        print(f"[acp-session] {role}/{agent_id} using new (force_new)", file=sys.stderr)
        return sid, "new"

    existing = agent_list_by_raw_key(project, raw_key)
    old_sid = None
    if existing and existing.get(f"{role}_id"):
        old_sid = agent_get_session(project, raw_key, role, agent_id)

    if old_sid:
        is_alive = _acp_bridge_ping(project, base_tool, old_sid)
        if is_alive:
            if message:
                _acp_bridge_call(project, base_tool, "session/prompt",
                                 {"sessionId": old_sid, "prompt": message})
                return old_sid, "prompt"
            return old_sid, "return"
        else:
            try:
                _acp_bridge_call(project, base_tool, "session/resume",
                                 {"sessionId": old_sid})
                if message:
                    _acp_bridge_call(project, base_tool, "session/prompt",
                                     {"sessionId": old_sid, "prompt": message})
                acp_session_register(project, raw_key, role, agent_id, old_sid, slot)
                return old_sid, "resume"
            except Exception as e:
                print(f"[acp-session] {role}/{agent_id} resume failed: {e}, "
                      f"falling back to new", file=sys.stderr)
                return _do_new(project, raw_key, role, agent_id, slot, base_tool,
                               reason=f"resume failed: {e}")

    mgr_row = agent_list_by_raw_key(project, "__manager__")
    mgr_slot = mgr_row.get("slot", "") if mgr_row else ""
    mgr_base = mgr_slot.split("-")[0] if "-" in mgr_slot else ""
    if base_tool == mgr_base or not mgr_base:
        try:
            mgr_sid = agent_get_session(project, "__manager__", "manager")
            if mgr_sid:
                result = _acp_bridge_call(project, base_tool, "session/fork",
                                          {"sessionId": mgr_sid, "role": role,
                                           "agentId": agent_id})
                sid = result.get("sessionId", "") if isinstance(result, dict) else ""
                if sid:
                    acp_session_register(project, raw_key, role, agent_id, sid, slot)
                    _prompt_after_connect(project, base_tool, sid, role, message)
                    return sid, "fork"
        except Exception as e:
            print(f"[acp-session] {role}/{agent_id} fork failed: {e}, "
                  f"falling back to new", file=sys.stderr)
    else:
        print(f"[acp-session] {role}/{agent_id} cross-tool "
              f"({base_tool} vs {mgr_base}), using new", file=sys.stderr)

    return _do_new(project, raw_key, role, agent_id, slot, base_tool)


def _prompt_after_connect(project: str, base_tool: str, session_id: str, role: str,
                          message: str | None) -> None:
    """Send the handoff message after session/new|fork.

    ACP's session/new and session/fork do not accept a message; without this
    prompt the first Worker/Reviewer turn starts empty. Role marker is minimal;
    the full role definition still comes from the prompt file/preset.
    """
    if not message:
        return
    prompt = message if "[role:" in message else f"[role:{role}]\n{message}"
    _acp_bridge_call(project, base_tool, "session/prompt",
                     {"sessionId": session_id, "prompt": prompt})


def _session_id_from_result(result: dict) -> str:
    if not isinstance(result, dict):
        raise AgentWorkingError(
            f"ACP session/new returned non-dict result: {type(result).__name__}"
        )
    session_id = result.get("sessionId")
    if not isinstance(session_id, str) or not session_id.strip():
        raise AgentWorkingError("ACP session/new returned no usable sessionId")
    return session_id.strip()


def _do_new(project, raw_key, role, agent_id, slot, base_tool, reason=""):
    result = _acp_bridge_call(project, base_tool, "session/new",
                              {"role": role, "agentId": agent_id})
    sid = _session_id_from_result(result)
    acp_session_register(project, raw_key, role, agent_id, sid, slot)
    _prompt_after_connect(project, base_tool, sid, role, message)
    label = reason or "no-session"
    print(f"[acp-session] {role}/{agent_id} using new ({label})", file=sys.stderr)
    return sid, "new"


def _acp_bridge_call(project: str, base_tool: str, method: str, params: dict) -> dict:
    sp = _resolve_bridge_socket(project, base_tool)
    req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, default=str) + "\n"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect(sp)
        sock.sendall(req.encode())
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    finally:
        sock.close()
    return json.loads(data.decode()).get("result", {})


def _acp_bridge_ping(project: str, base_tool: str, session_id: str) -> bool:
    try:
        result = _acp_bridge_call(project, base_tool, "session/ping",
                                  {"sessionId": session_id})
        return bool(result and "error" not in str(result).lower())
    except Exception:
        return False


def _resolve_bridge_socket(project: str, base_tool: str = "") -> str:
    h = hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]
    return f"/tmp/freely-acp-{h}-{base_tool}.sock"


def agent_release(project: str, raw_key: str, role: str, agent_id: str = None):
    """Release one assignment; reviewer release requires the exact CSV entry id."""
    if role == "reviewer" and not agent_id:
        raise AgentWorkingError("agent_id required when releasing reviewer assignment")
    return _db_rpc(project, "agent_working.release", {
        "raw_key": _canon(raw_key), "role": role, "agent_id": agent_id or "",
    })


def agent_release_all(project: str, raw_key: str):
    """wt-close 时删除整行。"""
    return _db_rpc(project, "agent_working.delete", {"raw_key": _canon(raw_key)})


def agent_get_session(project: str, raw_key: str, role: str, agent_id: str = None) -> Optional[str]:
    """查某个 agent 的 session_id。"""
    result = _db_rpc(project, "agent_working.get_session", {
        "raw_key": _canon(raw_key), "role": role, "agent_id": agent_id or "",
    })
    return result.get("session_id") or None


def agent_next_free_and_assign(project: str, role: str, pool_size: int, raw_key: str) -> dict:
    """Atomic next_free + assign. Returns full RPC result. Fail-closed.

    Callers that launch worker/reviewer MUST use the returned agent_id to pick
    the slot — do not re-query and re-assign.
    """
    result = _db_rpc(project, "agent_working.next_free_and_assign", {
        "role": role,
        "pool_size": str(pool_size),
        "raw_key": _canon(raw_key),
    })
    return result


def agent_next_free(project: str, role: str, pool_size: int, raw_key: str = None) -> Optional[str]:
    """返回下一个可用的 agent NN。

    When raw_key is provided, uses atomic next_free_and_assign (idempotent for
    same raw_key+role). Omitting raw_key uses query-only path (read-only tools).
    Fail-closed on RPC errors — never invents manager_01/worker_01.
    """
    if raw_key:
        result = agent_next_free_and_assign(project, role, pool_size, raw_key)
        if not result.get("assigned"):
            return None
        return result.get("agent_id") or None
    result = _db_rpc(project, "agent_working.next_free", {
        "role": role, "pool_size": str(pool_size),
    })
    return result.get("agent_id") or None


def agent_list_by_raw_key(project: str, raw_key: str) -> dict:
    """返回某个 raw_key 的所有 agent 信息。"""
    result = _db_rpc(project, "agent_working.get", {"raw_key": _canon(raw_key)})
    return result.get("row", {}) or {}


def agent_cleanup_stale(project: str, max_age_hours: int = 24):
    return _db_rpc(project, "agent_working.cleanup_stale", {
        "max_age_hours": str(max_age_hours),
    })


def agent_stats(project: str) -> dict:
    return _db_rpc(project, "agent_working.stats", {})


REVIEW_PHASES = ["b1", "b2", "red", "dev", "green"]


def agent_record_review(project: str, raw_key: str, review_stage: str,
                        verdict: str, reviewed_by: str,
                        findings: list = None) -> dict:
    if review_stage not in REVIEW_PHASES:
        return {"error": f"unknown review_stage: {review_stage}"}
    if verdict not in ("PASS", "FAIL"):
        return {"error": f"verdict must be PASS or FAIL, got: {verdict}"}

    return _db_rpc(project, "agent_working.record_review", {
        "raw_key": _canon(raw_key),
        "review_stage": review_stage,
        "verdict": verdict,
        "reviewed_by": reviewed_by,
        "reviewed_at": "",
        "findings": json.dumps(findings or []),
    })


def agent_get_reviews(project: str, raw_key: str) -> dict:
    result = _db_rpc(project, "agent_working.get_reviews", {"raw_key": _canon(raw_key)})
    return result.get("reviews", {}) or {}


def agent_find_first_missing_review(project: str, raw_key: str) -> tuple:
    reviews = agent_get_reviews(project, raw_key)
    for i, phase in enumerate(REVIEW_PHASES):
        r = reviews.get(phase, {})
        if not r or r.get("verdict") != "PASS":
            return phase, REVIEW_PHASES[i:]
    return None, []


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: agent_working.py <action> <project> [args...]", file=sys.stderr)
        sys.exit(1)
    action = sys.argv[1]
    project = sys.argv[2]
    if action == "cleanup_stale":
        result = agent_cleanup_stale(project)
        print(f"cleaned: {result}")
    elif action == "release_all":
        raw_key = sys.argv[3] if len(sys.argv) > 3 else ""
        agent_release_all(project, raw_key)
        print("released")
    elif action == "stats":
        print(json.dumps(agent_stats(project), indent=2))
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

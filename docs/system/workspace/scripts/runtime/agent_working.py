"""agent_working table CRUD — uses freely-db-cli socket RPC (not direct SQLite).
Replaces agent-id.env file tracking. Table managed by freely_db_manager.py."""

import hashlib
import json
import os
import socket
from typing import Optional


def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.sock"


def _db_rpc(project: str, method: str, params: dict, timeout: float = 5.0) -> dict:
    """Send JSON-RPC to freely_db_manager daemon via Unix socket."""
    sp = _socket_path(project)
    req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, default=str) + "\n"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(sp)
        sock.sendall(req.encode())
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
    finally:
        sock.close()
    return json.loads(data.decode()).get("result", {})


def agent_assign(project: str, raw_key: str, role: str, agent_id: str,
                 worktree: str = "", branch: str = "", session_id: str = "",
                 test_worktree: str = "", test_branch: str = "",
                 slot: str = "", update_only: bool = False):
    """ACP session/new|fork 时写入。通过 DB RPC。

    Worker:  UPSERT (INSERT OR UPDATE) — raw_key 行不存在就创建
    Reviewer: UPDATE ONLY — raw_key 行必须已存在（Worker 创建的），
             行不存在说明 worktree 已被 wt-close 删除或存在 bug
    Manager: 独立行 "__manager__"，UPSERT
    """
    col = f"{role}_id"
    val = f"{agent_id}:{session_id}" if session_id else agent_id
    method = "agent_working.upsert_only" if update_only else "agent_working.upsert"
    return _db_rpc(project, method, {
        "raw_key": raw_key, "col": col, "val": val,
        "worktree": worktree, "branch": branch,
        "test_worktree": test_worktree, "test_branch": test_branch,
        "slot": slot, "role": role, "agent_id": agent_id
    })


# ── Unified ACP session management ─────────────────────────────


def acp_session_register(project: str, raw_key: str, role: str, agent_id: str,
                         session_id: str = "", slot: str = "",
                         worktree: str = "", branch: str = "",
                         test_worktree: str = "", test_branch: str = ""):
    """统一 session 注册入口。所有 session/new 或 session/fork 成功后调用。

    写入 agent_working 表 (含 slot), 作为后续 resume/prompt 的查询依据。
    """
    return agent_assign(project, raw_key, role, agent_id,
                        session_id=session_id, slot=slot,
                        worktree=worktree, branch=branch,
                        test_worktree=test_worktree, test_branch=test_branch)


def acp_session_connect(project: str, raw_key: str, role: str, agent_id: str,
                        slot: str, message: str = None,
                        force_new: bool = False) -> tuple:
    """统一 ACP session 操作选择。active detection + fallback safety net.

    决策树:
      1. force_new → session/new
      2. 有 session_id + slot 相同?
         alive → prompt(msg) 或 return
         dead  → resume → ok 或 fallback new + log
      3. 无 session + 同 base_tool + mgr 有 session → fork(Mgr)
         fork 失败 → fallback new + log
      4. 跨 base_tool → new + log

    Returns: (session_id, operation_used)
      operation_used: 'prompt' | 'resume' | 'fork' | 'new' | 'return'
    """
    import sys

    base_tool = slot.split('-')[0] if '-' in slot else slot
    bridge_socket = _resolve_bridge_socket(project, base_tool)

    # ── 0. 显式要求 new ──
    if force_new:
        sid = _acp_bridge_call(project, base_tool, "session/new",
                               {"role": role, "agentId": agent_id})
        acp_session_register(project, raw_key, role, agent_id, sid, slot)
        print(f"[acp-session] {role}/{agent_id} using new (force_new)", file=sys.stderr)
        return sid, "new"

    # ── 1. 查 agent_working ──
    existing = agent_list_by_raw_key(project, raw_key)
    old_sid = None
    if existing and existing.get(f"{role}_id"):
        val = existing[f"{role}_id"]
        old_sid = val.split(":")[-1] if ":" in str(val) else None

    if old_sid:
        # ── 2. session alive? ──
        is_alive = _acp_bridge_ping(project, base_tool, old_sid)
        if is_alive:
            if message:
                _acp_bridge_call(project, base_tool, "session/prompt",
                                 {"sessionId": old_sid, "prompt": message})
                return old_sid, "prompt"
            return old_sid, "return"
        else:
            # ── 3. dead → try resume ──
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

    # ── 4. 无 session → fork 或 new ──
    mgr_row = agent_list_by_raw_key(project, "__manager__")
    mgr_slot = mgr_row.get("slot", "") if mgr_row else ""
    mgr_base = mgr_slot.split('-')[0] if '-' in mgr_slot else ""
    if base_tool == mgr_base or not mgr_base:
        # Same base_tool or manager slot unknown → try fork
        try:
            mgr_sid = agent_get_session(project, "__manager__", "manager")
            if mgr_sid:
                result = _acp_bridge_call(project, base_tool, "session/fork",
                                          {"sessionId": mgr_sid, "role": role,
                                           "agentId": agent_id})
                sid = result.get("sessionId", "") if isinstance(result, dict) else ""
                if sid:
                    acp_session_register(project, raw_key, role, agent_id, sid, slot)
                    return sid, "fork"
        except Exception as e:
            print(f"[acp-session] {role}/{agent_id} fork failed: {e}, "
                  f"falling back to new", file=sys.stderr)
    else:
        print(f"[acp-session] {role}/{agent_id} cross-tool "
              f"({base_tool} vs {mgr_base}), using new", file=sys.stderr)

    return _do_new(project, raw_key, role, agent_id, slot, base_tool)


def _do_new(project, raw_key, role, agent_id, slot, base_tool, reason=""):
    """session/new + register."""
    result = _acp_bridge_call(project, base_tool, "session/new",
                              {"role": role, "agentId": agent_id})
    sid = result.get("sessionId", "") if isinstance(result, dict) else ""
    if sid:
        acp_session_register(project, raw_key, role, agent_id, sid, slot)
        label = reason or "no-session"
        print(f"[acp-session] {role}/{agent_id} using new ({label})", file=sys.stderr)
    return sid, "new"


def _acp_bridge_call(project: str, base_tool: str, method: str, params: dict) -> dict:
    """Send JSON-RPC to ACP bridge and return result."""
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
    """Check if session is alive on bridge."""
    try:
        result = _acp_bridge_call(project, base_tool, "session/ping",
                                  {"sessionId": session_id})
        return bool(result and "error" not in str(result).lower())
    except Exception:
        return False


def _resolve_bridge_socket(project: str, base_tool: str = "") -> str:
    """Resolve ACP bridge socket path per base_tool."""
    h = hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]
    return f"/tmp/freely-acp-{h}-{base_tool}.sock"


def agent_release(project: str, raw_key: str, role: str, agent_id: str = None):
    """session/close 时清除 session（保留 agent_id）。"""
    return _db_rpc(project, "agent_working.release", {
        "raw_key": raw_key, "role": role, "agent_id": agent_id or ""
    })


def agent_release_all(project: str, raw_key: str):
    """wt-close 时删除整行。"""
    return _db_rpc(project, "agent_working.delete", {"raw_key": raw_key})


def agent_get_session(project: str, raw_key: str, role: str, agent_id: str = None) -> Optional[str]:
    """查某个 agent 的 session_id。"""
    result = _db_rpc(project, "agent_working.get_session", {
        "raw_key": raw_key, "role": role, "agent_id": agent_id or ""
    })
    return result.get("session_id") or None


def agent_next_free(project: str, role: str, pool_size: int) -> Optional[str]:
    """返回下一个可用的 agent NN。"""
    result = _db_rpc(project, "agent_working.next_free", {
        "role": role, "pool_size": str(pool_size)
    })
    return result.get("agent_id") or None


def agent_list_by_raw_key(project: str, raw_key: str) -> dict:
    """返回某个 raw_key 的所有 agent 信息。"""
    result = _db_rpc(project, "agent_working.get", {"raw_key": raw_key})
    return result.get("row", {})


def agent_cleanup_stale(project: str, max_age_hours: int = 24):
    """清理 worktree 已不存在的行。"""
    return _db_rpc(project, "agent_working.cleanup_stale", {
        "max_age_hours": str(max_age_hours)
    })


def agent_stats(project: str) -> dict:
    """返回各角色占用/空闲统计。"""
    return _db_rpc(project, "agent_working.stats", {})

# ── CLI entry point ──────────────────────────────────────────────
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
        import json
        print(json.dumps(agent_stats(project), indent=2))
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

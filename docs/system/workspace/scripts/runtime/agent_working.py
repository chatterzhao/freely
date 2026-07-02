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
                 update_only: bool = False):
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
        "role": role, "agent_id": agent_id
    })


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

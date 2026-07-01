"""agent_working table CRUD — replaces agent-id.env file tracking."""

import sqlite3
import os
from typing import Optional


def _db_path(project: str) -> str:
    return os.path.join(project, ".freely", "freely.db")


def _connect(project: str) -> sqlite3.Connection:
    db = sqlite3.connect(_db_path(project))
    db.row_factory = sqlite3.Row
    return db


def agent_assign(project: str, raw_key: str, role: str, agent_id: str,
                 worktree: str = "", branch: str = "", session_id: str = "",
                 test_worktree: str = "", test_branch: str = ""):
    """ACP session/new 时写入一行。已存在则更新对应 role 列。"""
    col = f"{role}_id"
    val = f"{agent_id}:{session_id}" if session_id else agent_id
    db = _connect(project)
    cur = db.execute("SELECT * FROM agent_working WHERE raw_key = ?", [raw_key])
    row = cur.fetchone()
    if row:
        if role == "reviewer":
            existing = row[col] or ""
            pairs = _parse_pairs(existing)
            pairs[agent_id] = session_id
            val = _format_pairs(pairs) if pairs else agent_id
        db.execute(f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
                   [val, raw_key])
    else:
        db.execute(
            f"INSERT INTO agent_working (raw_key, worktree, branch, test_worktree, test_branch, {col}) "
            "VALUES (?,?,?,?,?,?)",
            [raw_key, worktree, branch, test_worktree, test_branch, val])
    db.commit()
    db.close()


def agent_release(project: str, raw_key: str, role: str, agent_id: str = None):
    """session/close 时清除 session 或整行。"""
    col = f"{role}_id"
    db = _connect(project)
    cur = db.execute("SELECT * FROM agent_working WHERE raw_key = ?", [raw_key])
    row = cur.fetchone()
    if not row:
        db.close(); return
    if role == "reviewer" and agent_id:
        pairs = _parse_pairs(row[col] or "")
        pairs.pop(agent_id, None)
        new_val = _format_pairs(pairs) if pairs else None
    else:
        current = row[col] or ""
        new_val = current.split(":", 1)[0] if ":" in current else None
    if new_val:
        db.execute(f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
                   [new_val, raw_key])
    else:
        db.execute(f"UPDATE agent_working SET {col}=NULL, updated_at=datetime('now') WHERE raw_key=?", [raw_key])
    db.commit()
    db.close()


def agent_release_all(project: str, raw_key: str):
    """wt-close 时删除整行。"""
    db = _connect(project)
    db.execute("DELETE FROM agent_working WHERE raw_key = ?", [raw_key])
    db.commit()
    db.close()


def agent_get_session(project: str, raw_key: str, role: str, agent_id: str = None) -> Optional[str]:
    """查某个 agent 的 session_id。"""
    col = f"{role}_id"
    db = _connect(project)
    cur = db.execute(f"SELECT {col} FROM agent_working WHERE raw_key = ?", [raw_key])
    row = cur.fetchone()
    db.close()
    if not row or not row[col]: return None
    if role == "reviewer" and agent_id:
        return _parse_pairs(row[col]).get(agent_id)
    return row[col].split(":", 1)[1] if ":" in row[col] else None


def agent_next_free(project: str, role: str, pool_size: int) -> Optional[str]:
    """返回下一个可用的 agent NN。"""
    prefix = f"{role}_"
    col = f"{role}_id"
    db = _connect(project)
    rows = db.execute(f"SELECT {col} FROM agent_working WHERE {col} IS NOT NULL").fetchall()
    db.close()
    occupied = set()
    for r in rows:
        val = r[col] or ""
        if role == "reviewer":
            for k in _parse_pairs(val):
                occupied.add(k)
        else:
            agent_part = val.split(":", 1)[0] if ":" in val else val
            if agent_part: occupied.add(agent_part)
    all_ids = {f"{prefix}{i:02d}" for i in range(1, pool_size + 1)}
    free = sorted(all_ids - occupied)
    return free[0] if free else None


def agent_list_by_raw_key(project: str, raw_key: str) -> dict:
    """返回某个 raw_key 的所有 agent 信息。"""
    db = _connect(project)
    cur = db.execute("SELECT * FROM agent_working WHERE raw_key = ?", [raw_key])
    row = cur.fetchone()
    db.close()
    return dict(row) if row else {}


def _parse_pairs(s: str) -> dict:
    if not s: return {}
    return dict(p.split(":", 1) for p in s.split(",") if ":" in p)


def _format_pairs(d: dict) -> str:
    return ",".join(f"{k}:{v}" for k, v in d.items() if v)


def agent_cleanup_stale(project: str, max_age_hours: int = 24):
    """Remove agent_working rows for worktrees that no longer exist."""
    import os as _os
    db = _connect(project)
    rows = db.execute("SELECT raw_key, worktree, test_worktree FROM agent_working").fetchall()
    cleaned = 0
    for row in rows:
        wt = row["worktree"]
        twt = row["test_worktree"]
        if wt and not _os.path.exists(wt):
            db.execute("DELETE FROM agent_working WHERE raw_key = ?", [row["raw_key"]])
            cleaned += 1
        elif twt and not _os.path.exists(twt):
            db.execute("UPDATE agent_working SET test_worktree=NULL, test_branch=NULL WHERE raw_key=?",
                       [row["raw_key"]])
            cleaned += 1
    db.commit()
    db.close()
    return cleaned


def agent_stats(project: str) -> dict:
    """Return occupancy stats per role."""
    db = _connect(project)
    result = {}
    for role, pool in [("manager", 1), ("worker", 10), ("reviewer", 99)]:
        col = f"{role}_id"
        rows = db.execute(f"SELECT {col} FROM agent_working WHERE {col} IS NOT NULL").fetchall()
        occupied = 0
        for r in rows:
            val = r[col] or ""
            if role == "reviewer":
                occupied += len(_parse_pairs(val))
            elif val:
                occupied += 1
        result[role] = {"occupied": occupied, "pool": pool, "free": pool - occupied}
    db.close()
    return result

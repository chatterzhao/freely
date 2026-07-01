-- Migration 001: agent_working table
-- Replaces agent-id.env file-based tracking.

CREATE TABLE IF NOT EXISTS agent_working (
    raw_key         TEXT PRIMARY KEY,
    worktree        TEXT NOT NULL,
    branch          TEXT NOT NULL,
    test_worktree   TEXT,
    test_branch     TEXT,
    manager_id      TEXT,
    worker_id       TEXT,
    reviewer_id     TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_aw_worker ON agent_working(worker_id);
CREATE INDEX IF NOT EXISTS idx_aw_manager ON agent_working(manager_id);
CREATE INDEX IF NOT EXISTS idx_aw_reviewer ON agent_working(reviewer_id);

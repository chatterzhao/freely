#!/usr/bin/env python3
"""chat-inbox.py — Chat inbox raw issue management.

Consumes chat messages from freely.db and materializes them as raw issues.
"""

import argparse
import os
import sys

# Add runtime scripts path for shared imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def cmd_show(db_path: str, chat_id: str) -> int:
    """Check if chat exists in inbox."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        'SELECT id, chat_type, message FROM chats WHERE id=? AND chat_type="new-issue"',
        (chat_id,)
    ).fetchone()
    conn.close()
    if row:
        print(f"id={row['id']} type={row['chat_type']} message={row['message'][:50]}...")
        return 0
    return 1


def cmd_materialize(db_path: str, chat_id: str, target_dir: str) -> int:
    """Materialize chat as raw issue."""
    import sqlite3
    from datetime import datetime, timezone

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        'SELECT id, issue_id, author, message, created_at FROM chats WHERE id=?',
        (chat_id,)
    ).fetchone()
    conn.close()

    if not row:
        print(f"Chat {chat_id} not found", file=sys.stderr)
        return 1

    os.makedirs(target_dir, exist_ok=True)
    issue_file = os.path.join(target_dir, "issue.md")

    # Parse message for title (first line) and body
    message = row['message']
    lines = message.strip().split('\n', 1)
    title = lines[0] if lines else "Untitled"
    body = lines[1] if len(lines) > 1 else ""

    # Generate frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    issue_id = row['issue_id'] or f"raw-{chat_id}"

    frontmatter = f"""---
name: {title[:50]}
description: {body[:100] if body else title[:100]}
kind: raw
phase_state: raw
open_questions: []
acceptance_criteria: []
acceptance_reviews: []
created: {now}
updated: {now}
---

# {title}

{body}
"""

    with open(issue_file, 'w') as f:
        f.write(frontmatter)

    print(f"Materialized {issue_id} → {issue_file}")
    return 0


def cmd_consume(db_path: str, chat_id: str, materialized_as: str) -> int:
    """Mark chat as consumed."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    affected = conn.execute(
        'UPDATE chats SET consumed=1, materialized_as=? WHERE id=?',
        (materialized_as, chat_id)
    ).rowcount
    conn.commit()
    conn.close()
    print(f"Consumed chat {chat_id} as {materialized_as} (affected={affected})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Chat inbox raw issue management")
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_show = sub.add_parser('show', help="Show chat details")
    p_show.add_argument('--db', required=True, help="SQLite DB path")
    p_show.add_argument('--id', required=True, help="Chat ID (YYYYMMDDHHMMSS)")

    p_mat = sub.add_parser('materialize', help="Materialize chat as raw issue")
    p_mat.add_argument('--db', required=True, help="SQLite DB path")
    p_mat.add_argument('--id', required=True, help="Chat ID")
    p_mat.add_argument('--target', required=True, help="Target directory")

    p_con = sub.add_parser('consume', help="Mark chat as consumed")
    p_con.add_argument('--db', required=True, help="SQLite DB path")
    p_con.add_argument('--id', required=True, help="Chat ID")
    p_con.add_argument('--materialized-as', required=True, help="Materialized issue ID")

    args = parser.parse_args()

    if args.cmd == 'show':
        return cmd_show(args.db, args.id)
    elif args.cmd == 'materialize':
        return cmd_materialize(args.db, args.id, args.target)
    elif args.cmd == 'consume':
        return cmd_consume(args.db, args.id, args.materialized_as)
    return 1


if __name__ == '__main__':
    sys.exit(main())
#!/usr/bin/env python3
"""migrate_handoff_to_a2a.py - Handoff 数据迁移到 A2A Task 格式

将现有的 handoffs 表数据迁移到 A2A Task 格式。

迁移策略：
1. 读取现有 handoffs 表
2. 转换为 A2A Task 格式
3. 写入新的 tasks 表
4. 验证数据一致性
5. 可选：删除旧 handoffs 表

运行方式:
  python3 docs/system/workspace/scripts/runtime/a2a/migrate_handoff_to_a2a.py \
    --project /path/to/project \
    --dry-run \
    --output migrated-tasks.json
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# 添加 runtime 目录到 path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, RUNTIME_DIR)


# ── Constants ────────────────────────────────────────────────────────────────

# exit_kind → A2A Task state 映射
EXIT_KIND_TO_TASK_STATE = {
    'manager_working': 'submitted',
    'worker_working': 'working',
    'worker_done': 'completed',
    'worker_blocked': 'input-required',
    'worker_handoff_needed': 'pending-input',
    'delegate_workers': 'submitted',
    'resume_manager': 'completed',
    'stop_ai': 'failed',
}

# Handoff 状态 → exit_kind 映射
HANDOFF_STATUS_TO_EXIT_KIND = {
    'pending': 'worker_working',
    'active': 'worker_working',
    'completed': 'worker_done',
    'blocked': 'worker_blocked',
    'stale': 'worker_blocked',
}


# ── Data Models ───────────────────────────────────────────────────────────────

@dataclass
class A2ATask:
    """A2A Task 格式"""
    id: str
    state: str
    created_at: str
    updated_at: str
    skill: str = ""
    prompt_file: str = ""
    worktree: str = ""
    branch: str = ""
    exit_kind: str = ""
    reason: str = ""
    progress: str = ""
    next_action: str = ""
    completion_summary: str = ""
    evidence_paths: str = ""
    worker_prompts_csv: str = ""
    session_id: str = ""
    error: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class HandoffRecord:
    """Handoff 记录格式"""
    handoff_id: str
    role: str
    raw_key: str
    prompt_file: str
    worktree: str
    branch: str
    parent: str
    prev_worker: str
    intent_kind: str
    status: str
    exit_kind: str
    reason: str
    restart_point: str
    next_action: str
    completion_summary: str
    evidence_paths: str
    worker_prompts_csv: str
    session_id: str
    created_by: str
    consumed_by: str
    created_at: str
    updated_at: str
    last_activity_at: str


# ── 数据库操作 ───────────────────────────────────────────────────────────────

def get_handoffs(db_path: str, role: Optional[str] = None, status: Optional[str] = None) -> List[HandoffRecord]:
    """从 handoffs 表读取数据"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM handoffs WHERE 1=1"
    params = []

    if role:
        query += " AND role = ?"
        params.append(role)

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [HandoffRecord(**dict(row)) for row in rows]


def create_tasks_table(db_path: str):
    """创建 tasks 表（如果不存在）"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            skill TEXT DEFAULT '',
            prompt_file TEXT DEFAULT '',
            worktree TEXT DEFAULT '',
            branch TEXT DEFAULT '',
            exit_kind TEXT DEFAULT '',
            reason TEXT DEFAULT '',
            progress TEXT DEFAULT '',
            next_action TEXT DEFAULT '',
            completion_summary TEXT DEFAULT '',
            evidence_paths TEXT DEFAULT '',
            worker_prompts_csv TEXT DEFAULT '',
            session_id TEXT DEFAULT '',
            error TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def insert_task(db_path: str, task: A2ATask):
    """插入 Task 到 tasks 表"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (
            id, state, created_at, updated_at,
            skill, prompt_file, worktree, branch,
            exit_kind, reason, progress, next_action,
            completion_summary, evidence_paths, worker_prompts_csv,
            session_id, error
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        task.id, task.state, task.created_at, task.updated_at,
        task.skill, task.prompt_file, task.worktree, task.branch,
        task.exit_kind, task.reason, task.progress, task.next_action,
        task.completion_summary, task.evidence_paths, task.worker_prompts_csv,
        task.session_id, task.error
    ))

    conn.commit()
    conn.close()


# ── 迁移逻辑 ───────────────────────────────────────────────────────────────

def migrate_handoff_to_task(handoff: HandoffRecord) -> A2ATask:
    """将 Handoff 记录转换为 A2A Task"""
    import uuid

    # 确定 exit_kind
    exit_kind = handoff.exit_kind
    if not exit_kind and handoff.status:
        exit_kind = HANDOFF_STATUS_TO_EXIT_KIND.get(handoff.status, 'worker_working')

    # 转换状态
    state = EXIT_KIND_TO_TASK_STATE.get(exit_kind, 'working')

    return A2ATask(
        id=str(uuid.uuid4()),
        state=state,
        created_at=handoff.created_at,
        updated_at=handoff.updated_at,
        skill=handoff.intent_kind,
        prompt_file=handoff.prompt_file,
        worktree=handoff.worktree,
        branch=handoff.branch,
        exit_kind=exit_kind,
        reason=handoff.reason,
        progress="",
        next_action=handoff.next_action,
        completion_summary=handoff.completion_summary,
        evidence_paths=handoff.evidence_paths,
        worker_prompts_csv=handoff.worker_prompts_csv,
        session_id=handoff.session_id,
        error="",
    )


def migrate_all(project: str, role: Optional[str] = None, dry_run: bool = False) -> Dict:
    """执行迁移"""
    db_path = os.path.join(project, ".freely", "freely.db")

    if not os.path.exists(db_path):
        return {
            "success": False,
            "error": f"Database not found: {db_path}",
        }

    # 读取 handoffs
    handoffs = get_handoffs(db_path, role=role)
    print(f"Found {len(handoffs)} handoffs to migrate")

    # 转换为 tasks
    tasks = []
    for handoff in handoffs:
        task = migrate_handoff_to_task(handoff)
        tasks.append({
            "original": asdict(handoff),
            "migrated": task.to_dict(),
        })
        print(f"  - {handoff.handoff_id} → {task.id} ({task.state})")

    if dry_run:
        print("\n[Dry-run] No changes written")
        return {
            "success": True,
            "dry_run": True,
            "count": len(tasks),
            "tasks": tasks,
        }

    # 创建 tasks 表并写入
    create_tasks_table(db_path)

    migrated_count = 0
    for task_data in tasks:
        task = A2ATask(**task_data["migrated"])
        insert_task(db_path, task)
        migrated_count += 1

    print(f"\nMigrated {migrated_count} tasks")

    return {
        "success": True,
        "dry_run": False,
        "count": migrated_count,
        "tasks": tasks,
    }


def verify_migration(project: str) -> Dict:
    """验证迁移结果"""
    db_path = os.path.join(project, ".freely", "freely.db")

    if not os.path.exists(db_path):
        return {
            "success": False,
            "error": f"Database not found: {db_path}",
        }

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 统计 handoffs 和 tasks
    cursor.execute("SELECT COUNT(*) FROM handoffs")
    handoffs_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    tasks_count = cursor.fetchone()[0]

    # 统计各状态
    cursor.execute("SELECT state, COUNT(*) FROM tasks GROUP BY state")
    state_stats = dict(cursor.fetchall())

    conn.close()

    return {
        "success": True,
        "handoffs_count": handoffs_count,
        "tasks_count": tasks_count,
        "state_stats": state_stats,
        "balanced": handoffs_count == tasks_count,
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Handoff 数据迁移到 A2A Task 格式")
    parser.add_argument("--project", required=True, help="Freely 项目路径")
    parser.add_argument("--dry-run", action="store_true", help="仅显示迁移预览，不写入")
    parser.add_argument("--role", choices=["manager", "worker"], help="只迁移指定角色的 handoff")
    parser.add_argument("--output", help="输出迁移结果到 JSON 文件")
    parser.add_argument("--verify", action="store_true", help="验证迁移结果")
    args = parser.parse_args()

    if args.verify:
        result = verify_migration(args.project)
        print(json.dumps(result, indent=2))
        return

    result = migrate_all(args.project, role=args.role, dry_run=args.dry_run)

    if result["success"]:
        print(f"\nMigration {'preview' if result['dry_run'] else 'completed'}: {result['count']} tasks")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Results saved to: {args.output}")
    else:
        print(f"Migration failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
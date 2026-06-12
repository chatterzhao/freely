#!/usr/bin/env python3
"""a2a_client.py - A2A Client (Manager 端)

实现 A2A 协议的客户端，用于 Freely Manager Agent。

功能：
- 能力发现 (discoverAgent)
- Task 创建和状态监控
- 与 Freely Handoff 机制集成

A2A 协议规范: https://github.com/A2A-Specification/A2A
"""

import argparse
import json
import os
import socket
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum

# ── Constants ────────────────────────────────────────────────────────────────

PROJECT = None  # set by main()

# A2A Task 状态
class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    INPUT_REQUIRED = "input-required"
    PENDING_INPUT = "pending-input"


# exit_kind → A2A Task state 映射 (与 server 保持一致)
EXIT_KIND_TO_TASK_STATE = {
    'manager_working': TaskState.SUBMITTED,
    'worker_working': TaskState.WORKING,
    'worker_done': TaskState.COMPLETED,
    'worker_blocked': TaskState.INPUT_REQUIRED,
    'worker_handoff_needed': TaskState.PENDING_INPUT,
    'delegate_workers': TaskState.SUBMITTED,
    'resume_manager': TaskState.COMPLETED,
    'stop_ai': TaskState.FAILED,
}

TASK_STATE_TO_EXIT_KIND = {v: k for k, v in EXIT_KIND_TO_TASK_STATE.items()}


# ── Data Models ───────────────────────────────────────────────────────────────

@dataclass
class AgentCard:
    name: str
    description: str
    url: str
    version: str
    capabilities: Dict
    skills: List[Dict]
    default_error_handling_mode: str = "agentic"
    freely: Optional[Dict] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentCard':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Task:
    id: str
    state: str = TaskState.SUBMITTED.value
    created_at: str = ""
    updated_at: str = ""
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
    error: str = ""
    session_id: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ── Utility Functions ─────────────────────────────────────────────────────────

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_hash(project: str) -> str:
    import hashlib
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-a2a-{_short_hash(project)}.sock"


# ── A2A Client ───────────────────────────────────────────────────────────────

class A2AClient:
    """A2A Unix Domain Socket Client"""

    def __init__(self, project: str):
        self.project = project
        self.socket_path = _socket_path(project)
        self._timeout = 30.0

    def _send_request(self, method: str, path: str, body: Optional[Dict] = None) -> Dict:
        """发送请求到 A2A Server"""
        if not os.path.exists(self.socket_path):
            raise RuntimeError(f"A2A Server not running at {self.socket_path}")

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self._timeout)
        try:
            sock.connect(self.socket_path)

            # 构造 HTTP 请求
            if body:
                body_json = json.dumps(body, default=str)
                http_request = f"{method} {path} HTTP/1.1\r\n"
                http_request += "Content-Type: application/json\r\n"
                http_request += f"Content-Length: {len(body_json)}\r\n"
                http_request += "Connection: close\r\n"
                http_request += "\r\n"
                http_request += body_json
            else:
                http_request = f"{method} {path} HTTP/1.1\r\n"
                http_request += "Connection: close\r\n"
                http_request += "\r\n"

            sock.sendall(http_request.encode())

            # 读取响应
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk

            # 解析 HTTP 响应
            response_text = data.decode("utf-8", errors="replace")
            lines = response_text.split("\r\n")
            if len(lines) == 1:
                lines = response_text.split("\n")

            # 解析状态行
            status_line = lines[0]
            parts = status_line.split(" ")
            if len(parts) >= 2:
                status = int(parts[1])
            else:
                status = 500

            # 解析 body
            body_start = response_text.find("\r\n\r\n")
            if body_start == -1:
                body_start = response_text.find("\n\n")
            if body_start != -1:
                body = response_text[body_start + 4:]
                return json.loads(body)
            else:
                return {"error": "Empty response"}

        finally:
            sock.close()

    def discover_agent(self) -> Optional[AgentCard]:
        """发现 Worker Agent Card"""
        try:
            response = self._send_request("GET", "/.well-known/agent.json")
            if "name" in response:
                return AgentCard.from_dict(response)
            return None
        except Exception as e:
            print(f"[A2A Client] discover_agent failed: {e}")
            return None

    def create_task(
        self,
        skill: str,
        prompt_file: str = "",
        worktree: str = "",
        branch: str = "",
        reason: str = "",
        session_id: str = "",
    ) -> Optional[Task]:
        """创建新 Task"""
        try:
            body = {
                "skill": skill,
                "prompt_file": prompt_file,
                "worktree": worktree,
                "branch": branch,
                "reason": reason,
                "session_id": session_id,
            }
            response = self._send_request("POST", "/tasks", body)
            if "id" in response:
                return Task.from_dict(response)
            return None
        except Exception as e:
            print(f"[A2A Client] create_task failed: {e}")
            return None

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取 Task"""
        try:
            response = self._send_request("GET", f"/tasks/{task_id}")
            if "id" in response:
                return Task.from_dict(response)
            return None
        except Exception as e:
            print(f"[A2A Client] get_task failed: {e}")
            return None

    def update_task(
        self,
        task_id: str,
        exit_kind: str = "",
        reason: str = "",
        progress: str = "",
        next_action: str = "",
        completion_summary: str = "",
        evidence_paths: str = "",
        worker_prompts_csv: str = "",
        error: str = "",
    ) -> Optional[Task]:
        """更新 Task"""
        try:
            body = {
                "exit_kind": exit_kind,
                "reason": reason,
                "progress": progress,
                "next_action": next_action,
                "completion_summary": completion_summary,
                "evidence_paths": evidence_paths,
                "worker_prompts_csv": worker_prompts_csv,
                "error": error,
            }
            # 移除空字段
            body = {k: v for k, v in body.items() if v}

            response = self._send_request("PATCH", f"/tasks/{task_id}", body)
            if "id" in response:
                return Task.from_dict(response)
            return None
        except Exception as e:
            print(f"[A2A Client] update_task failed: {e}")
            return None

    def list_tasks(self) -> List[Task]:
        """列出所有 Task"""
        try:
            response = self._send_request("GET", "/tasks")
            if "tasks" in response:
                return [Task.from_dict(t) for t in response["tasks"]]
            return []
        except Exception as e:
            print(f"[A2A Client] list_tasks failed: {e}")
            return []

    def wait_for_completion(
        self,
        task_id: str,
        timeout: float = 600.0,
        poll_interval: float = 2.0,
        on_state_change: Optional[Callable[[Task], None]] = None,
    ) -> Optional[Task]:
        """等待 Task 完成"""
        start_time = time.time()
        last_state = None

        while time.time() - start_time < timeout:
            task = self.get_task(task_id)
            if not task:
                break

            # 状态变化回调
            if on_state_change and task.state != last_state:
                on_state_change(task)
                last_state = task.state

            # 检查完成状态
            if task.state in (TaskState.COMPLETED.value, TaskState.FAILED.value):
                return task

            time.sleep(poll_interval)

        return None

    def subscribe_stream(self, task_id: str) -> None:
        """订阅 Task SSE 流（简化实现）"""
        print(f"[A2A Client] Subscribing to stream for task {task_id}")
        # 实际实现应使用 SSE 客户端库
        # 这里简化为轮询
        self._stream_loop(task_id)

    def _stream_loop(self, task_id: str):
        """流轮询循环"""
        last_state = None
        while True:
            try:
                task = self.get_task(task_id)
                if not task:
                    break

                if task.state != last_state:
                    print(f"[A2A Stream] Task {task_id} state: {task.state}")
                    last_state = task.state

                if task.state in (TaskState.COMPLETED.value, TaskState.FAILED.value):
                    break

                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[A2A Stream] Error: {e}")
                break


# ── Handoff 兼容层 ───────────────────────────────────────────────────────────

class A2AHandoffAdapter:
    """A2A 与 Handoff 的兼容层

    将 A2A Task 操作转换为 Freely Handoff 操作，
    保持向后兼容。
    """

    def __init__(self, project: str):
        self.project = project
        self._a2a_client = A2AClient(project)

    def discover_and_check_capability(self, skill: str) -> bool:
        """发现 Worker 并检查是否支持指定 skill"""
        agent_card = self._a2a_client.discover_agent()
        if not agent_card:
            return False

        # 检查 freely 扩展
        if not agent_card.freely:
            return False

        supported_skills = agent_card.freely.get("supportedSkills", [])
        return skill in supported_skills

    def create_task_with_fallback(
        self,
        skill: str,
        prompt_file: str = "",
        worktree: str = "",
        branch: str = "",
        reason: str = "",
        session_id: str = "",
    ) -> Optional[Dict]:
        """创建 Task，失败时 fallback 到 Handoff"""
        try:
            # 尝试 A2A
            task = self._a2a_client.create_task(
                skill=skill,
                prompt_file=prompt_file,
                worktree=worktree,
                branch=branch,
                reason=reason,
                session_id=session_id,
            )
            if task:
                return task.to_dict()
        except Exception as e:
            print(f"[A2A Handoff Adapter] A2A failed, falling back to Handoff: {e}")

        # Fallback 到 Handoff
        print("[A2A Handoff Adapter] Falling back to Handoff")
        return self._fallback_to_handoff(skill, prompt_file, worktree, branch, reason, session_id)

    def _fallback_to_handoff(
        self,
        skill: str,
        prompt_file: str,
        worktree: str,
        branch: str,
        reason: str,
        session_id: str,
    ) -> Optional[Dict]:
        """Fallback 到 Handoff"""
        # 导入 handoff 模块
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        try:
            import handoff
            handoff_id = handoff.insert_handoff(
                role="worker",
                raw_key=f"a2a-fallback-{skill}",
                prompt_file=prompt_file,
                worktree=worktree,
                branch=branch,
                intent_kind=skill,
                status="pending",
                reason=reason,
                session_id=session_id,
            )
            return {"handoff_id": handoff_id, "fallback": True}
        except Exception as e:
            print(f"[A2A Handoff Adapter] Handoff fallback failed: {e}")
            return None


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Freely A2A Client (Manager 端)")
    parser.add_argument("--project", required=True, help="Freely 项目路径")
    parser.add_argument("--discover", action="store_true", help="发现 Worker Agent")
    parser.add_argument("--list-tasks", action="store_true", help="列出所有 Task")
    parser.add_argument("--create-task", help="创建 Task (skill name)")
    parser.add_argument("--get-task", help="获取 Task (task_id)")
    parser.add_argument("--wait", help="等待 Task 完成 (task_id)")
    parser.add_argument("--check-capability", help="检查 Worker 能力 (skill name)")
    args = parser.parse_args()

    client = A2AClient(args.project)

    if args.discover:
        card = client.discover_agent()
        if card:
            print(json.dumps(card.to_dict(), indent=2))
        else:
            print("No Agent Card found")

    elif args.list_tasks:
        tasks = client.list_tasks()
        print(f"Total tasks: {len(tasks)}")
        for task in tasks:
            print(f"  - {task.id}: {task.state}")

    elif args.create_task:
        task = client.create_task(skill=args.create_task)
        if task:
            print(f"Task created: {task.id} ({task.state})")
        else:
            print("Task creation failed")

    elif args.get_task:
        task = client.get_task(args.get_task)
        if task:
            print(json.dumps(task.to_dict(), indent=2))
        else:
            print("Task not found")

    elif args.wait:
        task = client.wait_for_completion(args.wait)
        if task:
            print(f"Task completed: {task.state}")
            print(json.dumps(task.to_dict(), indent=2))
        else:
            print("Task wait timeout or error")

    elif args.check_capability:
        adapter = A2AHandoffAdapter(args.project)
        if adapter.discover_and_check_capability(args.check_capability):
            print(f"Worker supports skill: {args.check_capability}")
        else:
            print(f"Worker does not support skill: {args.check_capability}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""a2a_server.py - A2A Server (Worker 端)

实现 A2A 协议的服务端，用于 Freely Worker Agent。

功能：
- Agent Card endpoint (/.well-known/agent.json)
- Task CRUD endpoints
- SSE streaming 实时推送
- 与 Freely Handoff 机制集成

A2A 协议规范: https://github.com/A2A-Specification/A2A
"""

import argparse
import asyncio
import json
import os
import socket
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ── Constants ────────────────────────────────────────────────────────────────

PROJECT = None  # set by main()

A2A_VERSION = "1.0.0"

# A2A Task 状态
class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    INPUT_REQUIRED = "input-required"
    PENDING_INPUT = "pending-input"


# exit_kind → A2A Task state 映射
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

# ── Data Models ───────────────────────────────────────────────────────────────

@dataclass
class Task:
    """A2A Task Model (符合 Google A2A 协议规范)

    核心字段: id, state, agent_id, skill, session_id, message
    Freely 扩展: prompt_file, worktree, branch, exit_kind, reason, progress, next_action,
                completion_summary, evidence_paths, worker_prompts_csv, error
    """
    id: str = ""
    state: str = TaskState.SUBMITTED.value
    created_at: str = ""
    updated_at: str = ""
    session_id: str = ""
    skill: str = ""
    # A2A 标准字段
    name: str = ""
    description: str = ""
    agent_id: str = ""
    message: str = ""
    # Freely 扩展字段
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
    messages: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """转换为 dict，过滤 None 值"""
        d = {}
        for k, v in asdict(self).items():
            if v is not None:
                d[k] = v
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """从 dict 创建 Task"""
        # 兼容处理：跳过不存在于 dataclass 的字段
        valid = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in valid}
        return cls(**filtered)


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

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentCard':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ── In-Memory Task Store (临时，正式实现使用 DB) ────────────────────────────────

class TaskStore:
    """Task 存储，使用 SQLite 持久化（通过 freely_db_manager daemon）

    所有数据库操作通过 _db_rpc 进行，确保：
    - 进程重启后状态不丢失
    - 与 Freely Runtime 共享同一数据库
    """

    def __init__(self, project: str):
        self.project = project
        self._lock = threading.RLock()

    def _db_rpc(self, method: str, params: dict, timeout: float = 30.0) -> dict:
        """Send JSON-RPC to freely_db_manager daemon."""
        import socket as sock_module
        import hashlib
        import json as json_mod

        def _short_hash(p: str) -> str:
            return hashlib.sha256(os.path.abspath(p).encode()).hexdigest()[:16]

        socket_path = f"/tmp/freely-db-{_short_hash(self.project)}.sock"

        request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        sock = sock_module.socket(sock_module.AF_UNIX, sock_module.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(socket_path)
            sock.sendall((json_mod.dumps(request, default=str) + "\n").encode())
            sock.shutdown(sock_module.SHUT_WR)
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
        finally:
            sock.close()

        response = json_mod.loads(data.decode())
        if "error" in response:
            raise RuntimeError(response["error"].get("message", str(response["error"])))
        return response.get("result", {})

    def create(self, task: Task) -> Task:
        """创建新 Task，持久化到 SQLite"""
        task.id = str(uuid.uuid4())
        task.created_at = _now_utc()
        task.updated_at = _now_utc()
        task.state = TaskState.SUBMITTED.value

        result = self._db_rpc("a2a_task.insert", task.to_dict())
        task.id = result.get("task_id", task.id)
        return task

    def get(self, task_id: str) -> Optional[Task]:
        """从 SQLite 加载 Task"""
        result = self._db_rpc("a2a_task.get", {"task_id": task_id})
        record = result.get("record")
        if record:
            return Task.from_dict(record)
        return None

    def update(self, task_id: str, **kwargs) -> Optional[Task]:
        """更新 Task 字段"""
        kwargs["task_id"] = task_id
        kwargs["updated_at"] = _now_utc()
        result = self._db_rpc("a2a_task.update", kwargs)
        if result.get("affected", 0) > 0:
            return self.get(task_id)
        return None

    def update_state(self, task_id: str, state: str, **kwargs) -> Optional[Task]:
        """更新 Task 状态"""
        kwargs["task_id"] = task_id
        kwargs["state"] = state
        kwargs["updated_at"] = _now_utc()
        result = self._db_rpc("a2a_task.update", kwargs)
        if result.get("affected", 0) > 0:
            return self.get(task_id)
        return None

    def list_all(self) -> List[Task]:
        """列出所有 Task"""
        result = self._db_rpc("a2a_task.list", {})
        rows = result.get("rows", [])
        return [Task.from_dict(r) for r in rows]

    def delete(self, task_id: str) -> bool:
        """删除 Task"""
        result = self._db_rpc("a2a_task.delete", {"task_id": task_id})
        return result.get("affected", 0) > 0


# ── SSE Streaming ─────────────────────────────────────────────────────────────

class SSELock:
    """SSE 订阅管理"""

    def __init__(self):
        self._subscribers: Dict[str, asyncio.Queue] = {}
        self._lock = threading.RLock()

    def subscribe(self, task_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        with self._lock:
            self._subscribers[task_id] = queue
        return queue

    def unsubscribe(self, task_id: str):
        with self._lock:
            if task_id in self._subscribers:
                del self._subscribers[task_id]

    async def push(self, task_id: str, event: Dict):
        with self._lock:
            queue = self._subscribers.get(task_id)
        if queue:
            await queue.put(event)


# ── Global State ──────────────────────────────────────────────────────────────

# 注意：TaskStore 现在是实例变量，在 A2AServer.__init__ 中创建
# _task_store = TaskStore()  # 已废弃，使用 self._task_store
_sse_manager = SSELock()


# ── Utility Functions ─────────────────────────────────────────────────────────

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_hash(project: str) -> str:
    import hashlib
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-a2a-{_short_hash(project)}.sock"


def _create_agent_card(project: str, skill: str = "") -> AgentCard:
    """创建 Freely Worker Agent Card"""
    skills = [
        {
            "id": "freely-fix-execution",
            "name": "Bug Fix Execution",
            "description": "快速修复 bug 的特殊高效策略"
        },
        {
            "id": "freely-feat-execution",
            "name": "Feature Execution",
            "description": "新功能/大型改动的完整开发流程"
        },
        {
            "id": "freely-doc-B1_IBM-execution",
            "name": "B1_IBM Pre-Research",
            "description": "I→B→M 第一阶段预研收敛"
        },
        {
            "id": "freely-doc-B2_IBM-execution",
            "name": "B2_IBM Design",
            "description": "I→B→M 第二阶段实现设计"
        }
    ]

    if skill:
        skills = [s for s in skills if s["id"] == skill]

    freely_config = {
        "agentType": "worker",
        "worktreeIsolation": True,
        "worktreeRoot": f"{os.path.dirname(os.path.dirname(project))}/worktrees",
        "supportedExitKinds": list(EXIT_KIND_TO_TASK_STATE.keys()),
        "a2aSchema": "https://a2a-specification.github.io/A2A/schema",
        "supportedSkills": [s["id"] for s in skills],
        "transport": "unix-domain-socket",
        "socketPath": _socket_path(project),
    }

    return AgentCard(
        name="Freely Worker",
        description="Freely Worker Agent with worktree isolation for skill-based execution",
        url=f"unix://{_socket_path(project)}",
        version=A2A_VERSION,
        capabilities={
            "streaming": True,
            "pushNotifications": True,
            "stateTransitions": True,
        },
        skills=skills,
        default_error_handling_mode="agentic",
        freely=freely_config,
    )


# ── Unix Domain Socket Server ────────────────────────────────────────────────

class A2AServer:
    """A2A Unix Domain Socket Server"""

    def __init__(self, socket_path: str, project: str):
        self.socket_path = socket_path
        self.project = project
        self._running = False
        self._agent_card = _create_agent_card(project)
        self._task_store = TaskStore(project)

    def start(self):
        """启动 A2A Server"""
        # 清理旧 socket
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        self._running = True

        # 创建 socket
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.socket_path)
        server.listen(5)
        server.settimeout(1.0)

        print(f"[A2A Server] Listening on {self.socket_path}")

        while self._running:
            try:
                client, _ = server.accept()
                threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    print(f"[A2A Server] Error: {e}")

        server.close()
        print("[A2A Server] Stopped")

    def stop(self):
        """停止 A2A Server"""
        self._running = False
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

    def _handle_client(self, client: socket.socket):
        """处理客户端请求"""
        try:
            # 读取请求
            data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                data += chunk
                # 简单解析：按行读取，找到空行结束 headers
                if b"\r\n\r\n" in data or b"\n\n" in data:
                    break

            # 解析请求行
            request_text = data.decode("utf-8", errors="replace")
            lines = request_text.split("\n")
            if not lines:
                return

            request_line = lines[0].strip()
            parts = request_line.split(" ")
            if len(parts) < 2:
                return

            method, path = parts[0], parts[1]

            # 路由
            if path == "/.well-known/agent.json" or path == "/agent.json":
                self._handle_agent_card(client)
            elif path.startswith("/tasks/") and path.endswith("/stream"):
                self._handle_sse_stream(client, path)
            elif path == "/tasks" or path.startswith("/tasks/"):
                self._handle_tasks(client, method, path, request_text)
            else:
                self._send_response(client, 404, {"error": "Not Found"})

        except Exception as e:
            print(f"[A2A Server] Client error: {e}")
        finally:
            client.close()

    def _handle_agent_card(self, client: socket.socket):
        """返回 Agent Card"""
        card = self._agent_card.to_dict()
        self._send_json_response(client, 200, card)

    def _handle_tasks(self, client: socket.socket, method: str, path: str, request_text: str):
        """处理 Task CRUD 请求"""
        if path == "/tasks":
            if method == "POST":
                self._handle_create_task(client, request_text)
            elif method == "GET":
                self._handle_list_tasks(client)
            else:
                self._send_response(client, 405, {"error": "Method Not Allowed"})
        elif path.startswith("/tasks/"):
            task_id = path[7:]  # /tasks/{id}
            if method == "GET":
                self._handle_get_task(client, task_id)
            elif method == "PATCH":
                self._handle_update_task(client, task_id, request_text)
            else:
                self._send_response(client, 405, {"error": "Method Not Allowed"})
        else:
            self._send_response(client, 404, {"error": "Not Found"})

    def _handle_create_task(self, client: socket.socket, request_text: str):
        """创建新 Task"""
        try:
            # 解析 body
            body_start = request_text.find("\r\n\r\n")
            if body_start == -1:
                body_start = request_text.find("\n\n")
            if body_start != -1:
                body = request_text[body_start + 4:]
                data = json.loads(body)
            else:
                data = {}

            task = Task(
                id="",
                skill=data.get("skill", ""),
                prompt_file=data.get("prompt_file", ""),
                worktree=data.get("worktree", ""),
                branch=data.get("branch", ""),
                session_id=data.get("session_id", ""),
                reason=data.get("reason", ""),
                progress=data.get("progress", ""),
                next_action=data.get("next_action", ""),
            )

            task = self._task_store.create(task)

            response = {
                "id": task.id,
                "state": task.state,
                "created_at": task.created_at,
            }

            self._send_json_response(client, 202, response)

        except Exception as e:
            self._send_json_response(client, 400, {"error": str(e)})

    def _handle_list_tasks(self, client: socket.socket):
        """列出所有 Task"""
        tasks = self._task_store.list_all()
        self._send_json_response(client, 200, {"tasks": [t.to_dict() for t in tasks]})

    def _handle_get_task(self, client: socket.socket, task_id: str):
        """获取 Task"""
        task = self._task_store.get(task_id)
        if task:
            self._send_json_response(client, 200, task.to_dict())
        else:
            self._send_json_response(client, 404, {"error": "Task not found"})

    def _handle_update_task(self, client: socket.socket, task_id: str, request_text: str):
        """更新 Task"""
        try:
            task = self._task_store.get(task_id)
            if not task:
                self._send_json_response(client, 404, {"error": "Task not found"})
                return

            # 解析 body
            body_start = request_text.find("\r\n\r\n")
            if body_start == -1:
                body_start = request_text.find("\n\n")
            if body_start != -1:
                body = request_text[body_start + 4:]
                data = json.loads(body)
            else:
                data = {}

            # 更新字段
            update_fields = {}
            for field in ["state", "exit_kind", "reason", "progress", "next_action",
                          "completion_summary", "evidence_paths", "worker_prompts_csv",
                          "error", "session_id"]:
                if field in data:
                    update_fields[field] = data[field]

            # 转换 exit_kind 到 task state
            if "exit_kind" in data and "state" not in data:
                state = EXIT_KIND_TO_TASK_STATE.get(data["exit_kind"], TaskState.WORKING.value)
                update_fields["state"] = state.value

            task = self._task_store.update(task_id, **update_fields)

            self._send_json_response(client, 200, task.to_dict())

        except Exception as e:
            self._send_json_response(client, 400, {"error": str(e)})

    def _handle_sse_stream(self, client: socket.socket, path: str):
        """SSE 流式推送"""
        # /tasks/{id}/stream
        task_id = path[7:-8]  # /tasks/{id}/stream
        self._send_sse_response(client, task_id)

    def _send_json_response(self, client: socket.socket, status: int, data: Any):
        """发送 JSON 响应"""
        body = json.dumps(data, default=str)
        status_text = {200: "OK", 202: "Accepted", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed", 500: "Internal Server Error"}
        response = f"HTTP/1.1 {status} {status_text.get(status, 'Unknown')}\r\n"
        response += "Content-Type: application/json\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        client.sendall(response.encode())

    def _send_response(self, client: socket.socket, status: int, data: Any):
        """发送响应"""
        body = json.dumps(data, default=str)
        status_text = {200: "OK", 202: "Accepted", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed", 500: "Internal Server Error"}
        response = f"HTTP/1.1 {status} {status_text.get(status, 'Unknown')}\r\n"
        response += "Content-Type: application/json\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        client.sendall(response.encode())

    def _send_sse_response(self, client: socket.socket, task_id: str):
        """发送 SSE 流"""
        # 发送 SSE 头
        headers = "HTTP/1.1 200 OK\r\n"
        headers += "Content-Type: text/event-stream\r\n"
        headers += "Cache-Control: no-cache\r\n"
        headers += "Connection: keep-alive\r\n"
        headers += "\r\n"
        client.sendall(headers.encode())

        # 发送初始连接事件
        client.sendall(b"event: connected\ndata: {\"taskId\": \"" + task_id.encode() + b"\"}\n\n")

        # 模拟 SSE 推送（实际应使用 asyncio）
        def send_updates():
            while self._running:
                task = self._task_store.get(task_id)
                if task:
                    event = json.dumps({"taskId": task.id, "state": task.state, "updatedAt": task.updated_at})
                    try:
                        client.sendall(f"event: task-update\ndata: {event}\n\n".encode())
                    except:
                        break
                time.sleep(1)

        thread = threading.Thread(target=send_updates, daemon=True)
        thread.start()
        thread.join()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Freely A2A Server (Worker 端)")
    parser.add_argument("--project", required=True, help="Freely 项目路径")
    parser.add_argument("--skill", default="", help="Worker 技能")
    parser.add_argument("--start", action="store_true", help="启动 Server")
    parser.add_argument("--stop", action="store_true", help="停止 Server")
    args = parser.parse_args()

    global PROJECT
    PROJECT = args.project

    socket_path = _socket_path(args.project)

    if args.stop:
        if os.path.exists(socket_path):
            os.remove(socket_path)
            print(f"[A2A Server] Stopped (socket removed)")
        else:
            print(f"[A2A Server] Not running")
    elif args.start:
        server = A2AServer(socket_path, args.project)
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()


if __name__ == "__main__":
    main()

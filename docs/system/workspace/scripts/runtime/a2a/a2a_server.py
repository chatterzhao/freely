#!/usr/bin/env python3
"""a2a_server.py — A2A Protocol Server (official a2a-sdk)

Aligns with JiuwenSwarm's A2AChannel pattern:
- async AgentExecutor with proper input validation and streaming
- official SDK types, TaskStore, AgentExecutor, RequestHandler
- Starlette + Uvicorn over Unix socket
- All agent communication flows through A2A protocol (no bypass)

Reference: https://github.com/openJiuwen-ai/jiuwenswarm
"""

import argparse
import asyncio
import json
import os
import socket
import uuid
from datetime import datetime, timezone
from typing import Optional, List

# ── Official A2A SDK ────────────────────────────────────────────────────
from a2a.types import (
    Task, TaskState, TaskStatus, Message, Part,
    Artifact, AgentCard, AgentSkill, AgentCapabilities, AgentInterface,
    TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
)
from a2a.server.tasks import TaskStore as BaseTaskStore
from a2a.server.agent_execution.agent_executor import AgentExecutor as BaseAgentExecutor
from a2a.server.events.event_queue import EventQueue
from a2a.server.routes.jsonrpc_routes import create_jsonrpc_routes
from a2a.server.request_handlers import DefaultRequestHandler
from google.protobuf.json_format import MessageToJson

# ── Starlette + Uvicorn ─────────────────────────────────────────────────
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
import uvicorn

# ── Constants ───────────────────────────────────────────────────────────

PROJECT = None

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _short_hash(project: str) -> str:
    import hashlib
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]

def _socket_path(project: str) -> str:
    return f"/tmp/freely-a2a-{_short_hash(project)}.sock"


# ── Freely Skills ────────────────────────────────────────────────────────

FREELY_SKILLS = [
    AgentSkill(id="freely-fix-execution", name="Bug Fix Execution",
               description="快速修复 bug 的高效策略", tags=["fix", "bug"]),
    AgentSkill(id="freely-feat-execution", name="Feature Execution",
               description="新功能完整开发流程", tags=["feature"]),
    AgentSkill(id="freely-doc-B1_IBM-execution", name="B1_IBM Pre-Research",
               description="I→B→M 第一阶段预研", tags=["research"]),
    AgentSkill(id="freely-doc-B2_IBM-execution", name="B2_IBM Design",
               description="I→B→M 第二阶段设计", tags=["design"]),
    AgentSkill(id="freely-branch-management", name="Branch Management",
               description="自主分支生命周期管理", tags=["branch", "worktree"]),
    AgentSkill(id="freely-constitution-guard", name="Constitution Guard",
               description="强制执行宪法硬性约束", tags=["governance"]),
    AgentSkill(id="freely-worktree-maintenance", name="Worktree Maintenance",
               description="工位治理：核清单、安全 merge", tags=["worktree"]),
]


def _build_agent_card(project: str) -> AgentCard:
    return AgentCard(
        name="Freely Worker",
        description="Freely Worker Agent — worktree-isolated, skill-based A2A execution",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True, push_notifications=False),
        skills=FREELY_SKILLS,
        supported_interfaces=[
            AgentInterface(
                url=f"unix://{_socket_path(project)}",
                protocol_binding="jsonrpc",
                protocol_version="1.0.0",
            )
        ],
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain", "application/json"],
    )


# ── SQLite Task Store ────────────────────────────────────────────────────

class SQLiteTaskStore(BaseTaskStore):
    """TaskStore backed by SQLite via daemon RPC."""

    def __init__(self, project: str):
        self.project = project
        self._lock = asyncio.Lock()

    def _db_rpc(self, method: str, params: dict, timeout: float = 30.0) -> dict:
        h = _short_hash(self.project)
        sp = f"/tmp/freely-db-{h}.sock"
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

    @staticmethod
    def _db_state_to_pb(db_state: str) -> int:
        m = {'submitted': TaskState.TASK_STATE_SUBMITTED, 'working': TaskState.TASK_STATE_WORKING,
             'completed': TaskState.TASK_STATE_COMPLETED, 'failed': TaskState.TASK_STATE_FAILED,
             'input-required': TaskState.TASK_STATE_INPUT_REQUIRED,
             'pending-input': TaskState.TASK_STATE_INPUT_REQUIRED,
             'canceled': TaskState.TASK_STATE_CANCELED}
        return m.get(db_state, TaskState.TASK_STATE_SUBMITTED)

    @staticmethod
    def _pb_state_to_db(ts: int) -> str:
        m = {TaskState.TASK_STATE_SUBMITTED: 'submitted', TaskState.TASK_STATE_WORKING: 'working',
             TaskState.TASK_STATE_COMPLETED: 'completed', TaskState.TASK_STATE_FAILED: 'failed',
             TaskState.TASK_STATE_INPUT_REQUIRED: 'input-required',
             TaskState.TASK_STATE_CANCELED: 'canceled'}
        return m.get(ts, 'submitted')

    def _row_to_task(self, row: dict) -> Task:
        """Convert DB row → SDK Task protobuf (id + status.state)."""
        st = self._db_state_to_pb(row.get('state', ''))
        return Task(id=row.get('task_id', ''),
                    status=TaskStatus(state=st),
                    context_id=row.get('session_id', ''))

    def save(self, task: Task) -> Task:
        """Save task to SQLite. SDK Task.status.state → DB state."""
        state_str = self._pb_state_to_db(task.status.state if hasattr(task, 'status') and task.status else TaskState.TASK_STATE_SUBMITTED)
        existing = self._db_rpc("a2a_task.get", {"task_id": task.id}).get("record") if task.id else None
        if existing:
            self._db_rpc("a2a_task.update", {"task_id": task.id, "state": state_str, "updated_at": _now_utc()})
        else:
            if not task.id: task.id = str(uuid.uuid4())
            self._db_rpc("a2a_task.insert", {"task_id": task.id, "state": state_str})
        return task

    def get(self, task_id: str) -> Optional[Task]:
        row = self._db_rpc("a2a_task.get", {"task_id": task_id}).get("record")
        return self._row_to_task(row) if row else None

    def list(self) -> List[Task]:
        return [self._row_to_task(r) for r in self._db_rpc("a2a_task.list", {}).get("rows", [])]

    def delete(self, task_id: str) -> bool:
        return self._db_rpc("a2a_task.delete", {"task_id": task_id}).get("affected", 0) > 0

    # ── Extended operations ────────────────────────────────────────────

    def get_all_dicts(self) -> list:
        return self._db_rpc("a2a_task.list", {}).get("rows", [])

    def update_fields(self, task_id: str, **fields) -> bool:
        fields["task_id"] = task_id; fields["updated_at"] = _now_utc()
        return self._db_rpc("a2a_task.update", fields).get("affected", 0) > 0

    def raw_rpc(self, method: str, params: dict) -> dict:
        return self._db_rpc(method, params)


# ── Freely Agent Executor (aligns with JiuwenSwarm's _A2AAgentExecutor) ─

class PendingTask:
    """Pending task with async queue for streaming responses."""
    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()


class FreelyAgentExecutor(BaseAgentExecutor):
    """Bridges A2A SDK AgentExecutor to Freely runtime.

    Aligned with JiuwenSwarm's _A2AAgentExecutor:
    - Validates input (empty query → FAILED)
    - Emits TASK_STATE_WORKING on start
    - Creates task in SQLite for the Worker runtime to process
    - Streams status updates as TaskStatusUpdateEvent
    - Proper cleanup in finally block
    """

    def __init__(self, server: "A2AServer"):
        self._server = server
        self._pending: dict[str, PendingTask] = {}

    async def execute(self, context, event_queue: EventQueue) -> None:
        """Execute an A2A request — aligns with JiuwenSwarm's pattern."""
        task_id = str(context.task_id or f"a2a_{uuid.uuid4().hex[:12]}")
        ctx_id = str(context.context_id or f"ctx_{uuid.uuid4().hex[:8]}")

        # 1. Extract and validate input
        msg = context.get_user_message() if hasattr(context, 'get_user_message') else None
        query = ""
        files: list = []
        if msg and hasattr(msg, 'parts'):
            for p in msg.parts:
                if hasattr(p, 'text') and p.text:
                    query += p.text + "\n"
                if hasattr(p, 'url') and p.url:
                    files.append({"url": p.url})
            query = query.strip()

        if not query:
            # Aligns with JiuwenSwarm: empty query → immediate FAILED
            await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id=task_id, context_id=ctx_id,
                status=TaskStatus(state=TaskState.TASK_STATE_FAILED,
                                  message=Message(parts=[Part(text="empty query")])),
                final=True))
            await event_queue.close()
            return

        try:
            # 2. Emit WORKING
            await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id=task_id, context_id=ctx_id,
                status=TaskStatus(state=TaskState.TASK_STATE_WORKING), final=False))

            # 3. Create task in SQLite for Worker runtime
            internal_task = Task(id=str(uuid.uuid4()), status=TaskStatus(state=TaskState.TASK_STATE_SUBMITTED))
            self._server.task_store.save(internal_task)

            # Store task metadata via raw RPC
            metadata = dict(context.metadata or {}) if hasattr(context, 'metadata') else {}
            self._server.task_store.raw_rpc("a2a_task.update", {
                "task_id": internal_task.id, "state": "submitted",
                "agent_id": metadata.get("agent_id", "worker"),
                "skill": metadata.get("skill", ""),
                "prompt_file": metadata.get("prompt_file", ""),
                "worktree": metadata.get("worktree", ""),
                "branch": metadata.get("branch", ""),
                "raw_key": metadata.get("raw_key", ""),
                "message": query,
            })

            # 4. Emit artifact with internal task reference
            artifact_id = f"{task_id}_created"
            await event_queue.enqueue_event(TaskArtifactUpdateEvent(
                task_id=task_id, context_id=ctx_id,
                artifact=Artifact(
                    artifact_id=artifact_id,
                    name="task_created",
                    parts=[Part(text=f"internal_task_id={internal_task.id}")],
                ),
                append=False, last_chunk=False))

            # 5. Emit COMPLETED (task creation is complete; Worker runtime processes it)
            await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id=task_id, context_id=ctx_id,
                status=TaskStatus(state=TaskState.TASK_STATE_COMPLETED), final=True))

        except Exception as exc:
            await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id=task_id, context_id=ctx_id,
                status=TaskStatus(state=TaskState.TASK_STATE_FAILED,
                                  message=Message(parts=[Part(text=str(exc))])),
                final=True))
        finally:
            await event_queue.close()

    async def cancel(self, context, event_queue: EventQueue) -> None:
        task_id = str(context.task_id or "a2a")
        ctx_id = str(context.context_id or "")
        await event_queue.enqueue_event(TaskStatusUpdateEvent(
            task_id=task_id, context_id=ctx_id,
            status=TaskStatus(state=TaskState.TASK_STATE_CANCELED), final=True))
        await event_queue.close()


# ── A2A Server ───────────────────────────────────────────────────────────

class A2AServer:
    """A2A Protocol Server — async, official SDK + Starlette + Uvicorn.

    Supports dual transport:
    - Unix domain socket (local agents, zero network overhead)
    - TCP host:port (remote agents, network communication)

    Config via environment:
    - A2A_LISTEN_MODE=unix|tcp|both (default: unix)
    - A2A_TCP_HOST=0.0.0.0 (default)
    - A2A_TCP_PORT=19100 (default)
    """

    def __init__(self, project: str, socket_path: str = "",
                 tcp_host: str = "", tcp_port: int = 0):
        self.socket_path = socket_path or _socket_path(project)
        self.tcp_host = tcp_host or os.environ.get("A2A_TCP_HOST", "0.0.0.0")
        self.tcp_port = tcp_port or int(os.environ.get("A2A_TCP_PORT", "19100"))
        self.listen_mode = os.environ.get("A2A_LISTEN_MODE", "unix")
        self.project = project
        self._running = False
        self._servers: list = []
        self.agent_card = _build_agent_card(project)
        self.task_store = SQLiteTaskStore(project)
        self.executor = FreelyAgentExecutor(self)
        # Restore non-terminal tasks from WAL on startup (crash recovery)
        self._restore_tasks()

    def _restore_tasks(self):
        """Replay WAL: restore all non-terminal tasks into memory on startup.
        Terminal states (completed/failed/canceled) are skipped — they're done.
        """
        try:
            rows = self.task_store.get_all_dicts()
            restored = 0
            for row in rows:
                state = row.get("state", "")
                if state in ("completed", "failed", "canceled"):
                    continue
                # Non-terminal: restore to TaskStore (already in SQLite, just ensure
                # in-memory SDK cache is populated by loading via get())
                if row.get("task_id"):
                    self.task_store.get(row["task_id"])
                    restored += 1
            if restored > 0:
                import sys
                print(f"[A2A Gateway] Restored {restored} non-terminal tasks from WAL", file=sys.stderr)
        except Exception:
            pass  # DB not available → start with empty TaskStore (降级运行)

    def _build_app(self) -> Starlette:
        request_handler = DefaultRequestHandler(
            agent_executor=self.executor,
            task_store=self.task_store,
            agent_card=self.agent_card,
        )
        routes = create_jsonrpc_routes(request_handler=request_handler, rpc_url="/")
        routes.extend([
            Route("/.well-known/agent.json", self._agent_card_endpoint, methods=["GET"]),
            Route("/.well-known/agent-card.json", self._agent_card_endpoint, methods=["GET"]),
            Route("/tasks", self._tasks_endpoint, methods=["GET", "POST"]),
            Route("/tasks/latest-manager", self._latest_manager, methods=["GET"]),
            Route("/tasks/pending-delivery", self._pending_delivery, methods=["GET"]),
            Route("/tasks/launched-pids", self._launched_pids, methods=["GET"]),
            Route("/tasks/{task_id:path}", self._task_endpoint, methods=["GET", "PATCH"]),
        ])
        return Starlette(routes=routes)

    # ── Endpoints ──────────────────────────────────────────────────────

    async def _agent_card_endpoint(self, request: Request):
        return Response(MessageToJson(self.agent_card), media_type="application/json")

    async def _tasks_endpoint(self, request: Request):
        if request.method == "POST":
            try:
                body = await request.json()
                task = Task(id=str(uuid.uuid4()), status=TaskStatus(state=TaskState.TASK_STATE_SUBMITTED))
                task = self.task_store.save(task)
                fields = {"task_id": task.id, "state": "submitted",
                    "agent_id": body.get("agent_id", body.get("agentId", "worker")),
                    "skill": body.get("skill", ""),
                    "prompt_file": body.get("prompt_file", body.get("promptFile", "")),
                    "worktree": body.get("worktree", ""), "branch": body.get("branch", ""),
                    "raw_key": body.get("raw_key", body.get("rawKey", "")),
                    "completion_summary": body.get("summary", ""),
                    "worker_prompts_csv": body.get("workers", ""),
                    "message": body.get("message", ""),
                }
                self.task_store.raw_rpc("a2a_task.update", dict(fields))
                return JSONResponse({"id": task.id, "state": "submitted"}, status_code=202)
            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=400)
        else:
            qs = dict(request.query_params)
            rows = self.task_store.get_all_dicts()
            for key in ("state", "agent_id", "skill", "worktree", "raw_key", "delivery_status"):
                if key in qs: rows = [r for r in rows if r.get(key) == qs[key]]
            rows.sort(key=lambda r: r.get("created_at", ""), reverse=True)
            return JSONResponse({"tasks": rows})

    async def _task_endpoint(self, request: Request):
        task_id = request.path_params["task_id"]
        if task_id.endswith("/messages") and request.method == "POST":
            tid = task_id[:-9]; body = await request.json()
            self.task_store.raw_rpc("a2a_task.update-message", {
                "task_id": tid, "role": body.get("role", "worker"),
                "type": body.get("type", "text"), "content": body.get("content", "")})
            return JSONResponse({"ok": True})
        if task_id.endswith("/delivery") and request.method == "PATCH":
            tid = task_id[:-10]; body = await request.json()
            self.task_store.raw_rpc("a2a_task.update-delivery-status",
                {"task_id": tid, "delivery_status": body.get("delivery_status", "delivered")})
            return JSONResponse({"ok": True})
        if task_id.endswith("/worker-pid") and request.method == "PATCH":
            tid = task_id[:-12]; body = await request.json()
            self.task_store.raw_rpc("a2a_task.update-worker-pid",
                {"task_id": tid, "worker_pid": body.get("worker_pid", "")})
            return JSONResponse({"ok": True})
        if "/" in task_id:
            return JSONResponse({"error": "Not Found"}, status_code=404)
        if request.method == "GET":
            row = self.task_store.raw_rpc("a2a_task.get", {"task_id": task_id}).get("record")
            return JSONResponse(row) if row else JSONResponse({"error": "Not found"}, status_code=404)
        if request.method == "PATCH":
            body = await request.json()
            sm = {'submitted':'submitted','working':'working','completed':'completed',
                  'failed':'failed','input-required':'input-required','canceled':'canceled'}
            fields = {}
            if "state" in body: fields["state"] = sm.get(body["state"], body["state"])
            for k in ["completion_summary","evidence_paths","worker_prompts_csv","error",
                       "reason","next_action","progress","summary","next","evidence"]:
                if k in body: fields[k] = body[k]
            if "summary" in fields: fields.setdefault("completion_summary", fields.pop("summary"))
            if "next" in fields: fields.setdefault("next_action", fields.pop("next"))
            if "evidence" in fields: fields.setdefault("evidence_paths", fields.pop("evidence"))
            self.task_store.update_fields(task_id, **{k:v for k,v in fields.items() if v})
            row = self.task_store.raw_rpc("a2a_task.get", {"task_id": task_id}).get("record")
            return JSONResponse(row or {})
        return JSONResponse({"error": "Method Not Allowed"}, status_code=405)

    async def _latest_manager(self, request: Request):
        rows = self.task_store.get_all_dicts()
        mgr = [r for r in rows if r.get("agent_id", "").startswith("manager")]
        mgr.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        return JSONResponse(mgr[0] if mgr else {})

    async def _pending_delivery(self, request: Request):
        rows = self.task_store.get_all_dicts()
        pending = [r for r in rows if r.get("delivery_status") == "pending" and r.get("agent_id") == "worker"]
        pending.sort(key=lambda r: r.get("created_at", ""))
        return JSONResponse({"tasks": pending})

    async def _launched_pids(self, request: Request):
        raw_key = request.query_params.get("raw_key", "")
        result = []
        for r in self.task_store.get_all_dicts():
            if r.get("agent_id") == "worker" and r.get("state") == "working" and r.get("worker_pid"):
                if not raw_key or r.get("raw_key") == raw_key:
                    result.append({"task_id": r["task_id"], "worker_pid": r["worker_pid"],
                                   "worktree": r.get("worktree", "")})
        return JSONResponse({"rows": result})

    # ── Lifecycle ──────────────────────────────────────────────────────

    def start(self):
        """Start A2A Server with configured transport(s)."""
        app = self._build_app()

        if self.listen_mode in ("unix", "both"):
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
            uds_config = uvicorn.Config(app=app, uds=self.socket_path,
                                        log_level="info", access_log=False)
            uds_server = uvicorn.Server(uds_config)
            self._servers.append(uds_server)
            import threading
            t = threading.Thread(target=uds_server.run, daemon=True, name="a2a-uds")
            t.start()
            print(f"[A2A Gateway] Unix socket: {self.socket_path}")

        if self.listen_mode in ("tcp", "both"):
            tcp_config = uvicorn.Config(app=app, host=self.tcp_host, port=self.tcp_port,
                                        log_level="info", access_log=False)
            tcp_server = uvicorn.Server(tcp_config)
            self._servers.append(tcp_server)
            import threading
            t = threading.Thread(target=tcp_server.run, daemon=True, name="a2a-tcp")
            t.start()
            print(f"[A2A Gateway] TCP: {self.tcp_host}:{self.tcp_port}")

        if not self._servers:
            raise RuntimeError(f"Invalid A2A_LISTEN_MODE={self.listen_mode}")

        self._running = True
        # Keep main thread alive
        try:
            while self._running:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop all A2A Servers."""
        self._running = False
        for srv in self._servers:
            srv.should_exit = True
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        self._servers.clear()
        print("[A2A Gateway] Stopped")


# ── CLI ──────────────────────────────────────────────────────────────────

def _pid_file(project: str) -> str:
    return f"/tmp/freely-a2a-{_short_hash(project)}.pid"

def main():
    parser = argparse.ArgumentParser(description="Freely A2A Gateway (local + network)")
    parser.add_argument("--project", required=True)
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--tcp-host", default="")
    parser.add_argument("--tcp-port", type=int, default=0)
    parser.add_argument("--listen-mode", default="")  # unix|tcp|both
    args = parser.parse_args()
    sp = _socket_path(args.project)
    pf = _pid_file(args.project)

    if args.stop:
        # Graceful stop via PID file (aligns with JiuwenSwarm signal pattern)
        if os.path.exists(pf):
            try:
                with open(pf) as f:
                    pid = int(f.read().strip())
                os.kill(pid, 15)  # SIGTERM → triggers A2AServer.stop()
                import time
                for _ in range(50):
                    try: os.kill(pid, 0); time.sleep(0.1)
                    except OSError: break
                try: os.kill(pid, 0); os.kill(pid, 9)
                except OSError: pass
                print(f"[A2A Gateway] Stopped (PID {pid})")
            except (ValueError, OSError) as e:
                print(f"[A2A Gateway] Warning: {e}")
            if os.path.exists(pf): os.remove(pf)
        if os.path.exists(sp):
            os.remove(sp)
    elif args.start:
        with open(pf, 'w') as f:
            f.write(str(os.getpid()))
        import signal
        if args.listen_mode:
            os.environ["A2A_LISTEN_MODE"] = args.listen_mode
        srv = A2AServer(project=args.project, socket_path=sp,
                        tcp_host=args.tcp_host, tcp_port=args.tcp_port)

        def _on_term(signum, frame):
            srv.stop()
            if os.path.exists(pf): os.remove(pf)
            os._exit(0)
        signal.signal(signal.SIGTERM, _on_term)
        signal.signal(signal.SIGINT, _on_term)

        try: srv.start()
        except KeyboardInterrupt: srv.stop()
        finally:
            if os.path.exists(pf): os.remove(pf)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""acp_bridge_v2.py — ACP Bridge using official agent-client-protocol SDK.

Persistent Unix-socket relay between AI CLI agents (claude-agent-acp, codex-acp,
opencode) and Freely's monitor scripts. Uses the official agent-client-protocol
SDK (v0.10.1) for type-safe JSON-RPC communication.

Architecture:
  asyncio event loop
    ├─ async with spawn_agent_process(agent, "claude-agent-acp") → connection + process
    ├─ asyncio.start_unix_server(handle_client, socket_path)
    └─ handle_client: read JSON-RPC → call Agent sync methods → write response

Agent methods are SYNC (not async) — they return Pydantic response models directly:
  agent.new_session(cwd=..., mcp_servers=...) → NewSessionResponse(session_id=...)
  agent.resume_session(cwd=..., session_id=...) → ResumeSessionResponse(session_id=...)
  agent.prompt(prompt=[text_block(...)], session_id=...) → PromptResponse(stop_reason=...)
"""

import argparse
import asyncio
import hashlib
import json
import os
import sys
from typing import Optional, List, Any

from acp import (
    Agent,
    text_block,
    spawn_agent_process,
)


def _now_utc() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


class AcpBridgeV2:
    """Persistent ACP bridge using official SDK with asyncio event loop.

    Spawns an ACP agent subprocess via the SDK's async context manager,
    exposes a Unix socket for JSON-RPC clients.
    """

    def __init__(self, project: str, acp_bin: str, acp_args: Optional[List[str]] = None,
                 permission_mode: str = "default"):
        self.project = os.path.abspath(project)
        self.acp_bin = acp_bin
        self.acp_args = acp_args or []
        self.permission_mode = permission_mode
        self.socket_path = f"/tmp/freely-acp-{_short_hash(project)}.sock"
        self.pid_file = f"/tmp/freely-acp-{_short_hash(project)}.pid"
        self.log_path = os.path.join(project, ".freely", "run", "acp-bridge.log")

        self._agent: Optional[Agent] = None
        self._conn: Any = None
        self._proc: Any = None
        self._session_id: Optional[str] = None
        self._running = False

    def _log(self, msg: str) -> None:
        ts = _now_utc()
        line = f"[{ts}] [acp-bridge-v2] {msg}"
        print(line, file=sys.stderr, flush=True)
        try:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, "a") as f:
                f.write(line + "\n")
        except OSError:
            pass

    # ── Agent operations (sync — Agent methods return Pydantic models directly) ──

    def session_new(self, cwd: str = "", mcp_servers: Optional[List] = None) -> Optional[str]:
        if self._agent is None:
            self._log("agent not initialized")
            return None
        try:
            resp = self._agent.new_session(
                cwd=cwd or self.project,
                mcp_servers=mcp_servers or [],
            )
            self._session_id = resp.session_id
            self._log(f"session/new → {self._session_id}")
            if self.permission_mode != "default":
                try:
                    self._agent.set_session_mode(mode_id=self.permission_mode, session_id=self._session_id)
                except Exception:
                    pass
            return self._session_id
        except Exception as e:
            self._log(f"session/new failed: {e}")
            return None

    def session_resume(self, session_id: str, cwd: str = "") -> Optional[str]:
        if self._agent is None:
            return None
        try:
            resp = self._agent.resume_session(
                cwd=cwd or self.project,
                session_id=session_id,
            )
            self._session_id = resp.session_id
            self._log(f"session/resume → {self._session_id}")
            return self._session_id
        except Exception as e:
            self._log(f"session/resume failed: {e}")
            return None

    def session_prompt(self, prompt_text: str) -> dict:
        if self._agent is None or self._session_id is None:
            return {"error": "no active session"}
        try:
            resp = self._agent.prompt(
                prompt=[text_block(prompt_text)],
                session_id=self._session_id,
            )
            return {
                "stop_reason": resp.stop_reason or "",
                "usage": {
                    "input": resp.usage.input_tokens if resp.usage else 0,
                    "output": resp.usage.output_tokens if resp.usage else 0,
                } if resp.usage else {},
            }
        except Exception as e:
            self._log(f"session/prompt error: {e}")
            return {"error": str(e)}

    # ── Asyncio server ──────────────────────────────────────────────────────

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            data = await asyncio.wait_for(reader.read(65536), timeout=30.0)
            if not data:
                return
            request = json.loads(data.decode("utf-8", errors="replace"))
            method = request.get("method", "")
            req_id = request.get("id", 0)
            params = request.get("params", {})

            response = {"jsonrpc": "2.0", "id": req_id}

            if method == "session/new":
                sid = self.session_new(
                    cwd=params.get("cwd", ""),
                    mcp_servers=params.get("mcpServers"),
                )
                response["result" if sid else "error"] = (
                    {"sessionId": sid} if sid else {"code": -1, "message": "session_new failed"}
                )

            elif method == "session/resume":
                sid = self.session_resume(
                    session_id=params.get("sessionId", ""),
                    cwd=params.get("cwd", ""),
                )
                response["result" if sid else "error"] = (
                    {"sessionId": sid} if sid else {"code": -1, "message": "session_resume failed"}
                )

            elif method == "session/prompt":
                result = self.session_prompt(params.get("prompt", ""))
                response["result"] = result

            elif method == "ping":
                response["result"] = "pong"

            elif method == "shutdown":
                self._running = False
                response["result"] = "ok"

            else:
                response["error"] = {"code": -32601, "message": f"unknown method: {method}"}

            writer.write(json.dumps(response, default=str).encode() + b"\n")
            await writer.drain()
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            try:
                err = {"jsonrpc": "2.0", "id": 0, "error": {"code": -32603, "message": str(e)}}
                writer.write(json.dumps(err).encode() + b"\n")
                await writer.drain()
            except Exception:
                pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def _serve(self) -> None:
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        server = await asyncio.start_unix_server(self._handle_client, path=self.socket_path)
        os.chmod(self.socket_path, 0o600)
        self._log(f"listening on {self.socket_path}")
        async with server:
            await server.serve_forever()

    async def _run(self) -> None:
        agent = Agent()
        self._agent = agent
        async with spawn_agent_process(
            to_client=agent,
            command=self.acp_bin,
            *self.acp_args,
            cwd=self.project,
        ) as (conn, proc):
            self._conn = conn
            self._proc = proc
            self._running = True
            self._write_pid()
            agent.initialize(protocol_version=1)
            await self._serve()

    def start(self) -> None:
        self._log(f"starting bridge: {self.acp_bin} {' '.join(self.acp_args)}")
        asyncio.run(self._run())

    def stop(self) -> None:
        self._running = False
        for path in [self.socket_path, self.pid_file]:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass

    def _write_pid(self) -> None:
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))
        except Exception:
            pass


def main():
    # SDK hard requirement — fail early with a clear message
    try:
        from acp import Agent  # noqa: F401
    except ImportError:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  agent-client-protocol SDK 未安装                              ║
║                                                              ║
║  Freely ACP bridge 需要官方 Python SDK 与 AI 工具通信。         ║
║                                                              ║
║  安装:  pip3 install agent-client-protocol                    ║
║  (PEP 668): pip3 install --break-system-packages \\           ║
║                    agent-client-protocol                      ║
║                                                              ║
║  验证:  python3 -c "from acp import Agent; print('OK')"       ║
╚══════════════════════════════════════════════════════════════╝
""", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="ACP Bridge (SDK-based, async)")
    parser.add_argument("--project", required=True, help="Project path")
    parser.add_argument("--acp-bin", required=True, help="ACP binary (e.g. claude-agent-acp)")
    parser.add_argument("--acp-args", nargs="*", default=[], help="Extra args for ACP binary")
    parser.add_argument("--permission-mode", default="default", help="Permission mode")
    parser.add_argument("--foreground", action="store_true", help="Run in foreground")
    args = parser.parse_args()

    bridge = AcpBridgeV2(
        project=args.project,
        acp_bin=args.acp_bin,
        acp_args=args.acp_args,
        permission_mode=args.permission_mode,
    )
    bridge.start()


if __name__ == "__main__":
    main()

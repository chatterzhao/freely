#!/usr/bin/env python3
"""a2a_registry.py — A2A Agent Registry (A2X-style service discovery)

Aligns with JiuwenSwarm's A2X Registry pattern.
Enables Freely worktrees on different machines to discover each other.

Usage:
  Server:  python3 a2a_registry.py --start --port 8000
  Client:  python3 a2a_registry.py --register --endpoint http://host:19100 --role worker
           python3 a2a_registry.py --discover --role worker
"""

import argparse
import json
import os
import time
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict

# ── Data Models ──────────────────────────────────────────────────────────

@dataclass
class AgentRegistration:
    endpoint: str
    role: str  # "manager" | "worker"
    worktree: str = ""
    branch: str = ""
    skills: List[str] = field(default_factory=list)
    registered_at: str = ""
    last_heartbeat: str = ""
    ttl_seconds: int = 60

    def is_expired(self) -> bool:
        if not self.last_heartbeat:
            return False
        try:
            dt = datetime.fromisoformat(self.last_heartbeat)
            age = (datetime.now(timezone.utc) - dt).total_seconds()
            return age > self.ttl_seconds
        except:
            return False


class AgentRegistry:
    """In-memory agent registry with TTL-based expiration."""

    def __init__(self):
        self._agents: Dict[str, AgentRegistration] = {}
        self._lock = threading.RLock()
        self._cleanup_thread: Optional[threading.Thread] = None
        self._running = False

    def register(self, endpoint: str, role: str, worktree: str = "",
                 branch: str = "", skills: List[str] = None,
                 ttl: int = 60) -> AgentRegistration:
        with self._lock:
            now = datetime.now(timezone.utc).isoformat()
            if endpoint in self._agents:
                reg = self._agents[endpoint]
                reg.last_heartbeat = now
                reg.ttl_seconds = ttl
                if worktree: reg.worktree = worktree
                if branch: reg.branch = branch
                if skills: reg.skills = skills
            else:
                reg = AgentRegistration(
                    endpoint=endpoint, role=role, worktree=worktree,
                    branch=branch, skills=skills or [],
                    registered_at=now, last_heartbeat=now, ttl_seconds=ttl)
                self._agents[endpoint] = reg
            return reg

    def deregister(self, endpoint: str) -> bool:
        with self._lock:
            if endpoint in self._agents:
                del self._agents[endpoint]
                return True
            return False

    def discover(self, role: str = "", skill: str = "") -> List[AgentRegistration]:
        with self._lock:
            results = []
            for reg in self._agents.values():
                if reg.is_expired():
                    continue
                if role and reg.role != role:
                    continue
                if skill and skill not in reg.skills:
                    continue
                results.append(reg)
            return results

    def heartbeat(self, endpoint: str) -> bool:
        with self._lock:
            if endpoint in self._agents:
                self._agents[endpoint].last_heartbeat = datetime.now(timezone.utc).isoformat()
                return True
            return False

    def cleanup_expired(self) -> int:
        with self._lock:
            expired = [ep for ep, reg in self._agents.items() if reg.is_expired()]
            for ep in expired:
                del self._agents[ep]
            return len(expired)

    def start_cleanup_thread(self, interval: int = 30):
        self._running = True
        def _loop():
            while self._running:
                time.sleep(interval)
                n = self.cleanup_expired()
                if n:
                    print(f"[A2A Registry] Cleaned {n} expired agents")
        self._cleanup_thread = threading.Thread(target=_loop, daemon=True)
        self._cleanup_thread.start()

    def stop(self):
        self._running = False


# ── HTTP Server ──────────────────────────────────────────────────────────

def _run_server(port: int, registry: AgentRegistry):
    """Run a minimal HTTP registry server (no dependencies beyond stdlib)."""
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class RegistryHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self._json(200, {"status": "ok"})
            elif self.path.startswith("/discover"):
                role = self._query_param("role", "")
                skill = self._query_param("skill", "")
                agents = registry.discover(role=role, skill=skill)
                self._json(200, {"agents": [asdict(a) for a in agents]})
            elif self.path == "/agents":
                agents = registry.discover()
                self._json(200, {"agents": [asdict(a) for a in agents]})
            else:
                self._json(404, {"error": "Not Found"})

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}
            if self.path == "/register":
                reg = registry.register(
                    endpoint=body.get("endpoint", ""),
                    role=body.get("role", "worker"),
                    worktree=body.get("worktree", ""),
                    branch=body.get("branch", ""),
                    skills=body.get("skills", []),
                    ttl=body.get("ttl", 60))
                self._json(200, asdict(reg))
            elif self.path == "/heartbeat":
                ok = registry.heartbeat(body.get("endpoint", ""))
                self._json(200 if ok else 404, {"ok": ok})
            elif self.path.startswith("/deregister"):
                ok = registry.deregister(body.get("endpoint", ""))
                self._json(200, {"ok": ok})
            else:
                self._json(404, {"error": "Not Found"})

        def _json(self, status, data):
            body = json.dumps(data, default=str).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _query_param(self, key, default=""):
            import urllib.parse
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            vals = params.get(key, [default])
            return vals[0] if vals else default

        def log_message(self, format, *args):
            pass  # quiet

    server = HTTPServer(("0.0.0.0", port), RegistryHandler)
    print(f"[A2A Registry] Listening on 0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


# ── Registry Client ──────────────────────────────────────────────────────

class RegistryClient:
    """Client for the A2A Registry (aligns with JiuwenSwarm's A2XRegistryClient)."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, body: dict = None) -> dict:
        import urllib.request, urllib.error
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return {"error": str(e), "status": e.code}
        except Exception as e:
            return {"error": str(e)}

    def register(self, endpoint: str, role: str = "worker", **kwargs) -> dict:
        return self._request("POST", "/register", {"endpoint": endpoint, "role": role, **kwargs})

    def deregister(self, endpoint: str) -> dict:
        return self._request("POST", "/deregister", {"endpoint": endpoint})

    def discover(self, role: str = "", skill: str = "") -> list:
        params = []
        if role: params.append(f"role={role}")
        if skill: params.append(f"skill={skill}")
        path = "/discover?" + "&".join(params) if params else "/discover"
        return self._request("GET", path).get("agents", [])

    def heartbeat(self, endpoint: str) -> bool:
        return self._request("POST", "/heartbeat", {"endpoint": endpoint}).get("ok", False)

    def health(self) -> bool:
        return self._request("GET", "/health").get("status") == "ok"


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="A2A Agent Registry")
    parser.add_argument("--start", action="store_true", help="Start registry server")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--register", action="store_true", help="Register agent")
    parser.add_argument("--deregister", action="store_true", help="Deregister agent")
    parser.add_argument("--discover", action="store_true", help="Discover agents")
    parser.add_argument("--heartbeat", action="store_true", help="Send heartbeat")
    parser.add_argument("--endpoint", default="", help="Agent endpoint URL")
    parser.add_argument("--role", default="worker", help="Agent role")
    parser.add_argument("--registry-url", default="http://127.0.0.1:8000")
    parser.add_argument("--skill", default="")
    args = parser.parse_args()

    if args.start:
        registry = AgentRegistry()
        registry.start_cleanup_thread()
        _run_server(args.port, registry)
    else:
        client = RegistryClient(base_url=args.registry_url)
        if args.register:
            r = client.register(args.endpoint, role=args.role)
            print(json.dumps(r))
        elif args.deregister:
            r = client.deregister(args.endpoint)
            print(json.dumps(r))
        elif args.discover:
            agents = client.discover(role=args.role, skill=args.skill)
            print(json.dumps(agents, indent=2))
        elif args.heartbeat:
            ok = client.heartbeat(args.endpoint)
            print(json.dumps({"ok": ok}))
        else:
            parser.print_help()


if __name__ == "__main__":
    main()

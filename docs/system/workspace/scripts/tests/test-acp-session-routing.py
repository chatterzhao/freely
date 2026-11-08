#!/usr/bin/env python3
"""AT-001 — raw-20261103T132556Z / #4152 (ACP bridge 按 session 路由避免越权代答).

Isolated unit/integration harness. NO real ACP server, NO real platform: both
`acp-bridge.py` and `run-acp-prompt.py` are loaded as modules from --source-dir
and driven with fake sockets / fake transports / crafted JSON-RPC messages.

Layers under test:
  * client (run-acp-prompt.py, AUTHORITATIVE): a client bound to session B must
    NOT print session A's `agent_message_chunk` and must NOT answer session A's
    `session/request_permission`. Filtering is by *positively-mismatched*
    params.sessionId only; missing/unknown sessionId keeps legacy delivery
    (U6 prerequisite: never drop a message we cannot attribute).
  * bridge (acp-bridge.py, DEFENSE IN DEPTH): server notifications for a known
    session go to the owning client(s) only; unknown/missing session falls back
    to the legacy broadcast (never drop).
  * permission default: bypassPermissions is no longer the silent default; it
    requires explicit opt-in, CLAUDE_CODE_PERMISSION_MODE stays authoritative.

Run:
  python3 test-acp-session-routing.py [--source-dir DIR] [static|behavior|all]
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
# tests/ -> scripts/ (1 up) -> workspace (2) -> system (3) -> docs (4) -> repo (5)
REPO = HERE.parent.parent.parent.parent.parent
DEFAULT_SRC = REPO / "docs" / "system" / "workspace" / "scripts" / "runtime"

# Force the legacy in-process implementation; otherwise acp-bridge.py execv's
# into acp_bridge_v2.py when the acp SDK is importable (which would replace the
# test process). This matches the live runtime here (SDK not installed).
os.environ["FREELY_ACP_USE_SDK"] = "0"

PASS = 0
FAIL = 0


def ok(msg):
    global PASS
    PASS += 1
    print(f"  [ok] {msg}")


def bad(msg):
    global FAIL
    FAIL += 1
    print(f"  [FAIL] {msg}")


def load_module(name, src_dir, filename):
    path = Path(src_dir) / filename
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── fakes ────────────────────────────────────────────────────────────────
class FakeTransport:
    """Minimal transport for ACPClient: recv thread must exit immediately."""
    def __init__(self):
        self.sent = []

    def running(self):
        return False  # _recv_loop exits without blocking

    def recv(self):
        raise EOFError("closed")

    def send(self, line):
        self.sent.append(line)

    def close(self):
        pass


class FakeSock:
    def __init__(self):
        self.received = []

    def send(self, data):
        self.received.append(data)
        return len(data)


def set_session(client, sid):
    if hasattr(client, "set_session_id"):
        client.set_session_id(sid)
    else:  # baseline has no session_id at all
        client.session_id = sid


def make_update(sid, text):
    """server -> client: session/update carrying an agent_message_chunk."""
    msg = {
        "jsonrpc": "2.0",
        "method": "session/update",
        "params": {
            "update": {
                "sessionUpdate": "agent_message_chunk",
                "content": {"type": "text", "text": text},
            },
        },
    }
    if sid is not None:
        msg["params"]["sessionId"] = sid
    return msg


def make_permission(sid):
    """server -> client: session/request_permission (needs a response)."""
    msg = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "session/request_permission",
        "params": {
            "options": [
                {"kind": "allow_always", "optionId": "o-always"},
                {"kind": "allow_once", "optionId": "o-once"},
                {"kind": "reject_once", "optionId": "o-reject"},
            ],
        },
    }
    if sid is not None:
        msg["params"]["sessionId"] = sid
    return msg


# ── static checks ────────────────────────────────────────────────────────
def static_checks(src_dir):
    client_src = (Path(src_dir) / "run-acp-prompt.py").read_text(encoding="utf-8")
    bridge_src = (Path(src_dir) / "acp-bridge.py").read_text(encoding="utf-8")

    # GREEN#3: sessionId must appear on an INBOUND filter path (before def main).
    # Baseline: sessionId appears ONLY in outbound request params inside main().
    try:
        pre_main = client_src[: client_src.index("def main(")]
    except ValueError:
        pre_main = client_src
    if "sessionId" in pre_main:
        ok("static: sessionId referenced before main() (inbound filter present)")
    else:
        bad("static: sessionId NOT in inbound filter path (only outbound params)")

    if "_inbound_session_mismatch" in client_src:
        ok("static: client has _inbound_session_mismatch filter helper")
    else:
        bad("static: client lacks _inbound_session_mismatch filter helper")

    # GREEN#4: bypassPermissions explicit opt-in gate + routing registry.
    if "FREELY_ACP_BYPASS_PERMISSIONS" in bridge_src:
        ok("static: bypassPermissions requires explicit opt-in")
    else:
        bad("static: bypassPermissions is still a silent default")

    if "client_sessions" in bridge_src:
        ok("static: bridge tracks per-client session routing")
    else:
        bad("static: bridge has no session registry")


# ── behavior: client (authoritative fix) ─────────────────────────────────
def client_checks(src_dir):
    mod = load_module("acp_client_under_test", src_dir, "run-acp-prompt.py")

    def new_client(sid="B", mode="auto"):
        t = FakeTransport()
        c = mod.ACPClient(transport=t, mode=mode)
        set_session(c, sid)
        return c, t

    # RED#1: foreign session's chunk must NOT be printed to our stdout.
    c, _ = new_client("B")
    buf = io.StringIO()
    with redirect_stdout(buf):
        c._handle_message(make_update("A", "SECRET-A-CHUNK"))
    if "SECRET-A-CHUNK" not in buf.getvalue():
        ok("client: foreign-session agent_message_chunk dropped (B stdout clean)")
    else:
        bad("client: foreign-session chunk LEAKED into B stdout")

    # no-regression: own session's chunk IS printed.
    c, _ = new_client("B")
    buf = io.StringIO()
    with redirect_stdout(buf):
        c._handle_message(make_update("B", "OWN-B-CHUNK"))
    if "OWN-B-CHUNK" in buf.getvalue():
        ok("client: own-session chunk still printed (no regression)")
    else:
        bad("client: own-session chunk was wrongly dropped")

    # U6: chunk with NO sessionId is preserved (never drop unattributable msg).
    c, _ = new_client("B")
    buf = io.StringIO()
    with redirect_stdout(buf):
        c._handle_message(make_update(None, "NO-SID-CHUNK"))
    if "NO-SID-CHUNK" in buf.getvalue():
        ok("client: no-sessionId chunk preserved (U6 no-message-loss)")
    else:
        bad("client: no-sessionId chunk wrongly dropped")

    # U6: unknown own session (None) preserves legacy delivery.
    c, _ = new_client(None)
    buf = io.StringIO()
    with redirect_stdout(buf):
        c._handle_message(make_update("A", "UNKNOWN-OWN-CHUNK"))
    if "UNKNOWN-OWN-CHUNK" in buf.getvalue():
        ok("client: unknown-own-session preserved (no regression)")
    else:
        bad("client: unknown-own-session wrongly dropped")

    # RED#2a: foreign permission request must NOT be answered via _handle_message.
    c, t = new_client("B")
    c._handle_message(make_permission("A"))
    if not t.sent:
        ok("client: foreign permission request not answered (inbound filter)")
    else:
        bad("client: foreign permission request was auto-answered")

    # RED#2b / fix#2: _handle_permission_request itself refuses foreign session.
    c, t = new_client("B")
    c._handle_permission_request(make_permission("A"))
    if not t.sent:
        ok("client: permission handler refuses foreign session (no allow)")
    else:
        bad("client: permission handler auto-allowed a foreign session")

    # no-regression: own permission request still auto-answered with allow.
    c, t = new_client("B")
    c._handle_message(make_permission("B"))
    joined = " ".join(t.sent)
    if "o-always" in joined or "o-once" in joined:
        ok("client: own permission request still auto-answered (no regression)")
    else:
        bad("client: own permission request was not answered")

    # step mode + foreign session: must also never answer.
    c, t = new_client("B", mode="step")
    c._handle_message(make_permission("A"))
    if not t.sent:
        ok("client: step mode drops foreign permission (no allow/reject)")
    else:
        bad("client: step mode answered a foreign permission request")


# ── behavior: bridge (defense in depth) ──────────────────────────────────
def bridge_checks(src_dir):
    mod = load_module("acp_bridge_under_test", src_dir, "acp-bridge.py")

    def new_bridge():
        b = mod.AcpBridge.__new__(mod.AcpBridge)
        b.clients_lock = threading.Lock()
        b.clients = []
        b.client_sessions = {}  # fixed version uses it; baseline ignores it
        b.log_file = tempfile.mktemp(prefix="r14-bridge-", suffix=".log")
        return b

    def wire(b, mapping):
        socks = {}
        for label, sid in mapping.items():
            s = FakeSock()
            socks[label] = s
            b.clients.append(s)
        # register per-socket session ownership (fixed version only)
        for label, s in socks.items():
            sid = mapping[label]
            if sid is not None:
                b.client_sessions.setdefault(s, set()).add(sid)
        return socks

    # targeted delivery: server sends session A notification -> only A's client.
    b = new_bridge()
    socks = wire(b, {"A": "A", "B": "B"})
    b._broadcast_notification(make_update("A", "FOR-A"))
    a_bytes = b"".join(socks["A"].received).decode("utf-8", "replace")
    b_bytes = b"".join(socks["B"].received).decode("utf-8", "replace")
    if "FOR-A" in a_bytes and "FOR-A" not in b_bytes:
        ok("bridge: session A notification delivered to A only")
    else:
        bad("bridge: session A notification leaked to B (broadcast)")

    # no-regression / U6: unknown session falls back to broadcast (never drop).
    b = new_bridge()
    socks = wire(b, {"A": "A", "B": "B"})
    b._broadcast_notification(make_update("Z", "FOR-UNKNOWN"))
    a_bytes = b"".join(socks["A"].received).decode("utf-8", "replace")
    b_bytes = b"".join(socks["B"].received).decode("utf-8", "replace")
    if "FOR-UNKNOWN" in a_bytes and "FOR-UNKNOWN" in b_bytes:
        ok("bridge: unknown session -> broadcast fallback (no message loss)")
    else:
        bad("bridge: unknown session message was dropped or not broadcast")

    # no-regression / U6: notification with NO sessionId is still broadcast.
    b = new_bridge()
    socks = wire(b, {"A": "A", "B": "B"})
    b._broadcast_notification(make_update(None, "NO-SID"))
    a_bytes = b"".join(socks["A"].received).decode("utf-8", "replace")
    b_bytes = b"".join(socks["B"].received).decode("utf-8", "replace")
    if "NO-SID" in a_bytes and "NO-SID" in b_bytes:
        ok("bridge: no-sessionId notification still broadcast (no regression)")
    else:
        bad("bridge: no-sessionId notification lost")

    # no-regression: empty registry (no session learned yet) -> full broadcast.
    b = new_bridge()
    socks = wire(b, {"A": None, "B": None})
    b._broadcast_notification(make_update("A", "NO-REGISTRY"))
    a_bytes = b"".join(socks["A"].received).decode("utf-8", "replace")
    b_bytes = b"".join(socks["B"].received).decode("utf-8", "replace")
    if "NO-REGISTRY" in a_bytes and "NO-REGISTRY" in b_bytes:
        ok("bridge: empty registry -> broadcast (no regression)")
    else:
        bad("bridge: empty registry lost a message")


# ── behavior: permission default (GREEN#4) ───────────────────────────────
def permission_default_checks(src_dir):
    # Import acp-bridge.py in a clean subprocess; nothing about permission mode
    # may be inherited from the harness environment.
    bridge = Path(src_dir) / "acp-bridge.py"
    code = (
        "import os,importlib.util;"
        "os.environ['FREELY_ACP_USE_SDK']='0';"
        "s=importlib.util.spec_from_file_location('m',r'%s');"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "print(m.ACP_PERMISSION_MODE)" % str(bridge)
    )
    env = dict(os.environ)
    for k in ("CLAUDE_CODE_PERMISSION_MODE", "FREELY_ACP_BYPASS_PERMISSIONS"):
        env.pop(k, None)
    try:
        out = subprocess.check_output(
            [sys.executable, "-c", code], env=env, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception as e:  # pragma: no cover
        out = f"ERROR:{e}"
    if out == "default":
        ok("permission: bare default is 'default' (not bypassPermissions)")
    else:
        bad(f"permission: bare default is '{out}', expected 'default'")

    # explicit opt-in still yields bypassPermissions (escape hatch preserved).
    env2 = dict(env)
    env2["FREELY_ACP_BYPASS_PERMISSIONS"] = "1"
    try:
        out2 = subprocess.check_output(
            [sys.executable, "-c", code], env=env2, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception as e:  # pragma: no cover
        out2 = f"ERROR:{e}"
    if out2 == "bypassPermissions":
        ok("permission: explicit opt-in still enables bypassPermissions")
    else:
        bad(f"permission: opt-in produced '{out2}'")

    # CLAUDE_CODE_PERMISSION_MODE stays authoritative (production byte-identical).
    env3 = dict(env)
    env3["CLAUDE_CODE_PERMISSION_MODE"] = "acceptEdits"
    try:
        out3 = subprocess.check_output(
            [sys.executable, "-c", code], env=env3, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception as e:  # pragma: no cover
        out3 = f"ERROR:{e}"
    if out3 == "acceptEdits":
        ok("permission: CLAUDE_CODE_PERMISSION_MODE remains authoritative")
    else:
        bad(f"permission: authoritative env produced '{out3}'")


def main():
    args = sys.argv[1:]
    src_dir = str(DEFAULT_SRC)
    mode = "all"
    rest = []
    i = 0
    while i < len(args):
        if args[i] == "--source-dir" and i + 1 < len(args):
            src_dir = args[i + 1]
            i += 2
        else:
            rest.append(args[i])
            i += 1
    if rest:
        mode = rest[0]
    if mode not in ("static", "behavior", "all"):
        print(f"usage: {sys.argv[0]} [--source-dir DIR] [static|behavior|all]", file=sys.stderr)
        return 2
    print(f"AT-001 source-dir: {src_dir} mode: {mode}")
    if mode in ("static", "all"):
        static_checks(src_dir)
    if mode in ("behavior", "all"):
        client_checks(src_dir)
        bridge_checks(src_dir)
        permission_default_checks(src_dir)
    print(f"SUMMARY: {PASS} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

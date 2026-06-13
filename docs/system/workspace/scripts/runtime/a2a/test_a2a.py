#!/usr/bin/env python3
"""test_a2a.py — A2A protocol unit tests

Tests cover:
  T1: Parser (state-based, alias handling)
  T2: Registry (register/discover/heartbeat)
  T3: Types (official SDK + custom)
  T4: Client (transport selection, discovery)
  T5: Server setup (routes, executor)

Usage:
  python3 docs/system/workspace/scripts/runtime/a2a/test_a2a.py
"""

import os
import sys
import json
import time
import threading
from dataclasses import asdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, RUNTIME_DIR)
sys.path.insert(0, SCRIPT_DIR)

# ── Test runner ──────────────────────────────────────────────────────────

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = ""

passed = 0
failed = 0

def test(name):
    def decorator(fn):
        def wrapper():
            global passed, failed
            try:
                fn()
                print(f"  ✅ {name}")
                passed += 1
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                global failed_count
                failed += 1
        return wrapper
    return decorator


# ── T1: Parser ───────────────────────────────────────────────────────────

@test("Parser: validates all 6 A2A states")
def test_parser_states():
    from a2a_task_parser import VALID_STATES, extract_task_state
    assert 'submitted' in VALID_STATES
    assert 'working' in VALID_STATES
    assert 'completed' in VALID_STATES
    assert 'failed' in VALID_STATES
    assert 'input-required' in VALID_STATES
    assert 'pending-input' in VALID_STATES
    r = extract_task_state('```json\n{"state":"completed","summary":"done"}\n```')
    assert r['ok'] and r['state'] == 'completed'

@test("Parser: validates required summary field")
def test_parser_required():
    from a2a_task_parser import extract_task_state
    r = extract_task_state('```json\n{"state":"completed"}\n```')
    assert not r['ok']

@test("Parser: rejects invalid state")
def test_parser_invalid():
    from a2a_task_parser import extract_task_state
    r = extract_task_state('```json\n{"state":"invalid"}\n```')
    assert not r['ok']

@test("Parser: natural language aliases")
def test_parser_aliases():
    from a2a_task_parser import normalize_state
    assert normalize_state('done') == 'completed'
    assert normalize_state('delegate') == 'submitted'
    assert normalize_state('blocked') == 'input-required'
    assert normalize_state('stopped') == 'failed'
    assert normalize_state('handoff') == 'pending-input'
    # Valid states pass through
    assert normalize_state('working') == 'working'
    assert normalize_state('completed') == 'completed'

@test("Parser: no exit_kind legacy")
def test_parser_no_exit_kind():
    import a2a_task_parser
    assert not hasattr(a2a_task_parser, 'VALID_EXIT_KINDS')
    assert not hasattr(a2a_task_parser, 'EXIT_KIND_ALIASES')


# ── T2: Registry ─────────────────────────────────────────────────────────

@test("Registry: register and discover")
def test_registry_basic():
    from a2a_registry import AgentRegistry
    reg = AgentRegistry()
    reg.register("http://host1:19100", "worker", worktree="/tmp/wt1")
    reg.register("http://host2:19100", "manager")
    workers = reg.discover(role="worker")
    assert len(workers) == 1
    assert workers[0].endpoint == "http://host1:19100"
    assert workers[0].worktree == "/tmp/wt1"

@test("Registry: heartbeat and cleanup")
def test_registry_heartbeat():
    from a2a_registry import AgentRegistry
    reg = AgentRegistry()
    reg.register("http://host1:19100", "worker", ttl=1)
    time.sleep(0.1)
    assert reg.heartbeat("http://host1:19100")
    n = reg.cleanup_expired()
    assert n == 0  # heartbeat refreshed

@test("Registry: deregister")
def test_registry_deregister():
    from a2a_registry import AgentRegistry
    reg = AgentRegistry()
    reg.register("http://host1:19100", "worker")
    assert reg.deregister("http://host1:19100")
    assert len(reg.discover()) == 0

@test("Registry: discover by skill")
def test_registry_skill():
    from a2a_registry import AgentRegistry
    reg = AgentRegistry()
    reg.register("http://a:19100", "worker", skills=["freely-fix-execution"])
    reg.register("http://b:19100", "worker", skills=["freely-feat-execution"])
    results = reg.discover(skill="freely-fix-execution")
    assert len(results) == 1
    assert results[0].endpoint == "http://a:19100"


# ── T3: Types ────────────────────────────────────────────────────────────

@test("Types: official SDK types available")
def test_official_types():
    from a2a.types import (
        Task, TaskState, Message, Part, Artifact,
        AgentCard, AgentSkill, AgentCapabilities, AgentInterface,
        TaskStatusUpdateEvent, TaskArtifactUpdateEvent,
    )
    card = AgentCard(
        name="Test", description="Test agent",
        capabilities=AgentCapabilities(streaming=True),
        skills=[AgentSkill(id="test", name="Test")],
    )
    assert hasattr(card, 'name')
    assert hasattr(card, 'capabilities')

@test("Types: custom types compatible")
def test_custom_types():
    import a2a_types
    assert len(a2a_types.FREELY_SKILLS) == 7
    assert a2a_types.TaskState.SUBMITTED == 'submitted'
    event = a2a_types.TaskStatusUpdateEvent(
        task_id="t1",
        status=a2a_types.TaskStatus(state="completed"),
    )
    assert hasattr(event, 'task_id')


# ── T4: Client ───────────────────────────────────────────────────────────

@test("Client: local unix transport")
def test_client_local():
    from a2a_task import A2AClient
    c = A2AClient(project="/tmp/test")
    assert c._endpoint.startswith("unix://")

@test("Client: remote http transport")
def test_client_remote():
    from a2a_task import A2AClient
    c = A2AClient(url="http://192.168.1.100:19100")
    assert c._endpoint == "http://192.168.1.100:19100"

@test("Client: agent discovery")
def test_client_discovery():
    from a2a_task import A2AClient
    c = A2AClient(project="/tmp/test")
    endpoints = c.discover_agents()
    assert isinstance(endpoints, list)

@test("Client: connect to agents")
def test_client_connect():
    from a2a_task import A2AClient
    c = A2AClient(project="/tmp/test")
    remote = c.connect("http://other:19100")
    assert remote._url == "http://other:19100"
    local = c.connect("unix:///tmp/test.sock")
    assert local._socket_path == "/tmp/test.sock"

@test("Client: all 21 public API functions")
def test_client_api():
    import a2a_task
    for fn in ['create_task','get_task','update_task','delete_task','list_tasks',
        'list_by_raw_key','list_by_worktree','list_active','list_active_workers',
        'latest_manager','update_message','process_ai_reply','read_state_only',
        'pending_delivery','mark_delivered','set_worker_pid','launched_pids',
        'mark_stale','update_delivery_status','update_worker_pid','get_launched_pids']:
        assert hasattr(a2a_task, fn), f'Missing: {fn}'
        assert callable(getattr(a2a_task, fn)), f'Not callable: {fn}'


# ── T5: Server ───────────────────────────────────────────────────────────

@test("Server: routes are complete")
def test_server_routes():
    import os
    os.environ['A2A_LISTEN_MODE'] = 'unix'
    from a2a_server import A2AServer
    srv = A2AServer(project="/tmp/test", socket_path="/tmp/test.sock")
    app = srv._build_app()
    paths = []
    for route in app.routes:
        if hasattr(route, 'path'):
            paths.append(route.path)
    required = ['/', '/.well-known/agent.json', '/tasks', '/tasks/{task_id:path}',
                '/tasks/latest-manager', '/tasks/pending-delivery', '/tasks/launched-pids']
    for p in required:
        assert p in paths, f'Missing: {p}'

@test("Server: AgentCard has skills")
def test_server_agentcard():
    import os
    os.environ['A2A_LISTEN_MODE'] = 'unix'
    from a2a_server import _build_agent_card
    card = _build_agent_card("/tmp/test")
    assert len(card.skills) == 7
    skill_ids = [s.id for s in card.skills]
    assert 'freely-fix-execution' in skill_ids
    assert card.capabilities.streaming == True

@test("Server: dual transport config")
def test_server_dual():
    import os
    os.environ['A2A_LISTEN_MODE'] = 'both'
    from a2a_server import A2AServer
    srv = A2AServer(project="/tmp/test", socket_path="/tmp/test.sock",
                    tcp_host="127.0.0.1", tcp_port=19101)
    assert srv.listen_mode == 'both'
    assert srv.tcp_host == '127.0.0.1'
    assert srv.tcp_port == 19101

@test("Server: async executor")
def test_server_executor():
    import inspect
    from a2a_server import FreelyAgentExecutor
    assert inspect.iscoroutinefunction(FreelyAgentExecutor.execute)
    assert inspect.iscoroutinefunction(FreelyAgentExecutor.cancel)

@test("Server: SQLiteTaskStore inherits SDK")
def test_server_store():
    from a2a.server.tasks import TaskStore as SDKStore
    from a2a_server import SQLiteTaskStore
    assert issubclass(SQLiteTaskStore, SDKStore)


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    global passed, failed
    print("=== A2A Protocol Tests ===\n")

    # Run all tests
    for name, fn in sorted(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()

    total = passed + failed
    print(f"\n=== Results: {passed}/{total} passed ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""AT-001 — raw-20260807T121205Z / #4109 (reviewer assign raw_key in SSE event).

Bug: a2a-exit's existing-task update path sends only
state/summary/next/evidence/reason, so the a2a_server PATCH handler never puts
raw_key into the `state_update` SSE event. watchdog_sse._handle_needs_reviewer
then hits `FAIL-CLOSED: missing raw_key for reviewer assign` and no reviewer is
ever spawned — phase reviews are silently bypassed.

Fix under test: for a needs-review input-required transition, the update fields
MUST carry raw_key (from --raw-key, else from the task record fetched by task
id). If neither source has it, the transition is rejected (fail-closed) and no
PATCH / SSE event is emitted.

The test drives the real a2a_task.py::_main() CLI branch with a fake A2AClient
(no socket), so it works on a bare Python. Run against two roots:
  RED   : --source-dir <develop root>   (raw_key never emitted -> FAIL)
  GREEN : --source-dir <fix worktree>   (emitted + fail-closed -> PASS)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[5]
SRC = Path(os.environ.get("FREELY_SOURCE_ROOT", str(PROJECT))).resolve()
RAW_KEY = "raw-20260807T121205Z"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


class FakeClient:
    """Minimal A2AClient stand-in: records update calls, serves a task row."""

    def __init__(self, raw_key: str = ""):
        self.row = {"task_id": "t-review"}
        if raw_key:
            self.row["raw_key"] = raw_key
        self.updates: list[dict] = []
        self.created: list[dict] = []

    def get(self, task_id: str) -> dict:
        return dict(self.row)

    def update(self, task_id: str, **fields) -> dict:
        self.updates.append({"task_id": task_id, "fields": dict(fields)})
        return {"ok": True}

    def create(self, **kwargs) -> dict:
        self.created.append(kwargs)
        return {"id": "t-new"}


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(module_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_exit(module_path: Path, argv: list[str], client: FakeClient, tag: str):
    """Drive the real a2a-exit CLI branch; return (parsed stdout, module)."""
    module = load_module(module_path, f"a2a_review_probe_{tag}")
    old_client, old_argv = module._client, sys.argv
    module._client = lambda: client
    sys.argv = ["a2a_task.py"] + argv
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            module._main()
    finally:
        module._client = old_client
        sys.argv = old_argv
    lines = [line for line in buf.getvalue().splitlines() if line.strip().startswith("{")]
    result = json.loads(lines[-1]) if lines else {}
    return result, module


def sse_payload(fields: dict, task_id: str = "t-review") -> dict:
    """Mirror a2a_server.py PATCH handler's state_update SSE payload."""
    return {"task_id": task_id, "state": fields.get("state", ""),
            **{k: v for k, v in fields.items() if k != "state"}}


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: real a2a-exit CLI, needs-review raw_key routing ===")
    module = src / "docs/system/workspace/scripts/runtime/a2a_task.py"
    if not module.is_file():
        for label in ("raw_key resolved from task record is emitted in SSE payload",
                      "missing raw_key is rejected (no PATCH, no SSE event)",
                      "explicit --raw-key wins over task record",
                      "non-review transition unchanged",
                      "watchdog FAIL-CLOSED assertion preserved",
                      "AT wired into bin/test-all CORE and CI_CORE"):
            bad(f"{label} (a2a_task.py missing)")
        return

    # Run from a temp copy so the CLI's last-exit-task.env write never touches SRC.
    probe = tmp / "a2a_task_probe.py"
    shutil.copyfile(module, probe)

    # 1. valid raw_key from the task record must reach the SSE payload (emitted)
    c1 = FakeClient(raw_key=RAW_KEY)
    r1, _ = run_exit(probe, ["a2a-exit", "--state", "blocked", "--role", "worker",
                             "--reason", "needs-review:b1", "--task-id", "t-review",
                             "--summary", "B1 done"], c1, "record")
    emitted = bool(r1.get("ok")) and len(c1.updates) == 1
    payload = sse_payload(c1.updates[0]["fields"]) if c1.updates else {}
    expect(emitted and payload.get("raw_key") == RAW_KEY,
           "raw_key resolved from task record is emitted in SSE payload "
           f"(payload_raw_key={payload.get('raw_key')!r}, ok={r1.get('ok')})")

    # 2. genuinely missing raw_key must be rejected, with no PATCH / SSE event
    c2 = FakeClient(raw_key="")
    r2, _ = run_exit(probe, ["a2a-exit", "--state", "blocked", "--role", "worker",
                             "--reason", "needs-review:b2", "--task-id", "t-review",
                             "--summary", "B2 done"], c2, "missing")
    expect(r2.get("ok") is False and not c2.updates,
           "missing raw_key is rejected (no PATCH, no SSE event) "
           f"(ok={r2.get('ok')}, updates={len(c2.updates)})")

    # 3. explicit --raw-key takes precedence over the stored row
    c3 = FakeClient(raw_key=RAW_KEY)
    r3, _ = run_exit(probe, ["a2a-exit", "--state", "blocked", "--role", "worker",
                             "--reason", "needs-review:red", "--task-id", "t-review",
                             "--raw-key", RAW_KEY], c3, "explicit")
    f3 = c3.updates[0]["fields"] if c3.updates else {}
    expect(bool(r3.get("ok")) and f3.get("raw_key") == RAW_KEY,
           "explicit --raw-key wins over task record "
           f"(field={f3.get('raw_key')!r})")

    # 4. non-review transitions must not gain a new raw_key field
    c4 = FakeClient(raw_key=RAW_KEY)
    r4, _ = run_exit(probe, ["a2a-exit", "--state", "completed", "--role", "worker",
                             "--task-id", "t-review", "--summary", "done"], c4, "plain")
    f4 = c4.updates[0]["fields"] if c4.updates else {}
    expect(bool(r4.get("ok")) and "raw_key" not in f4,
           "non-review transition unchanged (no raw_key added)")

    # 5. watchdog's last-resort FAIL-CLOSED guard must remain intact
    watchdog = src / "docs/system/workspace/scripts/runtime/watchdog_sse.py"
    wtext = watchdog.read_text(encoding="utf-8") if watchdog.is_file() else ""
    expect("FAIL-CLOSED: missing raw_key for reviewer assign" in wtext,
           "watchdog FAIL-CLOSED assertion preserved")

    # 6. the AT must be wired into both aggregate lists
    aggregate = src / "bin/test-all"
    atext = aggregate.read_text(encoding="utf-8", errors="replace") if aggregate.is_file() else ""
    expect(atext.count("test-reviewer-assign-raw-key") >= 2,
           "AT wired into bin/test-all CORE and CI_CORE "
           f"(occurrences={atext.count('test-reviewer-assign-raw-key')})")


def main() -> int:
    global SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            SRC = Path(sys.argv[idx + 1]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="review-raw-key-at-"))
    try:
        behavior_checks(SRC, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

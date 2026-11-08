#!/usr/bin/env python3
"""AT-001 — raw-20261108T092758Z / #4225 (create-time replica duplication).

After a degraded pull (R6/#4182) the local ``platform_ids`` cache can be
partial: it may list only Gitee even though a canonical GitHub replica already
exists. ``issue-sync create`` then treats "missing locally" as "absent on the
platform" and builds a DUPLICATE replica, which makes ``_resolve_raw_identity``
return ``ambiguous`` and hard-blocks reconciliation. ``issue-sync close`` on the
same partial cache closes only the cached replicas, leaving the others OPEN.

This harness is fully isolated: no real platform, no network, no real repo. It
builds a temp project tree with a fake ``platform-adapter.py`` (configurable
``discover-raw`` receipt + ``close-multi`` logger), fake ``gh`` / ``gitee-issue.py``
that log create calls, and a real copy of ``issue-sync`` sourced as a library.

Run against two source roots:
  RED   : --source-dir /tmp/<develop-baseline>   (no guard → duplicates)
  GREEN : --source-dir <this worktree>            (guard → idempotent + heal)
  python3 test-issue-sync-replica-guard.py [--source-dir DIR] [static|unit|behavior|all]
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent.parent.parent
SRC = Path(os.environ.get("ACP_SOURCE_ROOT", str(REPO))).resolve()

RAW_KEY = "20260101T000000Z"
LOCAL_ID = f"raw-{RAW_KEY}"
I_ID = f"I-{RAW_KEY}-A"

PASS = 0
FAIL = 0


def ok(msg: str) -> None:
    global PASS
    PASS += 1
    print(f"  [ok] {msg}")


def bad(msg: str) -> None:
    global FAIL
    FAIL += 1
    print(f"  [FAIL] {msg}")


def _sync_dir(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "sync"


def _lifecycle_dir(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "lifecycle"


def _runtime_dir(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "runtime"


# ── fixture ────────────────────────────────────────────────────────────────
STUB_ADAPTER = r'''import json, os, sys
log = os.environ.get("STUB_LOG", "")
argv = sys.argv[1:]
if log:
    with open(log, "a") as f:
        f.write("ADAPTER " + " ".join(argv) + "\n")
cmd = argv[0] if argv else ""
if cmd == "discover-raw":
    print(os.environ.get("STUB_DISCOVER", "{}"))
elif cmd == "close-multi":
    print(json.dumps({"github": {"status": "closed"}, "gitee": {"status": "closed"}}))
elif cmd == "create-issue":
    print(json.dumps({"github": {"status": "created", "issue_id": "999"},
                      "gitee": {"status": "created", "issue_id": "ZZ9"}}))
else:
    print("{}")
'''

STUB_GITEE = r'''import json, os, sys
log = os.environ.get("STUB_LOG", "")
if log:
    with open(log, "a") as f:
        f.write("GITEE " + " ".join(sys.argv[1:]) + "\n")
argv = sys.argv[1:]
if "create" in argv:
    print(json.dumps({"number": "NEWA1"}))
elif "close" in argv:
    print(json.dumps({"number": "A1", "state": "closed"}))
else:
    print(json.dumps({"ok": True}))
'''

STUB_GH = r'''#!/usr/bin/env bash
log="${STUB_LOG:-/dev/null}.gh"
echo "$*" >> "$log"
case "$*" in
  "repo view --json nameWithOwner -q .nameWithOwner") echo "o/r"; exit 0 ;;
  issue\ create*) echo "https://github.com/o/r/issues/NEW88"; exit 0 ;;
  issue\ close*) exit 0 ;;
  issue\ edit*) exit 0 ;;
  *) exit 0 ;;
esac
'''


def write_doc(fix: Path, platform_ids: dict, phase: str = "proposed",
              canonical: bool = False) -> Path:
    """Strict 22-field frontmatter in canonical order, using raw_title values."""
    import yaml
    fm = {
        "schema_version": "1",
        "local_id": LOCAL_ID,
        "kind": "raw",
        "phase_state": phase,
        "absorbed_into": I_ID if phase == "absorbed" else "",
        "platform_ids": platform_ids,
        "primary_platform": "github",
        "canonical_issue_path": (
            f"docs/B2-docs/acp/x/{LOCAL_ID}/issues/{I_ID}.md"
            if (canonical or phase == "absorbed") else ""),
        "last_synced_comment_at": {},
        "hash": "",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "intake_id": "",
        "author": "platform",
        "channel": "github",
        "session_refs": [],
        "platform_state": "open",
        "promoted_children": [I_ID] if phase == "absorbed" else [],
        "source_candidate": "",
        "completed_at": "2026-01-02T00:00:00Z" if phase == "absorbed" else "",
        "closeout_note": "",
    }
    rendered = yaml.safe_dump(fm, default_flow_style=False,
                              allow_unicode=True, sort_keys=False).strip()
    p = fix / "docs" / "B1-docs" / LOCAL_ID / "issue.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\n{rendered}\n---\n\n# probe issue\n")
    if phase == "absorbed":
        canon = fix / fm["canonical_issue_path"]
        canon.parent.mkdir(parents=True, exist_ok=True)
        canon.write_text(f"# {I_ID}: probe\n")
    return p


def build_fixture() -> Path:
    fix = Path(tempfile.mkdtemp(prefix="freely-replica-guard."))
    (fix / "bin").mkdir(parents=True)
    (fix / "stub").mkdir()
    sync = fix / "docs" / "system" / "workspace" / "scripts" / "sync"
    life = fix / "docs" / "system" / "workspace" / "scripts" / "lifecycle"
    rt = fix / "docs" / "system" / "workspace" / "scripts" / "runtime"
    sync.mkdir(parents=True)
    life.mkdir(parents=True)
    rt.mkdir(parents=True)
    # Real code under test / helpers copied from SOURCE root.
    shutil.copy(SRC / "bin" / "issue-sync", fix / "bin" / "issue-sync")
    for name in ("raw_title_contract.py", "replica_guard.py"):
        f = _sync_dir(SRC) / name
        if f.exists():
            shutil.copy(f, sync / name)
    for name in ("raw_metadata_contract.py", "raw_lifecycle_effects.py"):
        f = _lifecycle_dir(SRC) / name
        if f.exists():
            shutil.copy(f, life / name)
    # Stub platform adapter (source of the discover-raw receipt + close-multi log).
    (sync / "platform-adapter.py").write_text(STUB_ADAPTER)
    (rt / "gitee-issue.py").write_text(STUB_GITEE)
    gh = fix / "stub" / "gh"
    gh.write_text(STUB_GH)
    gh.chmod(0o755)
    return fix


def env_for(fix: Path, discover: str = "{}") -> dict:
    env = dict(os.environ)
    env.update({
        "ROOT_DIR": str(fix),
        "GH_REPO": "o/r",
        "GITEE_REPO": "o/r",
        "FREELY_REPO_PLATFORMS": "github,gitee",
        "STUB_LOG": str(fix / "stub-log.txt"),
        "STUB_DISCOVER": discover,
        "PATH": f"{fix}/stub:{env.get('PATH','')}",
        "PYTHONPATH": f"{fix}/docs/system/workspace/scripts/lifecycle",
    })
    (fix / "stub-log.txt").write_text("")
    (fix / "stub-log.txt.gh").write_text("")
    return env


def run_sync(fix: Path, env: dict, call: str) -> tuple[int, str]:
    """Source issue-sync as a library and call `call` (no main dispatch)."""
    script = (
        'set -uo pipefail; '
        f'ROOT_DIR="{fix}"; source "$ROOT_DIR/bin/issue-sync"; '
        f'set +e; {call}; echo "RC=$?"'
    )
    r = subprocess.run(["bash", "-c", script], env=env,
                       capture_output=True, text=True, timeout=90)
    return r.returncode, (r.stdout + "\n" + r.stderr)


def gh_create_count(fix: Path) -> int:
    p = Path(str(fix / "stub-log.txt") + ".gh")
    if not p.exists():
        return 0
    return sum(1 for line in p.read_text().splitlines()
               if line.strip().startswith("issue create"))


def adapter_calls(fix: Path) -> list[str]:
    p = fix / "stub-log.txt"
    return p.read_text().splitlines() if p.exists() else []


def platform_ids_of(doc: Path) -> dict:
    import yaml
    yaml.SafeLoader.yaml_implicit_resolvers.pop("tag:yaml.org,2002:timestamp", None)
    fm = yaml.safe_load(doc.read_text().split("---", 2)[1]) or {}
    return fm.get("platform_ids", {}) or {}


# ── receipts ───────────────────────────────────────────────────────────────
GITHUB_ONLY = {"gitee": {"issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1", "synced_at": ""}}
RCPT_PRESENT = json.dumps({
    "github": {"status": "ok", "issue_id": "4151", "url": "https://github.com/o/r/issues/4151"},
    "gitee": {"status": "ok", "issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1"},
})
RCPT_ABSENT = json.dumps({
    "github": {"status": "missing"},
    "gitee": {"status": "ok", "issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1"},
})
RCPT_UNKNOWN = json.dumps({
    "github": {"status": "unknown", "reason": "search_unreadable"},
    "gitee": {"status": "ok", "issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1"},
})
RCPT_AMBIGUOUS = json.dumps({
    "github": {"status": "ambiguous", "reason": "duplicate_matches"},
    "gitee": {"status": "ok", "issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1"},
})


# ── static checks ──────────────────────────────────────────────────────────
def static_checks() -> None:
    print("=== STATIC: guard wiring (RED expects FAIL) ===")
    guard = _sync_dir(SRC) / "replica_guard.py"
    if guard.exists() and "classify_receipt" in guard.read_text():
        ok("replica_guard.py present with pure classify_receipt")
    else:
        bad("replica_guard.py missing / no classify_receipt (create would trust stale cache)")

    src = (SRC / "bin" / "issue-sync").read_text()
    for token, label in (
        ("_replica_receipt", "create consults platform-side discovery helper"),
        ("_replica_decide", "create uses per-platform decision"),
        ("_backfill_close_replicas", "close heals partial cache"),
        ("present)", "create has idempotent backfill branch"),
        ("indeterminate)", "create fails closed on degraded/ambiguous read"),
    ):
        if token in src:
            ok(f"issue-sync {label}")
        else:
            bad(f"issue-sync missing: {label}")

    r = subprocess.run(["bash", "-n", str(SRC / "bin" / "issue-sync")],
                       capture_output=True, text=True)
    if r.returncode == 0:
        ok("issue-sync bash -n clean")
    else:
        bad(f"issue-sync syntax error: {r.stderr.strip()}")

    if guard.exists():
        try:
            import ast
            ast.parse(guard.read_text())
            ok("replica_guard.py parses")
        except SyntaxError as e:
            bad(f"replica_guard.py syntax error: {e}")


# ── unit checks (pure classifier) ──────────────────────────────────────────
def unit_checks() -> None:
    print("=== UNIT: classify_receipt (pure) ===")
    guard = _sync_dir(SRC) / "replica_guard.py"
    if not guard.exists():
        bad("replica_guard.py absent — cannot unit-test classifier")
        return
    spec = importlib.util.spec_from_file_location("replica_guard_under_test", guard)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = [
        ("present", {"github": {"status": "ok", "issue_id": "4151", "url": "u"}}, "github", mod.PRESENT, "4151"),
        ("absent", {"github": {"status": "missing"}}, "github", mod.ABSENT, ""),
        ("unknown", {"github": {"status": "unknown"}}, "github", mod.INDETERMINATE, ""),
        ("ambiguous", {"github": {"status": "ambiguous"}}, "github", mod.INDETERMINATE, ""),
        ("ok-no-id", {"github": {"status": "ok"}}, "github", mod.INDETERMINATE, ""),
        ("platform-missing", {"gitee": {"status": "ok", "issue_id": "A1"}}, "github", mod.INDETERMINATE, ""),
        ("malformed", ["not", "a", "dict"], "github", mod.INDETERMINATE, ""),
        ("non-dict-entry", {"github": "oops"}, "github", mod.INDETERMINATE, ""),
    ]
    for name, receipt, platform, want_state, want_id in cases:
        state, iid, _url = mod.classify_receipt(receipt, platform)
        if state == want_state and iid == want_id:
            ok(f"classify {name}: {state}/{iid!r}")
        else:
            bad(f"classify {name}: got {state}/{iid!r}, want {want_state}/{want_id!r}")


# ── behavior checks (isolated fixture driving cmd_create / cmd_close) ───────
def behavior_create_present() -> None:
    print("=== BEHAVIOR create: partial cache + existing platform replica ===")
    fix = build_fixture()
    try:
        doc = write_doc(fix, dict(GITHUB_ONLY))  # github missing locally
        env = env_for(fix, RCPT_PRESENT)
        _rc, out = run_sync(fix, env, f"cmd_create {LOCAL_ID}")
        created = gh_create_count(fix)
        ids = platform_ids_of(doc)
        if created == 0:
            ok("no duplicate GitHub create (guard backfilled instead)")
        else:
            bad(f"created {created} duplicate GitHub replica(s) — cache trusted over platform")
        if str(ids.get("github", {}).get("issue_id", "")) == "4151":
            ok("platform_ids.github backfilled with the REAL existing id 4151")
        else:
            bad(f"github id not backfilled correctly: {ids.get('github')}")
        # gitee must remain intact (no regression)
        if str(ids.get("gitee", {}).get("issue_id", "")) == "A1":
            ok("gitee id unchanged")
        else:
            bad(f"gitee id changed: {ids.get('gitee')}")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def behavior_create_absent() -> None:
    print("=== BEHAVIOR create: genuinely absent replica still creates (no regression) ===")
    fix = build_fixture()
    try:
        write_doc(fix, dict(GITHUB_ONLY))
        env = env_for(fix, RCPT_ABSENT)
        run_sync(fix, env, f"cmd_create {LOCAL_ID}")
        created = gh_create_count(fix)
        if created >= 1:
            ok("missing replica still created via original path")
        else:
            bad("guard wrongly suppressed a legitimate create (absent receipt)")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def behavior_create_indeterminate() -> None:
    print("=== BEHAVIOR create: degraded/ambiguous read fails closed ===")
    for name, rcpt in (("unknown", RCPT_UNKNOWN), ("ambiguous", RCPT_AMBIGUOUS)):
        fix = build_fixture()
        try:
            write_doc(fix, dict(GITHUB_ONLY))
            env = env_for(fix, rcpt)
            run_sync(fix, env, f"cmd_create {LOCAL_ID}")
            created = gh_create_count(fix)
            if created == 0:
                ok(f"{name} receipt → no create (fail-closed, no duplicate risk)")
            else:
                bad(f"{name} receipt still created a replica (would duplicate)")
        finally:
            shutil.rmtree(fix, ignore_errors=True)


def behavior_healthy_path() -> None:
    print("=== BEHAVIOR: healthy path (full cache) = zero extra discovery I/O ===")
    full = {
        "github": {"issue_id": "4151", "url": "https://github.com/o/r/issues/4151", "synced_at": ""},
        "gitee": {"issue_id": "A1", "url": "https://gitee.com/o/r/issues/A1", "synced_at": ""},
    }
    fix = build_fixture()
    try:
        write_doc(fix, dict(full))
        env = env_for(fix, RCPT_PRESENT)
        run_sync(fix, env, f"cmd_create {LOCAL_ID}")
        disc = [c for c in adapter_calls(fix) if "discover-raw" in c]
        if not disc:
            ok("discover-raw not called when cache complete (byte-identical healthy path)")
        else:
            bad(f"guard added discovery I/O on healthy path: {disc}")
        if gh_create_count(fix) == 0:
            ok("healthy path creates nothing (both replicas already cached)")
        else:
            bad("healthy path created a replica")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def behavior_close_backfill() -> None:
    print("=== BEHAVIOR close: partial cache heals so ALL replicas closed ===")
    fix = build_fixture()
    try:
        doc = write_doc(fix, dict(GITHUB_ONLY), phase="absorbed", canonical=True)
        env = env_for(fix, RCPT_PRESENT)
        _rc, out = run_sync(fix, env, f"cmd_close {LOCAL_ID} completed")
        # close-multi arg must contain BOTH platform ids.
        close_calls = [c for c in adapter_calls(fix) if "close-multi" in c]
        joined = " ".join(close_calls)
        if "4151" in joined and "A1" in joined:
            ok("close-multi received BOTH github(4151) and gitee(A1) ids")
        else:
            bad(f"close-multi did not receive both ids (partial close / leak): {close_calls}")
        ids = platform_ids_of(doc)
        if str(ids.get("github", {}).get("issue_id", "")) == "4151":
            ok("platform_ids.github healed before close")
        else:
            bad(f"github id not healed: {ids.get('github')}")
        if "close complete" in out or "RC=0" in out:
            ok("strict close completed (phase transition valid after heal)")
        else:
            bad(f"close did not complete cleanly: {out[-300:]}")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def behavior_close_nonterminal_no_write() -> None:
    """R12 invariant: a rejected (non-terminal) close must not mutate the doc."""
    print("=== BEHAVIOR close: non-terminal raw = zero local writes ===")
    fix = build_fixture()
    try:
        doc = write_doc(fix, dict(GITHUB_ONLY), phase="proposed")  # NOT terminal
        before = doc.read_text()
        env = env_for(fix, RCPT_PRESENT)
        _rc, out = run_sync(fix, env, f"cmd_close {LOCAL_ID} completed")
        after = doc.read_text()
        if before == after:
            ok("non-terminal close left the doc byte-identical (no backfill write)")
        else:
            bad("backfill rewrote the doc before phase validation (R12 regression)")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def behavior_checks() -> None:
    behavior_create_present()
    behavior_create_absent()
    behavior_create_indeterminate()
    behavior_healthy_path()
    behavior_close_backfill()
    behavior_close_nonterminal_no_write()


def main() -> int:
    args = sys.argv[1:]
    mode = "all"
    i = 0
    while i < len(args):
        if args[i] == "--source-dir" and i + 1 < len(args):
            global SRC
            SRC = Path(args[i + 1]).resolve()
            i += 2
        else:
            mode = args[i]
            i += 1
    if mode not in ("static", "unit", "behavior", "all"):
        print("usage: ... [--source-dir DIR] [static|unit|behavior|all]", file=sys.stderr)
        return 2
    print(f"AT-001 source-dir: {SRC} mode: {mode}")
    if not (SRC / "bin" / "issue-sync").exists():
        print(f"[FATAL] no bin/issue-sync under {SRC}", file=sys.stderr)
        return 2
    if mode in ("static", "all"):
        static_checks()
    if mode in ("unit", "all"):
        unit_checks()
    if mode in ("behavior", "all"):
        behavior_checks()
    print(f"SUMMARY: {PASS} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

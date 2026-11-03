#!/usr/bin/env python3
"""Verify task-lifecycle-scan loads platform-adapter.py via importlib _get_pa().

Checks:
  1. _get_pa(project) loads docs/system/workspace/scripts/sync/platform-adapter.py
     as module "platform_adapter" and exposes configured_platforms /
     list_open_issue_records / _handlers / _safe.
  2. No direct "from platform_adapter import" statement remains in the scan.
  3. End-to-end: scan --json reports platform_health != degraded and total > 0.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
SCAN_PATH = ROOT / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
REQUIRED_SYMBOLS = ("configured_platforms", "list_open_issue_records", "_handlers", "_safe")


def load_scan():
    sys.path.insert(0, str(ROOT / "docs/system/workspace/scripts/lifecycle"))
    sys.path.insert(0, str(ROOT / "docs/system/workspace/scripts/runtime"))
    spec = importlib.util.spec_from_file_location("tls", SCAN_PATH)
    scan = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scan)
    return scan


def main() -> int:
    # 1. Loader smoke test
    try:
        scan = load_scan()
        pa = scan._get_pa(ROOT)
    except Exception as exc:
        print(f"FAIL: _get_pa() raised: {exc}")
        return 1
    missing = [s for s in REQUIRED_SYMBOLS if not hasattr(pa, s)]
    if missing:
        print(f"FAIL: _get_pa() module missing symbols: {missing}")
        return 1
    print("OK: _get_pa() loads platform-adapter.py and exposes required symbols")

    # 2. No direct import remains
    src = SCAN_PATH.read_text(encoding="utf-8")
    n_direct = src.count("from platform_adapter import")
    if n_direct != 0:
        print(f"FAIL: {n_direct} direct 'from platform_adapter import' statements remain")
        return 1
    print("OK: no direct 'from platform_adapter import' remains")

    # 3. End-to-end scan health
    r = subprocess.run(
        ["python3", str(SCAN_PATH), "--project", str(ROOT), "--json"],
        capture_output=True, text=True, timeout=180,
    )
    if r.returncode != 0:
        print(f"FAIL: scan exit {r.returncode}: {r.stderr[:500]}")
        return 1
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        print("FAIL: scan stdout is not valid JSON")
        return 1
    summary = data.get("summary", {})
    health = summary.get("platform_health", "")
    total = summary.get("total", 0)
    reason = summary.get("platform_degraded_reason", "")
    if health == "degraded":
        print(f"FAIL: platform_health degraded: {reason}")
        return 1
    if total <= 0:
        print("FAIL: total==0, platform issues still invisible to scan")
        return 1
    print(f"OK: platform_health={health}, total={total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""AT-001 for raw-20261109T074900Z: pkill -f must escape project paths.

RED (develop baseline):
  `pkill -f "python3.*a2a_server\\.py.*--project.*${project}.*--start"` puts an
  unescaped project path into a regex. A path containing `.`, `+`, `(` or `[`
  matches OTHER projects sharing the prefix, so stopping project A kills
  project B's A2A server.

GREEN:
  - a single `freely_escape_regex()` helper escapes regex metacharacters
  - both project-path pkill sites use it
  - reverse PoC: real `pgrep -f` against two live dummy processes proves the
    escaped pattern matches only its own project
  - fixed-pattern pkill sites (no project path) are untouched

Usage:
  python3 test-pkill-project-escape.py [--source-dir DIR] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[4]
FREELY = Path("docs/system/workspace/scripts/runtime/freely")

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve()
    freely = src / FREELY
    text = freely.read_text(encoding="utf-8", errors="replace") if freely.is_file() else ""

    # ── control: the bug is real on the baseline ───────────────────────
    proj_a = "/tmp/work/proj.v1"
    proj_b = "/tmp/work/projXv1"
    old_re = r"python3.*a2a_server\.py.*--project.*" + proj_a + r".*--start"
    check("C1 unescaped path really matches a sibling project (control)",
          bool(re.search(old_re, f"python3 a2a_server.py --project {proj_b} --start")),
          "dot is a regex wildcard -> sibling project is killed too")
    check("C2 fixed-pattern pkill sites exist (control)",
          'pkill -f "$p"' in text and 'pkill -f "$_p"' in text,
          "these carry no project path and must stay unchanged")

    # ── static ─────────────────────────────────────────────────────────
    check("S1 single escape helper defined",
          "freely_escape_regex()" in text and text.count("freely_escape_regex()") >= 1,
          "one helper, no scattered sed escaping")
    check("S2 both project-path pkill sites use the helper",
          text.count("--project.*${_escaped_project}") >= 2
          or text.count("--project.*${_freely_escaped_project}") >= 2
          or text.count("${_project_re}") >= 2,
          f"escaped pkill count={text.count('${_project_re}')}")
    check("S3 no raw project path in any pkill -f regex",
          not any("pkill -f" in ln and "--project" in ln and "${project}" in ln
                  for ln in text.splitlines()),
          "must not interpolate an unescaped path")
    check("S4 helper uses Python re.escape with argv (metacharacter-complete)",
          "re.escape" in text and "sys.argv[1]" in text and "<<'PY'" in text
          if "freely_escape_regex()" in text else False,
          "no hand-rolled incomplete escape table")

    # ── behavior: helper output (extracted, executed in bash) ──────────
    if "freely_escape_regex()" in text:
        start = text.find("freely_escape_regex()")
        fn_start = text.rfind("\n", 0, start) + 1
        # Grab the whole function up to the closing brace at column 0.
        end = text.find("\n}\n", start)
        fn = text[fn_start:end + 3] if end > 0 else ""
        script = fn + '\nprintf "%s" "$(freely_escape_regex "$1")"\n'
        probe = subprocess.run(["bash", "-c", script, "_", proj_a],
                               capture_output=True, text=True, timeout=30)
        escaped = probe.stdout.strip()
        plus_probe = subprocess.run(["bash", "-c", script, "_", "/tmp/p+v1(2)[3]"],
                                    capture_output=True, text=True, timeout=30)
        plus_escaped = plus_probe.stdout.strip()
        check("B1 helper escapes dots, plus, parens and brackets",
              probe.returncode == 0 and "\\." in escaped
              and all(x in plus_escaped for x in ("\\+", "\\(", "\\[")),
              f"escaped={escaped!r} plus={plus_escaped!r}")
        check("B2 escaped pattern does not match the sibling project",
              not bool(re.search(r"python3.*a2a_server\.py.*--project.*" + escaped + r".*--start",
                                 f"python3 a2a_server.py --project {proj_b} --start")),
              f"escaped={escaped!r}")
        check("B3 escaped pattern still matches its own project",
              bool(re.search(r"python3.*a2a_server\.py.*--project.*" + escaped + r".*--start",
                             f"python3 a2a_server.py --project {proj_a} --start")),
              "no false negative")
    else:
        for n in ("B1 helper escapes dots and plus",
                  "B2 escaped pattern does not match the sibling project",
                  "B3 escaped pattern still matches its own project"):
            check(n, False, "helper missing")

    # ── behavior: real pgrep -f reverse PoC (no process is killed) ──────
    marker_a = "freely-pkill-at-proj.v1"
    marker_b = "freely-pkill-at-projXv1"
    sleep_secs = 12
    procs = []
    try:
        for marker in (marker_a, marker_b):
            procs.append(subprocess.Popen(
                [sys.executable, "-c",
                 f"import time; time.sleep({sleep_secs})", marker],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        time.sleep(0.4)
        old = subprocess.run(["pgrep", "-f", marker_a], capture_output=True, text=True)
        new = subprocess.run(["pgrep", "-f", re.escape(marker_a)],
                             capture_output=True, text=True)
        old_ids = set(old.stdout.split())
        new_ids = set(new.stdout.split())
        check("B4 real pgrep: unescaped pattern hits extra processes",
              len(old_ids) >= 2, f"old_ids={len(old_ids)}")
        check("B5 real pgrep: escaped pattern hits only its own process",
              len(new_ids) == 1 and new_ids <= old_ids,
              f"new_ids={len(new_ids)} old_ids={len(old_ids)}")
    except FileNotFoundError:
        check("B4 real pgrep: unescaped pattern hits extra processes", False, "pgrep missing")
        check("B5 real pgrep: escaped pattern hits only its own process", False, "pgrep missing")
    finally:
        for p in procs:
            p.terminate()
            try:
                p.wait(timeout=3)
            except Exception:
                p.kill()

    # ── behavior: unrelated regressions ────────────────────────────────
    r = subprocess.run(["bash", "-n", str(freely)], capture_output=True, text=True)
    check("B6 runtime/freely syntax valid", r.returncode == 0, r.stderr[:200])

    ok = sum(1 for _, o, _ in results if o)
    failed = len(results) - ok
    if args.json:
        print(json.dumps({"ok": ok, "failed": failed,
                          "results": [{"name": n, "ok": o, "detail": d} for n, o, d in results]},
                         ensure_ascii=False, indent=2))
    else:
        for n, o, d in results:
            print(f"[{'PASS' if o else 'FAIL'}] {n}" + (f" — {d}" if not o else ""))
        print(f"SUMMARY: {ok} ok, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

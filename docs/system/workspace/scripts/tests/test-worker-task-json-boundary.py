#!/usr/bin/env python3
"""AT-001 for raw-20261109T085539Z: worker prompt must survive tab/newline.

RED (develop baseline):
  - consume_worker_tasks.py emits TSV and only strips \\n\\r, so a prompt with
    a tab shifts every field: worktree becomes part of the message, `[[ ! -d ]]`
    is true, and the task is (mis)labelled input-required / worktree_missing.
  - `except: pass` makes malformed input look like "no pending tasks".
  - no boundary lint for python3 -c interpolation.

GREEN:
  - the dispatch channel is JSON Lines, decoded through a NUL-separated
    stream (no shell interpolation of AI-generated text)
  - malformed rows are reported to stderr and skipped with a count
  - a boundary lint detects single-quoted `$var` inside python3 -c bodies
    without flagging the argv-safe form introduced by R22

Usage:
  python3 test-worker-task-json-boundary.py [--source-dir DIR] [--json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[4]
RUNTIME = Path("docs/system/workspace/scripts/runtime")
QUALITY = Path("docs/system/workspace/scripts/quality")
CONSUMER = RUNTIME / "consume_worker_tasks.py"
DECODER = RUNTIME / "decode_worker_tasks.py"
LINT = QUALITY / "python-c-boundary-lint.py"
FREELY = RUNTIME / "freely"
R22_TEST = Path("docs/system/workspace/scripts/tests/test-external-input-boundary.py")

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def run(cmd, *, stdin: str = "", cwd: str | None = None):
    return subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                          cwd=cwd, timeout=60)


def rows_input(message: str) -> str:
    return json.dumps({"rows": [{
        "task_id": "task-1", "message": message,
        "worktree": "/tmp/wt", "branch": "fix/x",
        "raw_key": "raw-1", "skill": "freely-fix-execution",
    }]})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve()
    if not src.is_dir():
        print(f"source dir missing: {src}")
        return 2

    consumer, decoder = src / CONSUMER, src / DECODER
    lint, freely = src / LINT, src / FREELY
    csrc = consumer.read_text(encoding="utf-8", errors="replace") if consumer.is_file() else ""
    fsrc = freely.read_text(encoding="utf-8", errors="replace") if freely.is_file() else ""

    # ── control: prove the bug is real on the baseline ─────────────────
    # Simulate the pre-fix emitter shape directly (it no longer exists in the
    # worktree): a tab inside the message shifts every following field. This
    # is a mechanism control, independent of which source tree is under test.
    tricky = "line1\ncode:\tindented\there"
    old_line = "\t".join(["task-1", tricky.replace("\n", " "),
                          "/tmp/wt", "fix/x", "raw-1", "skill"])
    check("C1 old TSV shape really shifts fields (control)",
          len(old_line.split("\t")) > 6,
          f"fields={len(old_line.split(chr(9)))} (6 expected)")
    check("C2 R22 argv-safe form still present (control)",
          "sys.argv" in fsrc or "R22" in fsrc or "<<'PY'" in fsrc,
          "do not regress the R22 injection fix")

    # ── static ─────────────────────────────────────────────────────────
    check("S1 emit side is JSON Lines, not TSV",
          "json.dumps" in csrc and "\\t" not in csrc.split("except")[0] if csrc else False,
          "emitter must not print tab-separated rows")
    check("S2 decoder exists", decoder.is_file(), str(decoder))
    dispatch_tsv = [ln for ln in fsrc.splitlines()
                    if "IFS=$'\\t'" in ln and "_task_id" in ln]
    check("S3 worker dispatch consumes NUL-separated stream",
          "read -r -d ''" in fsrc and not dispatch_tsv,
          "no shell tab-splitting of AI text (other unrelated IFS uses stay)")
    check("S4 except:pass replaced by explicit report + count",
          "except" in csrc and "pass" not in csrc[csrc.rfind("except"):][:200]
          and "stderr" in csrc,
          "malformed rows must be visible")
    check("S5 boundary lint exists", lint.is_file(), str(lint))

    # ── behavior: end-to-end prompt preservation ───────────────────────
    tricky = 'line1\ncode:\tindented\there "quoted" and $HOME'
    if consumer.is_file() and decoder.is_file():
        emitted = run([sys.executable, str(consumer)], stdin=rows_input(tricky), cwd=str(src))
        try:
            obj = json.loads(emitted.stdout.strip().splitlines()[0])
            roundtrip_msg = obj.get("message", "")
        except Exception as exc:
            roundtrip_msg = f"PARSE_FAIL: {exc}"
        check("B1 tab/newline/quote survive emission",
              roundtrip_msg == tricky,
              f"got={roundtrip_msg!r}")

        decoded = run([sys.executable, str(decoder)], stdin=emitted.stdout, cwd=str(src))
        fields = decoded.stdout.split("\0")
        check("B2 decoder emits 6 NUL-separated fields, message intact",
              decoded.returncode == 0 and len(fields) >= 7
              and fields[1] == tricky and fields[2] == "/tmp/wt",
              f"rc={decoded.returncode} fields={len(fields)} msg={fields[1][:60]!r}")

        malformed = emitted.stdout + "NOT-JSON\n" + emitted.stdout
        mal = run([sys.executable, str(decoder)], stdin=malformed, cwd=str(src))
        ok_fields = mal.stdout.split("\0")
        check("B3 malformed row skipped with explicit stderr report",
              mal.returncode == 0 and "NOT-JSON" not in mal.stdout
              and "skip" in (mal.stderr or "").lower()
              and len(ok_fields) >= 13,
              f"rc={mal.returncode} stderr={(mal.stderr or '')[:160]!r} fields={len(ok_fields)}")
        check("B4 field order unchanged",
              fields[0] == "task-1" and fields[3] == "fix/x"
              and fields[4] == "raw-1" and fields[5] == "freely-fix-execution",
              f"fields={fields[:6]}")
        empty = run([sys.executable, str(decoder)], stdin="", cwd=str(src))
        check("B5 empty input is a clean no-op",
              empty.returncode == 0 and empty.stdout == "",
              f"rc={empty.returncode} out={empty.stdout!r}")
    else:
        for n in ("B1 tab/newline/quote survive emission",
                  "B2 decoder emits 6 NUL-separated fields, message intact",
                  "B3 malformed row skipped with explicit stderr report",
                  "B4 field order unchanged", "B5 empty input is a clean no-op"):
            check(n, False, "consumer/decoder missing")

    # ── behavior: boundary lint ────────────────────────────────────────
    if lint.is_file():
        with __import__("tempfile").TemporaryDirectory() as td:
            bad = Path(td) / "bad.sh"
            bad.write_text("python3 -c \"print('$review_branch')\"\n", encoding="utf-8")
            good = Path(td) / "good.sh"
            good.write_text("python3 - \"$ROOT_DIR\" \"$branch\" <<'PY'\nimport sys\nPY\n",
                            encoding="utf-8")
            r_bad = run([sys.executable, str(lint), "--path", str(bad)], cwd=str(src))
            r_good = run([sys.executable, str(lint), "--path", str(good)], cwd=str(src))
            check("B6 lint flags single-quoted $var inside python3 -c",
                  r_bad.returncode == 1 and "review_branch" in r_bad.stdout,
                  f"rc={r_bad.returncode} out={r_bad.stdout[:180]!r}")
            check("B7 lint does not flag argv-safe heredoc form",
                  r_good.returncode == 0,
                  f"rc={r_good.returncode} out={r_good.stdout[:180]!r}")
        r_repo = run([sys.executable, str(lint), "--path", str(src / "docs/system/workspace/scripts/runtime")],
                     cwd=str(src))
        check("B8 lint reports a baseline count without crashing",
              r_repo.returncode in (0, 1) and "count" in r_repo.stdout.lower(),
              f"rc={r_repo.returncode} out={r_repo.stdout[:180]!r}")
    else:
        for n in ("B6 lint flags single-quoted $var inside python3 -c",
                  "B7 lint does not flag argv-safe heredoc form",
                  "B8 lint reports a baseline count without crashing"):
            check(n, False, "lint missing")

    # ── regression: R22 test must stay green ───────────────────────────
    if (src / R22_TEST).is_file():
        r = run([sys.executable, str(src / R22_TEST)], cwd=str(src))
        check("B9 R22 external-input-boundary regression green",
              r.returncode == 0, f"rc={r.returncode} out={(r.stdout + r.stderr)[-180:]}")
    else:
        check("B9 R22 external-input-boundary regression green", False, "test missing")

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

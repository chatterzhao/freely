#!/usr/bin/env python3
"""AT-001 for raw-20261104T080200Z / #4175 (R32).

`docs/system/workspace/scripts/README.md` declares bin/ a projection layer, yet
`bin/pr-review-guarded` carried an 806-line implementation with no counterpart
under `workspace/scripts/**`. This AT pins the fix and the guard:

* the implementation moved to `scripts/worktree/pr-review-guarded` and
  `bin/pr-review-guarded` is a four-line exec shim;
* `scripts/bin-projections.yaml` registers every bin file over the threshold,
  and `bin/check-bin-projection` refuses unregistered files, stale entries and
  permanent exemptions;
* the inventory is written down, and the remaining debt is tracked by a
  follow-up raw instead of being silently grandfathered.

Runs against `git archive develop` to prove RED.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-bin-projection.py"
BIN_CMD = "bin/pr-review-guarded"
REAL = "docs/system/workspace/scripts/worktree/pr-review-guarded"
REGISTRY = "docs/system/workspace/scripts/bin-projections.yaml"
LINT = "bin/check-bin-projection"
INVENTORY = "docs/system/workspace/scripts/bin-inventory.md"
FOLLOWUP = "raw-20261111T125724Z"
SHIM_MAX = 8

OK: list[str] = []
FAIL: list[str] = []


def array_has(text: str, marker: str, entry: str) -> bool:
    """True when `entry` is a line of the array that starts at `marker`."""
    i = text.index(marker) + len(marker)
    j = text.index(")", i)
    return entry in [line.strip() for line in text[i:j].splitlines()]


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001 - report, never abort the suite
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def load_doc(src: Path) -> dict:
    return json.loads((src / REGISTRY).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="", help="root to inspect (RED: a develop snapshot)")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else ROOT
    print(f"source: {src}")

    bin_path = src / BIN_CMD
    real_path = src / REAL

    # ---- static ----
    def c01():
        return (bin_path.is_file() and bin_path.stat().st_mode & 0o111
                and real_path.is_file() and real_path.stat().st_mode & 0o111), \
            "bin shim or the real implementation is missing / not executable"

    def c02():
        if not bin_path.is_file():
            return False, f"missing {BIN_CMD}"
        text = bin_path.read_text(encoding="utf-8")
        size = len(text.splitlines())
        return size <= SHIM_MAX and "exec bash" in text and REAL in text, \
            f"{size} lines, exec={'exec bash' in text}, points-at-real={REAL in text}"

    def c03():
        if not real_path.is_file():
            return False, f"missing {REAL}"
        text = real_path.read_text(encoding="utf-8")
        need = ["MAX_ROUNDS=3", "REVIEWER_SKILL", "verdict_override", "review_branch"]
        missing = [n for n in need if n not in text]
        return not missing and len(text.splitlines()) > 700, f"moved body lacks {missing}"

    def c04():
        lint = src / LINT
        return lint.is_file() and bool(lint.stat().st_mode & 0o111), f"missing {LINT}"

    def c05():
        doc = load_doc(src)
        return doc.get("schema_version") == 1 and int(doc.get("threshold_lines") or 0) > 0, \
            "registry header is incomplete"

    def c06():
        doc = load_doc(src)
        off = [e["path"] for e in doc.get("entries", []) if e.get("path") == BIN_CMD]
        return not off, f"{BIN_CMD} is still registered, but it is a projection now"

    def c07():
        doc = load_doc(src)
        stale = [e["path"] for e in doc.get("entries", []) if not (src / e["path"]).is_file()]
        return not stale, f"stale registry entries: {stale[:4]}"

    def c08():
        doc = load_doc(src)
        threshold = int(doc["threshold_lines"])
        bad = []
        for entry in doc.get("entries", []):
            path = src / entry["path"]
            if path.is_file() and len(path.read_text(encoding='utf-8', errors='replace').splitlines()) <= threshold:
                bad.append(entry["path"])
        return not bad, f"entries that no longer need an exemption: {bad[:4]}"

    def c09():
        impl = [e for e in load_doc(src).get("entries", [])
                if e.get("class") == "implementation-in-bin"]
        missing = [e["path"] for e in impl if e.get("followup") != FOLLOWUP]
        return bool(impl) and not missing, f"{len(impl)} impl entries, bad followup on {missing[:3]}"

    def c10():
        inv = src / INVENTORY
        if not inv.is_file():
            return False, f"missing {INVENTORY}"
        text = inv.read_text(encoding="utf-8")
        rows = re.findall(r"^\| `bin/", text, re.MULTILINE)
        return len(rows) >= 30 and FOLLOWUP in text, \
            f"inventory has {len(rows)} rows, followup referenced={FOLLOWUP in text}"

    def c11():
        ta = (src / "bin/test-all").read_text(encoding="utf-8")
        wired = array_has(ta, "\nCORE=(", AT_NAME) and array_has(ta, "\nCI_CORE=(", AT_NAME)
        return wired, "AT not wired into both CORE and CI_CORE"

    def c12():
        svg = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-pr-review-projection"' in svg, "story not registered in epics-map"

    check("implementation and shim both exist and are executable", c01)
    check("bin/ entry is a projection of the real source", c02)
    check("the moved body still holds the review logic", c03)
    check("projection lint exists and is executable", c04)
    check("registry header is complete", c05)
    check("the migrated command left the registry", c06)
    check("no stale registry entries", c07)
    check("no permanent exemptions", c08)
    check("remaining debt points at the follow-up raw", c09)
    check("inventory lists the bin/ entries", c10)
    check("AT wired into CORE and CI_CORE", c11)
    check("story registered in epics-map", c12)

    # ---- behaviour ----
    def b13():
        """The lint passes on the real tree."""
        if not (src / LINT).is_file():
            return False, f"missing {LINT}"
        proc = subprocess.run([sys.executable, str(src / LINT), "--json"],
                              capture_output=True, text=True, timeout=120)
        try:
            data = json.loads(proc.stdout)
        except Exception:  # noqa: BLE001
            return False, f"rc={proc.returncode} stdout={proc.stdout[:120]}"
        return proc.returncode == 0 and data.get("ok") is True, \
            f"rc={proc.returncode} errors={data.get('errors')}"

    def b14():
        """An unregistered, too-large bin file must be refused."""
        if not (src / LINT).is_file():
            return False, f"missing {LINT}"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bin").mkdir()
            (root / "docs/system/workspace/scripts").mkdir(parents=True)
            (root / REGISTRY).write_text(json.dumps(
                {"schema_version": 1, "threshold_lines": 5, "entries": []}), encoding="utf-8")
            (root / "bin/big").write_text("\n".join(["echo x"] * 12) + "\n", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(src / LINT), "--project", str(root)],
                                  capture_output=True, text=True, timeout=120)
            return proc.returncode == 1 and "not registered" in proc.stderr, \
                f"rc={proc.returncode} stderr={proc.stderr.strip()[:140]}"

    def b15():
        """A stale exemption (file already a projection) must be refused."""
        if not (src / LINT).is_file():
            return False, f"missing {LINT}"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bin").mkdir()
            (root / "docs/system/workspace/scripts").mkdir(parents=True)
            (root / REGISTRY).write_text(json.dumps({
                "schema_version": 1, "threshold_lines": 5,
                "entries": [{"path": "bin/small", "lines": 1, "class": "dispatcher", "reason": "x"}],
            }), encoding="utf-8")
            (root / "bin/small").write_text("echo x\n", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(src / LINT), "--project", str(root)],
                                  capture_output=True, text=True, timeout=120)
            return proc.returncode == 1 and "delete its registry entry" in proc.stderr, \
                f"rc={proc.returncode} stderr={proc.stderr.strip()[:140]}"

    def b16():
        """The projection must still run: no args fails fast, and it reaches the real file."""
        if not bin_path.is_file():
            return False, f"missing {BIN_CMD}"
        proc = subprocess.run(["bash", str(bin_path)], capture_output=True, text=True, timeout=120)
        text = (proc.stdout or "") + (proc.stderr or "")
        reached = "pr-review-guarded" in text or "Usage" in text or "unknown" in text.lower()
        return proc.returncode != 0 and reached, \
            f"rc={proc.returncode} text={text.strip()[:140]}"

    check("lint passes on the real tree", b13)
    check("unregistered oversized bin file is refused", b14)
    check("stale exemption is refused", b15)
    check("the projection still dispatches", b16)

    print(f"\nSUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())

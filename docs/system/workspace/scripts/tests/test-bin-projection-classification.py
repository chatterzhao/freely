#!/usr/bin/env python3
"""AT-001 (C-A / raw-20261111T125724Z): classify the 35 implementation-in-bin
entries WITHOUT creating a permanent exemption.

Design intent (project sources, not guesses):
  * `docs/system/workspace/scripts/README.md`: bin/ is a projection layer, real
    implementation belongs under workspace/scripts/**.
  * `bin/check-bin-projection` header: three machine-checkable rules -
    coverage (>threshold must be registered), staleness (registered file must
    exist), shrink (a registered file that becomes a projection must be removed;
    "no permanent exemptions - this is what makes the debt shrink").
  * the raw's repair plan: self-contained lint/aggregate entries (check-*,
    test-all) stay in bin/ and are labelled `standalone-tool` with a concrete
    reason; only entries judged to be real business implementations are
    migrated, in independent batches.

The regression risk this AT pins: adding `standalone-tool` must NOT become a
permanent exemption. All three original rules must still apply to it, plus the
new class/reason validity checks. The baseline (develop) must fail because its
35 reasons are all placeholders.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

REGISTRY = "docs/system/workspace/scripts/bin-projections.yaml"
LINT = "bin/check-bin-projection"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print("  [ok] " + label)


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print("  [FAIL] " + label)


def check(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def registry(src: Path) -> dict:
    return json.loads(read(src / REGISTRY))


def run_lint(src: Path, root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(src / LINT), "--project", str(root), "--json"],
                          capture_output=True, text=True, timeout=60)


def make_project(src: Path, root: Path, mutate=None) -> None:
    (root / "bin").mkdir(parents=True, exist_ok=True)
    (root / REGISTRY).parent.mkdir(parents=True, exist_ok=True)
    doc = registry(src)
    files = {}
    for e in doc["entries"]:
        rel = e["path"]
        if rel in files:
            continue
        # fabricate a file whose line count exceeds the threshold
        files[rel] = "\n".join(["# placeholder"] * max(1, e["lines"])) + "\n"
    if mutate:
        files, doc = mutate(files, doc)
    for rel, body in files.items():
        (root / rel).write_text(body, encoding="utf-8")
    (root / REGISTRY).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def lint_case(src: Path, mutate=None) -> dict:
    with tempfile.TemporaryDirectory(prefix="at-binproj-") as td:
        root = Path(td)
        make_project(src, root, mutate)
        p = run_lint(src, root)
        try:
            return json.loads(p.stdout.strip() or "{}")
        except json.JSONDecodeError:
            return {"ok": False, "errors": ["lint did not emit JSON"], "raw": p.stdout + p.stderr}


def static_checks() -> None:
    print("=== STATIC: classification and gate strength ===")
    d = registry(SRC)
    lint = read(SRC / LINT)
    check("standalone-tool" in d["classes"], "S1 standalone-tool is a declared class")
    entries = [e for e in d["entries"] if e["class"] != "dispatcher"]
    standalone = [e for e in entries if e["class"] == "standalone-tool"]
    migrate = [e for e in entries if e["class"] == "implementation-in-bin"]
    check(len(standalone) == 22, "S2 22 entries classified standalone-tool (got " + str(len(standalone)) + ")")
    check(len(migrate) == 13, "S3 13 entries remain for later migration (got " + str(len(migrate)) + ")")
    placeholders = [e["path"] for e in entries
                    if "case by case" in str(e["reason"]).lower()
                    or str(e["reason"]).startswith("implementation still lives in bin/")]
    check(not placeholders, "S4 every entry has a concrete reason (placeholders: " + str(placeholders) + ")")
    check("not declared in registry classes" in lint, "S5 lint validates class against declared classes")
    check("concrete classification decision" in lint, "S6 lint rejects placeholder reasons")
    check("not registered in" in lint and "stale entry" in lint
          and "delete its registry entry" in lint,
          "S7 all three original gate rules are still present")
    check("standalone-tool`" in lint or "standalone-tool" in lint,
          "S8 lint documents that standalone-tool is not an exemption")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real lint against fabricated projects ===")
    good = lint_case(SRC)
    check(good.get("ok") is True, "B1 healthy classified registry passes the lint")

    def unregistered(files, doc):
        files["bin/unregistered-big"] = "\n".join(["# x"] * 60) + "\n"
        return files, doc
    r = lint_case(SRC, unregistered)
    check(not r.get("ok") and any("not registered" in e for e in r.get("errors", [])),
          "B2 coverage rule still rejects an unregistered large bin file")

    def stale(files, doc):
        doc["entries"].append({"path": "bin/ghost", "lines": 60,
                               "class": "standalone-tool", "reason": "ghost entry"})
        return files, doc
    r = lint_case(SRC, stale)
    check(not r.get("ok") and any("stale entry" in e for e in r.get("errors", [])),
          "B3 staleness rule still rejects a missing file")

    def shrunk(files, doc):
        files["bin/check-runtime-size"] = "# tiny projection\n"
        return files, doc
    r = lint_case(SRC, shrunk)
    check(not r.get("ok") and any("delete its registry entry" in e for e in r.get("errors", [])),
          "B4 shrink rule still applies to a standalone-tool entry (no exemption)")

    def bad_class(files, doc):
        doc["entries"][0]["class"] = "made-up-class"
        return files, doc
    r = lint_case(SRC, bad_class)
    check(not r.get("ok") and any("not declared in registry classes" in e for e in r.get("errors", [])),
          "B5 an undeclared class is rejected")

    def placeholder(files, doc):
        doc["entries"][0]["reason"] = "implementation still lives in bin/; judged case by case in the follow-up"
        return files, doc
    r = lint_case(SRC, placeholder)
    check(not r.get("ok") and any("concrete classification decision" in e for e in r.get("errors", [])),
          "B6 a placeholder reason is rejected")

    if BASE:
        print("=== BASELINE CONTROL: develop placeholders ===")
        d = registry(BASE)
        entries = [e for e in d["entries"] if e["class"] != "dispatcher"]
        ph = [e for e in entries if "case by case" in str(e["reason"]).lower()]
        check(len(ph) == 35, "R1 develop really had 35 placeholder reasons (RED is real)")
        check("standalone-tool" not in d["classes"],
              "R2 develop really had no standalone-tool class")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()

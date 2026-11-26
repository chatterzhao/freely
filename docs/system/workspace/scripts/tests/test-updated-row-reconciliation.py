#!/usr/bin/env python3
"""AT-001 for raw-20261125T122804Z / I-20261125T122804Z-A.

The `| updated |` row in a raw body is a projection of frontmatter
`updated_at`. It has several legitimate writers, so two replicas may carry
different timestamps while asserting identical lifecycle meaning. The replica
gate must ignore that generated value but keep comparing every other body line.

Usage: python3 ...test-updated-row-reconciliation.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

OK = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def load_gate(src: Path):
    path = src / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"
    spec = importlib.util.spec_from_file_location("raw_reconciliation_at", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def record(key: str, body: str, state: str = "closed") -> dict:
    return {
        "raw_key": f"raw-{key}",
        "title": "fix: generated updated row must not split replicas",
        "body": body,
        "state": state,
        "labels": ["kind/raw", "severity/p1"],
        "comments": [],
        "status": "ok",
    }


BASE_BODY = """workflow_kind: fix ## fix: generated updated row | Field | Value | |-------|-------| | local_id | `raw-20261125T122804Z` | | kind | `raw` | | phase_state | `absorbed` | | canonical | `none` | | created | 2026-11-25T12:28:05Z | | updated | {updated} | --- > governance note. ## 现象 body text."""


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    mod = load_gate(src)
    text = (src / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py").read_text(encoding="utf-8")

    check("gate source readable", bool(text))
    check("generated updated row normalized in body projection",
          "updated" in text and ("_UPDATED_ROW" in text or "updated_row" in text or "generated" in text.lower()))

    old = mod.canonical_projection(record("20261125T122804Z", BASE_BODY.format(updated="2026-11-25T12:28:05Z")))
    new = mod.canonical_projection(record("20261125T122804Z", BASE_BODY.format(updated="2026-11-26T04:58:57Z")))
    check("updated-only drift yields identical fingerprint",
          old["fingerprint"] == new["fingerprint"], f"{old['fingerprint'][:12]} vs {new['fingerprint'][:12]}")

    changed = BASE_BODY.format(updated="2026-11-26T04:58:57Z").replace("body text.", "different body text.")
    other = mod.canonical_projection(record("20261125T122804Z", changed))
    check("human body change still diverges", other["fingerprint"] != new["fingerprint"])

    phase = BASE_BODY.format(updated="2026-11-26T04:58:57Z").replace("| phase_state | `absorbed` |", "| phase_state | `proposed` |")
    phase_rec = mod.canonical_projection(record("20261125T122804Z", phase))
    check("lifecycle table row still diverges", phase_rec["fingerprint"] != new["fingerprint"])

    key = "20261125T122804Z"
    replicas = {
        "github": record(key, BASE_BODY.format(updated="2026-11-25T12:28:05Z")),
        "gitee": record(key, BASE_BODY.format(updated="2026-11-25T12:28:05Z")),
    }
    local = record(key, BASE_BODY.format(updated="2026-11-26T04:58:57Z"))
    receipt = mod.reconcile(raw_key=key, configured_platforms=["github", "gitee"],
                            replicas=replicas, local=local)
    check("reconcile ok with updated-only drift", receipt.get("ok") is True,
          str(receipt.get("diagnostics"))[:160])

    local_bad = record(key, changed)
    blocked = mod.reconcile(raw_key=key, configured_platforms=["github", "gitee"],
                            replicas=replicas, local=local_bad)
    check("reconcile still blocks real body change", blocked.get("ok") is False
          and any(d.get("code") == "content_diverged" for d in blocked.get("diagnostics", [])))

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

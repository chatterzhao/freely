#!/usr/bin/env python3
"""AT-001 — raw-20261108T141300Z / #4231.

`freely feedback --severity` writes P0/P1 into the raw frontmatter AND labels
every platform replica `severity/Pn`. `raw-issue-pull` -> `pull_raw_issue()`
rebuilt the local frontmatter from the strict 21 fields only, so materialization
silently dropped priority: the local read view fell back to P2 while the
platforms still showed P0/P1. `raw_reconciliation.canonical_projection` then
had to exclude `severity/*` to avoid a fake divergence.

Pins the whole chain: label resolution (including fail-closed on conflict),
the real materialization output, legacy zero-rewrite, and comparison restored.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (severity dropped -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
import tempfile
import unittest.mock as mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("SEVERITY_SOURCE_ROOT", str(PROJECT))).resolve()
RAW_KEY = "20261108T141300Z"
TEMPLATE = "docs/B1-docs/raw-20261103T132548Z/issue.md"

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


def _load(name: str, rel: str):
    path = SRC / rel
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def static_checks(src: Path) -> None:
    print("=== STATIC: severity survives materialization and is comparable ===")
    adapter = (src / "docs/system/workspace/scripts/sync/platform-adapter.py").read_text(errors="replace")
    recon = (src / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py").read_text(errors="replace")
    expect("def severity_from_replicas" in adapter and 'fm["severity"] = severity' in adapter,
           "pull writes a resolved severity into the materialized frontmatter")
    expect('startswith(("phase/", "severity/"))' not in recon
           and "severity/* IS now" in recon,
           "canonical_projection no longer excludes severity/*")


def _template_body(src: Path) -> str:
    text = (src / TEMPLATE).read_text(errors="replace")
    parts = text.split("---", 2)
    import yaml
    fm = yaml.safe_load(parts[1]) or {}
    # The template is an absorbed R17 doc. pull rebuilds phase_state from the
    # `phase/proposed` label, so normalize everything absorption-related.
    fm.update({"phase_state": "proposed", "absorbed_into": "",
               "canonical_issue_path": "", "completed_at": "", "closeout_note": "",
               "platform_state": "open", "promoted_children": []})
    return ("---\n" + yaml.safe_dump(fm, sort_keys=False)
            + "---\n\n# materialized severity probe\n")


def _replica(src: Path, labels, severity_body: bool = True) -> dict:
    return {
        "status": "ok",
        "raw_key": f"raw-{RAW_KEY}",
        "issue_id": "9999",
        "url": "https://example.invalid/issues/9999",
        "title": f"[RAW-{RAW_KEY}] severity materialization probe",
        "labels": list(labels),
        "body": _template_body(src) if severity_body else "# no frontmatter\n",
        "created_at": "2026-11-08T14:13:00Z",
        "updated_at": "2026-11-08T14:13:00Z",
        "state": "open",
        "comments": [],
    }


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: label resolution + real materialization ===")
    try:
        adapter = _load("pa_severity_probe", "docs/system/workspace/scripts/sync/platform-adapter.py")
        recon = _load("recon_severity_probe", "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py")
    except Exception as exc:
        for label in ("single severity resolved", "conflict fails closed", "legacy stays absent",
                      "P0 survives materialization", "legacy raw not rewritten",
                      "projection keeps severity labels"):
            bad(f"{label} (module unavailable: {type(exc).__name__})")
        return

    resolver = getattr(adapter, "severity_from_replicas", None)
    if resolver is None:
        for label in ("single severity resolved", "conflict fails closed", "legacy stays absent"):
            bad(f"{label} (severity_from_replicas missing)")
    else:
        value, warnings = resolver({
            "github": {"labels": ["kind/raw", "severity/P0"]},
            "gitee": {"labels": ["kind/raw", "severity/p0", "phase/proposed"]},
        })
        expect(value == "P0" and not warnings,
               f"single severity resolved and case-normalized (got {value!r}, {warnings})")

        try:
            resolver({"github": {"labels": ["severity/P0"]},
                      "gitee": {"labels": ["severity/P1"]}})
            bad("conflict fails closed (no error raised)")
        except ValueError:
            ok("conflict fails closed (distinct explicit values rejected)")

        value, warnings = resolver({"github": {"labels": ["kind/raw"]},
                                    "gitee": {"labels": ["kind/raw"]}})
        expect(value is None and warnings,
               f"legacy stays absent but is reported, not guessed (got {value!r}, {warnings})")

    # End-to-end: call the REAL pull_raw_issue with platform reads mocked.
    def materialize(labels):
        target = tmp / f"target-{len(list(tmp.iterdir()))}"
        rep = _replica(src, labels)
        with mock.patch.object(adapter, "discover_raw_replicas",
                               return_value={"github": dict(rep), "gitee": dict(rep)}), \
             mock.patch.object(adapter, "check_and_claim_assignee", return_value=(True, "ok")), \
             mock.patch.object(adapter, "_update_issue_title", return_value=True):
            adapter.pull_raw_issue(RAW_KEY, target)
        return (target / "issue.md").read_text(encoding="utf-8")

    try:
        text = materialize(["kind/raw", "phase/proposed", "severity/P0"])
        has_field = bool(re.search(r"^severity:\s*P0\s*$", text, re.MULTILINE))
        expect(has_field,
               f"P0 survives materialization into the local frontmatter (found={has_field})")
        if has_field:
            sys.path.insert(0, str(src / "docs/system/workspace/scripts/lifecycle"))
            from raw_metadata_contract import resolve_severity, parse_issue_text
            metadata, _ = parse_issue_text(text)
            expect(resolve_severity(metadata) == "P0",
                   f"single-owner parser reads severity P0 (got {resolve_severity(metadata)})")
        else:
            bad("single-owner parser reads severity P0 (field missing)")
    except Exception as exc:
        bad(f"P0 survives materialization (raised {type(exc).__name__}: {exc})")
        bad(f"single-owner parser reads severity P0 (materialization failed)")

    try:
        legacy = materialize(["kind/raw", "phase/proposed"])
        expect(not re.search(r"^severity:", legacy, re.MULTILINE),
               "legacy raw (no severity label) is not rewritten")
    except Exception as exc:
        bad(f"legacy raw not rewritten (raised {type(exc).__name__}: {exc})")

    p0 = recon.canonical_projection({"raw_key": f"raw-{RAW_KEY}", "title": "t", "body": "b",
                                     "state": "open", "labels": ["kind/raw", "severity/P0"]})
    p1 = recon.canonical_projection({"raw_key": f"raw-{RAW_KEY}", "title": "t", "body": "b",
                                     "state": "open", "labels": ["kind/raw", "severity/P1"]})
    expect(any(str(x).lower() == "severity/p0" for x in p0["labels"])
           and p0["fingerprint"] != p1["fingerprint"],
           "projection keeps severity labels and distinguishes P0 from P1")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)
    tmp = Path(tempfile.mkdtemp(prefix="severity-"))
    try:
        behavior_checks(src, tmp)
    finally:
        import subprocess
        subprocess.run(["rm", "-rf", str(tmp)], check=False)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

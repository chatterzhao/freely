#!/usr/bin/env python3
"""AT-001 (raw-20261113T084851Z): raw-issue-pull must keep local replicas
consistent with the platform WITHOUT hand-edited data.

Design intent (project sources, not guesses):
  * raw_reconciliation.canonical_projection compares title/body/state/labels
    AND comments. Its comment says "platform copies never inline them" - i.e.
    the LOCAL document is expected to mirror platform comments as
    `### comment-*` blocks, compared separately by _comments().
  * `bin/issue-sync` header: raw lifecycle ends at
    "configured-platform close (absorbed/closed)". A platform phase/* label is
    a creation-time snapshot; re-materialization must not demote a local
    terminal state back to proposed.

Before this fix `pull_raw_issue` ignored `details["comments"]` and always set
phase from the (stale) platform label, so every pull made the local replica
diverge and callers were tempted to hand-edit comment blocks / phase back into
shape to satisfy the fail-closed gate.

The behavioural check loads the REAL adapter under test, stubs only transport
functions, materializes into a temp dir, then feeds the result through the REAL
raw_reconciliation + raw-reconciliation-gate readers. Baseline (develop) must
fail the same assertions.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path
from unittest import mock

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

ADAPTER_REL = "docs/system/workspace/scripts/sync/platform-adapter.py"
GATE_REL = "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py"
RECON_REL = "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"
KEY = "20261113T084851Z"
COMMENT = "拆解为以下任务:\n1. [I-20261113T084851Z-A](will-be-updated)"

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


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def lifecycle_on_path(src: Path) -> None:
    p = str(src / "docs/system/workspace/scripts/lifecycle")
    if p not in sys.path:
        sys.path.insert(0, p)


def fixture_frontmatter(src: Path) -> str:
    lifecycle_on_path(src)
    from raw_metadata_contract import RAW_METADATA_FIELDS

    defaults = {
        "schema_version": "1", "local_id": f"raw-{KEY}", "kind": "raw",
        "phase_state": "proposed", "absorbed_into": "", "platform_ids": {},
        "primary_platform": "github", "canonical_issue_path": "",
        "last_synced_comment_at": {}, "hash": "",
        "created_at": "2026-11-13T08:48:51Z", "updated_at": "2026-11-13T08:48:51Z",
        "intake_id": "", "author": "platform", "channel": "github",
        "session_refs": [], "platform_state": "open", "promoted_children": [],
        "source_candidate": "", "completed_at": "", "closeout_note": "",
    }
    import yaml
    return yaml.safe_dump(
        {k: defaults.get(k, "") for k in RAW_METADATA_FIELDS},
        default_flow_style=False, allow_unicode=True, sort_keys=False,
    ).strip()


def make_replica(src: Path, title: str) -> dict:
    body = f"---\n{fixture_frontmatter(src)}\n---\n\nparity fixture body\n"
    return {
        "status": "ok", "raw_key": f"raw-{KEY}", "issue_id": "9001",
        "url": "https://example.invalid/issues/9001",
        "title": title, "body": body,
        "created_at": "2026-11-13T08:48:51Z", "updated_at": "2026-11-13T08:48:51Z",
        "labels": ["kind/raw", "phase/proposed"],
        "comments": [COMMENT],
        "state": "OPEN",
    }


def materialize(src: Path, target: Path, existing: str | None = None):
    lifecycle_on_path(src)
    mod = load(src / ADAPTER_REL, "adapter_parity_" + str(abs(hash(str(src)))))
    gate = load(src / GATE_REL, "gate_parity_" + str(abs(hash(str(src)))))
    recon = load(src / RECON_REL, "recon_parity_" + str(abs(hash(str(src)))))
    title = f"[RAW-{KEY}] " + mod.local_heading_title(KEY, "parity fixture")
    replica = make_replica(src, title)
    target.mkdir(parents=True, exist_ok=True)
    if existing is not None:
        (target / "issue.md").write_text(existing, encoding="utf-8")
    with mock.patch.object(mod, "discover_raw_replicas", return_value={"github": replica}), \
         mock.patch.object(mod, "check_and_claim_assignee", return_value=(True, "ok")), \
         mock.patch.object(mod, "severity_from_replicas", return_value=(None, [])):
        result = mod.pull_raw_issue(KEY, target)
    return mod, gate, recon, replica, result


def verdict(gate, recon, target: Path, replica: dict) -> dict:
    local = gate._local_record(target / "issue.md", KEY)
    return recon.reconcile(
        raw_key=KEY,
        configured_platforms=["github"],
        replicas={"github": replica},
        local=local,
    )


def static_checks() -> None:
    print("=== STATIC: pull mirrors comments and preserves terminal state ===")
    text = (SRC / ADAPTER_REL).read_text(encoding="utf-8")
    check('details.get("comments")' in text,
          "S1 pull reads the platform comments field")
    check("comment-platform-" in text,
          "S2 pull writes a parseable ### comment-* block")
    check("existing_terminal" in text,
          "S3 pull detects an existing terminal raw")
    check('("absorbed", "closed", "dropped")' in text,
          "S4 terminal states are enumerated explicitly")
    check("phase = existing_terminal" in text,
          "S5 terminal phase is preserved instead of overwritten")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real adapter + real reconciliation ===")
    with tempfile.TemporaryDirectory(prefix="at-parity-") as td:
        target = Path(td) / f"docs/B1-docs/raw-{KEY}"
        _, gate, recon, replica, result = materialize(SRC, target)
        check(result is not None, "B1 pull returns a materialized document")
        doc = (target / "issue.md").read_text(encoding="utf-8")
        check("### comment-platform-1" in doc and COMMENT in doc,
              "B2 platform comment is mirrored into the local document")
        d = verdict(gate, recon, target, replica)
        check(d["ok"], "B3 replica gate allows the pulled document (no hand-edited data)")
        check(not d["diagnostics"], "B4 no content/label/comment divergence remains")

        front = doc.split("---", 2)[1]
        check("phase_state: proposed" in front,
              "B5 a fresh raw still starts at the platform's proposed phase")

    with tempfile.TemporaryDirectory(prefix="at-parity-terminal-") as td:
        target = Path(td) / f"docs/B1-docs/raw-{KEY}"
        _, _, _, _, _ = materialize(SRC, target)
        absorbed = (target / "issue.md").read_text(encoding="utf-8")
        absorbed = absorbed.replace("phase_state: proposed", "phase_state: absorbed")
        absorbed = absorbed.replace("absorbed_into: ''", "absorbed_into: I-20261113T084851Z-A")
        absorbed = absorbed.replace("platform_state: open", "platform_state: closed")
        absorbed = absorbed.replace("completed_at: ''", "completed_at: '2026-11-13T08:50:00Z'")
        _, gate, recon, replica, _ = materialize(SRC, target, existing=absorbed)
        front = (target / "issue.md").read_text(encoding="utf-8").split("---", 2)[1]
        check("phase_state: absorbed" in front,
              "B6 re-materialization does not demote an absorbed raw to proposed")
        check("platform_state: closed" in front,
              "B7 terminal platform_state survives the pull")

    with tempfile.TemporaryDirectory(prefix="at-parity-idempotent-") as td:
        target = Path(td) / f"docs/B1-docs/raw-{KEY}"
        materialize(SRC, target)
        materialize(SRC, target)
        doc = (target / "issue.md").read_text(encoding="utf-8")
        check(doc.count("### comment-platform-") <= 1 and "comment-platform-2" not in doc,
              "B8 repeated pulls do not accumulate duplicate comment blocks")


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop adapter ===")
    with tempfile.TemporaryDirectory(prefix="at-parity-base-") as td:
        target = Path(td) / f"docs/B1-docs/raw-{KEY}"
        _, gate, recon, replica, _ = materialize(BASE, target)
        doc = (target / "issue.md").read_text(encoding="utf-8")
        check("### comment-platform-" not in doc,
              "R1 develop pull really drops platform comments (RED is real)")
        d = verdict(gate, recon, target, replica)
        check(not d["ok"] and any(x.get("code") == "content_diverged" for x in d["diagnostics"]),
              "R2 develop pull really makes the replica gate diverge")
    with tempfile.TemporaryDirectory(prefix="at-parity-base-term-") as td:
        target = Path(td) / f"docs/B1-docs/raw-{KEY}"
        materialize(BASE, target)
        absorbed = (target / "issue.md").read_text(encoding="utf-8")
        absorbed = absorbed.replace("phase_state: proposed", "phase_state: absorbed")
        absorbed = absorbed.replace("absorbed_into: ''", "absorbed_into: I-20261113T084851Z-A")
        materialize(BASE, target, existing=absorbed)
        front = (target / "issue.md").read_text(encoding="utf-8").split("---", 2)[1]
        check("phase_state: proposed" in front,
              "R3 develop pull really demotes an absorbed raw (RED is real)")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()

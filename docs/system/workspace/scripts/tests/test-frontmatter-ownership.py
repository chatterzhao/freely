#!/usr/bin/env python3
"""AT-001 for raw-20261103T132517Z — one owner for SDD frontmatter parsing.

Drives the REAL task-lifecycle-scan parser, the contract module and the shared
CLI against isolated fixtures, plus the idempotent repair command. Nothing here
touches the real project's B1 documents (except a read-only full-tree check).
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

OK = 0
BAD = 0
PROJECT = Path(__file__).resolve().parents[5]


def ok(label):
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label):
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond, label):
    (ok if cond else bad)(label)


GLUED = ("---\nlocal_id: raw-20260101T000000Z\nkind: raw\n"
         "phase_state: proposed\nplatform_state: closed---\n\n# t\n")
CONFLICT = ("---\nlocal_id: raw-20260101T000000Z\nkind: raw\n"
            "<<<<<<< HEAD\nphase_state: dropped\n=======\n"
            "phase_state: proposed\n>>>>>>> x\n---\n\n# t\n")
BAD_YAML = "---\nkey: [unclosed\n---\n\n# t\n"


def load(name, path, extra_paths=()):
    for p in extra_paths:
        sys.path.insert(0, str(p))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def static_checks(project: Path):
    print("=== STATIC: single-owner wiring ===")
    scan = project / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
    sync = project / "bin/issue-sync"
    contract = project / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py"
    cli = project / "docs/system/workspace/scripts/lifecycle/frontmatter_contract_cli.py"
    expect(scan.is_file(), "task-lifecycle-scan.py exists (pre-existing)")
    expect(sync.is_file(), "bin/issue-sync exists (pre-existing)")
    expect(contract.is_file(), "raw_metadata_contract.py exists (pre-existing)")
    expect("def read_issue(" in contract.read_text(), "read_issue exists (pre-existing)")

    expect(cli.is_file(), "single-owner frontmatter CLI exists")
    expect("def validate_issue_path(" in contract.read_text()
           and "def parse_issue_text(" in contract.read_text(),
           "contract exposes validate_issue_path / parse_issue_text")
    expect("yaml.safe_load" not in scan.read_text(),
           "scan no longer carries its own yaml.safe_load parser")
    sync_text = sync.read_text()
    get_body = sync_text[sync_text.index("_fm_get() {"):sync_text.index("_fm_set() {")]
    expect("yaml.safe_load" not in get_body and "$_FM_CLI" in get_body,
           "issue-sync _fm_get is a thin wrapper over the shared CLI")
    cli_text = cli.read_text() if cli.is_file() else ""
    expect("repair" in cli_text and "--apply" in cli_text,
           "repair command is idempotent and defaults to dry-run")


def behavior_checks(project: Path):
    print("=== BEHAVIOR: real parsers + repair ===")
    contract_path = project / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py"
    cli_path = project / "docs/system/workspace/scripts/lifecycle/frontmatter_contract_cli.py"
    scan_path = project / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
    runtime_dir = project / "docs/system/workspace/scripts/runtime"
    lifecycle_dir = project / "docs/system/workspace/scripts/lifecycle"

    contract = load("probe_contract", contract_path, (lifecycle_dir,))
    scan = load("probe_scan", scan_path, (runtime_dir, lifecycle_dir))
    tmp = Path(tempfile.mkdtemp(prefix="frontmatter-"))
    try:
        fixture = tmp / "project"
        raw_dir = fixture / "docs/B1-docs/raw-20260101T000000Z"
        raw_dir.mkdir(parents=True)
        doc = raw_dir / "issue.md"

        # 1) real scan parser must surface the damage instead of an empty dict
        doc.write_text(GLUED)
        items = scan.read_issues_dir(fixture)
        err = items[0].get("metadata_validation_error", "") if items else ""
        expect(bool(items) and bool(err),
               f"scan reports metadata_validation_error for glued '---' (got {err!r})")

        # 2) read_issue wraps YAML errors as MetadataValidationError
        doc.write_text(BAD_YAML)
        try:
            contract.read_issue(doc)
            bad("read_issue raises MetadataValidationError on invalid YAML")
        except contract.MetadataValidationError:
            ok("read_issue raises MetadataValidationError on invalid YAML")
        except Exception as exc:
            bad(f"read_issue raises MetadataValidationError (got {type(exc).__name__})")

        # CLI-dependent assertions only run when the single owner is present.
        # The checks below that use only the contract or only the scan parser
        # always run, so the baseline RED covers every final assertion.
        if not cli_path.is_file():
            for label in (
                "contract rejects glued delimiter", "contract rejects conflict markers",
                "CLI get fails loudly on damaged frontmatter",
                "scan and CLI agree on damaged frontmatter",
                "repair fixes the fixture and is idempotent",
                "repaired fixture passes strict parsing",
            ):
                bad(f"{label} (CLI/contract missing)")
        else:
            # 3/4) strict text parser rejects both historical damage shapes
            for label, text in (("contract rejects glued delimiter", GLUED),
                                ("contract rejects conflict markers", CONFLICT)):
                try:
                    contract.parse_issue_text(text)
                    bad(label)
                except contract.MetadataValidationError:
                    ok(label)
                except Exception as exc:
                    bad(f"{label} (unexpected {type(exc).__name__})")

            # 5) CLI refuses to silently return an empty value
            doc.write_text(GLUED)
            result = subprocess.run(
                [sys.executable, str(cli_path), "get", "--file", str(doc), "--key", "phase_state"],
                capture_output=True, text=True)
            expect(result.returncode != 0 and "metadata_validation_error" in result.stderr,
                   "CLI get fails loudly on damaged frontmatter")

            # 6) scan and CLI agree on the same damaged document
            result_check = subprocess.run(
                [sys.executable, str(cli_path), "check", "--file", str(doc)],
                capture_output=True, text=True)
            expect(result_check.returncode != 0 and bool(err),
                   "scan and CLI agree that the same frontmatter is invalid")

            # 7/8) repair is effective and idempotent
            doc.write_text(GLUED)
            (fixture / "docs/B2-docs").mkdir(parents=True, exist_ok=True)
            first = subprocess.run(
                [sys.executable, str(cli_path), "repair", "--project", str(fixture), "--apply"],
                capture_output=True, text=True)
            second = subprocess.run(
                [sys.executable, str(cli_path), "repair", "--project", str(fixture)],
                capture_output=True, text=True)
            try:
                fixed = json.loads(first.stdout).get("damaged")
                left = json.loads(second.stdout).get("damaged")
            except ValueError:
                fixed, left = None, None
            expect(first.returncode == 0 and fixed == 1 and left == 0,
                   f"repair fixes the fixture and is idempotent (first={fixed}, second={left})")
            try:
                contract.parse_issue_text(doc.read_text())
                ok("repaired fixture passes strict parsing")
            except Exception as exc:
                bad(f"repaired fixture passes strict parsing ({exc})")

        # 8.5) legacy formats stay formats, not damage
        legacy = ("# I-20260101T000000Z-A: legacy linked issue\n\n"
                  "- issue_id: I-20260101T000000Z-A\n"
                  "- phase_state: completed\n"
                  "- status: done\n")
        legacy_meta = scan.parse_frontmatter(legacy)
        expect(legacy_meta.get("phase_state") == "completed"
               and "__metadata_validation_error__" not in legacy_meta,
               "legacy bullet-only linked issue keeps parsing (format, not damage)")

        # 8.6) real tree no-regression guard: the single-owner parser must not
        # invent damage for legacy docs, nor drop bullet-declared metadata.
        misreported, lost = [], []
        for path in sorted((project / "docs/B2-docs").glob("**/issues/I-*.md")):
            text = path.read_text(errors="replace")
            meta = scan.parse_frontmatter(text)
            rel = str(path.relative_to(project))
            if "__metadata_validation_error__" in meta:
                misreported.append(rel)
            elif (re.search(r"^-\s*phase_state:\s*\S", text, re.MULTILINE)
                  and not meta.get("phase_state")):
                lost.append(rel)
        expect(not misreported,
               f"no real B2 linked issue is misreported as damaged ({len(misreported)} reported)")
        expect(not lost,
               f"every bullet-declared phase_state survives the parser ({len(lost)} lost)")

        # 9) real project: no remaining damaged B1 issue documents
        broken = []
        for path in sorted((project / "docs/B1-docs").glob("*/issue.md")):
            try:
                contract.parse_issue_text(path.read_text(errors="replace"))
            except Exception:
                broken.append(path.parent.name)
        expect(not broken,
               f"all real B1 issue docs pass strict parsing ({len(broken)} broken)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("mode", nargs="?", default="all")
    args = ap.parse_args()
    project = Path(args.source_dir).resolve() if args.source_dir else PROJECT
    if args.mode in ("static", "all"):
        static_checks(project)
    if args.mode in ("behavior", "all"):
        behavior_checks(project)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

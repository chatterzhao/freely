#!/usr/bin/env python3
"""AT-001 — raw-20261110T130144Z / #4286 (round 1 of the #4166 remainder).

Three defects, one contract each:

1. ``bin/issue-sync`` was a 1330-line single file: no subcommand could be
   sourced or tested on its own, so every change needed an end-to-end run.
   GREEN requires the main file to lose at least half its lines and every
   subcommand to live in its own sourceable module.
2. ``freely feedback`` and ``issue-sync create`` built the platform body and
   the label list independently (a hard-coded ``kind/raw,phase/proposed,…``
   literal versus shell-derived labels, and an ``awk`` "strip" that only
   deleted the ``---`` markers). GREEN requires one shared contract.
3. ``bin/issue-sync-bootstrap --delete`` called ``gh issue delete`` directly —
   the only platform write outside ``platform-adapter.py`` and undocumented.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("ISSUE_SYNC_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

ISSUE_SYNC = SRC / "bin/issue-sync"
MODULE_DIR = SRC / "bin/issue-sync.d"
BOOTSTRAP = SRC / "bin/issue-sync-bootstrap"
ADAPTER = SRC / "docs/system/workspace/scripts/sync/platform-adapter.py"
CONTRACT = SRC / "docs/system/workspace/scripts/sync/issue_create_contract.py"
RUNTIME = SRC / "docs/system/workspace/scripts/runtime/freely"

# The pre-split file was 1330 lines; the contract is "at least half gone".
PRE_SPLIT_LINES = 1330
MAX_MAIN_LINES = PRE_SPLIT_LINES // 2

CMD_MODULES = {
    "cmd-create.sh": "cmd_create",
    "cmd-update.sh": "cmd_update",
    "cmd-comment.sh": "cmd_comment",
    "cmd-close.sh": "cmd_close",
    "cmd-promote.sh": "cmd_promote",
    "cmd-promote-finalize.sh": "cmd_promote_finalize",
    "cmd-batch.sh": "cmd_batch",
    "cmd-scan.sh": "cmd_scan",
    "cmd-status.sh": "cmd_status",
}

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


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


# ── STATIC: one module per subcommand ────────────────────────────────────

def static_split() -> None:
    print("=== STATIC: issue-sync is a dispatcher, not a monolith ===")
    main_text = read(ISSUE_SYNC)
    lines = main_text.splitlines()
    expect(len(lines) <= MAX_MAIN_LINES,
           f"bin/issue-sync <= {MAX_MAIN_LINES} lines (got {len(lines)})")

    expect("issue-sync.d" in main_text and "source " in main_text,
           "bin/issue-sync sources its module directory")

    defined_in_main = [fn for fn in CMD_MODULES.values()
                       if f"{fn}() {{" in main_text]
    expect(not defined_in_main,
           f"no subcommand is defined inline ({defined_in_main})")

    for module, function in CMD_MODULES.items():
        path = MODULE_DIR / module
        expect(path.is_file() and f"{function}() {{" in read(path),
               f"{module} defines {function}()")

    libs = sorted(module.name for module in MODULE_DIR.glob("lib-*.sh")) if MODULE_DIR.is_dir() else []
    expect(len(libs) >= 3, f"shared helpers live in lib-*.sh ({libs})")


# ── STATIC: one create contract ──────────────────────────────────────────

def static_contract() -> None:
    print("=== STATIC: one body/label contract ===")
    contract = read(CONTRACT)
    expect(all(name in contract for name in ("strip_frontmatter", "platform_body", "labels_for")),
           "issue_create_contract.py owns strip_frontmatter/platform_body/labels_for")

    content_lib = read(MODULE_DIR / "lib-content.sh")
    expect("issue_create_contract.py" in content_lib,
           "issue-sync renders the body through the contract")
    expect('labels="$labels,severity/' not in content_lib,
           "issue-sync no longer assembles the label list itself")

    runtime = read(RUNTIME)
    expect("kind/raw,phase/proposed" not in runtime,
           "freely feedback no longer hard-codes the label list")
    expect("issue_create_contract.py" in runtime,
           "freely feedback renders through the contract")
    expect("--phase proposed" in runtime,
           "feedback states its phase instead of embedding it in a literal")


# ── STATIC: bootstrap delete goes through the adapter ────────────────────

def static_bootstrap() -> None:
    print("=== STATIC: bootstrap delete is a platform write ===")
    bootstrap = read(BOOTSTRAP)
    adapter = read(ADAPTER)
    expect("gh issue delete" not in bootstrap,
           "issue-sync-bootstrap does not call gh issue delete")
    expect("issue-write-one github delete" in bootstrap,
           "issue-sync-bootstrap deletes through the adapter")
    expect("def delete_issue" in adapter, "adapter exposes delete_issue")
    expect('action == "delete"' in adapter, "adapter dispatches the delete action")


# ── fixtures ─────────────────────────────────────────────────────────────

def seed_fixture(fix: Path, raw_id: str = "raw-20260101T000000Z") -> None:
    (fix / "bin").mkdir(parents=True, exist_ok=True)
    shutil.copy(ISSUE_SYNC, fix / "bin" / "issue-sync")
    if MODULE_DIR.is_dir():
        shutil.copytree(MODULE_DIR, fix / "bin" / "issue-sync.d")
    for rel in ("docs/system/workspace/scripts/lifecycle",
                "docs/system/workspace/scripts/sync"):
        dst = fix / rel
        dst.mkdir(parents=True, exist_ok=True)
        for path in (SRC / rel).glob("*.py"):
            shutil.copy(path, dst / path.name)
    (fix / "docs" / "B1-docs" / raw_id).mkdir(parents=True, exist_ok=True)


RAW_DOC = """---
schema_version: '1'
local_id: raw-20260101T000000Z
kind: raw
phase_state: proposed
severity: P0
primary_platform: github
platform_ids: {}
created_at: '2026-01-01T00:00:00Z'
updated_at: '2026-01-01T00:00:00Z'
---

workflow_kind: fix

# 探针标题

## 根因

正文第一段。

## Comments

### comment-20260101T010000Z
- source: system

这行不该出现在平台正文里。
"""


def source_call(fix: Path, expr: str) -> subprocess.CompletedProcess:
    script = (
        'set -uo pipefail; '
        f'ROOT_DIR="{fix}"; source "$ROOT_DIR/bin/issue-sync"; '
        f'set +e; {expr}'
    )
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=90)


# ── BEHAVIOR: modules are sourceable, projection is single-owner ─────────

def behavior_checks() -> None:
    print("=== BEHAVIOR: sourcing, labels, body ===")
    fix = Path(tempfile.mkdtemp(prefix="freely-issue-sync-modules.")).resolve()
    try:
        seed_fixture(fix)
        functions = " ".join(["cmd_create", "cmd_update", "cmd_comment", "cmd_close",
                              "cmd_promote", "cmd_promote_finalize", "cmd_batch",
                              "cmd_scan", "cmd_status", "_issue_body", "_labels"])
        proc = source_call(fix, f"declare -F {functions} | wc -l")
        expect(proc.stdout.strip() == "11",
               f"sourcing bin/issue-sync defines every entry point (got {proc.stdout.strip()})")

        doc = fix / "docs" / "B1-docs" / "raw-20260101T000000Z" / "issue.md"
        doc.write_text(RAW_DOC)

        labels = source_call(fix, f'_labels "{doc}"').stdout.strip()
        contract_labels = subprocess.run(
            [sys.executable, str(CONTRACT), "labels", "--file", str(doc)],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip()
        expect(labels == contract_labels == "kind/raw,phase/proposed,severity/P0",
               f"issue-sync and the contract agree on labels ({labels!r})")

        doc.write_text(RAW_DOC.replace("severity: P0\n", ""))
        legacy = source_call(fix, f'_labels "{doc}"').stdout.strip()
        expect(legacy.endswith("severity/P2"),
               f"legacy document without severity still yields P2 ({legacy!r})")
        doc.write_text(RAW_DOC)

        body = source_call(fix, f'_issue_body "{doc}" "raw-20260101T000000Z"').stdout
        expect(body.startswith("---\n") and body.count("schema_version") == 1,
               "platform body carries exactly one fenced frontmatter block")
        expect("workflow_kind: fix" in body, "platform body keeps workflow_kind")
        expect("## 探针标题" in body and "| local_id | `raw-20260101T000000Z` |" in body,
               "platform body keeps the title header and the field table")
        expect("## 根因" in body and "正文第一段。" in body,
               "platform body keeps the human body")
        expect("这行不该出现在平台正文里" not in body,
               "platform body drops the Comments section")

        # The contract must be the *only* renderer: the same document handed to
        # it directly (feedback's path) yields byte-identical output.
        direct = subprocess.run(
            [sys.executable, str(CONTRACT), "body", "--file", str(doc),
             "--local-id", "raw-20260101T000000Z", "--title", "探针标题"],
            capture_output=True, text=True, timeout=60,
        ).stdout
        expect(body == direct, "issue-sync and the contract render identical bodies")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


# ── BEHAVIOR: bootstrap delete reaches the adapter ───────────────────────

def behavior_bootstrap() -> None:
    print("=== BEHAVIOR: bootstrap --delete routes through the adapter ===")
    tmp = Path(tempfile.mkdtemp(prefix="freely-issue-sync-bootstrap.")).resolve()
    try:
        repo = tmp / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=False)
        subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                        "https://github.com/acme/demo.git"], check=False)
        (repo / "bin").mkdir()
        shutil.copy(BOOTSTRAP, repo / "bin" / "issue-sync-bootstrap")
        # The adapter imports freely_user_env from scripts/runtime; a fixture
        # without it fails on import, which would look like a product defect.
        for rel in ("docs/system/workspace/scripts/sync",
                    "docs/system/workspace/scripts/runtime"):
            dst = repo / rel
            dst.mkdir(parents=True, exist_ok=True)
            for path in (SRC / rel).glob("*.py"):
                shutil.copy(path, dst / path.name)

        gh_log = tmp / "gh.log"
        bindir = tmp / "stub"
        bindir.mkdir()
        stub = bindir / "gh"
        stub.write_text(
            "#!/usr/bin/env bash\n"
            f'printf \'%s\\n\' "$*" >> "{gh_log}"\n'
            'if [[ "$*" == *"repo view"* ]]; then echo "acme/demo"; exit 0; fi\n'
            "exit 0\n"
        )
        stub.chmod(0o755)

        env = dict(os.environ)
        env["PATH"] = f"{bindir}:" + env.get("PATH", "")
        env.pop("FREELY_PLATFORM_REPO", None)
        proc = subprocess.run(
            ["bash", str(repo / "bin" / "issue-sync-bootstrap"), "--delete",
             "https://github.com/acme/demo/issues/42"],
            cwd=str(repo), env=env, capture_output=True, text=True, timeout=120,
        )
        log = gh_log.read_text() if gh_log.is_file() else ""
        expect("issue delete" in log and "--repo acme/demo" in log,
               f"delete reaches gh with the adapter-resolved repo ({log.splitlines()[-1:]})")
        expect('"status": "deleted"' in proc.stdout,
               f"bootstrap reports the adapter receipt ({proc.stdout.strip()[:80]!r})")
        expect("https://github.com/acme/demo/issues/42" not in log,
               "the raw URL is no longer handed to gh")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    print(f"AT-001 source: {SRC}")
    static_split()
    static_contract()
    static_bootstrap()
    behavior_checks()
    behavior_bootstrap()
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

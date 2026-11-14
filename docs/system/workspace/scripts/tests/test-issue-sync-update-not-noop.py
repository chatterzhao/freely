#!/usr/bin/env python3
"""AT — `issue-sync update` must be able to normalize a platform replica.

Why this exists
---------------
`raw-20261114T101138Z` (GitHub #4653 / Gitee IKVBNJ) could not pass
`raw-reconciliation-gate`: its GitHub title had lost the `[RAW-<key>]`
prefix, so `_resolve_raw_identity()` fell back to three body matches and
failed closed as `ambiguous`. The documented way to fix a platform title is
`freely feedback edit` / `issue-sync update` — both project through
`_platform_title()`.

They could not fix it, because the scan-state bookkeeping is one-way:

  * `_scan_state_record_sync()` writes `{mtime, synced_at}` and never `hash`;
  * `_changed_since_last_sync()` reads `synced_issues.<id>.hash` and treats a
    missing hash as "unchanged".

So `cmd_update()` returned `skip update: ... unchanged since last sync` for
every issue that had ever been created — the explicit, operator-initiated
update path was a permanent no-op, and no platform replica could ever be
normalized without hand-editing the platform.

Contracts pinned here
---------------------
1. `_scan_state_record_sync()` records the content hash it claims to compare.
2. A legacy entry (recorded before hashes existed) counts as *changed*, so a
   normal `update`/`scan`/`batch` can repair it instead of skipping forever.
3. `cmd_update()` — an explicit single-issue command — is not gated by the
   batch de-duplication heuristic at all.

Run:
  RED   : python3 test-issue-sync-update-not-noop.py --source-dir <develop>
  GREEN : python3 test-issue-sync-update-not-noop.py
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import json
import os
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

LIB_STATE = SRC / "bin/issue-sync.d/lib-state.sh"
CMD_UPDATE = SRC / "bin/issue-sync.d/cmd-update.sh"

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  FAIL {message}")
        FAILURES.append(message)


def _bash(script: str, env_extra: dict[str, str]) -> subprocess.CompletedProcess:
    env = {**os.environ, **env_extra}
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)


def test_record_sync_stores_the_hash() -> None:
    """The writer must record what the reader compares."""
    print("AT-1: _scan_state_record_sync records the content hash")
    with tempfile.TemporaryDirectory() as tmp:
        issues = Path(tmp)
        doc = issues / "issue.md"
        doc.write_text("# title\n\nbody\n", encoding="utf-8")
        script = f'''
set -eu
ISSUES_DIR="{issues}"
source "{LIB_STATE}"
_scan_state_record_sync "raw-20260101T000000Z" "{doc}"
cat "{issues}/.scan-state"
'''
        proc = _bash(script, {})
        state_text = proc.stdout.strip()
        try:
            state = json.loads(state_text or "{}")
        except json.JSONDecodeError:
            state = {}
        entry = (state.get("synced_issues") or {}).get("raw-20260101T000000Z") or {}
        check(bool(entry.get("hash")), "synced_issues entry carries a `hash` field")
        check(
            entry.get("hash") == subprocess.run(
                ["bash", "-c", f'''
ISSUES_DIR="{issues}"
source "{LIB_STATE}"
_content_hash "{doc}"
'''], capture_output=True, text=True).stdout.strip(),
            "recorded hash equals _content_hash() of the same file",
        )


def test_legacy_entry_is_treated_as_changed() -> None:
    """A pre-hash record must be repairable, not permanently frozen."""
    print("AT-2: legacy scan-state entry (no hash) counts as changed")
    with tempfile.TemporaryDirectory() as tmp:
        issues = Path(tmp)
        doc = issues / "issue.md"
        doc.write_text("# title\n\nbody\n", encoding="utf-8")
        (issues / ".scan-state").write_text(json.dumps({
            "last_sync_at": "2026-01-01T00:00:00Z",
            "synced_issues": {
                "raw-20260101T000000Z": {"mtime": 1, "synced_at": "2026-01-01T00:00:00Z"},
            },
        }), encoding="utf-8")
        script = f'''
ISSUES_DIR="{issues}"
source "{LIB_STATE}"
if _changed_since_last_sync "raw-20260101T000000Z" "{doc}"; then echo CHANGED; else echo UNCHANGED; fi
'''
        proc = _bash(script, {})
        check(proc.stdout.strip() == "CHANGED", "legacy entry without hash reports CHANGED")

        # A never-recorded issue keeps the original "first sync" semantics.
        script_new = f'''
ISSUES_DIR="{issues}"
source "{LIB_STATE}"
if _changed_since_last_sync "raw-20260202T000000Z" "{doc}"; then echo CHANGED; else echo UNCHANGED; fi
'''
        proc_new = _bash(script_new, {})
        check(
            proc_new.stdout.strip() == "UNCHANGED",
            "unknown issue still reports UNCHANGED (initial batch is not spammed)",
        )


def test_explicit_update_is_not_gated() -> None:
    """`update` is an operator command, not a batch scan."""
    print("AT-3: cmd_update does not gate on the batch de-duplication heuristic")
    source = CMD_UPDATE.read_text(encoding="utf-8") if CMD_UPDATE.is_file() else ""
    check(bool(source), "cmd-update.sh exists")
    check(
        "_changed_since_last_sync" not in source,
        "cmd-update.sh does not call _changed_since_last_sync",
    )
    check(
        "skip update" not in source,
        "cmd-update.sh has no `skip update` short-circuit",
    )


def test_body_projection_does_not_re_emit_the_local_h1() -> None:
    """The local H1 anchors the title; the platform body carries `## <title>`.

    A real platform body (e.g. #4654) starts at `## <title>` + the metadata
    table. Re-emitting the document's own `# <title>` after the governance
    note duplicates the header, and the replica gate then reports
    `content_diverged` forever because the local projection strips that H1.
    """
    print("AT-4: body projection does not duplicate the local H1")
    contract = SRC / "docs/system/workspace/scripts/sync/issue_create_contract.py"
    if not contract.is_file():
        check(False, "issue_create_contract.py exists")
        return
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "issue.md"
        doc.write_text(
            "---\n"
            "local_id: raw-20260101T000000Z\n"
            "kind: raw\n"
            "phase_state: proposed\n"
            "---\n\n"
            "# feat: demo title\n\n"
            "## 现象\n\ntext\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(contract), "body", "--file", str(doc),
             "--local-id", "raw-20260101T000000Z", "--title", "feat: demo title"],
            capture_output=True, text=True,
        )
        out = proc.stdout
        check(proc.returncode == 0, "contract body renders")
        check("## feat: demo title" in out, "generated body carries the `## <title>` header")
        body_lines = [line for line in out.splitlines() if line.startswith("# ")]
        check(body_lines == [], f"no duplicated H1 in platform body (found {body_lines})")


def test_body_projection_is_idempotent() -> None:
    """Re-projecting an already-projected document must not add a second header.

    A document materialised from a platform copy already carries the generated
    header (`## <title>` + metadata table + `---` + governance note). The
    projector must recognise it and emit exactly one header, otherwise every
    `issue-sync update` doubles the header and the replica gate reports
    `content_diverged` again (#4653).
    """
    print("AT-5: body projection is idempotent for a materialised document")
    contract = SRC / "docs/system/workspace/scripts/sync/issue_create_contract.py"
    if not contract.is_file():
        check(False, "issue_create_contract.py exists")
        return

    front = (
        "---\nlocal_id: raw-20260101T000000Z\nkind: raw\n"
        "phase_state: proposed\n---\n\n"
    )
    plain = front + "# feat: demo title\n\n## 现象\n\ntext\n"
    # Same document after one materialisation round: H1 + generated header.
    rendered = (
        front
        + "# feat: demo title\n\n"
        + "## feat: demo title\n\n"
        + "| Field | Value |\n|-------|-------|\n"
        + "| local_id | `raw-20260101T000000Z` |\n| kind | `raw` |\n"
        + "| phase_state | `proposed` |\n| canonical | `none` |\n"
        + "| created | unknown |\n| updated | unknown |\n\n"
        + "---\n\n"
        + "> **Freely 治理**：这是 raw issue `raw-20260101T000000Z`。实现前请用 "
          "`wt-create --raw-key 20260101T000000Z` 创建专属工位，确保代码修改在包含此 "
          "raw-key 的分支上进行。\n\n"
        + "## 现象\n\ntext\n"
    )

    def render(text: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "issue.md"
            doc.write_text(text, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(contract), "body", "--file", str(doc),
                 "--local-id", "raw-20260101T000000Z", "--title", "feat: demo title"],
                capture_output=True, text=True,
            )
            return proc.stdout

    plain_body, rendered_body = render(plain), render(rendered)
    check(plain_body.count("| Field | Value |") == 1, "plain document yields one header")
    check(rendered_body.count("| Field | Value |") == 1,
          f"materialised document yields one header (got {rendered_body.count('| Field | Value |')})")
    check(plain_body == rendered_body, "both document shapes project to the same body")


def test_mirrored_comment_does_not_leak_into_the_body() -> None:
    """A mirrored comment whose text starts with `##` stays out of the body.

    Comment blocks are delivered as real platform comments. Ending the skip at
    "any `###`/`##` heading" let a comment that opens with `## 方案修正` fall
    back into the body, so the body projection disagreed with the local
    projection forever (#4653).
    """
    print("AT-6: a mirrored comment that starts with a heading stays out of the body")
    contract = SRC / "docs/system/workspace/scripts/sync/issue_create_contract.py"
    if not contract.is_file():
        check(False, "issue_create_contract.py exists")
        return
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "issue.md"
        doc.write_text(
            "---\nlocal_id: raw-20260101T000000Z\nkind: raw\n"
            "phase_state: proposed\n---\n\n"
            "# feat: demo title\n\n"
            "## 现象\n\ntext\n\n"
            "### comment-platform-1\n- source: platform\n- event: mirrored\n\n"
            "## 方案修正\n\n补充说明。\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(contract), "body", "--file", str(doc),
             "--local-id", "raw-20260101T000000Z", "--title", "feat: demo title"],
            capture_output=True, text=True,
        )
        out = proc.stdout
        check("## 现象" in out, "human body is kept")
        check("补充说明" not in out, "mirrored comment text is not published as body")
        check("comment-platform-1" not in out, "comment marker is not published as body")


def main() -> int:
    print(f"source: {SRC}")
    if not LIB_STATE.is_file():
        print(f"  FAIL lib-state.sh missing: {LIB_STATE}")
        print("SUMMARY: 0 ok, 1 failed")
        return 1
    test_record_sync_stores_the_hash()
    test_legacy_entry_is_treated_as_changed()
    test_explicit_update_is_not_gated()
    test_body_projection_does_not_re_emit_the_local_h1()
    test_body_projection_is_idempotent()
    test_mirrored_comment_does_not_leak_into_the_body()
    failed = len(FAILURES)
    ok = 23 - failed
    print(f"SUMMARY: {ok} ok, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

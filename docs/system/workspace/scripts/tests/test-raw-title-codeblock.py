#!/usr/bin/env python3
r"""AT-001 — raw-20261110T093145Z / #4269 (code-block-aware raw H1).

Both `platform-adapter.pull_raw_issue()` (materialization) and
`raw-reconciliation-gate._local_record()` (replica gate) looked for the local
H1 with a bare `^#\s+` regex. A raw body containing a python code block whose
comments start with `# ` (extremely common in bug reports) therefore:

  * made materialization THINK an H1 already existed and skip injecting one;
  * made the gate pick `# -> StateFileError: ...` as the LOCAL title, then
    discard everything before it, producing `content_diverged` and blocking
    `pr-create-guarded` for a healthy raw.

Fix: a single code-block-aware heading finder in `raw_title_contract.py`,
reused by both sides; the gate emits an explicit `missing_local_title`
diagnostic instead of silently borrowing a code comment.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (bare regex -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from importlib.machinery import SourceFileLoader
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[5]
SRC = Path(os.environ.get("TITLE_SOURCE_ROOT", str(PROJECT))).resolve()

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


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_loader(name, SourceFileLoader(name, str(path)))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def static_checks(src: Path) -> None:
    print("=== STATIC: single code-block-aware contract, reused by both sides ===")
    contract = src / "docs/system/workspace/scripts/sync/raw_title_contract.py"
    adapter = src / "docs/system/workspace/scripts/sync/platform-adapter.py"
    gate = src / "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py"
    ctext = contract.read_text(encoding="utf-8") if contract.is_file() else ""
    atext = adapter.read_text(encoding="utf-8") if adapter.is_file() else ""
    gtext = gate.read_text(encoding="utf-8") if gate.is_file() else ""

    expect("def find_local_heading" in ctext and "_FENCE" in ctext
           and "fence_char" in ctext,
           "raw_title_contract exports a fenced-code-block-aware heading finder")
    expect("find_local_heading" in atext
           and not re.search(r're\.search\(r?"\^#\[ \\t\]\+\\S"', atext),
           "materialization reuses the finder instead of a bare ^# regex")
    expect("find_local_heading" in gtext and "missing_local_title" in gtext,
           "replica gate reuses the finder and reports an explicit missing title")

    backfill = src / "bin/raw-issue-backfill-h1"
    btext = backfill.read_text(encoding="utf-8") if backfill.is_file() else ""
    expect("find_local_heading" in btext and 'H1.search(body)' not in btext,
           "H1 backfill reuses the finder instead of its own bare regex")

    h1test = src / "docs/system/workspace/scripts/tests/test-materialize-h1"
    if h1test.is_file():
        r = subprocess.run(["bash", str(h1test), "all"], cwd=src,
                           capture_output=True, text=True, timeout=240)
        expect(r.returncode == 0,
               f"existing H1 regression suite still passes (rc={r.returncode})")
    else:
        bad("existing H1 regression suite still passes (test missing)")

    # The backfill command must repair a document whose only '# ' lines live
    # inside a code block, rather than skipping it as "already has a heading".
    backfill = src / "bin/raw-issue-backfill-h1"
    if backfill.is_file():
        probe = Path(tempfile.mkdtemp(prefix="h1-backfill-at-"))
        try:
            doc = probe / "docs" / "B1-docs" / "raw-CODEBLOCK" / "issue.md"
            doc.parent.mkdir(parents=True)
            (probe / "docs/system/workspace/scripts/sync").mkdir(parents=True)
            import shutil
            shutil.copy(src / "docs/system/workspace/scripts/sync/raw_title_contract.py",
                        probe / "docs/system/workspace/scripts/sync/raw_title_contract.py")
            doc.write_text(
                "---\nschema_version: '1'\nlocal_id: raw-CODEBLOCK\nkind: raw\n"
                "issue_title: 'fix: code comment is not a heading'\n---\n\n"
                "workflow_kind: fix\n\n```python\n"
                "# -> StateFileError: unknown state key\n```\n", encoding="utf-8")
            r = subprocess.run([sys.executable, str(backfill), "--project", str(probe),
                                "--apply", "--no-platform"],
                               capture_output=True, text=True, timeout=120)
            text = doc.read_text(encoding="utf-8")
            expect(r.returncode == 0 and "# fix: code comment is not a heading" in text,
                   "backfill repairs a doc whose only '# ' lines are code comments")
        finally:
            import shutil
            shutil.rmtree(probe, ignore_errors=True)
    else:
        bad("backfill repairs a doc whose only '# ' lines are code comments (cmd missing)")


def unit_checks(src: Path) -> None:
    print("=== UNIT: heading finder ignores fenced code blocks ===")
    contract = src / "docs/system/workspace/scripts/sync/raw_title_contract.py"
    if not contract.is_file():
        for _ in range(3):
            bad("heading finder (contract missing)")
        return
    try:
        c = _load("rtc_at", contract)
        finder = getattr(c, "find_local_heading", None)
    except Exception as exc:
        finder = None
        print(f"  (load error: {type(exc).__name__})")
    expect(callable(finder), "find_local_heading is callable")

    body_with_comment = """workflow_kind: fix

## 背景

```python
p.write_text('KEY="v"')
state_file.read_state(p)
# -> StateFileError: unknown state key: 'LAST_MANAGER_CONTINUITY_GENERATED'
```

## 修复
"""
    if callable(finder):
        got = finder(body_with_comment)
        expect(got is None,
               f"no H1 + code comment -> None, not a borrowed title (got {got!r})")
    else:
        bad("no H1 + code comment -> None (helper missing)")

    body_with_h1 = """# fix: real title

workflow_kind: fix

```python
# -> StateFileError: not a title
```
"""
    if callable(finder):
        got = finder(body_with_h1)
        title = got[0] if isinstance(got, (tuple, list)) else got
        expect(title == "fix: real title",
               f"real H1 wins over a later code comment (got {title!r})")
    else:
        bad("real H1 wins over a later code comment (helper missing)")

    # Guard: tilde fences and a normal H1 must still work.
    body_tilde = """~~~bash
# not a title
~~~

# fix: tilde fence title
"""
    if callable(finder):
        got = finder(body_tilde)
        title = got[0] if isinstance(got, (tuple, list)) else got
        expect(title == "fix: tilde fence title",
               f"tilde fences are ignored too (got {title!r})")
    else:
        bad("tilde fences are ignored too (helper missing)")


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: real materialization + real local record ===")
    adapter_path = src / "docs/system/workspace/scripts/sync/platform-adapter.py"
    gate_path = src / "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py"

    KEY = "20261110T093145Z"
    TITLE = f"[RAW-{KEY}] fix: code block comment must not become the raw title"
    FM = ("---\n"
          "schema_version: '1'\nlocal_id: raw-" + KEY + "\nkind: raw\nphase_state: proposed\n"
          "absorbed_into: ''\nplatform_ids: {}\nprimary_platform: github\n"
          "canonical_issue_path: ''\nlast_synced_comment_at: {}\nhash: ''\n"
          "created_at: '2026-11-10T09:31:45Z'\nupdated_at: '2026-11-10T09:31:45Z'\n"
          "intake_id: ''\nauthor: platform\nchannel: github\nsession_refs: []\n"
          "platform_state: open\npromoted_children: []\nsource_candidate: ''\n"
          "completed_at: ''\ncloseout_note: ''\n---\n\n")
    BODY = (FM + "workflow_kind: fix\n\n## 背景\n\n"
            "```python\nstate_file.read_state(p)\n"
            "# -> StateFileError: unknown state key: 'LAST_MANAGER_CONTINUITY_GENERATED'\n"
            "```\n\n## 修复\nx\n")

    if not adapter_path.is_file():
        bad("materialization injects an H1 despite the code comment (adapter missing)")
    else:
        try:
            pa = _load("pa_title_at", adapter_path)
            pa.discover_raw_replicas = lambda k: {
                "github": {"status": "ok", "issue_id": "4269", "title": TITLE, "body": BODY,
                           "created_at": "2026-11-10T09:31:45Z", "updated_at": "2026-11-10T09:31:45Z",
                           "labels": [], "url": "https://github.com/x/y/issues/4269", "state": "OPEN"},
            }
            pa.check_and_claim_assignee = lambda p, i, who: (True, "ok")
            pa._update_issue_title = lambda p, i, t: True
            target = tmp / "docs" / "B1-docs" / f"raw-{KEY}"
            pa.pull_raw_issue(KEY, target)
            text = (target / "issue.md").read_text(encoding="utf-8")
            # The heading must be the human part of the platform title and must
            # appear BEFORE the code comment (i.e. an actual H1 was injected).
            expect(text.find("# fix: code block comment") >= 0
                   and text.find("# fix: code block comment") < text.find("# -> StateFileError"),
                   "materialization injects a real H1 ahead of the code comment")
            expect("workflow_kind: fix" in text and "## 背景" in text,
                   "materialization preserves the full body")
        except Exception as exc:
            bad(f"materialization injects an H1 despite the code comment ({type(exc).__name__}: {exc})")
            bad("materialization preserves the full body (previous step failed)")
            text = ""

    # Real _local_record must NOT borrow the code comment as the title.
    if not gate_path.is_file():
        bad("local record does not borrow a code comment as title (gate missing)")
        bad("local record keeps the full body when no H1 exists (gate missing)")
        return
    try:
        gate = _load("gate_title_at", gate_path)
        doc = tmp / "issue-no-h1.md"
        doc.write_text("---\nlocal_id: raw-" + KEY + "\n---\n\n" +
                       "workflow_kind: fix\n\n```python\n# -> StateFileError: not a title\n```\n",
                       encoding="utf-8")
        rec = gate._local_record(doc, KEY)
        expect(rec["title"] == "",
               f"local record does not borrow a code comment as title (got {rec['title']!r})")
        expect("workflow_kind: fix" in rec["body"] and "StateFileError" in rec["body"],
               "local record keeps the full body when no H1 exists")
    except Exception as exc:
        bad(f"local record does not borrow a code comment as title ({type(exc).__name__}: {exc})")
        bad("local record keeps the full body when no H1 exists (previous step failed)")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="raw-title-at-"))
    try:
        static_checks(src)
        unit_checks(src)
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""AT-001 — raw-20261104T084406Z / #4187 (feedback --severity 落盘).

`freely feedback --severity P0|P1|P2` validates the value then DISCARDS it:
no raw frontmatter field, no platform label, no scan ordering, so priority is
lost and triage must be maintained by hand in an external goal file.

Design constraint (no regression, R2 precedent): RAW_METADATA_FIELDS is a
strict 21-field tuple that validate() enforces EXACTLY over 59 strict docs +
a hardcoded contract test + new_raw_metadata() self-validate. severity is
therefore an OPTIONAL 22nd field, defaulted to P2 at the read view
(normalize()), NOT a required field and NOT a bulk 824-file rewrite.

Harness is isolated: no real platform, no network, no writes to the protected
tree. It drives the REAL feedback runtime (sourced as a library) against a
stub platform-adapter that captures the create-issue argv, plus unit tests on
the REAL raw_metadata_contract, plus `_labels` behavior from the REAL
issue-sync sourced in a fixture tree.

Run against two source roots:
  RED   : --source-dir /tmp/<develop-baseline>  (no severity -> RED)
  GREEN : --source-dir <this worktree>          (severity -> GREEN)
  python3 test-feedback-severity.py [--source-dir DIR] [static|unit|behavior|all]
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent.parent.parent
SRC = Path(os.environ.get("ACP_SOURCE_ROOT", str(REPO))).resolve()

PASS = 0
FAIL = 0


def ok(m: str) -> None:
    global PASS
    PASS += 1
    print(f"  [ok] {m}")


def bad(m: str) -> None:
    global FAIL
    FAIL += 1
    print(f"  [FAIL] {m}")


def _runtime(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "runtime"


def _lifecycle(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "lifecycle"


def _sync(src: Path) -> Path:
    return src / "docs" / "system" / "workspace" / "scripts" / "sync"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── static checks ──────────────────────────────────────────────────────────
def static_checks() -> None:
    print("=== STATIC: severity wiring ===")
    contract = (_lifecycle(SRC) / "raw_metadata_contract.py").read_text()
    freely = (_runtime(SRC) / "freely").read_text()
    adapter = (_sync(SRC) / "platform-adapter.py").read_text()
    issue_sync = (SRC / "bin" / "issue-sync").read_text()

    if "VALID_SEVERITIES" in contract and "SEVERITY_FIELD" in contract:
        ok("contract declares severity levels + field")
    else:
        bad("contract missing severity (no VALID_SEVERITIES / SEVERITY_FIELD)")

    # feedback must pass severity into the new_raw_metadata() heredoc that builds
    # the created frontmatter (not merely validate it in the --severity case).
    fb_create = freely[freely.index("cmd_feedback()"):] if "cmd_feedback()" in freely else ""
    heredoc = ""
    if "new_raw_metadata(" in fb_create:
        start = fb_create.index("new_raw_metadata(")
        heredoc = fb_create[start:start + 400]
    if "severity=severity" in heredoc or "severity=" in heredoc:
        ok("feedback passes severity into new_raw_metadata frontmatter")
    else:
        bad("feedback still discards severity (new_raw_metadata has no severity arg)")

    if "severity/" in issue_sync:
        ok("issue-sync _labels emits severity/* label")
    else:
        bad("issue-sync has no severity label")

    if "labels" in adapter and "create_issue" in adapter and "def create_issue" in adapter:
        ok("platform-adapter create-issue present (label threading checked in behavior)")
    else:
        bad("platform-adapter create-issue missing")

    if "DEFAULT_SEVERITY" in contract and "normalize" in contract:
        ok("contract normalize backfills default severity")
    else:
        bad("contract normalize missing severity default")

    r = subprocess.run(["bash", "-n", str(SRC / "bin" / "issue-sync")],
                       capture_output=True, text=True)
    if r.returncode == 0:
        ok("issue-sync bash -n clean")
    else:
        bad(f"issue-sync syntax error: {r.stderr.strip()}")


# ── unit checks (pure contract) ────────────────────────────────────────────
def unit_checks() -> None:
    print("=== UNIT: raw_metadata_contract severity semantics ===")
    contract = load_module("rmc_under_test", _lifecycle(SRC) / "raw_metadata_contract.py")
    if not hasattr(contract, "VALID_SEVERITIES"):
        bad("contract has no VALID_SEVERITIES (severity not implemented) — RED")
        return

    base = dict(
        local_id="raw-20260101T000000Z", platform_ids={},
        primary_platform="github", created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z", author="platform", channel="github",
    )

    # 1. canonical 21-field doc (no severity) STILL validates — zero regression.
    m = contract.new_raw_metadata(**base)
    try:
        contract.validate(m)
        ok("canonical 21-field doc validates unchanged (no regression)")
    except Exception as e:
        bad(f"canonical doc no longer validates: {e}")

    # 2. new_raw_metadata(severity=...) appends a legal field.
    try:
        mp = contract.new_raw_metadata(**dict(base, severity="P0"))
        if mp.get("severity") == "P0" and list(mp)[-1] == "severity":
            ok("new_raw_metadata(severity=P0) appends severity: P0")
        else:
            bad(f"new_raw_metadata severity not appended correctly: {list(mp)}")
    except TypeError:
        bad("new_raw_metadata has no severity parameter")
    except Exception as e:
        bad(f"new_raw_metadata(severity) raised: {e}")

    # 3. validate accepts P0/P1/P2 and rejects junk.
    for lvl in ("P0", "P1", "P2"):
        try:
            contract.validate(contract.new_raw_metadata(**dict(base, severity=lvl)))
            ok(f"validate accepts severity {lvl}")
        except Exception as e:
            bad(f"validate rejected legal {lvl}: {e}")
    for junk in ("P3", "urgent", "", 7):
        mm = dict(contract.new_raw_metadata(**base)); mm["severity"] = junk
        try:
            contract.validate(mm)
            bad(f"validate accepted illegal severity {junk!r}")
        except Exception:
            ok(f"validate rejects illegal severity {junk!r}")

    # 4. normalize() backfills P2 for legacy docs (存量回填 at read view, no rewrite).
    legacy = {"local_id": "raw-x", "kind": "raw", "phase_state": "proposed", "platform_ids": {}}
    view = contract.normalize(legacy)
    if view.get("severity") == "P2":
        ok("normalize backfills default severity P2 for legacy docs")
    else:
        bad(f"normalize did not backfill P2: severity={view.get('severity')!r}")
    for lvl in ("P0", "P1", "P2"):
        view2 = contract.normalize(dict(legacy, severity=lvl))
        if view2.get("severity") == lvl:
            ok(f"normalize preserves explicit {lvl}")
        else:
            bad(f"normalize lost {lvl}: {view2.get('severity')!r}")
    view3 = contract.normalize(dict(legacy, severity="BOGUS"))
    if view3.get("severity") == "P2":
        ok("normalize coerces invalid severity to P2")
    else:
        bad(f"normalize leaked invalid severity: {view3.get('severity')!r}")


# ── behavior: drive the REAL feedback runtime in a stub fixture ─────────────
STUB_ADAPTER = r'''import json, os, sys
argv = sys.argv[1:]
log = os.environ.get("STUB_LOG", "")
if log:
    with open(log, "a") as f:
        f.write(json.dumps(argv) + "\n")
# argv: create-issue <local_id> <title> <body> [labels]
print(json.dumps({"github": {"status": "created", "issue_id": "101"},
                  "gitee": {"status": "created", "issue_id": "GG1"}}))
'''

STUB_CONFIG = r'''#!/usr/bin/env python3
print("FREELY_REPO_PLATFORMS=github,gitee")'''


def build_feedback_fixture() -> Path:
    # Copy the WHOLE docs/system/workspace tree (isolated temp dir): the freely
    # monolith sources a chain of runtime libs at load time, so every source
    # target must resolve. Then stub only the platform boundary + config.
    fix = Path(tempfile.mkdtemp(prefix="freely-fb-sev."))
    (fix / "bin").mkdir(parents=True)
    shutil.copytree(SRC / "docs" / "system" / "workspace", fix / "docs" / "system" / "workspace")
    rt = fix / "docs" / "system" / "workspace" / "scripts" / "runtime"
    sy = fix / "docs" / "system" / "workspace" / "scripts" / "sync"
    (sy / "platform-adapter.py").write_text(STUB_ADAPTER)
    (rt / "freely_config.py").write_text(STUB_CONFIG)
    (rt / "freely_config.py").chmod(0o755)
    return fix


def run_feedback(fix: Path, severity: str) -> tuple[int, str, list]:
    log = fix / "stub-log.jsonl"
    log.write_text("")
    env = dict(os.environ)
    env.update({
        "STUB_LOG": str(log),
        "FREELY_REPO_PLATFORMS": "github,gitee",
        "GH_REPO": "o/r", "GITEE_REPO": "o/r",
    })
    body_text = (
        "## 根因\\nseverity 校验后被丢弃，优先级信息丢失。\\n"
        "## 影响\\n无法按优先级分诊与排序，只能外部清单人工维护。\\n"
        "## 修复方案\\nfrontmatter 增加 severity 并纳入合同校验与平台标签。\\n"
    )
    script = (
        'set -uo pipefail; '
        f'ROOT_DIR="{fix}"; source "$ROOT_DIR/docs/system/workspace/scripts/runtime/freely"; '
        'set +e; cmd_feedback create --title "fix: probe severity" --body ' + f'"{body_text}" '
        f'--kind fix --severity {severity}; echo "RC=$?"'
    )
    r = subprocess.run(["bash", "-c", script], env=env, capture_output=True,
                       text=True, timeout=120)
    calls = []
    if log.exists():
        for line in log.read_text().splitlines():
            if line.strip():
                try:
                    calls.append(json.loads(line))
                except Exception:
                    pass
    return r.returncode, (r.stdout + "\n" + r.stderr), calls


def behavior_checks() -> None:
    print("=== BEHAVIOR: feedback create threads severity ===")
    fix = build_feedback_fixture()
    try:
        rc, out, calls = run_feedback(fix, "P0")
        if not calls:
            bad(f"feedback never called create-issue (stub got no argv). out={out[-600:]}")
            return
        argv = calls[0]
        body = argv[3] if len(argv) > 3 else ""
        labels = argv[4] if len(argv) > 4 else ""

        # RED criterion 1: frontmatter carries severity: P0
        sev_in_fm = ("severity: P0" in body or "severity: 'P0'" in body
                     or '"severity": "P0"' in body)
        if sev_in_fm:
            ok("--severity P0 -> frontmatter contains severity: P0")
        else:
            bad(f"--severity P0 -> frontmatter missing severity: {body[:220]!r}")
        if "severity/P0" in labels:
            ok("create-issue passes severity/P0 label")
        else:
            bad(f"create-issue labels missing severity/P0: labels={labels!r}")

        # no-regression: default P2 path yields legal severity + label.
        rc2, out2, calls2 = run_feedback(fix, "P2")
        if not calls2:
            bad("feedback P2 path produced no create-issue call")
        else:
            body2 = calls2[0][3] if len(calls2[0]) > 3 else ""
            labels2 = calls2[0][4] if len(calls2[0]) > 4 else ""
            sev2 = ("severity: P2" in body2 or "severity: 'P2'" in body2
                    or '"severity": "P2"' in body2)
            if sev2:
                ok("default severity P2 persisted explicitly")
            else:
                bad(f"default severity not in frontmatter: {body2[:160]!r}")
            if "severity/P2" in labels2:
                ok("default severity/P2 label passed")
            else:
                bad(f"default severity label missing: {labels2!r}")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def labels_checks() -> None:
    """REAL issue-sync _labels() emits severity/Pn from frontmatter (default P2)."""
    print("=== BEHAVIOR: issue-sync _labels severity ===")
    fix = Path(tempfile.mkdtemp(prefix="freely-lbl-sev."))
    try:
        (fix / "bin").mkdir(parents=True)
        shutil.copy(SRC / "bin" / "issue-sync", fix / "bin" / "issue-sync")
        d = fix / "docs" / "B1-docs" / "raw-20260101T000000Z"
        d.mkdir(parents=True)
        # P0 doc
        doc0 = d / "issue.md"
        doc0.write_text("---\nkind: raw\nphase_state: proposed\nseverity: P0\n---\n\n# probe\n")
        script = (
            'set -uo pipefail; '
            f'ROOT_DIR="{fix}"; source "$ROOT_DIR/bin/issue-sync"; '
            f'set +e; _labels "{doc0}"; echo "RC=$?"'
        )
        r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60)
        if "severity/P0" in r.stdout:
            ok("_labels emits severity/P0 for a P0 doc")
        else:
            bad(f"_labels missing severity/P0: {r.stdout.strip()!r} {r.stderr[-200:]!r}")
        # legacy doc without severity -> default P2 label (存量回填 at label view)
        doc1 = d / "issue.md"
        doc1.write_text("---\nkind: raw\nphase_state: proposed\n---\n\n# probe legacy\n")
        r2 = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60)
        if "severity/P2" in r2.stdout:
            ok("_labels defaults legacy doc to severity/P2")
        else:
            bad(f"_labels missing default severity/P2: {r2.stdout.strip()!r}")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def scan_checks() -> None:
    """cmd_scan orders P0 -> P1 -> P2 and backfills legacy docs as P2."""
    print("=== BEHAVIOR: scan orders by severity ===")
    fix = Path(tempfile.mkdtemp(prefix="freely-scan-sev."))
    try:
        (fix / "bin").mkdir(parents=True)
        shutil.copy(SRC / "bin" / "issue-sync", fix / "bin" / "issue-sync")
        b1 = fix / "docs" / "B1-docs"
        b1.mkdir(parents=True)
        docs = {
            "raw-20260101T000001Z": "P2",
            "raw-20260101T000002Z": "P0",
            "raw-20260101T000003Z": "P1",
            "raw-20260101T000004Z": "",  # legacy: no severity field
        }
        for lid, sev in docs.items():
            d = b1 / lid
            d.mkdir(parents=True)
            sev_line = f"severity: {sev}\n" if sev else ""
            (d / "issue.md").write_text(
                f"---\nkind: raw\nphase_state: proposed\n{sev_line}---\n\n# {lid}\n"
            )
        script = (
            'set -uo pipefail; '
            f'ROOT_DIR="{fix}"; source "$ROOT_DIR/bin/issue-sync"; '
            'set +e; cmd_scan; echo "RC=$?"'
        )
        r = subprocess.run(["bash", "-c", script], capture_output=True,
                           text=True, timeout=60)
        rows = [line for line in r.stdout.splitlines() if "CREATE " in line]
        import re
        sevs = [m.group(1) for line in rows
                for m in [re.search(r"sev=(P[012])", line)] if m]
        rank = {"P0": 0, "P1": 1, "P2": 2}
        ordered = [rank[s] for s in sevs]
        if len(ordered) == 4 and ordered == sorted(ordered):
            ok("scan output is ordered P0 -> P1 -> P2")
        else:
            bad(f"scan severity order wrong: {sevs} / rows={len(rows)} / {r.stdout[-300:]!r}")
        legacy_row = next((line for line in rows if "000004Z" in line), "")
        if "sev=P2" in legacy_row:
            ok("scan backfills legacy doc as sev=P2")
        else:
            bad(f"scan did not report legacy as P2: {legacy_row!r}")
    finally:
        shutil.rmtree(fix, ignore_errors=True)


def adapter_checks() -> None:
    """Real adapter forwards labels, and keeps the legacy 2-arg handler path."""
    print("=== BEHAVIOR: adapter create-issue label threading ===")
    mod = load_module("adapter_sev", _sync(SRC) / "platform-adapter.py")
    seen = []

    class Probe:
        name = "probe"

        def create_issue(self, title, body, labels=""):
            seen.append(labels)
            return {"status": "created"}

    class Legacy:
        name = "legacy"

        def create_issue(self, title, body):
            return {"status": "created"}

    mod.configured_platforms = lambda: ["probe"]
    mod._handler_for = lambda platform: Probe()
    # A develop baseline has create_issue(local_id, title, body) only; report
    # that as a normal RED failure instead of aborting the whole harness.
    try:
        result = mod.create_issue("raw-x", "t", "b", "severity/P0")
    except TypeError as exc:
        result = None
        bad(f"adapter create_issue has no labels parameter (RED): {exc}")
    if result is not None:
        if seen == ["severity/P0"] and result.get("probe", {}).get("status") == "created":
            ok("adapter forwards severity/P0 to the platform handler")
        else:
            bad(f"adapter dropped labels: seen={seen} result={result}")

    mod._handler_for = lambda platform: Legacy()
    legacy = mod.create_issue("raw-x", "t", "b")
    # configured_platforms() is stubbed to ["probe"], so the result key stays
    # "probe" even though the handler was replaced with a 2-arg legacy one.
    if any(item.get("status") == "created" for item in legacy.values()):
        ok("legacy 2-arg handler path unchanged (no regression)")
    else:
        bad(f"legacy create_issue broke: {legacy}")


def main() -> int:
    args = sys.argv[1:]
    mode = "all"
    i = 0
    while i < len(args):
        if args[i] == "--source-dir" and i + 1 < len(args):
            global SRC
            SRC = Path(args[i + 1]).resolve()
            i += 2
        else:
            mode = args[i]
            i += 1
    if mode not in ("static", "unit", "behavior", "all"):
        print("usage: ... [--source-dir DIR] [static|unit|behavior|all]", file=sys.stderr)
        return 2
    print(f"AT-001 source-dir: {SRC} mode: {mode}")
    if not (_runtime(SRC) / "freely").exists():
        print(f"[FATAL] no runtime/freely under {SRC}", file=sys.stderr)
        return 2
    if mode in ("static", "all"):
        static_checks()
    if mode in ("unit", "all"):
        unit_checks()
    if mode in ("behavior", "all"):
        behavior_checks()
        labels_checks()
        scan_checks()
        adapter_checks()
    print(f"SUMMARY: {PASS} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""AT-001 for raw-20261108T134853Z — GitHub labels must exist before `gh issue create`.

`feedback create` passes severity/Pn (plus kind/phase) to `gh issue create
--label`. GitHub does not auto-create labels, so a fresh clone/repo makes the
whole create fail and leaves a PARTIAL raw with no GitHub copy. The handler must
create the missing labels and retry, without extra work when labels already exist.

All behaviour runs against a fake `subprocess.run`; no real gh call is made.
"""
import argparse
import importlib.util
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
from unittest import mock

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


def load_adapter(project: Path):
    p = project / "docs/system/workspace/scripts/sync/platform-adapter.py"
    spec = importlib.util.spec_from_file_location("probe_adapter", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FakeGh:
    """Simulate gh: first issue create may fail because a label is missing."""

    def __init__(self, fail_kind=None, fail_twice=False):
        self.calls = []
        self.fail_kind = fail_kind  # None | "label" | "auth"
        self.fail_twice = fail_twice

    def issue_creates(self):
        return [c for c in self.calls if c[:3] == ["gh", "issue", "create"]]

    def label_creates(self):
        return [c for c in self.calls if c[:3] == ["gh", "label", "create"]]

    def run(self, args, **kwargs):
        self.calls.append(list(args))
        if args[:3] == ["gh", "issue", "create"]:
            n = len(self.issue_creates())
            if self.fail_kind and (n == 1 or (self.fail_twice and n == 2)):
                if self.fail_kind == "label":
                    return SimpleNamespace(
                        returncode=1, stdout="",
                        stderr="could not add label: 'severity/P0' not found\n",
                    )
                return SimpleNamespace(returncode=1, stdout="", stderr="authentication failed\n")
            return SimpleNamespace(
                returncode=0, stdout="https://github.com/o/r/issues/42\n", stderr=""
            )
        if args[:3] == ["gh", "repo", "view"]:
            return SimpleNamespace(returncode=0, stdout="o/r\n", stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")


def invoke(mod, fake, labels="severity/P0,kind/raw,phase/proposed"):
    handler = mod.GitHubHandler()
    handler._repo = lambda: "o/r"
    with mock.patch.object(mod.subprocess, "run", fake.run):
        result = handler.create_issue("title", "body", labels)
    return result


def static_checks(project: Path):
    print("=== STATIC: label bootstrap contract ===")
    text = (project / "docs/system/workspace/scripts/sync/platform-adapter.py").read_text()
    # Guards: these capabilities already exist on develop.
    expect("class GitHubHandler" in text, "GitHubHandler exists (pre-existing)")
    expect("def create_issue(self, title, body, labels=\"\")" in text,
           "create_issue already accepts labels (pre-existing)")
    expect('"gh", "label", "create"' in text or "gh label create" in text,
           "handler can create missing GitHub labels")
    expect("ensure_github_labels" in text or "ensure_labels" in text,
           "a dedicated label-ensure helper exists")
    body = text[text.index("    def create_issue(self, title, body, labels=\"\")"):]
    body = body[:body.index("\n    def ", 10)] if "\n    def " in body[10:] else body
    expect("ensure_github_labels" in body and "subprocess.run" in body,
           "create_issue body delegates label bootstrap and retries the create")

    # Same-round prerequisites (R13 precedent): a labelled raw must still pass
    # the replica-consistency gate. The local projection used to hard-code [].
    gate = (project / "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py").read_text()
    recon = (project / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py").read_text()
    expect('"labels": []' not in gate,
           "local replica projection no longer hard-codes empty labels")
    expect('startswith(("phase/", "severity/"))' in recon,
           "replica comparison excludes creation-time/presentation labels")


def behavior_checks(project: Path):
    print("=== BEHAVIOR: fake gh, no real platform calls ===")
    try:
        mod = load_adapter(project)
    except Exception as exc:
        bad(f"adapter module cannot be loaded: {exc}")
        return

    # 1) missing label -> create labels + retry -> created
    fake = FakeGh(fail_kind="label")
    result = invoke(mod, fake)
    expect(result.get("status") == "created",
           f"missing label is repaired and the issue is created ({result})")
    expect(len(fake.issue_creates()) == 2, "issue create is retried exactly once")
    expect(len(fake.label_creates()) == 3,
           f"one label create per requested label (got {len(fake.label_creates())})")

    # 2) no duplicate label create calls
    names = [c[3] for c in fake.label_creates()]
    expect(len(names) > 0 and len(names) == len(set(names)),
           "each label is created only once (idempotent)")

    # 3) labels already exist -> zero extra calls
    fake_ok = FakeGh(fail_kind=None)
    result_ok = invoke(mod, fake_ok)
    expect(result_ok.get("status") == "created" and not fake_ok.label_creates(),
           "healthy labels cause no label-create calls (idempotent fast path)")
    expect(len(fake_ok.issue_creates()) == 1, "healthy labels cause exactly one issue create")

    # 4) unrelated failure -> no retry, no label bootstrap
    fake_auth = FakeGh(fail_kind="auth")
    result_auth = invoke(mod, fake_auth)
    expect(result_auth.get("status") == "error" and len(fake_auth.issue_creates()) == 1
           and not fake_auth.label_creates(),
           "non-label failures are not masked or retried")

    # 5) no labels -> no label work at all
    fake_plain = FakeGh(fail_kind=None)
    result_plain = invoke(mod, fake_plain, labels="")
    expect(result_plain.get("status") == "created" and not fake_plain.label_creates(),
           "legacy no-label path stays untouched")

    # 6) retry still fails -> bounded, returns the error
    fake_twice = FakeGh(fail_kind="label", fail_twice=True)
    result_twice = invoke(mod, fake_twice, labels="severity/P0")
    expect(result_twice.get("status") == "error" and len(fake_twice.issue_creates()) == 2,
           "retry is bounded (no infinite loop) and still fails closed")

    # Same-round prerequisite: local vs platform label projections must agree.
    try:
        rp = project / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"
        spec = importlib.util.spec_from_file_location("probe_recon", str(rp))
        recon_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recon_mod)
        local = recon_mod.canonical_projection({
            "raw_key": "raw-X", "title": "t", "body": "b", "state": "absorbed",
            "labels": ["kind/raw"],
        })
        remote = recon_mod.canonical_projection({
            "raw_key": "raw-X", "title": "t", "body": "b", "state": "closed",
            "labels": ["kind/raw", "phase/proposed", "severity/P0"],
        })
        expect(local["labels"] == remote["labels"] == ("kind/raw",),
               "local and platform label projections agree for the same raw")
        drifted = recon_mod.canonical_projection({
            **{"raw_key": "raw-X", "title": "t", "body": "b", "state": "closed"},
            "labels": ["kind/linked"],
        })
        expect(drifted["labels"] != local["labels"],
               "a real kind/* label difference is still detected")

        gp = project / "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py"
        spec2 = importlib.util.spec_from_file_location("probe_gate", str(gp))
        gate_mod = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(gate_mod)
        with tempfile.TemporaryDirectory(prefix="gate-") as td:
            doc = Path(td) / "issue.md"
            doc.write_text(
                "---\nschema_version: '1'\nlocal_id: raw-20260101T000000Z\n"
                "kind: raw\nphase_state: absorbed\nseverity: P0\n---\n\n# t\n\nbody\n",
                encoding="utf-8",
            )
            record = gate_mod._local_record(doc, "20260101T000000Z")
            # R17 same-round fix: a document that does not declare labels must
            # not invent them, or legacy unlabelled platform copies diverge.
            expect(record["labels"] == [],
                   f"local projection leaves labels undeclared ({record['labels']})")
    except Exception as exc:
        bad(f"replica-label projection probe crashed: {exc}")


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

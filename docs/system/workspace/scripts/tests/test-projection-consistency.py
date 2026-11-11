#!/usr/bin/env python3
"""AT-001 for raw-20261104T080259Z / #4179 (R33).

A projection is a copy of a truth file that something else executes or reads:
`.githooks/<hook>` wraps `workspace/hooks/<hook>.sh`, `bin/<cmd>` projects onto
`workspace/scripts/**`, deployed skills are copies of `workspace/skills/**`, and
the generated AGENTS section quotes skill names. Nothing proved those copies
still matched their source, so `.githooks/` accumulated four dead `.sh` copies
and the AGENTS generator kept quoting `freely-fix-execution` /
`freely-feature-execution`, which do not exist.

This AT pins:
* `.githooks/` holds wrappers only — no `.sh` copies, no backups;
* `projection.lock` records source path + hash + target for all four kinds;
* `freely projections verify` exits 0 when consistent and non-zero when any
  projection is tampered with;
* the AGENTS generator and template quote only real skill names;
* the check runs in CI.

Runs against `git archive develop` to prove RED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-projection-consistency.py"
LOCK = "projection.lock"
VERIFIER = "docs/system/workspace/scripts/quality/projection_verify.py"
WRAPPERS = ["commit-msg", "post-checkout", "post-rewrite", "pre-commit",
            "pre-merge-commit", "pre-push", "pre-rebase", "reference-transaction"]
DEAD_COPIES = ["pre-commit.sh", "pre-merge-commit.sh", "pre-push.sh",
               "reference-transaction.sh"]
GHOST_SKILLS = ["freely-fix-execution", "freely-feature-execution", "freely-feat-execution"]
KINDS = {"hooks", "skills", "bin", "agents"}

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001 - report, never abort the suite
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def array_has(text: str, marker: str, entry: str) -> bool:
    i = text.index(marker) + len(marker)
    j = text.index(")", i)
    return entry in [line.strip() for line in text[i:j].splitlines()]


def load_lock(src: Path) -> dict:
    return json.loads((src / LOCK).read_text(encoding="utf-8"))


def skill_names(src: Path) -> set[str]:
    return {p.parent.name for p in (src / "docs/system/workspace/skills").glob("*/SKILL.md")}


def run_verifier(src: Path, project: Path | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, str(src / VERIFIER), "verify", "--project", str(project or src)]
    return subprocess.run(args, capture_output=True, text=True, timeout=180)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="", help="root to inspect (RED: a develop snapshot)")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else ROOT
    print(f"source: {src}")

    hooks_dir = src / ".githooks"

    # ---- static ----
    def c01():
        copies = [n for n in DEAD_COPIES if (hooks_dir / n).exists()]
        return not copies, f"dead hook copies still present: {copies}"

    def c02():
        extra = sorted(p.name for p in hooks_dir.iterdir()
                       if p.is_file() and p.name not in WRAPPERS and p.name != ".gitignore")
        return not extra, f"non-wrapper files in .githooks/: {extra}"

    def c03():
        missing = [n for n in WRAPPERS if not (hooks_dir / n).is_file()]
        return not missing, f"missing wrappers: {missing}"

    def c04():
        bad = []
        for name in WRAPPERS:
            text = (hooks_dir / name).read_text(encoding="utf-8", errors="replace")
            if "exec bash" not in text or "workspace/hooks/" not in text:
                bad.append(name)
        return not bad, f"wrappers that do not delegate to the truth script: {bad}"

    def c05():
        return (src / LOCK).is_file(), f"missing {LOCK}"

    def c06():
        doc = load_lock(src)
        need = {"schema_version", "owner", "entries"}
        return need.issubset(doc) and doc["schema_version"] == 1, \
            f"lock header incomplete: {sorted(doc)}"

    def c07():
        """The lock must declare all four kinds and carry the repo-local three.

        Deployed skills live under $HOME, so their entries go to a machine-local
        sibling lock (recorded by `deploy-skills`), never into the tracked one.
        """
        doc = load_lock(src)
        declared = set(doc.get("kinds") or [])
        present = {e.get("kind") for e in doc.get("entries", [])}
        repo_kinds = KINDS - {"skills"}
        return KINDS.issubset(declared) and repo_kinds.issubset(present), \
            f"declared={sorted(declared)} present={sorted(present)}"

    def c08():
        bad = []
        for entry in load_lock(src).get("entries", []):
            need = {"kind", "source", "target", "sha256"}
            if not need.issubset(entry):
                bad.append(f"{entry.get('target', '?')}: missing {sorted(need - set(entry))}")
        return not bad, "; ".join(bad[:3])

    def c09():
        bad = []
        for entry in load_lock(src).get("entries", []):
            for key in ("source", "target"):
                rel = entry.get(key) or ""
                if not rel or not (src / rel).exists():
                    bad.append(f"{entry.get('target')}: {key}={rel!r} does not exist")
        return not bad, "; ".join(bad[:3])

    def c10():
        """The recorded hash must equal the source file's real hash."""
        bad = []
        for entry in load_lock(src).get("entries", []):
            rel = entry.get("source") or ""
            path = src / rel
            if not path.is_file():
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != entry.get("sha256"):
                bad.append(rel)
        return not bad, f"stale hashes for {bad[:3]}"

    def c11():
        v = src / VERIFIER
        return v.is_file() and bool(v.stat().st_mode & 0o111), f"missing {VERIFIER}"

    def c12():
        """`freely projections` must reach the verifier through bin/projections.

        The dispatch is inline (the `harness-status` precedent) because the R31
        size budget forbids growing the monolith; what matters is that the entry
        point exists and ends at the real implementation.
        """
        mono = (src / "docs/system/workspace/scripts/runtime/freely").read_text(encoding="utf-8")
        dispatched = re.search(r"^\s+projections\) exec bash \"\$SELF_ROOT/bin/projections\"", mono, re.M)
        shim = src / "bin/projections"
        points = shim.is_file() and "projection_verify.py" in shim.read_text(encoding="utf-8")
        return dispatched is not None and points, \
            f"dispatch={dispatched is not None} bin/projections->{points}"

    def c13():
        ghosts = []
        for rel in ("docs/system/workspace/AGENTS.md.example",
                    "docs/system/workspace/scripts/runtime/freely"):
            text = (src / rel).read_text(encoding="utf-8", errors="replace")
            for ghost in GHOST_SKILLS:
                if ghost in text:
                    ghosts.append(f"{rel}:{ghost}")
        return not ghosts, f"non-existent skill names still quoted: {ghosts}"

    def c14():
        """Every skill name quoted by the template must exist on disk."""
        text = (src / "docs/system/workspace/AGENTS.md.example").read_text(encoding="utf-8")
        quoted = set(re.findall(r"freely-[A-Za-z0-9_-]+", text))
        missing = sorted(quoted - skill_names(src))
        return not missing, f"template quotes unknown skills: {missing}"

    def c15():
        ta = (src / "bin/test-all").read_text(encoding="utf-8")
        wired = array_has(ta, "\nCORE=(", AT_NAME) and array_has(ta, "\nCI_CORE=(", AT_NAME)
        return wired, "AT not wired into both CORE and CI_CORE"

    def c16():
        svg = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-projection-consistency"' in svg, "story not registered in epics-map"

    check("dead hook copies removed", c01)
    check(".githooks holds wrappers only", c02)
    check("all eight wrappers present", c03)
    check("every wrapper delegates to its truth script", c04)
    check("projection.lock exists", c05)
    check("lock header is complete", c06)
    check("lock covers hooks/skills/bin/agents", c07)
    check("every entry records kind/source/target/sha256", c08)
    check("every recorded path exists", c09)
    check("every recorded hash matches its source", c10)
    check("verifier exists and is executable", c11)
    check("runtime exposes `freely projections`", c12)
    check("no ghost skill names in generator or template", c13)
    check("template quotes only real skill names", c14)
    check("AT wired into CORE and CI_CORE", c15)
    check("story registered in epics-map", c16)

    # ---- behaviour ----
    def b17():
        """Consistent tree -> exit 0."""
        if not (src / VERIFIER).is_file():
            return False, f"missing {VERIFIER}"
        proc = run_verifier(src)
        return proc.returncode == 0, f"rc={proc.returncode} {(proc.stdout + proc.stderr).strip()[:200]}"

    def b18():
        """Tampering must be caught on both sides of a projection.

        For a delegate entry the lock pins the *truth* hash, so editing the truth
        is drift; breaking the wrapper's exec line is drift too. Both are checked
        because either one silently detaches the projection from its source.
        """
        if not (src / VERIFIER).is_file():
            return False, f"missing {VERIFIER}"
        entry = next((e for e in load_lock(src).get("entries", [])
                      if e.get("kind") == "hooks"), None)
        if entry is None:
            return False, "no hooks entry in the lock"
        results = []
        for side in ("source", "target"):
            with tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp) / "tree"
                sandbox_tree(src, copy)
                path = copy / entry[side]
                if side == "source":
                    # The lock pins the truth hash: any edit is drift.
                    path.write_text(path.read_text(encoding="utf-8") + "\n# tampered\n",
                                    encoding="utf-8")
                else:
                    # A wrapper may be edited freely as long as it still execs
                    # its truth script; drift means the delegation is broken.
                    path.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
                proc = run_verifier(src, copy)
                ok = proc.returncode != 0 and entry["target"] in (proc.stdout + proc.stderr)
                results.append(f"{side}:rc={proc.returncode}")
                if not ok:
                    return False, (f"{side} tamper not caught: "
                                   f"{'; '.join(results)} out={(proc.stdout + proc.stderr).strip()[:160]}")
        return True, "; ".join(results)

    def b19():
        """A missing lock is a refusal (2), never a silent pass."""
        if not (src / VERIFIER).is_file():
            return False, f"missing {VERIFIER}"
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_verifier(src, Path(tmp))
            return proc.returncode == 2, f"rc={proc.returncode}"

    def b20():
        """`freely projections verify` reaches the verifier through the projection."""
        entrypoint = src / "bin/freely"
        if not entrypoint.is_file():
            return False, "missing bin/freely"
        proc = subprocess.run(["bash", str(entrypoint), "projections", "verify",
                               "--project", str(src)],
                              capture_output=True, text=True, timeout=240)
        text = proc.stdout + proc.stderr
        return proc.returncode == 0 and ("projection" in text.lower()), \
            f"rc={proc.returncode} out={text.strip()[:200]}"

    check("verify exits 0 on a consistent tree", b17)
    check("verify refuses a tampered projection", b18)
    check("verify refuses a missing lock", b19)
    check("freely projections verify dispatches", b20)

    print(f"\nSUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 0 if not FAIL else 1


def sandbox_tree(src: Path, dst: Path) -> None:
    """Copy every path the lock references, so only the tamper shows up."""
    import shutil
    for item in load_lock(src).get("entries", []):
        for rel in (item.get("source"), item.get("target")):
            if not rel or rel.startswith("/"):
                continue
            source = src / rel
            target = dst / rel
            if not source.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                if not target.exists():
                    shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
    shutil.copy2(src / LOCK, dst / LOCK)


if __name__ == "__main__":
    raise SystemExit(main())

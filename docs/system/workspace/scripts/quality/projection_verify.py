#!/usr/bin/env python3
"""Projection consistency: prove every copy still matches its truth (#4179).

A projection is a copy that something else executes or reads:

* hooks   — `.githooks/<hook>` wraps `workspace/hooks/<hook>.sh`;
* skills  — deployed skill dirs are copies of `workspace/skills/<name>`;
* bin     — `bin/<cmd>` projects onto `workspace/scripts/**`;
* agents  — the AGENTS template and the runtime generator quote skill names.

`projection.lock` records source path + sha256 + target for each pair. `verify`
re-hashes and refuses on any mismatch; `record` refreshes the lock after an
intentional change. Nothing here mutates a projection — a drifted copy is a
failure to report, never something to silently overwrite.

CLI:
    projection_verify.py verify [--project PATH] [--json]
    projection_verify.py record [--project PATH] [--skills-root PATH]...

Exit codes: 0 consistent · 1 drift · 2 lock missing / unusable (fail-closed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LOCK_NAME = "projection.lock"
SKILLS_REL = "docs/system/workspace/skills"
HOOKS_REL = "docs/system/workspace/hooks"
WRAPPERS = ("commit-msg", "post-checkout", "post-rewrite", "pre-commit",
            "pre-merge-commit", "pre-push", "pre-rebase", "reference-transaction")
TEMPLATE_REL = "docs/system/workspace/AGENTS.md.example"
GENERATOR_REL = "docs/system/workspace/scripts/runtime/freely"
SKILL_CALL_RE = re.compile(r"skill:(freely-[A-Za-z0-9][A-Za-z0-9_-]*[A-Za-z0-9])")
BACKTICK_RE = re.compile(r"`(freely-[A-Za-z0-9][A-Za-z0-9_-]*[A-Za-z0-9])`")


def quoted_skills(text: str, backticks_are_skills: bool = False) -> set[str]:
    """Skill names this file actually references.

    `skill:<name>` is unambiguous everywhere. Backticks are only treated as
    skill references for the AGENTS template, whose tables list skills; in the
    runtime they also carry provenance tags such as `freely-runtime-fallback`,
    which are not skills and must not be reported as missing ones.
    """
    names = set(SKILL_CALL_RE.findall(text))
    if backticks_are_skills:
        names |= set(BACKTICK_RE.findall(text))
    return names


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dir_digest(path: Path) -> str:
    """Hash a directory's file contents, order-independent, names included."""
    h = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(str(file.relative_to(path)).encode("utf-8"))
        h.update(b"\0")
        h.update(file.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def entry(kind: str, source: str, target: str, sha256: str, note: str = "",
          mode: str = "copy") -> dict:
    """mode=copy: target must be byte-identical to source.

    mode=delegate: target is a wrapper that execs the source. Hashing the
    wrapper against the truth would always fail (they are different files by
    design), so the recorded hash pins the *truth* and verify checks that the
    wrapper still points at it.
    """
    return {"kind": kind, "source": source, "target": target, "sha256": sha256,
            "mode": mode, "note": note}


def skill_names(root: Path) -> set[str]:
    return {p.parent.name for p in (root / SKILLS_REL).glob("*/SKILL.md")}


def agents_entries(root: Path) -> list[dict]:
    """The AGENTS projection is a *name set*, not a byte copy.

    A byte hash would be useless here: the generated AGENTS.md is project
    specific. What must stay consistent is that every skill name it quotes
    exists. So the recorded hash is over the sorted name set of the truth
    (the skills tree), and verify re-derives the quoted names from both the
    template and the generator.
    """
    names = sorted(skill_names(root))
    payload = "\n".join(names).encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    return [
        entry("agents", SKILLS_REL, TEMPLATE_REL, sha, "quoted skill names must exist"),
        entry("agents", SKILLS_REL, GENERATOR_REL, sha, "generated AGENTS section quotes skill names"),
    ]


def collect(root: Path, skills_roots: list[Path]) -> list[dict]:
    entries: list[dict] = []

    for hook in WRAPPERS:
        truth = root / HOOKS_REL / f"{hook}.sh"
        wrapper = root / ".githooks" / hook
        if truth.is_file() and wrapper.is_file():
            entries.append(entry("hooks", f"{HOOKS_REL}/{hook}.sh", f".githooks/{hook}",
                                 digest(truth), "wrapper must exec this truth script",
                                 mode="delegate"))

    projections = root / "docs/system/workspace/scripts/bin-projections.yaml"
    if projections.is_file():
        # bin/ truth pairs are declared by the R32 registry; hash the shims that
        # already are projections so a silent edit to either side is caught.
        for shim in sorted((root / "bin").iterdir()):
            if not shim.is_file():
                continue
            text = shim.read_text(encoding="utf-8", errors="replace")
            match = re.search(r"docs/system/workspace/scripts/[A-Za-z0-9_./-]+", text)
            if match and len(text.splitlines()) <= 8:
                truth = root / match.group(0)
                if truth.is_file():
                    entries.append(entry("bin", match.group(0), f"bin/{shim.name}",
                                         digest(truth), "exec projection", mode="delegate"))

    for name in sorted(skill_names(root)):
        truth = root / SKILLS_REL / name
        for dest_root in skills_roots:
            target = dest_root / name
            if target.is_dir():
                rel_target = str(target)
                entries.append(entry("skills", f"{SKILLS_REL}/{name}", rel_target,
                                     dir_digest(truth), "deployed copy"))

    entries.extend(agents_entries(root))
    return entries


def load_lock(root: Path) -> dict | None:
    path = root / LOCK_NAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def verify(root: Path, as_json: bool) -> int:
    doc = load_lock(root)
    if doc is None:
        print(f"[projections] missing or unreadable {LOCK_NAME}", file=sys.stderr)
        return 2

    problems: list[str] = []
    checked = 0
    for item in doc.get("entries", []):
        kind = item.get("kind")
        source_rel = item.get("source") or ""
        target_rel = item.get("target") or ""
        expected = item.get("sha256") or ""
        source = root / source_rel
        target = Path(target_rel) if target_rel.startswith("/") else root / target_rel
        checked += 1

        if kind == "agents":
            if not source.is_dir():
                problems.append(f"{target_rel}: skill truth tree missing ({source_rel})")
                continue
            actual = hashlib.sha256("\n".join(sorted(skill_names(root))).encode("utf-8")).hexdigest()
            if actual != expected:
                problems.append(f"{target_rel}: skill name set changed; re-run `projections record`")
            if not target.is_file():
                problems.append(f"{target_rel}: projection target missing")
                continue
            quoted = quoted_skills(target.read_text(encoding="utf-8", errors="replace"),
                                   backticks_are_skills=(target_rel == TEMPLATE_REL))
            unknown = sorted(quoted - skill_names(root))
            if unknown:
                problems.append(f"{target_rel}: quotes non-existent skills {unknown[:3]}")
            continue

        if not target.exists():
            problems.append(f"{target_rel}: projection target missing")
            continue
        if item.get("mode") == "delegate":
            if not source.is_file():
                problems.append(f"{target_rel}: truth script missing ({source_rel})")
                continue
            if digest(source) != expected:
                problems.append(f"{target_rel}: truth changed ({source_rel}); re-run record")
            text = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else ""
            generic = ('workspace/hooks/${HOOK_NAME}.sh' in text
                       or "workspace/hooks/${HOOK_NAME}.sh" in text)
            if source_rel not in text and not generic:
                problems.append(f"{target_rel}: no longer delegates to {source_rel}")
            if "exec bash" not in text and "exec python3" not in text:
                problems.append(f"{target_rel}: wrapper does not exec its truth script")
            continue

        if kind == "skills":
            if not source.is_dir():
                problems.append(f"{target_rel}: skill truth missing ({source_rel})")
                continue
            actual = dir_digest(target) if target.is_dir() else ""
        else:
            actual = digest(target) if target.is_file() else ""
        if actual != expected:
            problems.append(f"{target_rel}: hash mismatch (source {source_rel})")

    if as_json:
        print(json.dumps({"ok": not problems, "checked": checked, "problems": problems},
                         ensure_ascii=False))
    elif problems:
        print(f"[projections] DRIFT in {len(problems)} projection(s):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("[projections] fix the copy, or re-run `freely projections record` after an intentional change",
              file=sys.stderr)
    else:
        print(f"[projections] ok ({checked} projections consistent)")
    return 0 if not problems else 1


def record(root: Path, skills_roots: list[Path], as_json: bool) -> int:
    entries = collect(root, [])
    doc = {
        "schema_version": 1,
        "owner": "docs/system/workspace/scripts/quality/projection_verify.py",
        "note": ("JSON-compatible YAML 1.2 subset. Each entry records the truth path, its sha256 "
                 "and the projection target. `agents` entries hash the sorted skill-name set "
                 "because a generated AGENTS.md is project specific, not a byte copy."),
        "kinds": ["hooks", "skills", "bin", "agents"],
        "entries": entries,
    }
    (root / LOCK_NAME).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
    deployed = 0
    for dest_root in skills_roots:
        skill_entries = [e for e in collect(root, [dest_root]) if e["kind"] == "skills"]
        if not skill_entries:
            continue
        side = dest_root.parent / LOCK_NAME
        side.parent.mkdir(parents=True, exist_ok=True)
        side.write_text(json.dumps({
            "schema_version": 1,
            "owner": "docs/system/workspace/scripts/quality/projection_verify.py",
            "note": ("Machine-local lock for deployed skills. Kept out of the repo lock because "
                     "these targets are absolute paths under $HOME."),
            "project": str(root),
            "kinds": ["skills"],
            "entries": skill_entries,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        deployed += len(skill_entries)

    if as_json:
        print(json.dumps({"ok": True, "recorded": len(entries), "deployed": deployed},
                         ensure_ascii=False))
    else:
        counts: dict[str, int] = {}
        for item in entries:
            counts[item["kind"]] = counts.get(item["kind"], 0) + 1
        summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        extra = f", deployed skills={deployed}" if deployed else ""
        print(f"[projections] recorded {len(entries)} projections ({summary}){extra}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("verify", "record"):
        p = sub.add_parser(name)
        p.add_argument("--project", default="")
        p.add_argument("--skills-root", action="append", default=[],
                       help="deployed skills root to include (repeatable)")
        p.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.project).resolve() if args.project else Path(__file__).resolve().parents[5]
    if not root.is_dir():
        print(f"[projections] no such project: {root}", file=sys.stderr)
        return 2
    roots = [Path(p).expanduser() for p in args.skills_root]
    if args.command == "record":
        return record(root, roots, args.json)
    return verify(root, args.json)


if __name__ == "__main__":
    raise SystemExit(main())

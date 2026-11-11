#!/usr/bin/env python3
"""AT-001 for raw-20261104T075959Z / #4164.

Skill corpus single-source contract: a machine-readable overlap/routing matrix,
loop|owner|supersedes frontmatter on every SKILL.md, a lint that fails closed,
no duplicated enum wording, and the AT wired into both test-all suites.

The same AT runs against a `git archive develop` snapshot to prove RED.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-skill-frontmatter-contract.py"
PHRASE = "从 gate 源码提取"

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # a missing artifact must be a RED, not a crash
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def skills_dir(src: Path) -> Path:
    return src / "docs/system/workspace/skills"


def skill_files(src: Path) -> list[Path]:
    return sorted(skills_dir(src).glob("*/SKILL.md"))


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    out: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def load_map(src: Path):
    return json.loads((skills_dir(src) / "skill-map.yaml").read_text(encoding="utf-8"))


def lint_on_fixture(src: Path, compliant: bool) -> int:
    lint = src / "bin/check-skill-frontmatter"
    if not lint.is_file():
        raise FileNotFoundError(f"missing lint: {lint}")
    with tempfile.TemporaryDirectory(prefix="skill-fm-") as td:
        d = Path(td) / "skills"
        (d / "foo").mkdir(parents=True)
        extra = "loop: governance\nowner: workflow\nsupersedes: []\n" if compliant else ""
        (d / "foo" / "SKILL.md").write_text(
            f"---\nname: foo\ndescription: >-\n  fixture\n{extra}---\n\n# foo\n", encoding="utf-8"
        )
        fixture_map = {
            "schema_version": 1,
            "enums": {"loops": ["governance"], "owners": ["workflow"]},
            "skills": {
                "foo": {
                    "loop": "governance",
                    "owner": "workflow",
                    "inputs": [],
                    "outputs": [],
                    "triggers": [],
                }
            },
            "overlap_groups": [],
            "routing": {"governance": "foo"},
        }
        (d / "skill-map.yaml").write_text(json.dumps(fixture_map), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(lint), "--skills-dir", str(d), "--map", str(d / "skill-map.yaml")],
            capture_output=True, text=True,
        )
        return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(ROOT))
    args = ap.parse_args()
    src = Path(args.source_dir).resolve()
    files = skill_files(src)
    names = [p.parent.name for p in files]

    print("=== STATIC: matrix / frontmatter single source ===")

    def c1():
        p = skills_dir(src) / "skill-map.yaml"
        return p.is_file(), f"missing {p}"

    check("skill-map.yaml exists as the single source", c1)

    def c2():
        p = src / "bin/check-skill-frontmatter"
        return p.is_file(), f"missing {p}"

    check("frontmatter lint exists", c2)

    def c3():
        load_map(src)
        return True, ""

    check("skill-map.yaml is stdlib-parseable JSON/YAML subset", c3)

    def c4():
        m = load_map(src)
        got = set(m.get("skills", {}))
        missing = sorted(set(names) - got)
        return not missing, f"map misses {len(missing)} skills: {missing[:4]}"

    check("matrix covers every SKILL.md", c4)

    def c5():
        m = load_map(src)
        bad = [k for k, v in m.get("skills", {}).items()
               if not all(f in v for f in ("loop", "owner", "inputs", "outputs", "triggers"))]
        return not bad, f"incomplete entries: {bad[:4]}"

    check("matrix entries carry loop/owner/inputs/outputs/triggers", c5)

    def c6():
        m = load_map(src)
        groups = m.get("overlap_groups", [])
        ids = {g.get("id") for g in groups}
        want = {"human-interruption", "worktree-governance", "execution-flow"}
        return len(groups) == 3 and ids == want, f"groups={sorted(ids)}"

    check("three overlap groups are recorded with a decision", c6)

    def c7():
        m = load_map(src)
        skills = m.get("skills", {})
        bad = [g.get("id") for g in m.get("overlap_groups", [])
               if g.get("decision") not in ("keep_separate", "merge")
               or g.get("entrypoint") not in skills
               or not g.get("reason")]
        return not bad, f"invalid groups: {bad}"

    check("each overlap group has a legal decision, entrypoint and reason", c7)

    def c8():
        m = load_map(src)
        skills = m.get("skills", {})
        routing = m.get("routing", {})
        loops = set(m.get("enums", {}).get("loops", []))
        bad = [lp for lp in loops if not isinstance(routing.get(lp), str) or routing[lp] not in skills]
        return bool(loops) and not bad, f"routing holes: {bad}"

    check("routing gives exactly one entrypoint per loop", c8)

    def c9():
        bad = [p.parent.name for p in files if "loop" not in frontmatter(p)]
        return not bad, f"{len(bad)} skills lack loop: {bad[:4]}"

    check("every SKILL.md frontmatter declares loop", c9)

    def c10():
        bad = [p.parent.name for p in files if "owner" not in frontmatter(p)]
        return not bad, f"{len(bad)} skills lack owner: {bad[:4]}"

    check("every SKILL.md frontmatter declares owner", c10)

    def c11():
        bad = [p.parent.name for p in files if "supersedes" not in frontmatter(p)]
        return not bad, f"{len(bad)} skills lack supersedes: {bad[:4]}"

    check("every SKILL.md frontmatter declares supersedes", c11)

    def c12():
        m = load_map(src)
        bad = [p.parent.name for p in files
               if frontmatter(p).get("loop") != m.get("skills", {}).get(p.parent.name, {}).get("loop")]
        return not bad, f"loop drift: {bad[:4]}"

    check("frontmatter loop matches the matrix", c12)

    def c13():
        m = load_map(src)
        bad = [p.parent.name for p in files
               if frontmatter(p).get("owner") != m.get("skills", {}).get(p.parent.name, {}).get("owner")]
        return not bad, f"owner drift: {bad[:4]}"

    check("frontmatter owner matches the matrix", c13)

    def c14():
        m = load_map(src)
        loops = set(m.get("enums", {}).get("loops", []))
        bad = [p.parent.name for p in files if frontmatter(p).get("loop") not in loops]
        return not bad, f"unknown loop values: {bad[:4]}"

    check("loop values come from the matrix enum", c14)

    def c15():
        m = load_map(src)
        owners = set(m.get("enums", {}).get("owners", []))
        bad = [p.parent.name for p in files if frontmatter(p).get("owner") not in owners]
        return not bad, f"unknown owner values: {bad[:4]}"

    check("owner values come from the matrix enum", c15)

    def c16():
        m = load_map(src)
        orphan = sorted(set(m.get("skills", {})) - set(names))
        return not orphan, f"matrix orphans: {orphan[:4]}"

    check("matrix has no orphan entries", c16)

    def c17():
        # Scope = capability tree (docs/system/workspace), not the development
        # governance tree: B1/raw issue.md quotes the very phrase in its own
        # acceptance criteria, so a literal `grep -r docs/` is self-contradictory.
        scope = src / "docs/system/workspace"
        docs = src / "docs"
        hits = [str(p.relative_to(docs)) for p in scope.rglob("*.md")
                if PHRASE in p.read_text(encoding="utf-8", errors="replace")]
        return not hits, f"duplicated enum wording in {hits[:3]}"

    check("no duplicated gate-enum wording remains in capability docs", c17)

    def c18():
        text = (src / "bin/test-all").read_text(encoding="utf-8")
        core = re.search(r"CORE=\((.*?)\)", text, re.S)
        ci = re.search(r"CI_CORE=\((.*?)\)", text, re.S)
        ok = bool(core and AT_NAME in core.group(1) and ci and AT_NAME in ci.group(1))
        return ok, "AT missing from CORE or CI_CORE"

    check("AT is wired into test-all CORE and CI_CORE", c18)

    def c19():
        text = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-skill-overlap-matrix"' in text, "story not registered in epics-map"

    check("B2 story registered in epics-map.svg", c19)

    print("=== BEHAVIOR: lint fails closed on a missing contract ===")

    def c20():
        rc = lint_on_fixture(src, compliant=False)
        return rc != 0, f"lint returned {rc} for a SKILL.md without loop/owner"

    check("lint refuses a skill without loop/owner", c20)

    def c21():
        rc = lint_on_fixture(src, compliant=True)
        return rc == 0, f"lint returned {rc} for a compliant fixture"

    check("lint accepts a compliant fixture", c21)

    print(f"SUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())

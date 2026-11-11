#!/usr/bin/env python3
"""AT-001 for raw-20261111T083905Z / #4291 (R28.5).

Skill merge with an index compatibility period: retired skills keep a machine
readable alias to a surviving entrypoint, their knowledge is merged as chapters
(not dropped), supersedes is backfilled, executable truth has no dangling
references, and the route resolver / lint / CI all guard the result.

Runs against `git archive develop` to prove RED.
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
AT_NAME = "test-skill-merge-compat.py"

ALIASES = {
    "freely-signal-intent-understanding": "freely-human-interruption-manager-triage",
    "freely-chat-issue-routing": "freely-human-interruption-manager-triage",
    "freely-mem9-continuity-bridge": "freely-continuity-watchdog",
    "freely-tool-cc-codex-mcp-runtime": "freely-ai-cli-availability-manager",
}
RETIRED = set(ALIASES)
TARGETS = set(ALIASES.values())
BASELINE_SKILLS = 37
MERGED_CHAPTER = "## 合并自"

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def skills_dir(src: Path) -> Path:
    return src / "docs/system/workspace/skills"


def load_map(src: Path):
    return json.loads((skills_dir(src) / "skill-map.yaml").read_text(encoding="utf-8"))


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


def run_tool(src: Path, *args: str):
    return subprocess.run([sys.executable, str(src / "bin/skill-route"), *args],
                          capture_output=True, text=True)


def lint_fixture(src: Path, dangling: bool) -> int:
    lint = src / "bin/check-skill-frontmatter"
    if not lint.is_file():
        raise FileNotFoundError(f"missing lint: {lint}")
    with tempfile.TemporaryDirectory(prefix="skill-alias-") as td:
        d = Path(td) / "skills"
        (d / "kept").mkdir(parents=True)
        (d / "kept" / "SKILL.md").write_text(
            "---\nname: kept\nloop: governance\nowner: workflow\n"
            "supersedes: [freely-retired]\n---\n\n# kept\n", encoding="utf-8")
        target = "freely-does-not-exist" if dangling else "kept"
        matrix = {
            "schema_version": 1,
            "enums": {"loops": ["governance"], "owners": ["workflow"]},
            "skills": {"kept": {"loop": "governance", "owner": "workflow",
                                "inputs": [], "outputs": [], "triggers": []}},
            "aliases": {"freely-retired": target},
            "overlap_groups": [],
            "routing": {"governance": "kept"},
        }
        (d / "skill-map.yaml").write_text(json.dumps(matrix), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(lint), "--skills-dir", str(d), "--map", str(d / "skill-map.yaml")],
            capture_output=True, text=True).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(ROOT))
    src = Path(ap.parse_args().source_dir).resolve()
    sd = skills_dir(src)
    live = sorted(p.parent.name for p in sd.glob("*/SKILL.md"))

    print("=== STATIC: merge + alias compatibility ===")

    def c1():
        return "aliases" in load_map(src), "skill-map.yaml has no aliases section"

    check("matrix declares an alias compatibility section", c1)

    def c2():
        got = load_map(src).get("aliases", {})
        return got == ALIASES, f"aliases={got}"

    check("four retired skills map to three surviving entrypoints", c2)

    def c3():
        skills = load_map(src).get("skills", {})
        bad = sorted(RETIRED & set(skills))
        return not bad, f"retired names still in matrix skills: {bad}"

    check("retired names removed from matrix skills", c3)

    def c4():
        m = load_map(src)
        aliases = m.get("aliases", {})
        skills = m.get("skills", {})
        if not aliases:
            return False, "no aliases declared"
        bad = [f"{k}->{v}" for k, v in aliases.items() if v not in skills]
        return not bad, f"dangling alias targets: {bad}"

    check("every alias target exists in matrix skills", c4)

    def c5():
        left = [n for n in RETIRED if (sd / n).exists()]
        return not left, f"retired directories still present: {sorted(left)}"

    check("retired skill directories are gone", c5)

    def c6():
        return len(live) < BASELINE_SKILLS and len(live) <= 35, f"skill count={len(live)}"

    check(f"skill count dropped from {BASELINE_SKILLS} (now {len(live)})", c6)

    def c7():
        return (src / "bin/skill-route").is_file(), "missing bin/skill-route"

    check("route resolver exists", c7)

    print("=== BEHAVIOR: alias resolution, supersedes, lint ===")

    def c8():
        bad = []
        for alias, target in ALIASES.items():
            proc = run_tool(src, alias)
            if proc.returncode != 0 or target not in proc.stdout:
                bad.append(f"{alias}: rc={proc.returncode} out={proc.stdout.strip()[:60]}")
        return not bad, f"alias resolution failures: {bad[:2]}"

    check("every alias resolves to its surviving entrypoint", c8)

    def c9():
        proc = run_tool(src, "--loop", "intake")
        want = load_map(src).get("routing", {}).get("intake")
        return proc.returncode == 0 and want in proc.stdout, f"rc={proc.returncode} out={proc.stdout.strip()[:80]}"

    check("route resolver answers a loop query", c9)

    def c10():
        bad = []
        for target in TARGETS:
            fm = frontmatter(sd / target / "SKILL.md")
            expected = {k for k, v in ALIASES.items() if v == target}
            got = set(re.findall(r"freely-[a-z0-9-]+", fm.get("supersedes", "")))
            if not expected <= got:
                bad.append(f"{target}: supersedes={sorted(got)} want>={sorted(expected)}")
        return not bad, f"supersedes not backfilled: {bad[:2]}"

    check("surviving entrypoints declare supersedes", c10)

    def c11():
        bad = []
        for target in TARGETS:
            text = (sd / target / "SKILL.md").read_text(encoding="utf-8")
            if MERGED_CHAPTER not in text:
                bad.append(f"{target}: no merged chapter")
                continue
            for alias, tgt in ALIASES.items():
                if tgt == target and alias not in text:
                    bad.append(f"{target}: missing merged content from {alias}")
        return not bad, f"knowledge lost: {bad[:2]}"

    check("retired knowledge merged as chapters, not dropped", c11)

    def c12():
        text = (sd / "README.md").read_text(encoding="utf-8")
        listed = [n for n in RETIRED if re.search(rf"^\s*[-*|].*`{re.escape(n)}`", text, re.M)]
        return not listed and "别名" in text, f"README still lists {listed} or has no alias note"

    check("skill index no longer lists retired skills", c12)

    def c13():
        rc = lint_fixture(src, dangling=True)
        return rc != 0, f"lint returned {rc} for a dangling alias"

    check("lint refuses a dangling alias", c13)

    def c14():
        rc = lint_fixture(src, dangling=False)
        return rc == 0, f"lint returned {rc} for a valid alias"

    check("lint accepts a valid alias", c14)

    def c15():
        # Executable truth only; B1/B2 history and the matrix itself are allowed.
        scopes = [src / "AGENTS.md", src / "bin", src / ".githooks",
                  src / "docs/system/workspace/agents", src / "docs/system/workspace/hooks"]
        files: list[Path] = []
        for s in scopes:
            files += [s] if s.is_file() else [p for p in s.rglob("*") if p.is_file()]
        hits = []
        for p in files:
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for name in RETIRED:
                if name in text:
                    hits.append(f"{p.relative_to(src)}:{name}")
        return not hits, f"dangling executable references: {hits[:3]}"

    check("no dangling references in executable truth", c15)

    def c16():
        text = (src / "bin/test-all").read_text(encoding="utf-8")
        core = re.search(r"CORE=\((.*?)\)", text, re.S)
        ci = re.search(r"CI_CORE=\((.*?)\)", text, re.S)
        return bool(core and ci and AT_NAME in core.group(1) and AT_NAME in ci.group(1)), "AT not in both suites"

    check("AT wired into test-all CORE and CI_CORE", c16)

    def c17():
        text = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-skill-merge-compat"' in text, "story not registered"

    check("B2 story registered in epics-map.svg", c17)

    print(f"SUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())

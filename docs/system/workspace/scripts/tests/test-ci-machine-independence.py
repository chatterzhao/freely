#!/usr/bin/env python3
"""AT-001 — raw-20261112T015715Z / #4307.

Verifies that `test-contract-single-source.py` proves deploy-skills READS the
tool registry instead of depending on whether this machine happens to have
`cline` installed. Before the fix, a machine without cline makes
`bin/test-all --ci` permanently red, which blocks `freely test-gate run` and
therefore every issue closeout.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>

Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("CI_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

CONTRACT = SRC / "docs/system/workspace/scripts/tests/test-contract-single-source.py"
TEST_ALL = SRC / "bin/test-all"
DEPLOY = SRC / "bin/deploy-skills"
SVG = SRC / "docs/epics-map.svg"
STORY = SRC / "docs/B2-docs/gate/ci-machine-independence"

# develop e003532b5 — the product script must stay byte-identical.
BASELINE_DEPLOY_SHA256 = "1c8a6dd09bb3c06f85c75edaf11c006223515c928c10fc034dc1c4b9ef9f8e7e"

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


def clean_env() -> dict[str, str]:
    """PATH with every directory that provides a `cline` binary removed.

    No external shim is added: the test under inspection must supply its own
    premise from inside its process.
    """
    env = dict(os.environ)
    kept = []
    for entry in env.get("PATH", "").split(os.pathsep):
        if entry and not (Path(entry) / "cline").is_file():
            kept.append(entry)
    env["PATH"] = os.pathsep.join(kept)
    return env


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True,
                          text=True, timeout=300)


def static_checks() -> None:
    print("=== STATIC: environment premise is self-contained ===")
    t = read(CONTRACT)

    expect("tool-probe-bin" in t and ("TemporaryDirectory" in t or "mkdtemp" in t),
           "S1 test builds its own private stub directory")

    env_kwargs = re.findall(r"env\s*=\s*[A-Za-z_]\w*", t)
    expect(len(env_kwargs) >= 3 and "dict(os.environ)" in t,
           "S2 three subprocess.run calls share a copied env")

    expect(re.search(r'["\']cline["\']', t) is not None and "0o755" in t,
           "S3 stub is named cline and made executable")
    expect(not any(p in t for p in ("/opt/homebrew", "/Users/", ".local/bin")),
           "S4 no hard-coded machine paths")
    expect(re.search(r"os\.environ\s*\[[^\]]+\]\s*=", t) is None,
           "S5 global os.environ is never assigned")

    expect("registry missing: deploy-skills fails closed" in t
           and "explicit --tools still works" in t,
           "S6 fail-closed and explicit-tools assertions preserved")

    digest = hashlib.sha256(DEPLOY.read_bytes()).hexdigest() if DEPLOY.is_file() else ""
    expect(digest == BASELINE_DEPLOY_SHA256,
           "S7 bin/deploy-skills unchanged from develop e003532b5")

    ta = read(TEST_ALL)
    expect("test-contract-single-source.py" in ta,
           "S8 CI_CORE keeps the contract test")
    expect(ta.count("test-ci-machine-independence.py") >= 2,
           "S9 AT wired into both CORE and CI_CORE")
    expect(STORY.is_dir() and 'id="story-ci-machine-independence"' in read(SVG),
           "S10 epic gate / story ci-machine-independence registered")


def _sandbox(tmp: Path) -> Path:
    sb = tmp / "negative-control"
    rels = (
        "bin/deploy-skills",
        "docs/system/workspace/tools/tool-registry.toml",
        "docs/system/workspace/scripts/runtime/freely",
        "docs/system/workspace/scripts/runtime/paths.sh",
        "docs/system/workspace/scripts/runtime/raw_key_canon.py",
        "docs/system/workspace/scripts/runtime/tool-registry-query.py",
        "docs/system/workspace/scripts/worktree/wt-create",
    )
    for rel in rels:
        src = SRC / rel
        if src.is_file():
            dst = sb / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return sb


def behavior_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: clean PATH, no external shim ===")
    env = clean_env()
    if shutil.which("cline", path=env["PATH"]) is not None:
        print("PRECONDITION FAILURE: a real cline binary is still reachable; "
              "this run cannot prove machine independence", file=sys.stderr)
        for label in ("B1", "B2", "B3"):
            bad(f"{label} precondition: cline still on PATH")
        return

    r1 = run([sys.executable, str(CONTRACT), "--source-dir", str(SRC)], SRC, env)
    out1 = r1.stdout + r1.stderr
    expect(r1.returncode == 0 and "SUMMARY: 13 ok, 0 failed" in out1,
           "B1 clean PATH: contract test 13 ok / 0 failed")

    if os.environ.get("FREELY_AT_NESTED") == "1":
        ok("B2 nested inside test-all: recursion guard (verified at top level)")
    else:
        nested = dict(env)
        nested["FREELY_AT_NESTED"] = "1"
        r2 = run(["bash", str(TEST_ALL), "--ci"], SRC, nested)
        out2 = r2.stdout + r2.stderr
        # Assert the STABLE property ("the whole verified subset is green"),
        # not the exact member count: hard-coding "22 ok" made this AT red the
        # moment any test was onboarded to CI_CORE, which is a maintenance trap
        # rather than a regression signal. The subset can only grow (§S8 pins
        # that no existing member was removed).
        m = re.search(r"SUMMARY: (\d+) ok, (\d+) failed", out2)
        green = bool(m) and int(m.group(2)) == 0 and int(m.group(1)) >= 22
        expect(r2.returncode == 0 and green,
               f"B2 clean PATH: test-all --ci all green, >=22 ok "
               f"({m.group(0) if m else 'no SUMMARY line'})")

    # Negative control: changing the registry's cline probe word must make the
    # "cline detected" assertion fail even though the stub exists. This is what
    # separates "fix the test" from "make the assertion always true".
    sb = _sandbox(tmp)
    normal = run([sys.executable, str(CONTRACT), "--source-dir", str(sb)], sb, env)
    out_normal = normal.stdout + normal.stderr
    reg = sb / "docs/system/workspace/tools/tool-registry.toml"
    text = read(reg)
    mutated = re.sub(r"(test_command\s*=\s*[\"'])cline\b",
                     r"\1definitely-not-a-real-binary-xyz", text)
    if reg.is_file():
        reg.write_text(mutated, encoding="utf-8")
    broken = run([sys.executable, str(CONTRACT), "--source-dir", str(sb)], sb, env)
    out_broken = broken.stdout + broken.stderr
    expect(normal.returncode == 0 and "SUMMARY: 13 ok, 0 failed" in out_normal
           and broken.returncode != 0 and "[FAIL] registry present" in out_broken,
           "B3 negative control: registry mutation still fails the assertion")


def main() -> None:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="ci-machine-") as td:
        static_checks()
        behavior_checks(Path(td))
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    sys.exit(0 if BAD == 0 else 1)


if __name__ == "__main__":
    main()

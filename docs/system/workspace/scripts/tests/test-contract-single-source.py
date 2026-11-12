#!/usr/bin/env python3
"""AT-001 — raw-20261103T132614Z / #4154.

Scope of this round: the two faces of #4154 that are both "same value, many
copies" and have an executable RED acceptance in the issue:

1. tool-registry.toml path. `runtime/freely:67` and `tool-launchers.sh:56` are
   right, but `bin/deploy-skills:72` and `runtime/freely::_init_acp_tool_setup`
   point at a non-existent `scripts/runtime/tool-registry.toml`. Both degrade
   silently: deploy-skills falls back to `tools="claude"`, ACP setup logs one
   warning and returns 0.

2. raw-key format. `worktree/wt-create:279-284` accepts legacy
   `YYYYMMDD-HHMM` but only warns, while `runtime/raw_key_canon.py` only
   understands `YYYYMMDDTHHMMSSZ`. A legacy key is then embedded into branch
   names as `raw-20261103-1326` and every downstream `T...Z` extractor returns
   an empty raw_key.

The other faces of #4154 (TS↔Rust bridge contract, platform write paths,
error model, $SELF_ROOT vs $project roots) are owned by existing open issues
#4179 / #4166 / #4161 and are explicitly out of scope here.

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
SRC = Path(os.environ.get("CONTRACT_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

RUNTIME = SRC / "docs/system/workspace/scripts/runtime"

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


# ── STATIC: one owner for the registry path, one normalizer for raw keys ──

def static_checks() -> None:
    print("=== STATIC: single source wiring ===")
    deploy = read(SRC / "bin/deploy-skills")
    freely = read(RUNTIME / "freely")
    wt_create = read(SRC / "docs/system/workspace/scripts/worktree/wt-create")
    canon = read(RUNTIME / "raw_key_canon.py")
    paths = read(RUNTIME / "paths.sh")

    expect("freely_tool_registry_path" in deploy and 'tools="claude"' not in deploy,
           "deploy-skills uses the shared registry path and has no claude fallback")

    acp = freely[freely.find("_init_acp_tool_setup()"):freely.find("_init_acp_tool_setup()") + 1600]
    expect("$TOOL_REGISTRY" in acp and "scripts/runtime/tool-registry.toml" not in acp,
           "ACP tool setup reuses $TOOL_REGISTRY instead of a wrong local path")

    expect("freely_tool_registry_path()" in paths,
           "runtime/paths.sh owns the registry path constant")

    offenders = []
    for rel, text in (
        ("bin/deploy-skills", deploy),
        ("runtime/freely", freely),
        ("worktree/wt-create", wt_create),
    ):
        if "scripts/runtime/tool-registry.toml" in text:
            offenders.append(rel)
    expect(not offenders, f"no production reference to the wrong registry path ({offenders})")

    expect("raw_key_canon.py" in wt_create,
           "wt-create normalizes raw keys through the single owner")
    expect("_LEGACY" in canon and '__main__' in canon,
           "raw_key_canon.py understands legacy keys and is callable")


# ── BEHAVIOR: missing registry must fail closed, not fall back ────────────

def _build_deploy_tree(tmp: Path) -> Path:
    tree = tmp / "deploy-tree"
    (tree / "bin").mkdir(parents=True)
    (tree / "docs/system/workspace/skills").mkdir(parents=True)
    tools = tree / "docs/system/workspace/tools"
    tools.mkdir(parents=True)
    runtime = tree / "docs/system/workspace/scripts/runtime"
    runtime.mkdir(parents=True)

    shutil.copy2(SRC / "bin/deploy-skills", tree / "bin/deploy-skills")
    for rel in (
        "docs/system/workspace/scripts/runtime/paths.sh",
        "docs/system/workspace/scripts/runtime/tool-registry-query.py",
    ):
        src = SRC / rel
        if src.is_file():
            shutil.copy2(src, tree / rel)
    reg = SRC / "docs/system/workspace/tools/tool-registry.toml"
    if reg.is_file():
        shutil.copy2(reg, tools / "tool-registry.toml")
    return tree


def registry_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: registry present/missing ===")

    # #4307: the assertion below proves deploy-skills READS the registry, not
    # that this machine happens to have cline installed. Supply the probe
    # binary from a test-private temp dir and inject it per subprocess, so the
    # result is machine-independent and the global environment stays intact.
    stub = tmp / "tool-probe-bin"
    stub.mkdir(parents=True, exist_ok=True)
    probe = stub / "cline"
    probe.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    probe.chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = f"{stub}{os.pathsep}{env.get('PATH', '')}"

    tree = _build_deploy_tree(tmp)
    script = tree / "bin/deploy-skills"
    reg = tree / "docs/system/workspace/tools/tool-registry.toml"

    if not script.is_file():
        bad("registry present: registry tools are read (cline detected)")
        bad("registry missing: deploy-skills fails closed")
        bad("explicit --tools still works")
        return

    present = subprocess.run(["bash", str(script), "--dry-run"], capture_output=True,
                             text=True, timeout=60, env=env)
    combined_present = (present.stdout + present.stderr).lower()
    # `cline` appears only because deploy-skills read it from the registry;
    # the old fallback path never looked at the file and printed only claude.
    expect("cline" in combined_present,
           "registry present: registry tools are read (cline detected)")

    if reg.is_file():
        reg.rename(reg.with_suffix(".toml.away"))
    try:
        missing = subprocess.run(["bash", str(script), "--dry-run"], capture_output=True,
                                 text=True, timeout=60, env=env)
    finally:
        if reg.with_suffix(".toml.away").is_file():
            reg.with_suffix(".toml.away").rename(reg)

    combined = (missing.stdout + missing.stderr).lower()
    expect(missing.returncode != 0 and "tool-registry" in combined,
           "registry missing: deploy-skills fails closed")

    explicit = subprocess.run(["bash", str(script), "--dry-run", "--tools", "claude"],
                              capture_output=True, text=True, timeout=60, env=env)
    expect(explicit.returncode == 0, "explicit --tools still works")


# ── BEHAVIOR: legacy raw keys are normalized at the single owner ─────────

def raw_key_checks() -> None:
    print("=== BEHAVIOR: legacy raw-key normalization ===")
    canon = RUNTIME / "raw_key_canon.py"
    cases = [
        ("20261103-1326", "raw-20261103T132600Z", "legacy YYYYMMDD-HHMM pads seconds"),
        ("20261103-132645", "raw-20261103T132645Z", "legacy YYYYMMDD-HHMMSS keeps seconds"),
        ("20261103T132614Z", "raw-20261103T132614Z", "canonical key is unchanged"),
        ("fix/raw-20261103-1326-slug", "raw-20261103T132600Z", "branch name yields canonical key"),
    ]
    if not canon.is_file():
        for _in, _out, label in cases:
            bad(label)
        return
    for value, expected, label in cases:
        proc = subprocess.run([sys.executable, str(canon), value],
                              capture_output=True, text=True, timeout=30)
        expect(proc.stdout.strip() == expected, label)


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-contract-single-") as d:
        tmp = Path(d)
        static_checks()
        registry_checks(tmp)
        raw_key_checks()
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""AT-001 for raw-20261105T121046Z — installed state must be provable and in sync.

All behaviour runs against a temporary FREELY_HOME and a temporary git project
tree; nothing here reads or writes the real ~/.freely or ~/.local/bin.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

OK = 0
BAD = 0
SOURCE = Path(__file__).resolve().parents[2]  # docs/system/workspace


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


def load_module(source: Path, name: str):
    p = source / "scripts/quality/install_state.py"
    spec = importlib.util.spec_from_file_location(name, str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_project(root: Path, lines: int = 3) -> str:
    (root / "bin").mkdir(parents=True)
    (root / "docs/system/workspace/scripts/runtime").mkdir(parents=True)
    (root / "docs/system/workspace/scripts/worktree").mkdir(parents=True)
    (root / "docs/system/workspace").mkdir(parents=True, exist_ok=True)
    for rel in (
        "bin/freely",
        "bin/issue-sync",
        "bin/freely-package",
        "docs/system/workspace/scripts/runtime/freely",
        "docs/system/workspace/scripts/worktree/pr-merge-guarded",
        "docs/system/workspace/package-allowlist.txt",
    ):
        (root / rel).write_text("content-" + rel + "-" + str(lines) + "\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "init"], check=True)
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"], text=True
    ).strip()


def make_version(home: Path, name: str, root: Path, mod, head: str | None = None):
    v = home / "versions" / name
    (v / "bin").mkdir(parents=True)
    (v / "bin/freely").write_text("#!/bin/sh\necho installed\n")
    head = head or subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"], text=True
    ).strip()
    (v / ".freely_version").write_text(
        f"FREELY_VERSION={name}\nFREELY_PACKAGED_FROM={head}\n"
    )
    mod.write_manifest(v, root)
    return v


def static_checks(source: Path):
    print("=== STATIC: install-state wiring ===")
    q = source / "scripts/quality"
    # Guard assertions: these capabilities already exist on develop, so a RED
    # that fails them would mean the harness itself is broken, not the feature.
    project = source.parents[2]
    expect((project / "bin/freely-package").is_file(), "freely-package exists (pre-existing)")
    runtime_text = (source / "scripts/runtime/freely").read_text()
    expect("cmd_doctor()" in runtime_text, "cmd_doctor exists (pre-existing)")
    expect((q / "install_state.py").is_file(), "install_state library exists")
    cli = q / "install-state-check.py"
    expect(cli.is_file(), "install-state-check CLI exists")
    cli_text = cli.read_text() if cli.is_file() else ""
    expect("import install_state" in cli_text or "install_state" in cli_text,
           "CLI delegates to the shared library")

    # source = <project>/docs/system/workspace; parents[2] is the project root.
    project = source.parents[2]
    pkg_text = (project / "bin/freely-package").read_text() if (project / "bin/freely-package").is_file() else ""
    expect("--activate" in pkg_text, "freely-package exposes --activate")
    expect("auto" in pkg_text, "freely-package accepts an auto version")
    expect("write_manifest" in pkg_text or "write-hashes" in pkg_text
           or "--write-manifest" in pkg_text,
           "freely-package writes the hash manifest")
    merge_text = (source / "scripts/worktree/pr-merge-guarded").read_text()
    expect("install-state" in merge_text or "freely-package" in merge_text,
           "merge followthrough triggers a repackage")
    runtime = (source / "scripts/runtime/freely").read_text()
    expect("install-state-check" in runtime, "cmd_doctor reports install state")


def behavior_checks(source: Path):
    print("=== BEHAVIOR: isolated install state ===")
    if not (source / "scripts/quality/install_state.py").is_file():
        for label in (
            "behind latest is reported", "dangling latest is reported",
            "dangling bin link is reported", "hash drift is reported",
            "write_manifest produces .freely_hashes", "activate swaps latest atomically",
            "activate reports success", "check passes on a synced install",
            "activate is idempotent for the same HEAD", "latest never dangles after activate",
            "activate keeps a healthy bin link", "CLI exit code follows check result",
            "CLI JSON carries the diagnosis",
        ):
            bad(f"{label} (library missing)")
        return

    mod = load_module(source, "install_state_probe")
    tmp = Path(tempfile.mkdtemp(prefix="install-state-"))
    try:
        root = tmp / "project"
        home = tmp / "home"
        binlink = tmp / "bin" / "freely"
        binlink.parent.mkdir(parents=True)
        (home / "versions").mkdir(parents=True)
        head = make_project(root)

        # 1) behind
        v_old = make_version(home, "old-nightly", root, mod, head="deadbeef")
        os.symlink("old-nightly", home / "versions/latest")
        result = mod.check_state(home, root, binlink)
        expect(not result["ok"] and any("behind" in e for e in result["errors"]),
               "behind latest is reported (rc != 0)")

        # 2) dangling latest
        (home / "versions/latest").unlink()
        os.symlink("does-not-exist", home / "versions/latest")
        result = mod.check_state(home, root, binlink)
        expect(not result["ok"] and any("dangling" in e for e in result["errors"]),
               "dangling latest is reported")

        # 3) dangling bin link
        (home / "versions/latest").unlink()
        os.symlink("old-nightly", home / "versions/latest")
        os.symlink("/no/such/installed/freely", binlink)
        result = mod.check_state(home, root, binlink)
        expect(not result["ok"] and any("dangling" in e for e in result["errors"]),
               "dangling bin link is reported")

        # 4) hash drift
        binlink.unlink()
        (root / "bin/freely").write_text("changed after packaging\n")
        result = mod.check_state(home, root, binlink)
        expect(not result["ok"] and any("hash" in e.lower() for e in result["errors"]),
               "hash drift is reported")

        # 5) manifest
        expect(mod.write_manifest(v_old, root) and (v_old / ".freely_hashes").is_file(),
               "write_manifest produces .freely_hashes")

        # 6) activate atomic swap
        v_new = make_version(home, "new-nightly", root, mod, head=head)
        before = [p.name for p in (home / "versions").iterdir()]
        activation = mod.activate(home, v_new, binlink)
        latest = home / "versions/latest"
        expect(latest.is_symlink() and latest.resolve() == v_new.resolve(),
               "activate swaps latest atomically")
        expect(activation.get("ok") is True, "activate reports success")

        # 7) synced check
        result = mod.check_state(home, root, binlink)
        expect(result["ok"], f"check passes on a synced install ({result['errors']})")

        # 8) idempotence: no new version dir for the same HEAD
        again = mod.activate(home, v_new, binlink)
        after = [p.name for p in (home / "versions").iterdir()]
        expect(again.get("idempotent") is True or sorted(before + ["new-nightly"]) == sorted(after),
               "activate is idempotent for the same HEAD")
        expect(latest.is_symlink() and latest.exists(), "latest never dangles after activate")

        # 9) healthy link is preserved
        healthy = tmp / "bin/healthy"
        os.symlink(str(root / "bin/freely"), healthy)
        mod.activate(home, v_new, healthy)
        expect(healthy.is_symlink() and os.readlink(healthy) == str(root / "bin/freely"),
               "activate keeps a healthy bin link")

        # 10) CLI contract
        cli = source / "scripts/quality/install-state-check.py"
        good = subprocess.run(
            [sys.executable, str(cli), "--project", str(root), "--home", str(home),
             "--bin", str(binlink), "--json"], capture_output=True, text=True,
        )
        v_bad = make_version(home, "behind-nightly", root, mod, head="0000000")
        os.symlink("behind-nightly", home / "versions/latest.tmp")
        os.replace(home / "versions/latest.tmp", home / "versions/latest")
        broken = subprocess.run(
            [sys.executable, str(cli), "--project", str(root), "--home", str(home),
             "--bin", str(binlink), "--json"], capture_output=True, text=True,
        )
        expect(good.returncode == 0 and broken.returncode != 0,
               f"CLI exit code follows check result (good={good.returncode}, bad={broken.returncode})")
        try:
            payload = json.loads(broken.stdout)
            expect(payload.get("ok") is False, "CLI JSON carries the diagnosis")
        except json.JSONDecodeError:
            bad("CLI JSON carries the diagnosis (not parseable)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("mode", nargs="?", default="all")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else SOURCE.parents[1]
    if args.source_dir:
        # source-dir is a project root; our helpers take the workspace root
        source = src / "docs/system/workspace"
    else:
        source = SOURCE
    if args.mode in ("static", "all"):
        static_checks(source)
    if args.mode in ("behavior", "all"):
        behavior_checks(source)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

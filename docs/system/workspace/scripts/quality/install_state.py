#!/usr/bin/env python3
"""Single source of truth for installed-state identity and activation.

The installed copy (``$FREELY_HOME/versions/<ver>``) used to be a write-only
artifact: nothing compared it with the project tree, ``latest`` was never
switched, and a dangling ``~/.local/bin/freely`` went unnoticed. This module
owns all four operations so `freely-package`, `freely doctor` and the merge
followthrough can never disagree:

    write_manifest(version_dir, root)   record source hashes at packaging time
    check_state(home, project, bin)     prove identity / detect drift + dangling
    activate(home, version_dir, bin)    atomic latest swap + link repair

All paths are injectable: tests use a temporary FREELY_HOME and a temporary git
project tree, never the real installation.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

# Files whose bytes decide whether "the installed freely is THIS source tree".
# Directories are covered transitively by these entry points; keep the list small
# so every packaging run stays cheap and the manifest stays human-reviewable.
KEY_FILES = (
    "bin/freely",
    "bin/issue-sync",
    "bin/freely-package",
    "docs/system/workspace/scripts/runtime/freely",
    "docs/system/workspace/scripts/worktree/pr-merge-guarded",
    "docs/system/workspace/package-allowlist.txt",
)
MANIFEST_NAME = ".freely_hashes"
VERSION_NAME = ".freely_version"


def default_home() -> Path:
    return Path(os.environ.get("FREELY_HOME") or (Path.home() / ".freely"))


def default_bin() -> Path:
    return Path.home() / ".local/bin/freely"


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_hashes(root: Path) -> dict[str, str]:
    root = Path(root)
    return {
        rel: _sha(root / rel)
        for rel in KEY_FILES
        if (root / rel).is_file()
    }


def write_manifest(version_dir: Path, root: Path) -> dict[str, str]:
    """Record the source hashes that produced this version. Called only after
    packaging integrity verification has succeeded."""
    version_dir = Path(version_dir)
    hashes = file_hashes(root)
    (version_dir / MANIFEST_NAME).write_text(
        json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return hashes


def read_manifest(version_dir: Path) -> dict[str, str]:
    path = Path(version_dir) / MANIFEST_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def head_of(project: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(project), "rev-parse", "--short", "HEAD"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def packaged_from(version_dir: Path) -> str:
    path = Path(version_dir) / VERSION_NAME
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("FREELY_PACKAGED_FROM="):
                return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return ""


def latest_target(home: Path) -> Path | None:
    latest = Path(home) / "versions/latest"
    if latest.is_symlink():
        return latest.resolve() if latest.exists() else None
    return latest if latest.is_dir() else None


def check_state(home: Path, project: Path, bin_path: Path) -> dict:
    """Return {"ok": bool, "errors": [...], "details": {...}}.

    Fail-closed: a missing latest, an unreadable version file, a HEAD behind the
    project, hash drift, or a dangling PATH link each produce an explicit error.
    """
    errors: list[str] = []
    details: dict[str, str] = {}
    home, project, bin_path = Path(home), Path(project), Path(bin_path)

    head = head_of(project)
    if not head:
        errors.append("cannot resolve project HEAD (not a git tree?)")
    details["project_head"] = head or "unknown"

    latest = home / "versions/latest"
    target = latest_target(home)
    if target is None:
        errors.append(f"dangling latest: {latest} does not resolve to a version directory")
    else:
        details["active_version"] = target.name
        pf = packaged_from(target)
        details["packaged_from"] = pf or "unknown"
        if not (target / VERSION_NAME).is_file():
            errors.append(f"installed version has no {VERSION_NAME}: {target}")
        elif not pf or not head or not (head.startswith(pf) or pf.startswith(head)):
            errors.append(
                f"installed state is behind project HEAD (packaged_from={pf or 'unknown'}, head={head or 'unknown'})"
            )
        manifest = read_manifest(target)
        if not manifest:
            errors.append(f"installed version has no hash manifest: {target}")
        else:
            current = file_hashes(project)
            drift = [
                rel for rel, expected in manifest.items()
                if current.get(rel) != expected
            ]
            if drift:
                errors.append("hash drift: " + ", ".join(sorted(drift)))

    if bin_path.is_symlink() and not bin_path.exists():
        errors.append(f"dangling bin link: {bin_path} -> {os.readlink(bin_path)}")
    elif bin_path.is_symlink():
        resolved = str(bin_path.resolve())
        if "/versions/" in resolved and not Path(resolved).exists():
            errors.append(f"bin link points at a deleted version: {resolved}")
        details["command_path"] = resolved

    return {"ok": not errors, "errors": errors, "details": details}


def activate(home: Path, version_dir: Path, bin_path: Path) -> dict:
    """Atomically switch `latest` to a verified version and repair a broken PATH link.

    Refuses to touch anything when the version is unverified, so a failed
    packaging run always leaves the previous installation usable.
    """
    home, version_dir, bin_path = Path(home), Path(version_dir), Path(bin_path)
    if not version_dir.is_dir():
        raise ValueError(f"refusing to activate a missing version: {version_dir}")
    if not (version_dir / VERSION_NAME).is_file():
        raise ValueError(f"refusing to activate an unverified version: {version_dir}")
    if not read_manifest(version_dir):
        raise ValueError(f"refusing to activate a version without a hash manifest: {version_dir}")

    versions = home / "versions"
    versions.mkdir(parents=True, exist_ok=True)
    latest = versions / "latest"
    previous = os.readlink(latest) if latest.is_symlink() else None

    # os.replace over a symlink is atomic: readers see either the old or the new
    # target, never a missing `latest`.
    tmp = versions / f".latest.tmp.{os.getpid()}"
    tmp.unlink(missing_ok=True)
    os.symlink(version_dir.name, tmp)
    os.replace(tmp, latest)

    # Only repair a broken/absent link. An existing healthy link may legitimately
    # point at the project tree (dev mode) and must not be overwritten.
    exe = version_dir / "bin/freely"
    link_fixed = False
    if (bin_path.is_symlink() and not bin_path.exists()) or not bin_path.exists():
        if exe.is_file():
            if bin_path.is_symlink():
                bin_path.unlink()
            bin_path.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(str(exe), bin_path)
            link_fixed = True

    return {
        "ok": True,
        "active": version_dir.name,
        "previous": previous,
        "idempotent": previous == version_dir.name,
        "link_fixed": link_fixed,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Freely installed-state identity")
    ap.add_argument("--project", default=str(Path.cwd()))
    ap.add_argument("--home", default=str(default_home()))
    ap.add_argument("--bin", default=str(default_bin()))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--root", default=None, help="source root for --write-manifest")
    ap.add_argument("--output", default=None, help="version dir for --write-manifest")
    ap.add_argument("--write-manifest", action="store_true")
    ap.add_argument("--version-dir", default=None, help="version dir for --activate")
    ap.add_argument("--activate", action="store_true")
    args = ap.parse_args(argv)

    if args.write_manifest:
        if not args.root or not args.output:
            print("ERROR: --write-manifest needs --root and --output", file=sys.stderr)
            return 2
        payload = {"ok": True, "hashes": write_manifest(args.output, args.root)}
    elif args.activate:
        if not args.version_dir:
            print("ERROR: --activate needs --version-dir", file=sys.stderr)
            return 2
        try:
            payload = activate(args.home, args.version_dir, args.bin)
        except ValueError as exc:
            payload = {"ok": False, "errors": [str(exc)]}
    else:
        payload = check_state(args.home, args.project, args.bin)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif payload.get("ok"):
        print("install_state: ok " + json.dumps(payload.get("details", {}), ensure_ascii=False))
    else:
        for err in payload.get("errors", []):
            print(f"install_state: ERROR {err}", file=sys.stderr)
        print("  fix: freely-package --version auto --activate", file=sys.stderr)
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

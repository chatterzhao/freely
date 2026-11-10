#!/usr/bin/env python3
"""AT-001 — raw-20261104T080014Z / #4166 (round 1).

Scope of this round: platform writes have one implementation.

`bin/issue-sync` used to call `gh issue create/comment/close/edit` inline while
Gitee went through `gitee-issue.py`, so every entry point had its own
label/body/error behaviour. The adapter already owns the GitHub/Gitee handlers
(`create-issue`, `update-issue`, `close-multi` with 0/3/1 exit codes); this
round adds a single-platform `issue-write-one` command and makes issue-sync use
it instead of `gh`.

The remaining #4166 items (splitting the 800-line `bin/issue-sync`, unifying
`feedback` body/labels with `issue-sync create`, and `issue-sync-bootstrap`'s
direct `gh issue delete`) are tracked by a follow-up raw issue.

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
SRC = Path(os.environ.get("PLATFORM_SYNC_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

ADAPTER = SRC / "docs/system/workspace/scripts/sync/platform-adapter.py"
ISSUE_SYNC = SRC / "bin/issue-sync"
MODULE_DIR = SRC / "bin/issue-sync.d"

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


# ── STATIC ───────────────────────────────────────────────────────────────

def static_checks() -> None:
    print("=== STATIC: one platform-write implementation ===")
    # #4286: bin/issue-sync only dispatches; read the whole program.
    sync = "\n".join(read(path) for path in
                      [ISSUE_SYNC, *sorted(MODULE_DIR.glob("*.sh"))])
    adapter = read(ADAPTER)

    direct = [needle for needle in (
        "gh issue create", "gh issue comment", "gh issue close", "gh issue edit",
    ) if needle in sync]
    expect(not direct, f"issue-sync has no direct gh issue writes ({direct})")

    expect("platform-adapter.py" in sync and "issue-write-one" in sync,
           "issue-sync writes through the adapter command")

    expect('a[1] == "issue-write-one"' in adapter
           and "handler.add_comment(number, body)" in adapter,
           "adapter exposes a single-platform write routed to the handler")


# ── BEHAVIOR: adapter single-platform create reaches the platform CLI ──

def _stub_gh(tmp: Path) -> tuple[Path, Path]:
    bindir = tmp / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    log = tmp / "gh.log"
    stub = bindir / "gh"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        f'printf \'%s\\n\' "$*" >> "{log}"\n'
        'if [[ "$*" == *"issue create"* ]]; then echo "https://github.com/acme/demo/issues/7"; exit 0; fi\n'
        "exit 0\n"
    )
    stub.chmod(0o755)
    return bindir, log


def behavior_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: adapter create-issue-one ===")
    if not ADAPTER.is_file():
        bad("adapter create reaches gh with labels")
        return
    repo = tmp / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=False)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                    "https://github.com/acme/demo.git"], check=False)
    bindir, log = _stub_gh(tmp)
    env = dict(os.environ)
    env["PATH"] = f"{bindir}:" + env.get("PATH", "")
    proc = subprocess.run(
        [sys.executable, str(ADAPTER), "issue-write-one", "github", "create", "",
         "T", "B", "kind/raw,phase/proposed"],
        cwd=str(repo), env=env, capture_output=True, text=True, timeout=60,
    )
    log_text = log.read_text() if log.is_file() else ""
    expect(proc.returncode == 0 and "issue create" in log_text
           and "--label kind/raw,phase/proposed" in log_text
           and "https://github.com/acme/demo/issues/7" in proc.stdout,
           "adapter create reaches gh with labels")


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-platform-sync-") as d:
        tmp = Path(d).resolve()
        static_checks()
        behavior_checks(tmp)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

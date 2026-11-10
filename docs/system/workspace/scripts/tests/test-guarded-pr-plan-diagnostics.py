#!/usr/bin/env python3
"""AT-001 for raw-20261110T052506Z: guarded PR plan must be diagnosable.

RED (develop baseline):
  - plan_platform_updates() drops observations[platform]["error"]
  - recovery is a single fixed string pointing at "sync branches" even when
    the real cause is an unreachable platform
  - fetch_branch_head() has no subprocess timeout (a hung git fetch hangs the
    whole guarded command)

GREEN:
  - each failing platform carries a truncated real error in the plan
  - recovery is classified: environment/network vs branch divergence
  - all git subprocesses in fetch_branch_head have one shared timeout constant
  - all-or-nothing aggregation, classify_branch and safe paths are unchanged

Usage:
  python3 test-guarded-pr-plan-diagnostics.py [--source-dir DIR] [--json]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[4]
LIFECYCLE_REL = Path("docs/system/workspace/scripts/sync/pr_lifecycle.py")
ADAPTER_REL = Path("docs/system/workspace/scripts/sync/platform-adapter.py")
EXISTING_TEST = Path("docs/system/workspace/scripts/tests/test-command-lifecycle-pr-update.py")

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve()
    if not src.is_dir():
        print(f"source dir missing: {src}")
        return 2

    lc_path = src / LIFECYCLE_REL
    ad_path = src / ADAPTER_REL
    if not lc_path.is_file() or not ad_path.is_file():
        print("lifecycle/adapter source missing")
        return 2
    lc = load(lc_path, "pr_lifecycle_at")
    ad = load(ad_path, "platform_adapter_at")
    lc_src = lc_path.read_text(encoding="utf-8", errors="replace")
    ad_src = ad_path.read_text(encoding="utf-8", errors="replace")

    # ── control group: TRUE on the baseline, prove assertions measure the
    #    right thing and that fail-closed semantics are preserved ──────────
    check("C1 classify_branch 5 states unchanged (control)",
          [lc.classify_branch("local", None, lambda *_: False),
           lc.classify_branch("local", "local", lambda *_: False),
           lc.classify_branch("local", "x", lambda *_: True),
           lc.classify_branch("local", "x", lambda l, r: l == "local"),
           lc.classify_branch("local", "x", lambda *_: False)]
          == ["absent", "equal", "behind", "ahead", "diverged"],
          "classification matrix")
    check("C2 SAFE/BLOCKED state sets unchanged (control)",
          lc.SAFE_BRANCH_STATES == {"absent", "behind", "equal"}
          and lc.BLOCKED_BRANCH_STATES == {"ahead", "diverged"},
          "state sets")

    # ── static group ──────────────────────────────────────────────────
    check("S1 single timeout constant declared",
          "GIT_FETCH_TIMEOUT_SECS" in ad_src
          and ad_src.count("GIT_FETCH_TIMEOUT_SECS") >= 3
          and "timeout=GIT_FETCH_TIMEOUT_SECS" in ad_src,
          "one constant, one git helper, no scattered literals")
    check("S2 plan retains observation error",
          'obs.get("error")' in lc_src or "obs['error']" in lc_src or
          'observation.get("error")' in lc_src,
          "plan must copy the real error into details")
    check("S3 recovery classifier is a single source",
          "def recovery_for_plan" in lc_src and "recovery_for_plan" in ad_src,
          "pure function in lifecycle, adapter calls it, no literal duplication")
    check("S4 two distinct recovery texts",
          "def recovery_for_plan" in lc_src and "ls-remote" in lc_src
          and "同步" in lc_src,
          "environment text must contain a probe command; branch text stays Chinese sync hint")

    # ── behavior: plan error propagation ──────────────────────────────
    CAUSE = "ssh: connect to host github.com port 22: Operation timed out"
    observations = {
        "github": {"branch_state": "error", "error": CAUSE},
        "gitee": {"branch_state": "absent"},
    }
    plan = lc.plan_platform_updates(
        configured_platforms=["github", "gitee"], observations=observations
    )
    check("B1 plan carries real error for failing platform",
          "connect to host" in str(plan["platforms"]["github"].get("error", "")),
          f"github detail={plan['platforms']['github']}")
    check("B2 all-or-nothing aggregation unchanged",
          plan["safe_to_execute"] is False and plan["actions"] == []
          and plan["platforms"]["gitee"]["action"] == "blocked_by_aggregate",
          f"plan={plan}")
    check("B3 healthy platform detail has no invented error",
          "error" not in plan["platforms"]["gitee"],
          "do not fabricate diagnostics for platforms that were fine")

    # ── behavior: recovery classification ─────────────────────────────
    if hasattr(lc, "recovery_for_plan"):
        env_rec = lc.recovery_for_plan(plan)
        div_plan = lc.plan_platform_updates(
            configured_platforms=["github", "gitee"],
            observations={"github": {"branch_state": "behind"},
                          "gitee": {"branch_state": "diverged"}},
        )
        div_rec = lc.recovery_for_plan(div_plan)
        check("B4 environment recovery names a probe command",
              "ls-remote" in env_rec and "ssh" in env_rec and "同步" not in env_rec,
              f"env={env_rec[:160]}")
        check("B5 diverged recovery still says sync branches",
              "同步" in div_rec and "ls-remote" not in div_rec,
              f"div={div_rec[:160]}")
        check("B6 safe plan recovery is the branch-sync text",
              "同步" in lc.recovery_for_plan(lc.plan_platform_updates(
                  configured_platforms=["github"],
                  observations={"github": {"branch_state": "equal"}})),
              "unchanged for non-failure paths")
    else:
        for n in ("B4 environment recovery names a probe command",
                  "B5 diverged recovery still says sync branches",
                  "B6 safe plan recovery is the branch-sync text"):
            check(n, False, "recovery_for_plan missing")

    # ── behavior: guarded_pr_update return body ────────────────────────
    class FailingHandler:
        name = "github"

        def remote_name(self):
            return "all"

        def fetch_branch_head(self, _branch):
            raise RuntimeError(CAUSE)

        def push_branch(self, _branch):
            raise AssertionError("must not push on a failed plan")

        def ensure_pr(self, *_args):
            raise AssertionError("must not create PR on a failed plan")

    def fake_run(argv, **_kwargs):
        if argv[:2] == ["git", "rev-parse"]:
            return SimpleNamespace(returncode=0, stdout="local\n", stderr="")
        return SimpleNamespace(returncode=1, stdout="", stderr="")

    with patch.object(ad, "configured_platforms", return_value=["github", "gitee"]), \
         patch.object(ad, "_handler_for", side_effect=lambda p:
                      FailingHandler() if p == "github" else None), \
         patch.object(ad.subprocess, "run", side_effect=fake_run):
        result = ad.guarded_pr_update("fix/x", title="t", body="b")
    body = json.dumps(result, ensure_ascii=False)
    check("B7 guarded failure result contains the real cause",
          "connect to host" in body and "github" in body,
          f"body={body[:260]}")
    check("B8 guarded failure result does not push anything",
          result.get("success") is False and result.get("stage") == "plan"
          and result.get("actions", []) == [],
          f"stage={result.get('stage')}")

    # ── behavior: timeout on every git call in fetch_branch_head ────────
    calls: list[dict] = []

    def recording_run(argv, **kwargs):
        calls.append({"argv": argv, "kwargs": kwargs})
        if argv[:2] == ["git", "fetch"]:
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        if argv[:2] == ["git", "rev-parse"] and "--verify" not in argv and len(argv) == 3:
            return SimpleNamespace(returncode=0, stdout="abc123\n", stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    handler = object.__new__(ad.GitHubHandler)
    with patch.object(ad.subprocess, "run", side_effect=recording_run), \
         patch.object(ad.GitHubHandler, "remote_name", return_value="all"):
        try:
            ad.GitHubHandler.fetch_branch_head(handler, "fix/x")
        except Exception:
            pass
    fetch_calls = [c for c in calls if c["argv"][:2] == ["git", "fetch"]]
    rev_calls = [c for c in calls if c["argv"][:2] == ["git", "rev-parse"]]
    check("B9 git fetch has an explicit timeout",
          bool(fetch_calls) and all("timeout" in c["kwargs"] for c in fetch_calls),
          f"calls={fetch_calls}")
    check("B10 rev-parse has an explicit timeout",
          bool(rev_calls) and all("timeout" in c["kwargs"] for c in rev_calls),
          f"calls={rev_calls}")

    # timeout expiry must surface as an explicit environment error, not hang
    def timeout_run(argv, **_kwargs):
        raise subprocess.TimeoutExpired(argv, 30)

    with patch.object(ad.subprocess, "run", side_effect=timeout_run), \
         patch.object(ad.GitHubHandler, "remote_name", return_value="all"):
        try:
            ad.GitHubHandler.fetch_branch_head(handler, "fix/x")
            msg = ""
        except Exception as exc:
            msg = str(exc)
    check("B11 timeout produces explicit environment diagnostic",
          "timed out" in msg.lower() and "github" in msg.lower(),
          f"msg={msg[:200]!r}")

    # ── existing regression suite must stay green ──────────────────────
    if (src / EXISTING_TEST).is_file():
        r = subprocess.run([sys.executable, str(src / EXISTING_TEST)],
                           cwd=str(src), capture_output=True, text=True, timeout=120)
        check("B12 existing pr-update regression suite green",
              r.returncode == 0,
              f"rc={r.returncode} out={(r.stdout + r.stderr)[-220:]}")
    else:
        check("B12 existing pr-update regression suite green", False, "test file missing")

    ok = sum(1 for _, o, _ in results if o)
    failed = len(results) - ok
    if args.json:
        print(json.dumps({"ok": ok, "failed": failed,
                          "results": [{"name": n, "ok": o, "detail": d} for n, o, d in results]},
                         ensure_ascii=False, indent=2))
    else:
        for n, o, d in results:
            print(f"[{'PASS' if o else 'FAIL'}] {n}" + (f" — {d}" if not o else ""))
        print(f"SUMMARY: {ok} ok, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

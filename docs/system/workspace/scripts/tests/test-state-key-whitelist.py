#!/usr/bin/env python3
"""AT-001 — raw-20261110T084522Z / #4264 (state-key whitelist contract).

`state_file.py::ALLOWED_KEYS` claimed to come from a "full scan" but only
covered a subset of the write shapes, leaving 50 written keys unregistered.
`read_state` calls `_check_key` on EVERY line (including legacy `KEY=value`),
so one unregistered key makes a whole existing state file unreadable; shell
callers swallow that with `|| true`, silently dropping state.

This AT verifies:
  1. every key actually written by `runtime/freely` is registered;
  2. the scanner itself covers all five write shapes (heredoc, here-string,
     printf template, echo redirect, `--kv`), so it cannot silently miss keys;
  3. legacy and TAB+JSON files for the newly registered keys round-trip
     verbatim; a forged unknown key is still REJECTED.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (77 keys, lint missing -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("KEY_SOURCE_ROOT", str(PROJECT))).resolve()

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


def load_module(src: Path):
    path = src / "docs/system/workspace/scripts/runtime/state_file.py"
    spec = importlib.util.spec_from_file_location("_state_key_at", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_state_key_at"] = module
    spec.loader.exec_module(module)
    return module


# The 65 keys found by re-scanning develop 6b927cae1 with all five write shapes
# (50 from the first pass + 15 manager/preemption keys hidden behind a
# command-substitution heredoc target).
EXPECTED_NEW_KEYS = """
ACTIVE_RUNNING_WORKER_COUNT AVAILABLE_NEW_WORKER_SLOTS
LAST_MANAGER_CONTINUITY_CONSUMED LAST_MANAGER_CONTINUITY_GENERATED
LAST_MANAGER_WORKER_PROMPTS_CONSUMED LAST_MANAGER_WORKER_PROMPTS_GENERATED
LAST_PREEMPTION_AT LAST_PREEMPTION_INTAKE_ID LAST_PREEMPTION_MODE
LAST_PREEMPTION_PID LAST_PREEMPTION_REASON LAUNCHED_WORKER_PROMPTS
MAX_PARALLEL_WORKERS QUEUED_WORKER_PROMPTS QUEUED_WORKER_PROMPT_BLOCKERS
ABSORPTION_TARGET CLASSIFICATION CLOSEOUT_GATE CLOSEOUT_GATE_COMMAND
CLOSEOUT_PROMOTION_GATE CLOSEOUT_REQUIRES_ADEQUACY CLOSEOUT_REVIEW_ARTIFACT_POLICY
CLOSEOUT_TARGET_LANE CREATED_AT DELEGATED_WORKTREE ENTRYPOINT_MODE FORCE_FRESH
INTAKE_ID LAST_TESTED_AT LAST_TESTED_COMMIT LINKED_ARTIFACT LOOP_GUARD_L1_STRIKES
LOOP_GUARD_L2_START_BYTES LOOP_GUARD_L2_START_TIME LOOP_GUARD_L3_ACCUMULATED
MINIMUM_EVIDENCE_LEVEL OPERATOR_STOP_BOUNDARY_EPOCH OPERATOR_STOP_BOUNDARY_RECORDED_AT
OWNER_ISSUE PENDING_INTAKE_ITEMS PRE_TESTS_PATH PROJECT_ROOT REACTION
REQUIRED_ACCEPTANCE_ITEM_IDS_CSV REQUIRED_TEST_LANES_CSV RESOLVED_BY
SOURCE_INTAKE_ID SOURCE_PROMPT_FILE STARTUP_TRUTH_PHASE STARTUP_TRUTH_PUBLISHED_AT
STATUS SUPERVISOR_PID TARGET_ENVIRONMENT TARGET_PROJECT TEST_STATUS UPDATED_AT
VERIFICATION_ARTIFACT_DIR VERIFICATION_METADATA_MISSING_FIELDS
VERIFICATION_METADATA_PRESENT acquired_at owner_pid prev_exit_kind
prev_worker_launched reason started_at
""".split()


def static_checks(src: Path) -> None:
    print("=== STATIC: whitelist complete and lint is the contract ===")
    module_path = src / "docs/system/workspace/scripts/runtime/state_file.py"
    if module_path.is_file():
        text = module_path.read_text(encoding="utf-8")
        expect("full scan" not in text and "check-state-file-keys" in text,
               "whitelist no longer claims an unverified survey; points at the lint")
    else:
        bad("whitelist no longer claims an unverified 'full scan' (module missing)")

    lint = src / "bin/check-state-file-keys"
    if not lint.is_file():
        bad("key-contract lint exists (missing)")
        bad("lint reports zero missing keys (lint missing)")
        bad("lint reports zero stale keys (lint missing)")
        return
    ok("key-contract lint exists")
    r = subprocess.run([sys.executable, str(lint), "--project", str(src), "--json"],
                       capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        data = {"missing": ["<unparseable>"], "stale": ["<unparseable>"]}
    expect(r.returncode == 0 and not data.get("missing"),
           f"lint reports zero missing keys (got {len(data.get('missing', []))}, rc={r.returncode})")
    expect(not data.get("stale"),
           f"lint reports zero stale keys (got {len(data.get('stale', []))})")


def scanner_checks(src: Path, tmp: Path) -> None:
    print("=== SCANNER: all five write shapes are visible to the lint ===")
    lint = src / "bin/check-state-file-keys"
    if not lint.is_file():
        for label in ("heredoc", "command-substitution heredoc target",
                      "here-string first line", "printf template",
                      "echo redirect", "--kv argv write",
                      "no local shell variables leaked"):
            bad(f"scanner extracts {label} (lint missing)")
        return

    probe = tmp / "probe"
    runtime = probe / "docs/system/workspace/scripts/runtime"
    runtime.mkdir(parents=True)
    # The lint loads ALLOWED_KEYS from the probe project.
    import shutil
    shutil.copy(src / "docs/system/workspace/scripts/runtime/state_file.py",
                runtime / "state_file.py")
    (runtime / "freely").write_text("""\
cat >"$state_file" <<EOF
HEREDOC_KEY="a"
SECOND_HEREDOC="b"
EOF
cat >"$(manager_worker_launch_state_file "$project")" <<EOF
CMD_SUBST_KEY="a"
EOF
cat > "$state_file" <<< "HERE_FIRST=one
HERE_SECOND=two"
printf 'PRINTF_KEY="%s"\\n' "$x"
echo "ECHO_KEY=$val" > "$state_file"
python3 "$STATE_FILE_PY" write "$state_file" --kv "KV_KEY=$value"
""", encoding="utf-8")

    r = subprocess.run([sys.executable, str(lint), "--project", str(probe), "--json"],
                       capture_output=True, text=True, timeout=120)
    try:
        found = set(json.loads(r.stdout)["missing"])
    except (json.JSONDecodeError, KeyError):
        found = set()
    # All probe keys are deliberately NOT whitelisted, so they show up as missing.
    for label, key in (("heredoc", "HEREDOC_KEY"),
                       ("command-substitution heredoc target", "CMD_SUBST_KEY"),
                       ("here-string first line", "HERE_FIRST"),
                       ("printf template", "PRINTF_KEY"),
                       ("echo redirect", "ECHO_KEY"),
                       ("--kv argv write", "KV_KEY")):
        expect(key in found, f"scanner extracts {label} (missing={sorted(found)[:8]})")
    # A too-greedy heredoc regex once swallowed local shell variables from a
    # here-string payload; those must never be mistaken for state keys.
    leaked = [k for k in found if k in ("accumulated", "now_epoch", "state_file",
                                        "worker_launched", "window_start_bytes")]
    expect(not leaked, f"no local shell variables leaked into the key set (got {leaked})")


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: legacy + TAB/JSON round-trip, unknown still rejected ===")
    try:
        mod = load_module(src)
    except Exception as exc:
        for label in ("all newly registered keys readable as legacy",
                      "all newly registered keys writable as TAB+JSON",
                      "forged unknown key still rejected",
                      "verdict-compatible legacy file with mixed keys reads"):
            bad(f"{label} (module unusable: {type(exc).__name__})")
        return

    registered = set(mod.ALLOWED_KEYS)
    missing = [k for k in EXPECTED_NEW_KEYS if k not in registered]
    expect(not missing,
           f"all {len(EXPECTED_NEW_KEYS)} newly registered keys are in ALLOWED_KEYS "
           f"(missing {len(missing)}: {missing[:5]})")

    state = tmp / "legacy.env"
    failed_legacy = []
    for key in EXPECTED_NEW_KEYS:
        state.write_text(f'{key}="value-{key}"\n', encoding="utf-8")
        try:
            got = mod.read_state(state).get(key)
            if got != f"value-{key}":
                failed_legacy.append(key)
        except Exception:
            failed_legacy.append(key)
    expect(not failed_legacy,
           f"all newly registered keys readable as legacy KEY=value "
           f"(failed {len(failed_legacy)}: {failed_legacy[:5]})")

    failed_json = []
    for key in EXPECTED_NEW_KEYS:
        payload = {"k": f'x"$(touch {tmp}/marker)"`id`'}
        # write_state uses the real key, read_state must return it verbatim
        try:
            mod.write_state(state, {key: payload["k"]})
            got = mod.read_state(state).get(key)
            if got != payload["k"]:
                failed_json.append(key)
        except Exception:
            failed_json.append(key)
    expect(not failed_json and not (tmp / "marker").exists(),
           f"all newly registered keys writable as TAB+JSON, verbatim, no execution "
           f"(failed {len(failed_json)})")

    try:
        state.write_text('FORGED_UNKNOWN_KEY="x"\n', encoding="utf-8")
        mod.read_state(state)
        rejected = False
    except Exception:
        rejected = True
    expect(rejected, "forged unknown key still rejected (guard not weakened)")

    # The exact symptom from the issue: a legacy file with two manager keys.
    state.write_text(
        'LAST_MANAGER_CONTINUITY_GENERATED="/a/b"\n'
        'QUEUED_WORKER_PROMPTS="x,y"\n', encoding="utf-8")
    try:
        got = mod.read_state(state)
        ok_match = (got.get("LAST_MANAGER_CONTINUITY_GENERATED") == "/a/b"
                    and got.get("QUEUED_WORKER_PROMPTS") == "x,y")
    except Exception:
        ok_match = False
    expect(ok_match,
           "verdict-compatible legacy file with mixed keys reads (issue's repro)")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="state-keys-"))
    try:
        static_checks(src)
        scanner_checks(src, tmp)
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())

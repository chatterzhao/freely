#!/usr/bin/env python3
"""AT-001 for raw-20261104T075810Z: config schema must be machine-checkable.

RED (develop baseline):
  - no contracts/config/schema.yaml
  - no quality/config_schema.py
  - doctor never validates config types / unknown keys / missing keys
  - allowed_paths written as a string is silently ignored by every consumer

GREEN (this worktree):
  - schema exists, is stdlib-parseable, covers all 58 keys of .freely/config.toml
  - a string allowed_paths is reported with file:line and expected type
  - unknown keys and missing required keys are reported with file:line
  - a valid list-shaped config (including the shipped template) passes
  - doctor actually calls the validator (no second implementation)

Usage:
  python3 test-config-schema-validation.py [--source-dir DIR]
  python3 test-config-schema-validation.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[4]  # tests -> scripts -> workspace -> system -> docs -> root
SCHEMA_REL = Path("contracts/config/schema.yaml")
VALIDATOR_REL = Path("docs/system/workspace/scripts/quality/config_schema.py")
RUNTIME_REL = Path("docs/system/workspace/scripts/runtime/freely")
TEMPLATE_REL = Path("templates/config.toml.example")
ALLOWLIST_REL = Path("docs/system/workspace/package-allowlist.txt")

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def run(cmd: list[str], cwd: str | None = None, env: dict | None = None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=120)


def make_config(body: str, root: Path) -> Path:
    cfg_dir = root / ".freely"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg = cfg_dir / "config.toml"
    cfg.write_text(body, encoding="utf-8")
    return cfg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(DEFAULT_SOURCE))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve()
    if not src.is_dir():
        print(f"source dir missing: {src}")
        return 2

    schema = src / SCHEMA_REL
    validator = src / VALIDATOR_REL
    runtime = src / RUNTIME_REL
    template = src / TEMPLATE_REL
    allowlist = src / ALLOWLIST_REL

    # ── static group ────────────────────────────────────────────────
    check("S1 schema.yaml exists", schema.is_file(), str(schema))
    check("S2 validator exists", validator.is_file(), str(validator))

    schema_obj = None
    if schema.is_file():
        try:
            # YAML 1.2 JSON-compatible subset: stdlib only, no PyYAML needed.
            schema_obj = json.loads(schema.read_text(encoding="utf-8"))
            check("S3 schema stdlib-parseable", True, "json.loads ok")
        except Exception as exc:  # pragma: no cover - RED path
            check("S3 schema stdlib-parseable", False, repr(exc))
    else:
        check("S3 schema stdlib-parseable", False, "schema missing")

    covered = 0
    if schema_obj:
        keys = schema_obj.get("keys", {})
        sections = schema_obj.get("sections", {})
        covered = len(keys) + sum(len(v.get("keys", {})) for v in sections.values())
        check("S4 schema covers all 58 config keys", covered == 58, f"covered={covered}")
        ap_decl = sections.get("skip_ibm_gate", {}).get("keys", {}).get("allowed_paths", {})
        check("S5 allowed_paths declared list[str]",
              ap_decl.get("type") == "list[str]", f"type={ap_decl.get('type')!r}")
        declared = set(keys)
        for sec in sections.values():
            declared |= {f"{sec.get('name', '')}.{k}" for k in sec.get("keys", {})}
        # required keys must be declared as required
        req = [k for k, v in keys.items() if v.get("required") is True]
        check("S6 required keys declared", "PROJECT_ROOT" in req, f"required={req}")
        check("S7 every schema key has type/default/scope/consumer",
              all(all(f in v for f in ("type", "default", "scope", "consumers"))
                  for v in list(keys.values()) +
                  [x for s in sections.values() for x in s.get("keys", {}).values()]),
              "field completeness")
    else:
        for n in ("S4 schema covers all 58 config keys", "S5 allowed_paths declared list[str]",
                  "S6 required keys declared", "S7 every schema key has type/default/scope/consumer"):
            check(n, False, "schema missing")

    doctor_src = runtime.read_text(encoding="utf-8", errors="replace") if runtime.is_file() else ""
    check("S8 doctor wires the validator",
          "config_schema.py" in doctor_src and "config_schema:" in doctor_src,
          "cmd_doctor must call the single validator")
    check("S9 no second implementation of config validation in doctor",
          doctor_src.count("config_schema.py") == 1,
          f"references={doctor_src.count('config_schema.py')}")
    allow_txt = allowlist.read_text(encoding="utf-8", errors="replace") if allowlist.is_file() else ""
    check("S10 contracts/ is packaged",
          any(ln.strip().startswith("contracts/") for ln in allow_txt.splitlines()),
          "installed doctor must find the schema")

    # ── control group: facts that are TRUE on the baseline ───────────
    # These PASS in RED. They prove the assertions are not measuring the
    # wrong thing, and they are the evidence for two honest scope calls:
    #   * the shipped template is already list-shaped -> no template rewrite
    #   * the gate silently ignores a non-list -> this PR adds diagnosis,
    #     it does NOT change gate semantics (fail-closed there would
    #     dead-lock every PR because local config is a string today).
    tpl_txt = template.read_text(encoding="utf-8", errors="replace") if template.is_file() else ""
    check("S11 template already list-shaped (control)",
          "allowed_paths = [" in tpl_txt, "acceptance-3 first half is already true")
    gate = src / "docs/system/workspace/scripts/quality/governance-merge-gate"
    gate_src = gate.read_text(encoding="utf-8", errors="replace") if gate.is_file() else ""
    check("S12 gate silently ignores non-list (control)",
          "isinstance(raw, list)" in gate_src and "except Exception:" in gate_src,
          "root cause present on baseline; gate semantics unchanged by this PR")

    # ── behavior group ──────────────────────────────────────────────
    if not validator.is_file() or schema_obj is None:
        for n in ("B1 string allowed_paths reported with line", "B2 unknown key reported with line",
                  "B3 missing required key reported", "B4 valid list config passes",
                  "B5 shipped template passes", "B6 bool/int/float mismatch detected",
                  "B7 missing schema fails closed", "B8 doctor output carries diagnosis"):
            check(n, False, "validator/schema missing")
    else:
        with tempfile.TemporaryDirectory(prefix="cfg-schema-at-") as td:
            root = Path(td)

            bad = "\n".join([
                'PROJECT_ROOT = "' + str(root) + '"',
                'INTENT_FILE = "' + str(root / "docs/PROJECT_INTENT.md") + '"',
                'CONSTITUTION_FILE = "' + str(root / "docs/CONSTITUTION.md") + '"',
                'FREELY_HOME = "' + str(root) + '"',
                'CHECK_INTERVAL = 10',
                'AUTO_SWITCH_SLOT = true',
                'CONTEXT_WARN_RATIO = 0.7',
                'TOTALLY_UNKNOWN_KEY = "x"',
                '',
                '[skip_ibm_gate]',
                'allowed_paths = "[\'templates/\']"',
                '',
            ])
            cfg = make_config(bad, root)
            r = run([sys.executable, str(validator), "--project", str(root),
                     "--schema", str(schema)], cwd=str(src))
            out = r.stdout + r.stderr
            check("B1 string allowed_paths reported with line",
                  r.returncode == 1 and "allowed_paths" in out and ":11:" in out
                  and "list[str]" in out and "str" in out,
                  f"rc={r.returncode} out={out.strip()[:300]}")
            check("B2 unknown key reported with line",
                  "unknown key" in out.lower() and "TOTALLY_UNKNOWN_KEY" in out and ":8:" in out,
                  f"out={out.strip()[:300]}")

            cfg2 = make_config("\n".join([
                'PROJECT_ROOT = "' + str(root) + '"',
                'INTENT_FILE = "' + str(root / "docs/PROJECT_INTENT.md") + '"',
                'FREELY_HOME = "' + str(root) + '"',
                '',
                '[skip_ibm_gate]',
                'allowed_paths = ["templates/"]',
                '',
            ]), root)
            r2 = run([sys.executable, str(validator), "--project", str(root),
                      "--schema", str(schema)], cwd=str(src))
            out2 = r2.stdout + r2.stderr
            check("B3 missing required key reported",
                  r2.returncode == 1 and "CONSTITUTION_FILE" in out2 and "missing" in out2.lower(),
                  f"rc={r2.returncode} out={out2.strip()[:300]}")

            good_text = template.read_text(encoding="utf-8") if template.is_file() else ""
            cfg3 = make_config(good_text.replace(str('PROJECT_ROOT = ""'),
                                                 f'PROJECT_ROOT = "{root}"'), root)
            r3 = run([sys.executable, str(validator), "--project", str(root),
                      "--schema", str(schema)], cwd=str(src))
            out3 = r3.stdout + r3.stderr
            check("B4 valid list config passes", r3.returncode == 0 and "ok" in out3.lower(),
                  f"rc={r3.returncode} out={out3.strip()[:300]}")
            check("B5 shipped template passes",
                  "allowed_paths = [" in good_text and r3.returncode == 0,
                  "template already list-shaped; no rewrite needed")

            bad_types = "\n".join([
                'PROJECT_ROOT = "' + str(root) + '"',
                'INTENT_FILE = "' + str(root / "docs/PROJECT_INTENT.md") + '"',
                'CONSTITUTION_FILE = "' + str(root / "docs/CONSTITUTION.md") + '"',
                'FREELY_HOME = "' + str(root) + '"',
                'CHECK_INTERVAL = "ten"',
                'AUTO_SWITCH_SLOT = 1',
                'CONTEXT_WARN_RATIO = "0.7"',
                '',
                '[skip_ibm_gate]',
                'allowed_paths = ["templates/"]',
                '',
            ])
            make_config(bad_types, root)
            r4 = run([sys.executable, str(validator), "--project", str(root),
                      "--schema", str(schema)], cwd=str(src))
            out4 = r4.stdout + r4.stderr
            check("B6 bool/int/float mismatch detected",
                  r4.returncode == 1 and all(k in out4 for k in
                                             ("CHECK_INTERVAL", "AUTO_SWITCH_SLOT", "CONTEXT_WARN_RATIO")),
                  f"rc={r4.returncode} out={out4.strip()[:300]}")

            r5 = run([sys.executable, str(validator), "--project", str(root),
                      "--schema", str(root / "nope.yaml")], cwd=str(src))
            check("B7 missing schema fails closed", r5.returncode == 2,
                  f"rc={r5.returncode} out={(r5.stdout + r5.stderr).strip()[:200]}")

            # doctor must surface the diagnosis for a broken config, without
            # changing doctor's own exit contract (it is a diagnostic command).
            make_config(bad, root)
            freely = src / "bin" / "freely"
            if freely.is_file():
                env = dict(os.environ)
                env["FREELY_HOME"] = str(src)
                rd = run([str(freely), "doctor", "--project", str(root)], cwd=str(src), env=env)
                outd = rd.stdout + rd.stderr
                check("B8 doctor output carries diagnosis",
                      "config_schema:" in outd and "allowed_paths" in outd and ":11:" in outd,
                      f"rc={rd.returncode} out={outd.strip()[-400:]}")
            else:
                check("B8 doctor output carries diagnosis", False, "bin/freely missing")

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

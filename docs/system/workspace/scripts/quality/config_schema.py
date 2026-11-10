#!/usr/bin/env python3
"""Validate a project's .freely/config.toml against contracts/config/schema.yaml.

Single source of truth for config structure. Stdlib only (tomllib + json):
the schema file is written in the YAML 1.2 JSON-compatible subset, so an
installed freely needs no PyYAML to validate a config.

Exit codes:
  0  config conforms (prints "config_schema: ok")
  1  findings (type mismatch / unknown key / missing required key)
  2  environment unusable (schema or config missing, unparseable)

Every finding carries an absolute-or-relative ``file:line`` location and the
expected type. Nothing is silently coerced: a string where ``list[str]`` is
expected is an error, not a fallback to defaults.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA_REL = Path("contracts/config/schema.yaml")
SELF_ROOT = Path(__file__).resolve().parents[5]  # quality -> scripts -> workspace -> system -> docs -> root

TYPES = {
    "str": lambda v: isinstance(v, str),
    "bool": lambda v: isinstance(v, bool),
    "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "float": lambda v: isinstance(v, float)
    or (isinstance(v, int) and not isinstance(v, bool)),
    "list[str]": lambda v: isinstance(v, list) and all(isinstance(x, str) for x in v),
    "table": lambda v: isinstance(v, dict),
}

KEY_LINE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=")
SECTION_LINE = re.compile(r"^\s*\[([^\]]+)\]\s*$")


def locate(config_path: Path) -> tuple[dict[tuple[str, str], int], dict[str, int]]:
    """Return (section, key) -> 1-based line, and section -> line."""
    keys: dict[tuple[str, str], int] = {}
    sections: dict[str, int] = {}
    current = ""
    for lineno, line in enumerate(config_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = SECTION_LINE.match(line)
        if m:
            current = m.group(1).strip()
            sections[current] = lineno
            continue
        if line.lstrip().startswith("#"):
            continue
        m = KEY_LINE.match(line)
        if m:
            keys[(current, m.group(1))] = lineno
    return keys, sections


def type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "table"
    return type(value).__name__


def validate(config_path: Path, schema: dict) -> list[str]:
    findings: list[str] = []
    try:
        with config_path.open("rb") as fh:
            cfg = tomllib.load(fh)
    except Exception as exc:
        return [f"{config_path}:1: config unparseable: {exc}"]

    loc, sec_loc = locate(config_path)
    where = str(config_path)
    keys_spec: dict[str, dict] = schema.get("keys", {})
    sections_spec: dict[str, dict] = schema.get("sections", {})

    # 1. top-level scalar keys
    for key, spec in keys_spec.items():
        expected = spec.get("type", "str")
        if key not in cfg:
            if spec.get("required"):
                findings.append(
                    f"{where}:1: missing required key '{key}' (expected {expected})"
                )
            continue
        value = cfg[key]
        if expected in TYPES and not TYPES[expected](value):
            line = loc.get(("", key), 1)
            findings.append(
                f"{where}:{line}: key '{key}' expected {expected}, got {type_name(value)}"
            )

    # 2. unknown top-level keys (tables are checked as sections below)
    known_sections = set(sections_spec)
    for key, value in cfg.items():
        if key in keys_spec:
            continue
        if key in known_sections and isinstance(value, dict):
            continue
        line = loc.get(("", key), sec_loc.get(key, 1))
        findings.append(f"{where}:{line}: unknown key '{key}' (no schema entry)")

    # 3. declared sections
    for sec_name, sec in sections_spec.items():
        sec_keys: dict[str, dict] = sec.get("keys", {})
        body = cfg.get(sec_name)
        if body is None:
            continue
        if not isinstance(body, dict):
            line = sec_loc.get(sec_name, loc.get(("", sec_name), 1))
            findings.append(
                f"{where}:{line}: section '{sec_name}' expected table, got {type_name(body)}"
            )
            continue
        for key, spec in sec_keys.items():
            expected = spec.get("type", "str")
            if key not in body:
                if spec.get("required"):
                    findings.append(
                        f"{where}:{sec_loc.get(sec_name, 1)}: missing required key "
                        f"'{sec_name}.{key}' (expected {expected})"
                    )
                continue
            value = body[key]
            if expected in TYPES and not TYPES[expected](value):
                line = loc.get((sec_name, key), sec_loc.get(sec_name, 1))
                findings.append(
                    f"{where}:{line}: key '{sec_name}.{key}' expected {expected}, "
                    f"got {type_name(value)}"
                )
        for key in body:
            if key not in sec_keys:
                line = loc.get((sec_name, key), sec_loc.get(sec_name, 1))
                findings.append(
                    f"{where}:{line}: unknown key '{sec_name}.{key}' (no schema entry)"
                )

    # 4. unknown sections
    for key, value in cfg.items():
        if isinstance(value, dict) and key not in known_sections:
            line = sec_loc.get(key, 1)
            findings.append(f"{where}:{line}: unknown section '[{key}]' (no schema entry)")

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", help="project root containing .freely/config.toml")
    ap.add_argument("--config", help="explicit config.toml path (overrides --project)")
    ap.add_argument("--schema", help="explicit schema path (default: bundled contract)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    schema_path = Path(args.schema).resolve() if args.schema else SELF_ROOT / DEFAULT_SCHEMA_REL
    if args.config:
        config_path = Path(args.config).resolve()
    elif args.project:
        config_path = Path(args.project).resolve() / ".freely" / "config.toml"
    else:
        print("config_schema: UNAVAILABLE — --project or --config required", file=sys.stderr)
        return 2

    if not schema_path.is_file():
        print(f"config_schema: UNAVAILABLE — schema missing: {schema_path}", file=sys.stderr)
        return 2
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"config_schema: UNAVAILABLE — schema unparseable: {exc}", file=sys.stderr)
        return 2
    if not isinstance(schema.get("keys"), dict) or not isinstance(schema.get("sections"), dict):
        print("config_schema: UNAVAILABLE — schema missing keys/sections", file=sys.stderr)
        return 2
    if not config_path.is_file():
        print(f"config_schema: UNAVAILABLE — config missing: {config_path}", file=sys.stderr)
        return 2

    findings = validate(config_path, schema)
    if args.json:
        print(json.dumps({"ok": not findings, "config": str(config_path),
                          "schema": str(schema_path), "findings": findings},
                         ensure_ascii=False, indent=2))
    elif findings:
        print("config_schema: INVALID")
        for f in findings:
            print(f)
    else:
        n_keys = len(schema["keys"])
        n_sec = sum(len(s.get("keys", {})) for s in schema["sections"].values())
        print(f"config_schema: ok ({n_keys + n_sec} declared keys validated)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import tomllib
from pathlib import Path
from typing import Any

# ── Config file paths ──────────────────────────────────────────────

SELF_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def state_dir(project: str) -> Path:
    return Path(project) / ".freely"


def config_toml_path(project: str) -> Path:
    return state_dir(project) / "config.toml"


def config_env_path(project: str) -> Path:
    return state_dir(project) / "config.env"


def global_state_dir() -> Path:
    raw = os.environ.get("FREELY_HOME") or os.environ.get("HOME")
    return Path(raw or "~").expanduser() / ".freely"


def global_config_toml_path() -> Path:
    return global_state_dir() / "config.toml"


def global_config_env_path() -> Path:
    return global_state_dir() / "config.env"


# ── Readers ────────────────────────────────────────────────────────


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        key = key.strip()
        raw = raw.strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
            raw = raw[1:-1]
        values[key] = raw
    return values


def read_config_toml(project: str) -> dict[str, Any]:
    path = config_toml_path(project)
    if not path.is_file():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def read_config_from_path(path: str) -> dict[str, Any]:
    p = Path(path)
    if p.suffix == ".toml":
        if not p.is_file():
            return {}
        with p.open("rb") as f:
            return tomllib.load(f)
    return parse_env_file(p)


def read_config(project: str) -> dict[str, Any]:
    toml = read_config_toml(project)
    if toml:
        return toml
    env = parse_env_file(config_env_path(project))
    if env:
        return env
    return {}


# ── Shell export output ────────────────────────────────────────────


def _shell_quote(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def toml_to_env(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                lines.append(f'export {key}_{sub_key}={_shell_quote(sub_value)}')
        else:
            lines.append(f'export {key}={_shell_quote(value)}')
    return "\n".join(lines)


# ── TOML Writer (no tomli_w dependency) ────────────────────────────


def _toml_quote(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def dict_to_toml(data: dict[str, Any], comments: dict[str, str] | None = None) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if comments and key in comments:
            for cl in comments[key].split("\n"):
                lines.append(f"# {cl}")
        if isinstance(value, dict):
            lines.append(f"\n[{key}]")
            for sub_key, sub_value in value.items():
                lines.append(f'{sub_key} = {_toml_quote(sub_value)}')
        else:
            lines.append(f'{key} = {_toml_quote(value)}')
    lines.append("")
    return "\n".join(lines)


def write_config_toml(project: str, data: dict[str, Any]) -> None:
    path = config_toml_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dict_to_toml(data), encoding="utf-8")


def upsert_config_toml(project: str, key: str, value: str) -> None:
    path = config_toml_path(project)
    data: dict[str, Any] = {}
    if path.is_file():
        with path.open("rb") as f:
            data = tomllib.load(f)
    data[key] = value
    write_config_toml(project, data)


# ── Write config.env for backward compat ───────────────────────────


def write_config_env(project: str, data: dict[str, str]) -> None:
    path = config_env_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                lines.append(f'{key}_{sub_key}="{sub_value}"')
        else:
            lines.append(f'{key}="{value}"')
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ── CLI ────────────────────────────────────────────────────────────


def cmd_toml2env(args: argparse.Namespace) -> None:
    if args.file:
        data = read_config_from_path(args.file)
    else:
        data = read_config(args.project)
    if not data:
        sys.exit(1)
    print(toml_to_env(data))


def cmd_init_toml(args: argparse.Namespace) -> None:
    data: dict[str, Any] = {}
    if args.values:
        for item in args.values:
            if "=" not in item:
                continue
            key, val = item.split("=", 1)
            data[key.strip()] = val.strip()
    path = config_toml_path(args.project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dict_to_toml(data), encoding="utf-8")
    print(f"wrote: {path}")


def cmd_upsert(args: argparse.Namespace) -> None:
    upsert_config_toml(args.project, args.key, args.value)
    data = read_config_toml(args.project)
    flat: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(v, dict):
            for sk, sv in v.items():
                flat[f"{k}_{sk}"] = str(sv)
        else:
            flat[k] = str(v)
    if flat:
        write_config_env(args.project, flat)


def cmd_print(args: argparse.Namespace) -> None:
    data = read_config(args.project)
    if not data:
        sys.exit(1)
    for key, value in data.items():
        print(f'{key} = "{value}"')


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freely project configuration manager"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_toml2env = sub.add_parser("toml2env", help="Output config as shell exports")
    p_toml2env.add_argument("--project", default=".", help="Project root path")
    p_toml2env.add_argument(
        "--file", help="Config file path (bypasses project detection)"
    )

    p_init = sub.add_parser("init-toml", help="Generate config.toml")
    p_init.add_argument("--project", default=".", help="Project root path")
    p_init.add_argument(
        "--value", dest="values", action="append", help="KEY=VALUE pairs"
    )

    p_upsert = sub.add_parser("upsert", help="Upsert a config key")
    p_upsert.add_argument("--project", default=".", help="Project root path")
    p_upsert.add_argument("--key", required=True, help="Config key")
    p_upsert.add_argument("--value", required=True, help="Config value")

    p_print = sub.add_parser("print", help="Print config as key=value lines")
    p_print.add_argument("--project", default=".", help="Project root path")

    args = parser.parse_args()

    if args.command == "toml2env":
        cmd_toml2env(args)
    elif args.command == "init-toml":
        cmd_init_toml(args)
    elif args.command == "upsert":
        cmd_upsert(args)
    elif args.command == "print":
        cmd_print(args)


if __name__ == "__main__":
    main()

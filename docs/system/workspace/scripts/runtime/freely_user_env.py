#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path


def user_home() -> Path:
    home = os.environ.get("HOME") or os.environ.get("USERPROFILE") or "~"
    return Path(home).expanduser()


def is_windows() -> bool:
    return os.name == "nt"


def freely_home() -> Path:
    explicit = os.environ.get("FREELY_HOME")
    if explicit:
        return Path(explicit).expanduser()
    return user_home() / ".freely"


def bootstrap_env_file() -> Path:
    return freely_home() / ".env"


def default_credentials_env_candidates() -> list[Path]:
    if is_windows():
        appdata = os.environ.get("APPDATA")
        candidates: list[Path] = []
        if appdata:
            candidates.append(Path(appdata).expanduser() / "Freely" / "credentials.env")
        candidates.append(user_home() / ".freely" / "credentials.env")
        return candidates
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    config_root = (
        Path(xdg_config_home).expanduser()
        if xdg_config_home
        else user_home() / ".config"
    )
    return [
        config_root / "freely" / "credentials.env",
        user_home() / ".freely" / "credentials.env",
    ]


def preferred_credentials_env_file() -> Path:
    return default_credentials_env_candidates()[0]


def shell_value(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        values[key.strip()] = shell_value(raw)
    return values


def configured_env_file() -> Path:
    explicit = os.environ.get("FREELY_ENV_FILE")
    if explicit:
        return Path(explicit).expanduser()
    bootstrap_values = parse_env_file(bootstrap_env_file())
    pointed = bootstrap_values.get("FREELY_ENV_FILE")
    if pointed:
        return Path(pointed).expanduser()
    for candidate in default_credentials_env_candidates():
        if candidate.is_file():
            return candidate
    return preferred_credentials_env_file()


def checked_env_files() -> list[Path]:
    files: list[Path] = []
    explicit = os.environ.get("FREELY_ENV_FILE")
    if explicit:
        files.append(Path(explicit).expanduser())
    files.append(bootstrap_env_file())
    files.extend(default_credentials_env_candidates())
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in files:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)
    return deduped


def value(*keys: str) -> str | None:
    for key in keys:
        current = os.environ.get(key)
        if current:
            return current
    file_values = parse_env_file(configured_env_file())
    for key in keys:
        current = file_values.get(key)
        if current:
            return current
    return None


def path_hint() -> str:
    return str(configured_env_file())


def bootstrap_path_hint() -> str:
    return str(bootstrap_env_file())


def default_path_hint() -> str:
    return str(preferred_credentials_env_file())


def checked_paths_hint() -> str:
    return ", ".join(str(path) for path in checked_env_files())

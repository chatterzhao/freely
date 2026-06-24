#!/usr/bin/env python3
"""Tool registry query helper. Reads tool-registry.toml (or .json5) and outputs values for bash.

Usage:
  python3 tool-registry-query.py <registry-path> <tool> dot.path.to.field
  python3 tool-registry-query.py <registry-path> <tool> --keys  (list top-level keys)
  python3 tool-registry-query.py <registry-path> --list          (list all tool names)

File priority:
  If <registry-path> is a .toml file, also checks ~/.freely/tool-registry.toml.
  User keys override system keys (shallow merge per tool section).

Examples:
  python3 tool-registry-query.py tool-registry.toml codex acp.binary
  # → codex-acp

  python3 tool-registry-query.py tool-registry.toml opencode permission.mechanism
  # → env_var
"""

import os
import re
import sys


def _strip_json5(text: str) -> str:
    """Strip // line comments and /* block comments */ from JSON5 text."""
    result = []
    in_string = False
    in_block = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape:
            result.append(ch)
            escape = False
            i += 1
            continue
        if ch == '\\' and in_string:
            result.append(ch)
            escape = True
            i += 1
            continue
        if ch == '"' and not in_block:
            in_string = not in_string
            result.append(ch)
            i += 1
            continue
        if not in_string and not in_block and ch == '/' and i + 1 < len(text) and text[i + 1] == '/':
            i += 2
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
        if not in_string and not in_block and ch == '/' and i + 1 < len(text) and text[i + 1] == '*':
            in_block = True
            i += 2
            continue
        if in_block and ch == '*' and i + 1 < len(text) and text[i + 1] == '/':
            in_block = False
            i += 2
            continue
        if in_block:
            i += 1
            continue
        result.append(ch)
        i += 1

    text = ''.join(result)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text


def _load_toml(path: str) -> dict:
    """Load a TOML file, returning dict of tool sections."""
    import tomllib
    with open(path, 'rb') as f:
        return tomllib.load(f)


def _load_json5(path: str) -> dict:
    """Load a JSON5 file, returning dict of tool sections."""
    import json
    with open(path) as f:
        return json.loads(_strip_json5(f.read()))


def _load_registry(path: str) -> dict:
    """Load registry from path, auto-detecting format (.toml vs .json5)."""
    if path.endswith('.toml'):
        return _load_toml(path)
    else:
        return _load_json5(path)


def _merge_registries(system: dict, user: dict) -> dict:
    """Merge user registry over system registry. User tool keys override system."""
    merged = dict(system)
    for key, value in user.items():
        if key.startswith('_'):
            continue
        merged[key] = value  # user overrides entire tool section
    return merged


def _resolve_registry(registry_path: str) -> dict:
    """Load registry with file priority: ~/.freely/tool-registry.toml > system."""
    data = _load_registry(registry_path)

    # Check for user override: ~/.freely/tool-registry.toml
    user_path = os.path.expanduser("~/.freely/tool-registry.toml")
    if os.path.isfile(user_path) and registry_path.endswith('.toml'):
        try:
            user_data = _load_toml(user_path)
            data = _merge_registries(data, user_data)
        except Exception:
            pass  # user file corrupt → use system only

    return data


def _get(obj, path: str):
    """Get nested dict value by dot path."""
    parts = path.split(".")
    for part in parts:
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            return None
    return obj


def main():
    if len(sys.argv) < 2:
        print("Usage: tool-registry-query.py <registry> <tool> [field] | --list | <tool> --keys", file=sys.stderr)
        sys.exit(1)

    registry_path = sys.argv[1]
    if not os.path.isfile(registry_path):
        print(f"ERROR: registry file not found: {registry_path}", file=sys.stderr)
        sys.exit(1)

    data = _resolve_registry(registry_path)

    if len(sys.argv) == 3 and sys.argv[2] == "--list":
        for name in sorted(data):
            if not name.startswith("_"):
                print(name)
        return

    tool = sys.argv[2]

    # Resolve alias
    if tool in data.get("_aliases", {}):
        tool = data["_aliases"][tool]

    if tool not in data:
        print(f"ERROR: tool '{tool}' not in registry", file=sys.stderr)
        sys.exit(1)

    tool_data = data[tool]

    if len(sys.argv) == 4 and sys.argv[3] == "--keys":
        for k in sorted(tool_data):
            print(k)
        return

    if len(sys.argv) >= 4:
        field = sys.argv[3]
        value = _get(tool_data, field)

        if isinstance(value, bool):
            print("true" if value else "false")
        elif isinstance(value, list):
            print(" ".join(str(v) for v in value))
        elif value is None:
            print("")
            sys.exit(1)
        else:
            print(value)
    else:
        import json
        print(json.dumps(tool_data, indent=2))


if __name__ == "__main__":
    main()

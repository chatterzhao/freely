#!/usr/bin/env python3
"""Tool registry query helper. Reads tool-registry.json5 and outputs values for bash.

Usage:
  python3 tool-registry-query.py <registry-path> <tool> dot.path.to.field
  python3 tool-registry-query.py <registry-path> <tool> --keys  (list top-level keys)
  python3 tool-registry-query.py <registry-path> --list          (list all tool names)

Examples:
  python3 tool-registry-query.py tool-registry.json5 codex acp.binary
  # → codex-acp

  python3 tool-registry-query.py tool-registry.json5 opencode permission.mechanism
  # → env_var
"""

import re
import sys


def _strip_json5(text: str) -> str:
    """Strip // line comments and /* block comments */ from JSON5 text.
    Also strip trailing commas before ] and }."""
    # Remove // line comments (not inside strings)
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

    # Strip trailing commas before ] and }
    text = ''.join(result)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text


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

    import json
    registry_path = sys.argv[1]

    with open(registry_path) as f:
        text = f.read()

    data = json.loads(_strip_json5(text))

    if len(sys.argv) == 3 and sys.argv[2] == "--list":
        # List all tool names (excluding _aliases)
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
        print(json.dumps(tool_data, indent=2))


if __name__ == "__main__":
    main()

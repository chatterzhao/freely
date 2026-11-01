#!/usr/bin/env python3
"""Report configured agent harnesses, their capabilities, and recent cache telemetry.

This is the first concrete HarnessPort slice: it does not start or route agent
sessions. It answers the operational questions the comparison study surfaced:
which harness does each role use, what can that harness actually do, and is the
prompt cache being observed rather than assumed?
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tomllib
from pathlib import Path

# Capabilities are deliberately conservative: a missing entry means "unknown or
# unsupported", never "supported by accident". Keep this table next to the ACP
# adapter code when an adapter gains a capability.
CAPABILITIES = {
    "claude": {
        "session_new": True, "resume": True, "fork": True, "stream": True,
        "interrupt": True, "tools": True, "skills": True, "usage": True,
        "cache": True, "subagent": True, "mcp": True,
    },
    "codex": {
        "session_new": True, "resume": True, "fork": False, "stream": True,
        "interrupt": True, "tools": True, "skills": True, "usage": True,
        "cache": False, "subagent": False, "mcp": True,
    },
    "opencode": {
        "session_new": True, "resume": True, "fork": True, "stream": True,
        "interrupt": True, "tools": True, "skills": True, "usage": True,
        "cache": False, "subagent": False, "mcp": True,
    },
    "cline": {
        "session_new": True, "resume": True, "fork": False, "stream": True,
        "interrupt": True, "tools": True, "skills": True, "usage": False,
        "cache": False, "subagent": False, "mcp": True,
    },
    "dsh": {
        # The prototype is a Cordis bundle, not an ACP agent. An adapter is
        # required before Freely can select DSH as a harness.
        "session_new": False, "resume": False, "fork": False, "stream": False,
        "interrupt": False, "tools": False, "skills": False, "usage": False,
        "cache": False, "subagent": False, "mcp": False,
    },
}
ALIASES = {
    "cc": "claude", "claude": "claude", "kiro-cli": "claude", "iflow": "claude",
    "codex": "codex", "opencode": "opencode", "cline": "cline",
    "dsh": "dsh", "deepseek": "dsh", "deepseek-harness": "dsh",
}
BIN_KEYS = {
    "claude": "FREELY_ACP_CLAUDE_BIN",
    "codex": "FREELY_ACP_CODEX_BIN",
    "opencode": "FREELY_ACP_OPENCODE_BIN",
    "cline": "FREELY_ACP_CLINE_BIN",
}
CACHE_RE = re.compile(
    r"\[CACHE\].*?launch_kind=(\S+).*?prompt_bytes=(\d+).*?input=(\d+).*?cache_hit=(\d+).*?cache_miss=(\d+)"
)


def load_toml(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except Exception:
        return {}


def read_config(project: Path) -> dict:
    return load_toml(project / ".freely" / "config.toml")


def infer_tool(slot: str) -> str:
    head = re.split(r"-(?:apikey|account)-", slot, maxsplit=1)[0].strip().lower()
    if not head:
        return "unknown"
    for alias, tool in ALIASES.items():
        if head == alias or head.startswith(alias + "-"):
            return tool
    return head


def read_roles(project: Path, warnings: list[str]) -> list[dict]:
    table = load_toml(project / ".freely" / "agent-table.toml")
    agents = table.get("agents")
    if not isinstance(agents, list):
        warnings.append("agent-table missing or has no [[agents]]; role harnesses unknown")
        return []
    roles = []
    for entry in agents:
        if not isinstance(entry, dict):
            continue
        role = str(entry.get("role", "")).strip()
        if not role:
            continue
        agent_id = str(entry.get(f"{role}_id", "")).strip()
        slot = str(entry.get(f"{role}_slot", "")).strip()
        if not slot:
            continue
        roles.append({
            "role": role,
            "id": agent_id or f"{role}_?",
            "slot": slot,
            "tool": infer_tool(slot),
            "pool": entry.get("pool"),
        })
    if not roles:
        warnings.append("agent-table has no usable role/slot rows")
    return roles


def resolve_binary(tool: str, config: dict) -> str:
    configured = str(config.get(BIN_KEYS.get(tool, ""), "") or "").strip()
    if configured:
        return configured
    for candidate in (tool, tool.replace("-", "")):
        found = shutil.which(candidate)
        if found:
            return found
    return ""


def binary_status(path: str) -> str:
    if not path:
        return "missing"
    if os.path.isfile(path) and os.access(path, os.X_OK):
        return "ok"
    return "missing"


def enrich_role(role: dict, config: dict, warnings: list[str]) -> dict:
    tool = role["tool"]
    known = tool in CAPABILITIES
    capabilities = dict(CAPABILITIES.get(tool, {}))
    binary = resolve_binary(tool, config) if known else ""
    status = binary_status(binary) if known else "not_applicable"
    if not known:
        warnings.append(f"unknown adapter '{tool}' for {role['role']} ({role['id']}); capabilities unknown")
    elif status != "ok":
        warnings.append(f"harness binary missing for {role['role']} ({role['id']}): {tool}")
    return {**role, "known": known, "capabilities": capabilities, "binary": binary, "binary_status": status}


def cache_summary(project: Path, window: int) -> dict:
    log_dir = project / ".freely" / "logs"
    files = []
    if log_dir.is_dir():
        for path in log_dir.glob("cycle-*.log"):
            if path.name.endswith(".debug.log"):
                continue
            files.append(path)
    files.sort(key=lambda p: p.stat().st_mtime)
    files = files[-window:] if window > 0 else files
    total = {"lines": 0, "entries": 0, "input": 0, "hit": 0, "miss": 0, "by_kind": {}}
    for path in files:
        previous = None
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            match = CACHE_RE.search(line)
            if not match:
                continue
            total["lines"] += 1
            if line == previous:
                continue
            previous = line
            kind, prompt_bytes, input_tokens, hit, miss = match.groups()
            kind_data = total["by_kind"].setdefault(
                kind, {"entries": 0, "input": 0, "hit": 0, "miss": 0}
            )
            for key, value in (("entries", 1), ("input", int(input_tokens)), ("hit", int(hit)), ("miss", int(miss))):
                total[key] += value
                kind_data[key] += value
    denominator = total["hit"] + total["miss"]
    total["hit_rate"] = round(total["hit"] / denominator, 4) if denominator else None
    total["files"] = len(files)
    total["reported"] = denominator > 0
    return total


def check_required(roles: list[dict], required: list[str]) -> dict:
    missing = []
    for role in roles:
        for capability in required:
            if not role["capabilities"].get(capability):
                missing.append({"role": role["role"], "id": role["id"], "capability": capability})
    return {"capabilities": required, "status": "fail" if missing else "pass", "missing": missing}


def render_text(data: dict) -> str:
    lines = [f"Harness status: {data['project']}", f"adapter: {data['adapter'] or '(unset)'}", ""]
    if data["roles"]:
        lines.append("roles:")
        for role in data["roles"]:
            caps = role["capabilities"]
            present = ",".join(name for name, value in caps.items() if value) or "none"
            lines.append(
                f"  {role['role']:<8} {role['id']:<12} tool={role['tool']:<8} pool={role['pool']} "
                f"binary={role['binary_status']} caps={present}"
            )
    else:
        lines.append("roles: (none)")
    cache = data["cache"]
    rate = "unknown" if cache["hit_rate"] is None else f"{cache['hit_rate'] * 100:.1f}%"
    lines += [
        "",
        f"cache: files={cache['files']} lines={cache['lines']} entries={cache['entries']} "
        f"hit={cache['hit']} miss={cache['miss']} hit_rate={rate}",
    ]
    for kind, values in sorted(cache["by_kind"].items()):
        lines.append(f"  {kind}: entries={values['entries']} hit={values['hit']} miss={values['miss']}")
    if data["required"]["capabilities"]:
        lines += ["", f"required {','.join(data['required']['capabilities'])}: {data['required']['status']}"]
        for item in data["required"]["missing"]:
            lines.append(f"  missing: {item['role']} ({item['id']}) lacks {item['capability']}")
    if data["warnings"]:
        lines += ["", "warnings:"] + [f"  - {warning}" for warning in data["warnings"]]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report agent harness capabilities and cache telemetry.")
    parser.add_argument("--project", default="", help="Project root (default: current directory).")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--require", default="", help="Comma-separated capabilities every role must support.")
    parser.add_argument("--cache-window", type=int, default=50, help="Recent cycle logs to inspect (default 50).")
    parser.add_argument("--strict", action="store_true", help="Exit 3 when a configured binary is missing.")
    args = parser.parse_args()

    project = Path(args.project or os.getcwd()).resolve()
    warnings: list[str] = []
    config = read_config(project)
    if not config:
        warnings.append("config.toml missing or unreadable; using defaults")
    adapter = str(config.get("AGENT_AI_TOOL_ADAPTER", "") or "").strip()
    roles = [enrich_role(role, config, warnings) for role in read_roles(project, warnings)]
    required = [item.strip() for item in args.require.split(",") if item.strip()]
    data = {
        "project": str(project),
        "adapter": adapter,
        "roles": roles,
        "cache": cache_summary(project, args.cache_window),
        "required": check_required(roles, required),
        "warnings": warnings,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else render_text(data))
    if data["required"]["status"] == "fail":
        return 3
    if args.strict and any(role["binary_status"] == "missing" for role in roles):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

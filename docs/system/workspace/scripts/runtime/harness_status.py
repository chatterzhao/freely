#!/usr/bin/env python3
"""Report configured agent harnesses, their capabilities, and cache telemetry.

P0 HarnessPort slice: read-only. It does not start sessions. It answers:
which harness does each role use, can the ACP binary actually be found, what
does the registry declare, and is cache data reported or only estimated?
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

REPO_ROOT = Path(__file__).resolve().parents[5]
REGISTRY_PATH = REPO_ROOT / "docs" / "system" / "workspace" / "tools" / "tool-registry.toml"
# run-acp-prompt.py tries session/fork for every ACP tool and degrades to
# session/new when the tool rejects it. The registry declares fork support, but
# codex/cline are known to take the degraded path.
FORK_MODE = {"claude": "native", "opencode": "native", "codex": "degraded", "cline": "degraded"}
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


def load_registry() -> dict:
    return load_toml(REGISTRY_PATH)


def registry_tool(registry: dict, tool: str) -> dict:
    entry = registry.get(tool)
    return entry if isinstance(entry, dict) else {}


def infer_tool(slot: str, registry: dict) -> str:
    head = re.split(r"-(?:apikey|account)-", slot, maxsplit=1)[0].strip().lower()
    if not head:
        return "unknown"
    for name, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        aliases = [str(item).lower() for item in entry.get("aliases", [])]
        if head == name.lower() or head in aliases:
            return name.lower()
        if any(head.startswith(alias + "-") for alias in aliases + [name.lower()]):
            return name.lower()
    return head


def read_roles(project: Path, registry: dict, warnings: list[str]) -> list[dict]:
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
        slot = str(entry.get(f"{role}_slot", "")).strip()
        if not slot:
            continue
        roles.append({
            "role": role,
            "id": str(entry.get(f"{role}_id", "")).strip() or f"{role}_?",
            "slot": slot,
            "tool": infer_tool(slot, registry),
            "pool": entry.get("pool"),
        })
    if not roles:
        warnings.append("agent-table has no usable role/slot rows")
    return roles


def capabilities_for(tool: str, entry: dict) -> dict:
    acp = entry.get("acp") if isinstance(entry.get("acp"), dict) else {}
    adapters = entry.get("adapters") if isinstance(entry.get("adapters"), dict) else {}
    launch = adapters.get("launch_kinds", {}).get("acp", "") if isinstance(adapters.get("launch_kinds"), dict) else ""
    kinds = {item.strip() for item in str(launch).split(",") if item.strip()}
    session = entry.get("session") if isinstance(entry.get("session"), dict) else {}
    if not acp:
        return {}
    return {
        "session_new": "fresh" in kinds,
        "resume": "resume" in kinds and bool(session.get("supports_resume", True)),
        "fork": FORK_MODE.get(tool, "degraded" if "fork" in kinds else False),
        "stream": True,
        "interrupt": True,
        "tools": True,
        "skills": True,
        # Provider usage is not guaranteed. The runtime estimates input from
        # prompt bytes when usage is absent, so these must stay "unknown".
        "usage": "unknown",
        "cache": "unknown",
        "subagent": "unknown",
        "mcp": "unknown",
    }


def cache_candidates(tool: str, binary_name: str) -> list[Path]:
    root = Path.home() / ".cache" / "freely" / "acp" / tool
    if not root.is_dir():
        return []
    return sorted(root.glob(f"**/{binary_name}"))


def resolve_binary(tool: str, entry: dict, config: dict) -> tuple[str, str]:
    rc_key = f"FREELY_ACP_{tool.upper()}_BIN"
    configured = str(config.get(rc_key, "") or "").strip()
    acp = entry.get("acp") if isinstance(entry.get("acp"), dict) else {}
    binary_name = str(acp.get("binary", "") or tool)
    if configured:
        return (configured, "ok" if os.path.isfile(configured) and os.access(configured, os.X_OK) else "missing")
    found = shutil.which(binary_name)
    if found:
        return (found, "ok")
    cached = cache_candidates(tool, binary_name)
    if cached:
        return (str(cached[0]), "ok")
    direct = shutil.which(tool)
    if direct:
        return (direct, "direct-only")
    return ("", "missing")


def enrich_role(role: dict, registry: dict, config: dict, warnings: list[str]) -> dict:
    tool = role["tool"]
    entry = registry_tool(registry, tool)
    known = bool(entry)
    capabilities = capabilities_for(tool, entry) if known else {}
    binary, status = resolve_binary(tool, entry, config) if known else ("", "not_applicable")
    if not known:
        warnings.append(f"unknown adapter '{tool}' for {role['role']} ({role['id']}); capabilities unknown")
    elif status == "missing":
        warnings.append(f"ACP binary missing for {role['role']} ({role['id']}): {entry.get('acp', {}).get('binary', tool)}")
    elif status == "direct-only":
        warnings.append(f"{role['role']} ({role['id']}) resolves only the direct CLI '{tool}', not its ACP binary")
    return {**role, "known": known, "capabilities": capabilities, "binary": binary, "binary_status": status}


def cache_summary(project: Path, window: int) -> dict:
    log_dir = project / ".freely" / "logs"
    files = []
    if log_dir.is_dir():
        files = [p for p in log_dir.glob("cycle-*.log") if not p.name.endswith(".debug.log")]
    files.sort(key=lambda p: p.stat().st_mtime)
    files = files[-window:] if window > 0 else files
    total = {
        "files": len(files), "lines": 0, "entries": 0, "prompt_bytes": 0,
        "input": 0, "hit": 0, "miss": 0, "estimated": 0, "usage_entries": 0, "estimated_entries": 0,
        "by_kind": {},
    }
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
            prompt_bytes, input_tokens, hit, miss = int(prompt_bytes), int(input_tokens), int(hit), int(miss)
            estimated = input_tokens == prompt_bytes // 4
            kind_data = total["by_kind"].setdefault(
                kind, {"entries": 0, "prompt_bytes": 0, "input": 0, "hit": 0, "miss": 0, "estimated": 0}
            )
            for key, value in (
                ("entries", 1), ("prompt_bytes", prompt_bytes), ("input", input_tokens),
                ("hit", hit), ("miss", miss), ("estimated", 1 if estimated else 0),
            ):
                total[key] += value
                kind_data[key] += value
            if estimated:
                total["estimated_entries"] += 1
            else:
                total["usage_entries"] += 1
    denominator = total["hit"] + total["miss"]
    total["hit_rate"] = round(total["hit"] / denominator, 4) if denominator else None
    total["cache_reported"] = denominator > 0
    total["input_source"] = "usage" if total["usage_entries"] else ("estimated" if total["estimated_entries"] else "none")
    return total


def satisfies(value: object) -> bool:
    return value is True or value == "native"


def check_required(roles: list[dict], required: list[str]) -> dict:
    missing = []
    if required and not roles:
        for capability in required:
            missing.append({"role": "*", "id": "*", "capability": capability, "reason": "no_roles"})
    for role in roles:
        for capability in required:
            value = role["capabilities"].get(capability)
            if satisfies(value):
                continue
            if not role["known"]:
                reason = "unknown_adapter"
            elif value == "degraded":
                reason = "degraded"
            elif value is None or value == "unknown":
                reason = "unknown_or_not_probed"
            else:
                reason = "unsupported"
            missing.append({"role": role["role"], "id": role["id"], "capability": capability, "reason": reason})
    return {"capabilities": required, "status": "fail" if missing else "pass", "missing": missing}


def render_text(data: dict) -> str:
    lines = [f"Harness status: {data['project']}", f"adapter: {data['adapter'] or '(unset)'}", ""]
    if data["roles"]:
        lines.append("roles:")
        for role in data["roles"]:
            caps = role["capabilities"]
            present = ",".join(name for name, value in caps.items() if value is True or value == "native") or "none"
            degraded = ",".join(name for name, value in caps.items() if value == "degraded")
            lines.append(
                f"  {role['role']:<8} {role['id']:<12} tool={role['tool']:<8} pool={role['pool']} "
                f"binary={role['binary_status']} caps={present}"
                + (f" degraded={degraded}" if degraded else "")
            )
    else:
        lines.append("roles: (none)")
    cache = data["cache"]
    rate = "unknown" if cache["hit_rate"] is None else f"{cache['hit_rate'] * 100:.1f}%"
    lines += [
        "",
        f"cache: files={cache['files']} lines={cache['lines']} entries={cache['entries']} "
        f"hit={cache['hit']} miss={cache['miss']} hit_rate={rate} input_source={cache['input_source']}",
    ]
    for kind, values in sorted(cache["by_kind"].items()):
        lines.append(
            f"  {kind}: entries={values['entries']} hit={values['hit']} miss={values['miss']} estimated={values['estimated']}"
        )
    if data["required"]["capabilities"]:
        lines += ["", f"required {','.join(data['required']['capabilities'])}: {data['required']['status']}"]
        for item in data["required"]["missing"]:
            lines.append(f"  missing: {item['role']} ({item['id']}) lacks {item['capability']} [{item['reason']}]")
    if data["warnings"]:
        lines += ["", "warnings:"] + [f"  - {warning}" for warning in data["warnings"]]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report agent harness capabilities and cache telemetry.",
        epilog="Exit codes: 0 ok, 1 usage, 3 required capability/strict binary check failed.",
    )
    parser.add_argument("--project", default="", help="Project root (default: current directory).")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--require", default="", help="Comma-separated capabilities every role must support; exits 3 on failure.")
    parser.add_argument("--cache-window", type=int, default=50, help="Recent cycle logs to inspect (default 50).")
    parser.add_argument("--strict", action="store_true", help="Exit 3 when a configured harness is unknown, missing, or direct-only.")
    args = parser.parse_args()

    project = Path(args.project or os.getcwd()).resolve()
    registry = load_registry()
    if not registry:
        print(f"tool registry missing: {REGISTRY_PATH}", file=sys.stderr)
        return 2
    warnings: list[str] = []
    config = load_toml(project / ".freely" / "config.toml")
    if not config:
        warnings.append("config.toml missing or unreadable; using defaults")
    adapter = str(config.get("AGENT_AI_TOOL_ADAPTER", "") or "").strip()
    roles = [enrich_role(role, registry, config, warnings) for role in read_roles(project, registry, warnings)]
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
    if args.strict and any(role["binary_status"] in {"missing", "direct-only", "not_applicable"} for role in roles):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

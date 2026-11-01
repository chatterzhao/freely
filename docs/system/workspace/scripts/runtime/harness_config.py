#!/usr/bin/env python3
"""Role-level harness configuration: validate and atomically apply {role}_slot."""
from __future__ import annotations

import json
import os
import re
import shutil
import time
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
REGISTRY_PATH = REPO_ROOT / "docs" / "system" / "workspace" / "tools" / "tool-registry.toml"
REQUIREMENTS = {
    "manager": ["resume", "tools", "skills"],
    "worker": ["session_new", "tools", "skills"],
    "reviewer": ["resume", "tools", "skills"],
}


def _toml(path: Path) -> dict:
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except Exception:
        return {}


def _registry() -> dict:
    return _toml(REGISTRY_PATH)


def _tool(slot: str, registry: dict) -> str:
    head = re.split(r"-(?:apikey|account)-", slot, maxsplit=1)[0].strip().lower()
    for name, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        aliases = [str(x).lower() for x in entry.get("aliases", [])]
        if head == name.lower() or head in aliases or any(head.startswith(a + "-") for a in aliases + [name.lower()]):
            return name.lower()
    return head


def _roles(project: Path) -> list[dict]:
    table = _toml(project / ".freely" / "agent-table.toml")
    out = []
    for row in table.get("agents", []) or []:
        if not isinstance(row, dict):
            continue
        role = str(row.get("role", "")).strip()
        slot = str(row.get(f"{role}_slot", "")).strip()
        if role and slot:
            out.append({"role": role, "slot": slot, "id": str(row.get(f"{role}_id", ""))})
    return out


def _capabilities(tool: str, registry: dict) -> dict:
    entry = registry.get(tool, {}) if isinstance(registry.get(tool), dict) else {}
    if not entry:
        return {}
    acp = entry.get("acp") if isinstance(entry.get("acp"), dict) else {}
    adapters = entry.get("adapters") if isinstance(entry.get("adapters"), dict) else {}
    launch = str(adapters.get("launch_kinds", {}).get("acp", "")) if isinstance(adapters.get("launch_kinds"), dict) else ""
    kinds = {x.strip() for x in launch.split(",") if x.strip()}
    fork = {"claude": "native", "opencode": "native", "codex": "degraded", "cline": "degraded"}.get(tool, "degraded" if "fork" in kinds else "unsupported")
    return {"session_new": "fresh" in kinds, "resume": "resume" in kinds, "fork": fork,
            "tools": True, "skills": True, "usage": "unknown", "cache": "unknown", "mcp": "unknown"}


def _health(project: Path, tool: str, registry: dict) -> dict:
    config = _toml(project / ".freely" / "config.toml")
    key = f"FREELY_ACP_{tool.upper()}_BIN"
    configured = str(config.get(key, "") or "").strip()
    entry = registry.get(tool, {}) if isinstance(registry.get(tool), dict) else {}
    binary_name = str((entry.get("acp") or {}).get("binary") or tool)
    binary = configured or shutil.which(binary_name) or ""
    ok = bool(binary and os.path.isfile(binary) and os.access(binary, os.X_OK))
    return {"ok": ok, "binary": binary or None, "acp": bool(entry.get("acp")), "error": None if ok else "binary missing"}


def validate(project: str | Path, role: str, slot: str) -> dict:
    project = Path(project)
    registry = _registry()
    role = str(role or "").strip()
    slot = str(slot or "").strip()
    errors = []
    if role not in REQUIREMENTS:
        errors.append(f"unknown role: {role}")
    if not slot:
        errors.append("slot required")
    row = next((r for r in _roles(project) if r["role"] == role), None)
    if not row:
        errors.append(f"role not configured: {role}")
    tool = _tool(slot, registry) if slot else ""
    caps = _capabilities(tool, registry) if tool else {}
    health = _health(project, tool, registry) if tool else {"ok": False, "binary": None, "acp": False, "error": "tool unknown"}
    if tool and not caps:
        errors.append(f"unknown tool: {tool}")
    if not health.get("acp"):
        errors.append(f"tool has no ACP adapter: {tool}")
    if not health.get("ok"):
        errors.append(f"binary missing: {tool}")
    required = REQUIREMENTS.get(role, [])
    satisfied = True
    degraded = []
    for cap in required:
        value = caps.get(cap)
        if value in (True, "native"):
            continue
        if value == "degraded":
            degraded.append(cap)
            continue
        satisfied = False
        errors.append(f"missing required capability: {cap}")
    for cap, value in caps.items():
        if value == "degraded" and cap not in degraded:
            degraded.append(cap)
    return {"ok": not errors, "role": role, "slot": slot, "tool": tool,
            "capabilities": caps, "health": health, "requirements": required,
            "satisfied": satisfied, "degraded": degraded, "errors": errors}


def apply(project: str | Path, role: str, slot: str) -> dict:
    project = Path(project)
    result = validate(project, role, slot)
    if not result["ok"]:
        return {**result, "applied": False}
    path = project / ".freely" / "agent-table.toml"
    before = path.read_text(encoding="utf-8")
    pattern = re.compile(rf'^(\s*{re.escape(role)}_slot\s*=\s*)["\'][^"\']*["\']', re.MULTILINE)
    if not pattern.search(before):
        return {**result, "ok": False, "applied": False, "errors": result["errors"] + ["slot line not found"]}
    after = pattern.sub(lambda m: f'{m.group(1)}"{slot}"', before, count=1)
    backup = path.with_name(f"agent-table.toml.bak-{int(time.time())}")
    backup.write_text(before, encoding="utf-8")
    tmp = path.with_suffix(".toml.tmp")
    tmp.write_text(after, encoding="utf-8")
    tmp.replace(path)
    reread = validate(project, role, slot)
    audit_id = f"HC-{int(time.time() * 1000)}"
    audit = project / ".freely" / "run" / "harness-config-audit.jsonl"
    audit.parent.mkdir(parents=True, exist_ok=True)
    with audit.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"audit_id": audit_id, "role": role, "slot": slot, "tool": result["tool"], "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    return {**reread, "ok": reread["ok"], "applied": reread["ok"], "audit_id": audit_id,
            "diff": {f"{role}_slot": [result["slot"], slot]}, "requires_restart": [role],
            "backup": str(backup)}

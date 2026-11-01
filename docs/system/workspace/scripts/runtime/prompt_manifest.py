#!/usr/bin/env python3
"""Prompt segment manifest and prefix/cache telemetry."""
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path

SEGMENTS = [
    ("agent_role", "stable"), ("bootstrap", "stable"), ("fleet", "semi"),
    ("exit_contract", "stable"), ("scan", "dynamic"), ("chat", "dynamic"),
    ("continuation", "dynamic"), ("context_warning", "dynamic"),
    ("checkpoint", "dynamic"), ("thread_history", "dynamic"), ("session_handoff", "dynamic"),
]
KIND = dict(SEGMENTS)
MARKER = re.compile(r"<!--\s*FREELY_SEGMENT:([a-z_]+)\s*-->")


def split_prompt(text: str) -> list[dict]:
    matches = list(MARKER.finditer(text))
    if not matches:
        return [{"name": "full_prompt", "kind": "dynamic", "text": text}]
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        name = m.group(1)
        out.append({"name": name, "kind": KIND.get(name, "dynamic"), "text": text[m.end():end].strip()})
    return out


def build_manifest(text: str) -> dict:
    segments = []
    for seg in split_prompt(text):
        body = seg["text"].encode()
        segments.append({"name": seg["name"], "kind": seg["kind"], "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest()})
    prefix = [s for s in segments if s["kind"] in {"stable", "semi"}][:4]
    prefix_hash = hashlib.sha256("|".join(s["sha256"] for s in prefix).encode()).hexdigest() if prefix else None
    return {"segments": segments, "prefix_hash": prefix_hash, "segment_count": len(segments)}


def hit_rate(source: str, hit: int, miss: int):
    if source != "reported":
        return None
    total = int(hit or 0) + int(miss or 0)
    return (int(hit) / total) if total else None


def record_manifest(project: str | Path, text: str, role: str = "", session_id: str = "") -> dict:
    manifest = build_manifest(text)
    manifest.update({"role": role, "session_id": session_id,
                     "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    path = Path(project) / ".freely" / "run" / "prompt-manifest.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(manifest, ensure_ascii=False) + "\n")
    return {"recorded": True, "path": str(path), "manifest": manifest}

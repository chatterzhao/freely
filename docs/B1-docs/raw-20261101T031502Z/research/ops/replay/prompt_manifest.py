#!/usr/bin/env python3
"""C-C research replay: stable prefix hash + usage/cache three-state."""
import hashlib
import json

SEGMENTS = [
    ("agent_role", "stable", "role definition"),
    ("bootstrap", "stable", "intent/constitution paths + task"),
    ("fleet", "semi", "worktree/branch status"),
    ("exit_contract", "stable", "exit contract"),
    ("scan", "dynamic", "scan summary"),
    ("chat", "dynamic", "unconsumed chats"),
    ("continuation", "dynamic", "continuation"),
    ("context_warning", "dynamic", "context warning"),
    ("checkpoint", "dynamic", "checkpoint"),
    ("thread_history", "dynamic", "manager only"),
    ("session_handoff", "dynamic", "handoff"),
]


def manifest(tail_suffix: str):
    rows = []
    for name, kind, text in SEGMENTS:
        body = text + (tail_suffix if kind == "dynamic" else "")
        rows.append({"name": name, "kind": kind, "bytes": len(body.encode()),
                     "sha256": hashlib.sha256(body.encode()).hexdigest()})
    prefix = [r for r in rows if r["kind"] in {"stable", "semi"}]
    prefix_bytes = "|".join(r["sha256"] for r in prefix).encode()
    return {"segments": rows, "prefix_hash": hashlib.sha256(prefix_bytes).hexdigest()}


def cache_state(usage_source, cache_source, hit, miss):
    if usage_source != "reported" or cache_source != "reported":
        return {"hit_rate": None, "reason": "unknown: source is not reported"}
    if hit + miss == 0:
        return {"hit_rate": None, "reason": "no tokens"}
    return {"hit_rate": hit / (hit + miss), "reason": "reported"}


def main():
    a = manifest("A")
    b = manifest("B")
    out = {
        "prefix_hash_a": a["prefix_hash"],
        "prefix_hash_b": b["prefix_hash"],
        "prefix_stable": a["prefix_hash"] == b["prefix_hash"],
        "segments": len(a["segments"]),
        "stable_prefix_segments": [r["name"] for r in a["segments"] if r["kind"] in {"stable", "semi"}],
        "cache_reported": cache_state("reported", "reported", 80, 20),
        "cache_estimated": cache_state("estimated", "estimated", 0, 0),
        "cache_absent": cache_state("absent", "absent", 0, 0),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    assert out["prefix_stable"]
    assert out["cache_reported"]["hit_rate"] == 0.8
    assert out["cache_estimated"]["hit_rate"] is None
    assert out["cache_absent"]["hit_rate"] is None
    print("prompt manifest replay: OK")


if __name__ == "__main__":
    main()

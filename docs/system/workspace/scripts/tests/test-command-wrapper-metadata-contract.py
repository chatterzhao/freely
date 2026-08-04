#!/usr/bin/env python3
"""Command-wrapper metadata lifecycle contract validation."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
CONTRACT = ROOT / "docs/system/workspace/command-wrapper-metadata-lifecycle.md"

REQUIRED_SECTIONS = [
    "## Owner",
    "## Phase",
    "## Freshness",
    "## Rejection",
    "## Evidence",
]

REQUIRED_FIELDS = [
    "platform_ids",
    "phase_state",
    "last_synced_comment_at",
    "hash",
    "session_refs",
]


def main():
    if not CONTRACT.exists():
        print(f"FAIL: contract doc missing: {CONTRACT}")
        return 1
    text = CONTRACT.read_text(encoding="utf-8")
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in text]
    if missing_sections:
        print(f"FAIL: missing sections: {missing_sections}")
        return 1
    missing_fields = [f for f in REQUIRED_FIELDS if f not in text]
    if missing_fields:
        print(f"FAIL: missing field references: {missing_fields}")
        return 1
    print("OK (5 sections; fields referenced)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

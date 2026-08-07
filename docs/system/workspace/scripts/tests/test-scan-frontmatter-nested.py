#!/usr/bin/env python3
"""scan parse_frontmatter must resolve nested YAML (platform_ids) for strict raw issues."""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "docs/system/workspace/scripts/lifecycle"))
sys.path.insert(0, str(ROOT / "docs/system/workspace/scripts/runtime"))
from raw_metadata_contract import RAW_METADATA_FIELDS, validate

spec = importlib.util.spec_from_file_location(
    "tls", ROOT / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


def main():
    sample = ROOT / "docs/B1-docs/raw-20260804T073054Z/issue.md"
    fm = scan.parse_frontmatter(sample.read_text(encoding="utf-8"))
    if not isinstance(fm.get("platform_ids"), dict):
        print(f"FAIL: platform_ids parsed as {type(fm.get('platform_ids')).__name__}")
        return 1
    if tuple(fm.keys()) != RAW_METADATA_FIELDS:
        print(f"FAIL: field order mismatch: {tuple(fm.keys())}")
        return 1
    try:
        validate(fm, base_dir=ROOT)
        print("OK: nested platform_ids parsed; strict raw validates")
        return 0
    except Exception as exc:
        print(f"FAIL: validate error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

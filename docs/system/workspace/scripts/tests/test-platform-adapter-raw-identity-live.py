#!/usr/bin/env python3
"""Live check: discover_raw_replicas resolves a cross-referenced raw key uniquely."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_key")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
    pa = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pa)
    replicas = pa.discover_raw_replicas(args.raw_key)
    ok = True
    for platform, replica in sorted(replicas.items()):
        status = replica.get("status", "unknown")
        title = replica.get("title", "")
        print(f"{platform}={status} title={title}")
        if status != "ok":
            ok = False
    return 0 if ok and replicas else 1


if __name__ == "__main__":
    raise SystemExit(main())

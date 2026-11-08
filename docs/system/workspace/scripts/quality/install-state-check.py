#!/usr/bin/env python3
"""`freely doctor` entry point: prove the installed state equals this source tree.

Thin wrapper — every rule lives in install_state.py so packaging, doctor and the
merge followthrough cannot drift apart.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_state import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())

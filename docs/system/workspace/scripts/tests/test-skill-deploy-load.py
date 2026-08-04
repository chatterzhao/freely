#!/usr/bin/env python3
"""Deployed skill directories must all parse (codex + claude)."""
import pathlib
import re
import sys

import yaml


def check(root):
    root = pathlib.Path(root).expanduser()
    if not root.exists():
        return 0, []
    bad = []
    total = 0
    for path in root.glob("*/SKILL.md"):
        total += 1
        try:
            text = path.read_text(encoding="utf-8")
            m = re.match(r"^---\n(.*?)\n---", text, re.S)
            if m:
                yaml.safe_load(m.group(1))
        except Exception as exc:
            bad.append((path.parent.name, str(exc).split("\n")[0]))
    return total, bad


failed = False
for target in ("~/.codex/skills", "~/.claude/skills"):
    total, bad = check(target)
    print(f"{target}: total={total} invalid={len(bad)}")
    for name, err in bad[:10]:
        print(f"  {name}: {err}")
    if bad:
        failed = True
sys.exit(1 if failed else 0)

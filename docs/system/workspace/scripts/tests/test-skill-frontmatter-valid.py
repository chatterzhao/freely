#!/usr/bin/env python3
"""Validate all workspace SKILL.md frontmatter parses as YAML."""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[5]
SKILLS = ROOT / "docs/system/workspace/skills"


def load_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError("missing --- frontmatter")
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


bad = []
total = 0
for path in sorted(SKILLS.glob("*/SKILL.md")):
    total += 1
    try:
        data = load_frontmatter(path)
        if not data.get("name"):
            bad.append((path.parent.name, "missing name"))
    except Exception as exc:
        bad.append((path.parent.name, str(exc).split("\n")[0]))

print(f"total={total} invalid={len(bad)}")
for name, err in bad[:10]:
    print(f"  {name}: {err}")
sys.exit(1 if bad else 0)

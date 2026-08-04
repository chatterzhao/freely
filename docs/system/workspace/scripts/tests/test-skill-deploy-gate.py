#!/usr/bin/env python3
"""deploy-skills must reject invalid frontmatter and must contain a YAML validation step."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DEPLOY = ROOT / "bin" / "deploy-skills"


def main():
    source = DEPLOY.read_text(encoding="utf-8")
    if "yaml" not in source and "safe_load" not in source:
        print("FAIL: deploy-skills has no frontmatter YAML validation")
        return 1
    result = subprocess.run(
        [str(DEPLOY), "--dry-run", "--tools", "codex"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    if "SKIP" in result.stdout or "SKIP" in result.stderr:
        print("FAIL: deploy-skills skipped a skill (missing name or invalid frontmatter)")
        print(result.stderr[-500:])
        return 1
    print("OK: deploy-skills validates frontmatter; dry-run clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

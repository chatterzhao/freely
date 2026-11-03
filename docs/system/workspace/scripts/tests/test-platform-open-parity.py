#!/usr/bin/env python3
"""Live parity check: both platforms expose the same OPEN raw-key set, and every
open issue has a local raw doc recording both platform ids."""
import importlib.util
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
_spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)

RAW_KEY = re.compile(r"raw-(\d{8}T\d{6}Z)", re.IGNORECASE)


def collect_open_issues():
    openings = {}
    for handler in pa._handlers():
        records = handler.list_open_issue_records() or {}
        for issue_id, record in records.items():
            match = RAW_KEY.search(record.get("title", "") or "")
            if not match:
                continue
            openings.setdefault(match.group(1), {}).setdefault(handler.name, str(issue_id))
    return openings


def load_local_docs():
    docs = {}
    for path in (ROOT / "docs/B1-docs").glob("raw-*/issue.md"):
        text = path.read_text(errors="ignore")
        if not text.startswith("---"):
            continue
        try:
            fm = yaml.safe_load(text.split("---", 2)[1]) or {}
        except Exception:
            continue
        local_id = str(fm.get("local_id", ""))
        key = local_id.replace("raw-", "")
        if key:
            docs[key] = {"path": str(path.relative_to(ROOT)), "fm": fm}
    return docs


def main():
    openings = collect_open_issues()
    local = load_local_docs()
    errors = []
    github_keys = {key for key, plats in openings.items() if "github" in plats}
    gitee_keys = {key for key, plats in openings.items() if "gitee" in plats}
    if github_keys != gitee_keys:
        errors.append("open key sets differ: github-only=%s gitee-only=%s"
                      % (sorted(github_keys - gitee_keys), sorted(gitee_keys - github_keys)))
    for key in sorted(github_keys | gitee_keys):
        platforms = openings[key]
        doc = local.get(key)
        if doc is None:
            errors.append(f"{key}: missing local docs/B1-docs/raw-{key}/issue.md")
            continue
        ids = doc["fm"].get("platform_ids") or {}
        for platform, issue_id in sorted(platforms.items()):
            recorded = str((ids.get(platform) or {}).get("issue_id", "") or "")
            if recorded != issue_id:
                errors.append(f"{key}: {platform} recorded='{recorded}' platform='{issue_id}'")
        for platform in ("github", "gitee"):
            if platform not in platforms:
                errors.append(f"{key}: missing open copy on {platform}")
    if errors:
        print("FAIL: platform open parity broken")
        for error in errors:
            print("  -", error)
        return 1
    print(f"OK: github/gitee open raw-key sets equal ({len(github_keys)} keys); "
          f"all have local docs with both platform ids")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

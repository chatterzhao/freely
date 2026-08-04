#!/usr/bin/env bash
# Audit terminal raw metadata before task scanning. This entry is deliberately
# read-only: scan preparation must not create lifecycle facts, worktrees, PRs,
# commits, or platform side effects.
set -euo pipefail

PROJECT=""
DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) echo "[pre-scan-audit] unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$PROJECT" ]] || { echo "[pre-scan-audit] --project required" >&2; exit 1; }
[[ -d "$PROJECT" ]] || { echo "[pre-scan-audit] project not found: $PROJECT" >&2; exit 1; }

python3 - "$PROJECT" "$DRY_RUN" <<'PYEOF'
from __future__ import annotations

import sys
from pathlib import Path

import yaml

project = Path(sys.argv[1])
lifecycle = project / "docs/system/workspace/scripts/lifecycle"
sys.path.insert(0, str(lifecycle))
from raw_metadata_contract import MetadataValidationError, normalize, validate

findings = []
for issue_file in sorted((project / "docs/B1-docs").glob("raw-*/issue.md")):
    parts = issue_file.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        continue
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        continue
    view = normalize(metadata)
    if view["strict_schema"]:
        try:
            validate(metadata, base_dir=project)
        except MetadataValidationError as error:
            findings.append(f"{issue_file.parent.name}: {error}")
    elif view["phase_state"] == "absorbed":
        target = str(view.get("absorbed_into") or "")
        canonical = str(view.get("canonical_issue_path") or "")
        if not target and not canonical:
            findings.append(
                f"{issue_file.parent.name}: legacy absorbed state has no canonical relationship"
            )

for finding in findings:
    print(f"[pre-scan-audit] {finding}")
print(f"[pre-scan-audit] read-only: {len(findings)} finding(s), 0 files changed")
PYEOF

#!/usr/bin/env bash
set -euo pipefail

required=(
  "docs/milestones.md"
  "docs/system/workspace/agents/lead-agent.md"
  "docs/system/workspace/scripts/start-lead-agent.sh"
  "docs/system/workspace/skills/context-source-skill/SKILL.md"
  "docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md"
  "docs/system/workspace/skills/doc-ibm-execution/SKILL.md"
  "docs/system/workspace/skills/dev-loop-execution/SKILL.md"
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || {
    echo "[FAIL] missing required routing artifact: $path" >&2
    exit 1
  }
done

echo "[PASS] routing foundation artifacts present"

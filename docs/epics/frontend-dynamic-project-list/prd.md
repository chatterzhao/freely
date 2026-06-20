# PRD: Dynamic project list

## Problem
AppShell.tsx hardcoded ["freely", "freely-sandbox", "frontend-probe-demo"].
Cannot add projects without frontend code change.

## Fix
listProjects() on ProbeAdapter — runtime-driven, fallback to defaults.

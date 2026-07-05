---
b1_id: B1-20260619T035704Z
phase_state: completed
source_raw: raw-20260619T035704Z
source_url: https://github.com/chatterzhao/freely/issues/3022
produced_candidate: C-20260619T035704Z-A
created_at: 2026-06-19
---

# B1_IBM: governance-merge-gate parse_candidate_file 不识别单 # heading

## Input Source

- GitHub issue #3022
- Raw issue: docs/B1-docs/raw-20260619T035704Z/issue.md

## Problem

parse_candidate_file regex `^##{1,3}` rejects single `#` markdown headings. When candidates.md uses `# C-xxx`, zero records are parsed, gate reports "no valid source_candidate" with no diagnostic hint about heading format.

## Brainstorming

### Option A: Keep strict ## requirement, document it
Simple but doesn't help users who naturally use # for top-level headings.

### Option B: Accept #{1,3} + add diagnostic
Fix regex + improve error messages when file exists but heading doesn't match.

## Decision

Option B. Single-character regex change + error diagnostic for file-exists-but-no-match.

## Candidate
- candidate_id: C-20260619T035704Z-A
- status: promoted
- milestone: unassigned

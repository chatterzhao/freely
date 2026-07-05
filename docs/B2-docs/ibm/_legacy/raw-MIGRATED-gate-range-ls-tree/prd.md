# PRD: build_issue_index range-mode git ls-tree

## Problem
build_issue_index scanned ROOT_DIR filesystem. In range mode, new files in fix branch invisible.

## Fix
When USE_RANGE_VIEW: git ls-tree --name-only -r RANGE_SOURCE_REF:docs/issues/
Fallback to filesystem scan for non-range modes.

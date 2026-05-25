# PRD: Enforce Test-Pre-Merge Before Develop Merge

## Problem
hotfix → develop merges skip test-pre-merge verification. The pre-test adequacy gate exists but only catches issues at merge time, not before. This creates inconsistent quality gates.

## Requirements
1. ALL develop-bound merges must pass test-pre-merge or provide adequate break-glass evidence
2. hotfix path defined (lighter verification or explicit exemption)
3. Break-glass documented per LAWS.md §2D

## Scope
- pr-merge-guarded: add pre-merge verification check
- governance-merge-gate: enforcement logic
- Documentation: hotfix verification policy

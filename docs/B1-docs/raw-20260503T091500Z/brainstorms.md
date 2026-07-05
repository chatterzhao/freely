## Issue
GitHub #180 — enforce test-pre-merge before develop merge

## Problem
hotfix→develop merges currently skip test-pre-merge verification. The pre-test adequacy gate blocks merges that haven't been verified through test-pre-merge self-host. The gate exists but has no enforcement for hotfix paths.

## Design Goal
All branches merging to develop (feature, hotfix, release) must pass through test-pre-merge verification OR provide adequate break-glass evidence.

## Questions
- Should this be a gate on pr-merge-guarded that checks for test-pre-merge evidence?
- Or should hotfix have a different verification path that's lighter than full self-host?
- What's the minimum verification for hotfix (which is supposed to be fast)?

## Direction
- Option A: Gate pr-merge-guarded to require test-pre-merge evidence for all non-hotfix merges
- Option B: Add hotfix-specific verification path (e.g., pre-test run without full self-host)
- Option C: Make self-host verification more reliable (fix the env init issue)

## Acceptance Items
- tpm-001: All develop-bound merges require test-pre-merge or break-glass
- tpm-002: Hotfix verification path defined (if different from feature)
- tpm-003: Break-glass can bypass with documented reason

## Linked
- GitHub #180 (source)
- The timezone standardization experience showed that self-host env init is fragile

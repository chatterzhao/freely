# Brainstorm: Pr-create-pull-after-gates

## Discovery

`pr-create-guarded` currently runs `git pull origin develop` at Step 1, before any gate checks. Every time a gate fails and the user retries, the pull runs again — a wasted network round-trip since the remote hasn't changed.

## Root Cause

The original design put pull at Step 1 because it was a convenient place. But all gates are local-only checks — they don't need the remote. Only the push at Step 4 needs up-to-date remote state.

## Decision

Promote. Move pull from Step 1 to Step 3 (between gate-passed marker and push), forming a tight fetch-and-push sequence.

- candidate_id: C-20260616T044030Z-A
- title: Complete config.toml migration with auto-migration and backward compatibility
- status: promoted
- milestone: M-20260616T044030Z-A
- promoted_issue_path: docs/issues/I-20260616T044030Z-A/issue.md
- decision_reason: Auto-migration chosen over manual script to enable self-healing daemon startup
- next_action: Materialize I-* issue in B2_IBM
---

# Candidate: config.toml Complete Migration

## Problem
Phase 1+2 code merged but daemon can't start — config.toml doesn't exist and no fallback.

## Solution
Auto-migration in load_config(): missing config.toml → migrate from config.env.
freely init generates config.toml. config.toml.example for new users.

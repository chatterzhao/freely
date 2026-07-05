# Brainstorm - 20260407-0023--codex-auto-switch-probe-apikey-fallback

## Problem

`freely ai switch codex` currently stops too early when the OAuth inventory sweep returns `all_unavailable:*`, even if saved `apikey-*` slots still exist and should be exec-probed. The watchdog path shares that premature stop, so the same false negative can block both manual auto-switch and bounded recovery.

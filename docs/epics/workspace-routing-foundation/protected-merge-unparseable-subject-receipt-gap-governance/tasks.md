# Tasks

1. Materialize `C-20260411-0217-A` into a narrow milestone-owned governance issue with explicit non-regression boundaries.
2. Expand `test-governance-check-protected-branch-merge-receipt-backfills` to cover generic-subject pass/fail cases before modifying parser behavior.
3. Extend the ordinary receipt-gap ledger schema with an explicit unparseable-subject validation mode, or prove a separate ledger is safer and update references accordingly.
4. Teach `governance-check` to validate the new mode against absorbing protected merge truth, bounded owner truth, and verification truth.
5. Keep existing parseable-subject and trailer-bearing merge behavior unchanged.
6. Add the April 10 preferred-auth ancestry entries only after parser and regressions pass.
7. Complete verification writeback and milestone closeout once canonical `./bin/governance-check` is green again.

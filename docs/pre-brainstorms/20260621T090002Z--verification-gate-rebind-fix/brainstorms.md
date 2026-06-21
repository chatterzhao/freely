# B1_IBM: verification gate rebind path blocks regular workers

## Discovery
All worker delegation blocked because rebind path (Path A) enforces full 12-field verification metadata, but regular workers never have these fields. Only Path B (first launch) is non-blocking.

## Research
Two gate paths with inconsistent behavior — Path A blocks, Path B warns. The 12 fields (owner_issue, pre_tests_path, etc.) are designed for test-pre-merge family. Regular fix/feature workers should not be blocked.

## Decision
Align Path A behavior with Path B: log warning, write chat guidance, continue. Full verification remains at merge gate.

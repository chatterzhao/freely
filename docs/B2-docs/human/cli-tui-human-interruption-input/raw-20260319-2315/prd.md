# PRD: cli-tui-human-interruption-input

## Problem

Freely needs a usable CLI-side human interruption shell, but the shell must stay aligned with the existing durable intake architecture instead of becoming a second control plane.

## Product Requirement

`freely tui` must provide a multi-line composer for human interruption intake while preserving `.freely/intake/**` durability, Chinese input fidelity, and manager-owned claim/resolve behavior.

## Non-goals

- Do not add claim / resolve logic to the TUI itself
- Do not introduce a second persistence protocol
- Do not turn the TUI into a generic shell prompt

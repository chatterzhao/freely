# Brainstorm
Two remaining issues after slot full-name refactoring:
1. codex_infer_slot_kind_from_slot used account-*/apikey-* prefix match, fails with full names like codex-apikey-xxx
2. cmd_switch generic path constructed alias_name="${tool}-${slot}", double prefix with full names

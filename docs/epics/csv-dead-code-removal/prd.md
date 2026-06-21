# PRD: CSV dead code removal

## Changes
- manager_exit_contract_kind: removed CSV fallback (always-empty field)
- _manager_auto_consume_workers: simplified (~20 lines removed)
- 25→20 references; remaining are harmless empty-string read/writes

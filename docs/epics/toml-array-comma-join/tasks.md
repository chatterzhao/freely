# Tasks: TOML array comma-join + feedback validation + bash 3.2 guard

- issue_id: I-20260626T150328Z-A

## 1. Fix tool-registry-query.py
- [x] Change `" ".join` → `",".join` at line 111
- [x] Verify: `adapters.supported` returns `direct,acp`
- [x] Verify: `aliases` returns comma-separated values

## 2. Fix tool-launchers.sh alias loop
- [x] Change `for _a in $_aliases` → `for _a in ${_aliases//,/ }`
- [x] Verify: alias resolution works with comma-separated input

## 3. Add feedback format validation
- [x] Title type prefix check (`fix:`, `feat:`, `docs:`, etc.)
- [x] Title length check (≤ 100 chars total with prefix)
- [x] Body minimum length check (≥ 50 non-ws chars)
- [x] Body `## ` section heading check
- [x] Verify: all 4 checks reject bad inputs

## 4. Fix bash 3.2 empty array guard
- [x] Wrap `for _item in "${_bridge_env[@]}"` with `if [[ ${#_bridge_env[@]} -gt 0 ]]`
- [x] Verify: kiro-cli path no longer triggers "unbound variable"

## 5. Governance
- [x] B1_IBM: brainstorms.md, candidates.md, milestones.md
- [ ] B2_IBM: I-* issue, pre-tests.md, tasks.md, code-review (this file)
- [ ] pr-create-guarded
- [ ] pr-review-guarded
- [ ] pr-merge-guarded
- [ ] wt-close

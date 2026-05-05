# pre-tests: issue state refactor

- issue_id: I-20260505T1210Z-A

## Acceptance Items

### A1: TERMINAL_RAW is {absorbed, dropped}
```bash
grep 'TERMINAL_RAW' docs/system/workspace/scripts/runtime/task-lifecycle-scan.py | grep -q '"absorbed", "dropped"' && echo PASS || echo FAIL
```
- status: passed
- result: constants match IBM Framework §89

### A2: DONE_STATES is {done_b2_ibm, completed}
```bash
grep 'DONE_STATES' docs/system/workspace/scripts/runtime/task-lifecycle-scan.py | grep -q '"done_b2_ibm", "completed"' && echo PASS || echo FAIL
```
- status: passed
- result: verified

### A3: ACTIVE_B2 excludes legacy in_ibm
```bash
grep 'ACTIVE_B2' docs/system/workspace/scripts/runtime/task-lifecycle-scan.py | grep -qv 'in_ibm' && echo PASS || echo FAIL
```
- status: passed
- result: verified

### A4: Raw phase_state read prefers phase_state over status
```bash
grep -q 'fm.get("phase_state") or fm.get("status"' docs/system/workspace/scripts/runtime/task-lifecycle-scan.py && echo PASS || echo FAIL
```
- status: passed
- result: backward-compatible phase_state read

### A5: Migration script compiles
```bash
python3 -c "compile(open('bin/migrate-issue-phase-state').read(), 'migrate-issue-phase-state', 'exec'); print('PASS')"
```
- status: passed
- result: no syntax errors

### A6: Scan no longer false-positives on absorbed+closed items
```bash
python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . | python3 -c "
import json,sys; d=json.load(sys.stdin)
for i in d['items']:
    if i.get('key')=='20260502-1028': print('FAIL'); break
else: print('PASS')
"
```
- status: passed
- result: 20260502-1028 correctly excluded

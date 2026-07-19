#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-$(cd "$(dirname "$0")/../../../.." && pwd)}"
DB="$PROJECT/.freely/freely.db"
FAIL=0

fail() { echo "FAIL: $*"; FAIL=1; }
pass() { echo "PASS: $*"; }

echo "=== Agent Lifecycle Test ==="

# Test 1: worker_id must be NULL initially for non-__manager__ rows
echo "--- Test 1: No stale NULL rows ---"
STALE=$(python3 -c "
import sqlite3; db=sqlite3.connect('$DB')
c=db.execute(\"SELECT COUNT(*) FROM agent_working WHERE raw_key!='__manager__' AND worker_id IS NULL\").fetchone()[0]
print(c)
")
if [[ "$STALE" -eq 0 ]]; then pass "no stale NULL rows"; else fail "$STALE stale rows with worker_id=NULL"; fi

# Test 2: agent_next_free logic (direct SQL, no daemon needed)  
echo "--- Test 2: agent_next_free returns worker_01 when all free ---"
FREE=$(python3 -c "
import sqlite3; db=sqlite3.connect('$DB')
role='worker'; col='worker_id'; prefix='worker_'; pool=10
rows=db.execute(f'SELECT {col} FROM agent_working WHERE {col} IS NOT NULL').fetchall()
occupied={r[0].split(':')[0] for r in rows if r[0]}
all_ids={f'{prefix}{i:02d}' for i in range(1,pool+1)}
free=sorted(all_ids-occupied)
print(free[0] if free else 'NONE')
")
if [[ "$FREE" == "worker_01" ]]; then pass "first free is worker_01"; else fail "first free is $FREE"; fi

# Test 3: assign + verify + release cycle
echo "--- Test 3: Full lifecycle ---"
TEST_RK="test-lifecycle-$$"
python3 -c "
import sqlite3; db=sqlite3.connect('$DB')
# Assign
db.execute(\"INSERT INTO agent_working(raw_key,worktree,branch,worker_id,slot) VALUES(?,?,?,?,?) ON CONFLICT(raw_key) DO UPDATE SET worker_id=?,updated_at=datetime('now')\",
    ('$TEST_RK','/tmp/test','test-br','worker_05:ses_test','opencode-apikey-ds-flash-auto','worker_05:ses_test'))
db.commit()
# Verify
r=db.execute(\"SELECT worker_id FROM agent_working WHERE raw_key='$TEST_RK'\").fetchone()
if not r or not r[0]: print('ASSIGN_FAIL'); import sys; sys.exit(1)
print(f'assigned: {r[0]}')
# Check next_free excludes worker_05
rows=db.execute('SELECT worker_id FROM agent_working WHERE worker_id IS NOT NULL').fetchall()
occupied={row[0].split(':')[0] for row in rows if row[0]}
all_ids={f'worker_{i:02d}' for i in range(1,11)}
free=sorted(all_ids-occupied)
if 'worker_05' in free: print('FREE_CHECK_FAIL'); import sys; sys.exit(1)
print(f'free (first 3): {free[:3]}')
# Release  
db.execute(\"DELETE FROM agent_working WHERE raw_key='$TEST_RK'\")
db.commit()
# Verify released
rows=db.execute('SELECT worker_id FROM agent_working WHERE worker_id IS NOT NULL').fetchall()
occupied2={row[0].split(':')[0] for row in rows if row[0]}
free2=sorted(all_ids-occupied2)
if 'worker_05' not in free2: print('RELEASE_FAIL'); import sys; sys.exit(1)
print(f'released: worker_05 back in free')
"
if [[ $? -eq 0 ]]; then pass "full lifecycle"; else fail "lifecycle broken"; fi

echo "=== Result: $FAIL failures ==="
exit $FAIL

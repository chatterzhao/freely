#!/usr/bin/env bash
set -euo pipefail
PROJECT="${1:-$(cd "$(dirname "$0")/../../../.." && pwd)}"
DB="$PROJECT/.freely/freely.db"
python3 -c "
import sqlite3
# db-writer: cleanup-agent-working: 清理脚本删除过期 worker 记录，登记于 State 契约
db = sqlite3.connect('$DB')
c = db.execute(\"DELETE FROM agent_working WHERE raw_key != '__manager__' AND worker_id IS NULL AND manager_id IS NULL\")
db.commit()
print(f'cleaned {c.rowcount} stale rows')
"

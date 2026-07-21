"""Resume persisted ACP sessions from agent_working after runtime restart."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Callable

from agent_identity_value import parse_agent_entries
from agent_working import _acp_bridge_call, _db_rpc


def _slot_for_agent(project: str, agent_id: str) -> str:
    query = os.path.join(project, "bin", "agent-table-query")
    if not os.path.isfile(query):
        return ""
    result = subprocess.run(
        [query, "--get-slot", agent_id],
        capture_output=True,
        text=True,
        cwd=project,
        timeout=5,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def resume_persisted_sessions(
    project: str,
    slot_resolver: Callable[[str, str], str] = _slot_for_agent,
) -> list[dict]:
    """Resume each exact agent/session pair; ignore bare reservations."""
    rows = _db_rpc(project, "agent_working.get_all", {}).get("rows", [])
    outcomes: list[dict] = []

    for row in rows:
        raw_key = row.get("raw_key", "")
        for role in ("manager", "worker", "reviewer"):
            for agent_id, session_id in parse_agent_entries(
                row.get(f"{role}_id", "")
            ).items():
                if not session_id:
                    continue
                slot = slot_resolver(project, agent_id)
                base_tool = slot.split("-", 1)[0] if slot else ""
                outcome = {
                    "raw_key": raw_key,
                    "role": role,
                    "agent_id": agent_id,
                    "session_id": session_id,
                    "base_tool": base_tool,
                }
                if not base_tool:
                    outcome["status"] = "slot_unavailable"
                    outcomes.append(outcome)
                    continue
                try:
                    _acp_bridge_call(
                        project,
                        base_tool,
                        "session/resume",
                        {"sessionId": session_id, "cwd": project},
                    )
                    outcome["status"] = "resumed"
                except Exception as error:
                    outcome["status"] = "failed"
                    outcome["error"] = str(error)
                outcomes.append(outcome)

    return outcomes


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: agent_session_restore.py <project>", file=sys.stderr)
        return 2
    for outcome in resume_persisted_sessions(os.path.abspath(args[0])):
        print(json.dumps(outcome, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

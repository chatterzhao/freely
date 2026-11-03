#!/usr/bin/env python3
"""C-B research replay: ownership/handback/terminal rules as a small state machine."""
from dataclasses import dataclass, field

TERMINAL = {"completed", "failed", "canceled"}

@dataclass
class Task:
    task_id: str
    thread_key: str
    state: str = "pending"
    owner: str | None = None
    lease_until: int = 0
    handback_done: bool = False
    messages: list[str] = field(default_factory=list)

class Protocol:
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.handoffs: list[dict] = []

    def create(self, task_id, thread_key, owner="manager"):
        self.tasks[task_id] = Task(task_id, thread_key, owner=owner, lease_until=10)
        return self.tasks[task_id]

    def assign(self, task_id, worker, lease=10):
        t = self.tasks[task_id]
        if t.state in TERMINAL:
            raise ValueError("terminal task cannot be assigned")
        t.owner = worker
        t.lease_until = lease
        t.state = "working"
        self.handoffs.append({"task_id": task_id, "from": "manager", "to": worker, "kind": "assignment"})

    def followup(self, task_id, actor, now, stopped=False):
        t = self.tasks[task_id]
        if stopped:
            t.state = "canceled"
            t.owner = "human"
            return {"owner": "human", "action": "stop_wins"}
        if t.state in TERMINAL:
            if t.lease_until >= now and t.owner:
                return {"owner": t.owner, "action": "lease_owner"}
            t.owner = "manager"
            return {"owner": "manager", "action": "handback_expired"}
        if t.owner:
            return {"owner": t.owner, "action": "direct"}
        t.owner = "manager"
        return {"owner": "manager", "action": "unowned_to_manager"}

    def cross_ticket(self, task_id, target_task):
        t = self.tasks[task_id]
        if t.handback_done:
            return {"action": "duplicate_handback_rejected"}
        t.handback_done = True
        from_owner = t.owner
        t.owner = "manager"
        self.handoffs.append({"task_id": task_id, "from": from_owner, "to": "manager", "kind": "handback", "target": target_task})
        return {"action": "handback_once", "target": target_task}

    def worker_died(self, task_id):
        t = self.tasks[task_id]
        if t.state in TERMINAL:
            return {"action": "terminal_unchanged"}
        t.state = "working"
        t.owner = "manager"
        self.handoffs.append({"task_id": task_id, "from": "worker", "to": "manager", "kind": "recovery", "state": "working"})
        return {"action": "recovery_note", "task_state": t.state}

    def reviewer_fail(self, task_id, rounds):
        if rounds >= 3:
            t = self.tasks[task_id]
            t.state = "blocked"
            t.owner = "manager"
            return {"action": "handback_manager", "rounds": rounds}
        return {"action": "changes_requested", "rounds": rounds}


def main():
    p = Protocol()
    t = p.create("T-1", "github:o/r#1")
    p.assign("T-1", "worker-1")
    out = {}
    out["new_request_owner"] = t.owner
    out["active_followup"] = p.followup("T-1", "alice", now=5)
    out["cross_ticket_once"] = p.cross_ticket("T-1", "T-2")
    out["cross_ticket_twice"] = p.cross_ticket("T-1", "T-2")
    out["worker_died"] = p.worker_died("T-1")
    out["reviewer_fail_2"] = p.reviewer_fail("T-1", 2)
    out["reviewer_fail_3"] = p.reviewer_fail("T-1", 3)

    # completed lease owner, then expiry -> manager
    t2 = p.create("T-3", "github:o/r#3")
    p.assign("T-3", "worker-3", lease=20)
    t2.state = "completed"
    out["completed_followup_before_expiry"] = p.followup("T-3", "bob", now=15)
    out["completed_followup_after_expiry"] = p.followup("T-3", "bob", now=25)

    # human stop wins over worker ownership
    t3 = p.create("T-4", "github:o/r#4")
    p.assign("T-4", "worker-4")
    out["human_stop"] = p.followup("T-4", "owner", now=5, stopped=True)
    # Real thread fixture: two real comments on chatterzhao/freely#4070 must
    # stay on one task/one owner, not create a second task.
    t5 = p.create("T-4070", "github:chatterzhao/freely#4070")
    p.assign("T-4070", "worker-4070")
    real_comments = [
        ("IC_kwDOSIGLwc8AAAABLGREcA", "2026-07-21T22:35:54Z"),
        ("IC_kwDOSIGLwc8AAAABLGcLBQ", "2026-07-21T22:57:11Z"),
    ]
    for cid, _ in real_comments:
        r = p.followup("T-4070", "chatterzhao", now=5)
        assert r["action"] == "direct"
        t5.messages.append(cid)
    out["real_thread"] = {
        "thread_key": t5.thread_key,
        "owner": t5.owner,
        "messages": t5.messages,
        "task_count": len([x for x in p.tasks.values() if x.thread_key == t5.thread_key]),
    }
    out["handoffs"] = p.handoffs
    print(out)
    assert out["new_request_owner"] == "worker-1"
    assert out["active_followup"]["action"] == "direct"
    assert out["cross_ticket_once"]["action"] == "handback_once"
    assert out["cross_ticket_twice"]["action"] == "duplicate_handback_rejected"
    assert out["worker_died"]["task_state"] == "working"
    assert out["reviewer_fail_3"]["action"] == "handback_manager"
    assert out["completed_followup_before_expiry"]["action"] == "lease_owner"
    assert out["completed_followup_after_expiry"]["action"] == "handback_expired"
    assert out["human_stop"]["owner"] == "human"
    assert out["real_thread"]["task_count"] == 1
    assert out["real_thread"]["owner"] == "worker-4070"
    assert len(out["real_thread"]["messages"]) == 2
    print("handoff replay: OK")


if __name__ == "__main__":
    main()

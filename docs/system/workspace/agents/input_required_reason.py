"""InputRequiredReason — 全仓一致的 reason 枚举值。
所有 agent 必须使用此 Enum，禁止手写字符串。
新增 reason 时先改此文件再改路由表。"""

from enum import Enum


class InputRequiredReason(Enum):
    # Worker → Reviewer (per-step review)
    NEEDS_REVIEW_B1 = "needs-review:b1"
    NEEDS_REVIEW_B2 = "needs-review:b2"
    NEEDS_REVIEW_DEV = "needs-review:dev"
    NEEDS_REVIEW_RED = "needs-review:red"
    NEEDS_REVIEW_TEST = "needs-review:test"
    NEEDS_REVIEW_GATE = "needs-review:gate"

    # Worker → Manager
    NEEDS_MANAGER_DECISION = "needs-manager-decision"

    # Reviewer → Worker
    NEEDS_WORKER_RETRY = "needs-worker-retry"

    # Reviewer → Manager
    NEEDS_MANAGER_SCOPE = "needs-manager-scope"

    # Manager → Worker
    NEEDS_WORKER_TASK = "needs-worker-task"

    # Human interaction
    NEEDS_HUMAN_INPUT = "needs-human-input"

    # Fallback (任何无法识别 → manager_01)
    UNKNOWN = "unknown"

    @classmethod
    def from_string(cls, s: str) -> "InputRequiredReason":
        for reason in cls:
            if reason.value == s:
                return reason
        return cls.UNKNOWN

    @property
    def needs_role(self) -> str:
        """返回应由哪个 role 处理。"""
        mapping = {
            "needs-review": "reviewer",
            "needs-manager-decision": "manager",
            "needs-worker-retry": "worker",
            "needs-manager-scope": "manager",
            "needs-worker-task": "worker",
            "needs-human-input": "manager",
            "unknown": "manager",
        }
        prefix = self.value.split(":")[0] if ":" in self.value else self.value
        return mapping.get(prefix, "manager")

#!/usr/bin/env python3
"""a2a_types.py — Standard A2A Protocol Types

Aligned with Google A2A specification and a2a-sdk types used by JiuwenSwarm.
These types provide the canonical A2A data model for Freely's implementation.

Reference: https://github.com/A2A-Specification/A2A
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional, List, Dict


# ── Task States (A2A Standard) ──────────────────────────────────────────

class TaskState(str, Enum):
    """A2A Task states — identical to a2a.types.TaskState."""
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    INPUT_REQUIRED = "input-required"
    CANCELED = "canceled"

    # Alias from A2A spec
    PENDING_INPUT = "pending-input"


# ── Task Status ──────────────────────────────────────────────────────────

@dataclass
class TaskStatus:
    """A2A Task status with state and optional message — aligns with a2a.types.TaskStatus."""
    state: str
    message: Optional[Message] = None
    timestamp: str = ""

    def to_dict(self) -> dict:
        d = {"state": self.state}
        if self.message:
            d["message"] = self.message.to_dict()
        if self.timestamp:
            d["timestamp"] = self.timestamp
        return d


# ── Message ──────────────────────────────────────────────────────────────

class Role(str, Enum):
    USER = "user"
    AGENT = "agent"


@dataclass
class Part:
    """A2A Part — content fragment in a Message or Artifact. Aligns with a2a.types.Part."""
    text: str = ""
    data: Optional[Dict] = None
    url: str = ""
    raw: str = ""
    filename: str = ""
    media_type: str = ""

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {}
        if self.text:
            d["text"] = self.text
        if self.data is not None:
            d["data"] = self.data
        if self.url:
            d["url"] = self.url
        if self.raw:
            d["raw"] = self.raw
        if self.filename:
            d["filename"] = self.filename
        if self.media_type:
            d["media_type"] = self.media_type
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Part":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Message:
    """A2A Message — aligns with a2a.types.Message."""
    message_id: str = ""
    context_id: str = ""
    role: str = "user"
    parts: List[Part] = field(default_factory=list)
    metadata: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "messageId": self.message_id,
            "contextId": self.context_id,
            "role": self.role,
            "parts": [p.to_dict() for p in self.parts],
        }
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        parts_data = data.get("parts", [])
        parts = [Part.from_dict(p) for p in parts_data]
        return cls(
            message_id=data.get("messageId", data.get("message_id", "")),
            context_id=data.get("contextId", data.get("context_id", "")),
            role=data.get("role", "user"),
            parts=parts,
            metadata=data.get("metadata"),
        )


# ── Artifact ─────────────────────────────────────────────────────────────

@dataclass
class Artifact:
    """A2A Artifact — task output. Aligns with a2a.types.Artifact."""
    artifact_id: str = ""
    name: str = ""
    description: str = ""
    parts: List[Part] = field(default_factory=list)
    metadata: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "artifactId": self.artifact_id,
            "name": self.name,
            "parts": [p.to_dict() for p in self.parts],
        }
        if self.description:
            d["description"] = self.description
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Artifact":
        parts_data = data.get("parts", [])
        parts = [Part.from_dict(p) for p in parts_data]
        return cls(
            artifact_id=data.get("artifactId", data.get("artifact_id", "")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            parts=parts,
            metadata=data.get("metadata"),
        )


# ── A2A Events (Event-driven state transitions) ──────────────────────────

@dataclass
class TaskStatusUpdateEvent:
    """Emitted when a task's status changes. Aligns with a2a.types.TaskStatusUpdateEvent."""
    task_id: str
    context_id: str = ""
    status: TaskStatus = field(default_factory=lambda: TaskStatus(state=TaskState.SUBMITTED.value))
    final: bool = False
    metadata: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "taskId": self.task_id,
            "status": self.status.to_dict(),
            "final": self.final,
        }
        if self.context_id:
            d["contextId"] = self.context_id
        if self.metadata:
            d["metadata"] = self.metadata
        return d


@dataclass
class TaskArtifactUpdateEvent:
    """Emitted when a task produces output. Aligns with a2a.types.TaskArtifactUpdateEvent."""
    task_id: str
    context_id: str = ""
    artifact: Artifact = field(default_factory=Artifact)
    append: bool = False
    last_chunk: bool = False
    metadata: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "taskId": self.task_id,
            "artifact": self.artifact.to_dict(),
            "append": self.append,
            "lastChunk": self.last_chunk,
        }
        if self.context_id:
            d["contextId"] = self.context_id
        if self.metadata:
            d["metadata"] = self.metadata
        return d


# ── Agent Card ────────────────────────────────────────────────────────────

@dataclass
class AgentSkill:
    """A2A Agent Skill — aligns with a2a.types.AgentSkill."""
    id: str
    name: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    input_modes: List[str] = field(default_factory=lambda: ["text/plain"])
    output_modes: List[str] = field(default_factory=lambda: ["text/plain"])

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {"id": self.id, "name": self.name}
        if self.description: d["description"] = self.description
        if self.tags: d["tags"] = self.tags
        if self.examples: d["examples"] = self.examples
        if self.input_modes: d["inputModes"] = self.input_modes
        if self.output_modes: d["outputModes"] = self.output_modes
        return d


@dataclass
class AgentCapabilities:
    """A2A Agent Capabilities — aligns with a2a.types.AgentCapabilities."""
    streaming: bool = False
    push_notifications: bool = False
    state_transitions: bool = True

    def to_dict(self) -> dict:
        return {
            "streaming": self.streaming,
            "pushNotifications": self.push_notifications,
            "stateTransitions": self.state_transitions,
        }


@dataclass
class AgentInterface:
    """A2A Agent Interface — aligns with a2a.types.AgentInterface."""
    url: str
    protocol_binding: str = "jsonrpc"
    protocol_version: str = "1.0.0"

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "protocolBinding": self.protocol_binding,
            "protocolVersion": self.protocol_version,
        }


@dataclass
class AgentCard:
    """A2A Agent Card — aligns with a2a.types.AgentCard."""
    name: str
    description: str
    version: str = "1.0.0"
    url: str = ""
    capabilities: AgentCapabilities = field(default_factory=AgentCapabilities)
    skills: List[AgentSkill] = field(default_factory=list)
    supported_interfaces: List[AgentInterface] = field(default_factory=list)
    default_input_modes: List[str] = field(default_factory=lambda: ["text/plain"])
    default_output_modes: List[str] = field(default_factory=lambda: ["text/plain"])
    # Freely extensions
    freely: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "capabilities": self.capabilities.to_dict(),
            "skills": [s.to_dict() for s in self.skills],
            "supportedInterfaces": [i.to_dict() for i in self.supported_interfaces],
            "defaultInputModes": self.default_input_modes,
            "defaultOutputModes": self.default_output_modes,
        }
        if self.url:
            d["url"] = self.url
        if self.freely:
            d["freely"] = self.freely
        return d


# ── Task (A2A Standard) ──────────────────────────────────────────────────

@dataclass
class Task:
    """A2A Task — aligns with a2a.types.Task."""
    id: str = ""
    name: str = ""
    description: str = ""
    state: str = TaskState.SUBMITTED.value
    context_id: str = ""
    agent_id: str = ""
    skill: str = ""
    session_id: str = ""
    message: str = ""
    messages: List[Message] = field(default_factory=list)
    artifacts: List[Artifact] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    metadata: Optional[Dict] = None
    # Freely extension fields
    raw_key: str = ""
    worktree: str = ""
    branch: str = ""
    completion_summary: str = ""
    evidence_paths: str = ""
    worker_pid: str = ""
    error: str = ""
    freely: Optional[Dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "agentId": self.agent_id,
        }
        if self.description: d["description"] = self.description
        if self.context_id: d["contextId"] = self.context_id
        if self.skill: d["skill"] = self.skill
        if self.session_id: d["sessionId"] = self.session_id
        if self.message: d["message"] = self.message
        if self.messages: d["messages"] = [m.to_dict() for m in self.messages]
        if self.artifacts: d["artifacts"] = [a.to_dict() for a in self.artifacts]
        if self.created_at: d["createdAt"] = self.created_at
        if self.updated_at: d["updatedAt"] = self.updated_at
        if self.metadata: d["metadata"] = self.metadata
        # Freely fields
        if self.raw_key: d["rawKey"] = self.raw_key
        if self.branch: d["branch"] = self.branch
        if self.completion_summary: d["completionSummary"] = self.completion_summary
        if self.evidence_paths: d["evidencePaths"] = self.evidence_paths
        if self.error: d["error"] = self.error
        if self.freely: d["freely"] = self.freely
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data.get("id", data.get("task_id", "")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            state=data.get("state", TaskState.SUBMITTED.value),
            context_id=data.get("contextId", data.get("context_id", "")),
            agent_id=data.get("agentId", data.get("agent_id", "")),
            skill=data.get("skill", ""),
            session_id=data.get("sessionId", data.get("session_id", "")),
            message=data.get("message", ""),
            created_at=data.get("createdAt", data.get("created_at", "")),
            updated_at=data.get("updatedAt", data.get("updated_at", "")),
            metadata=data.get("metadata"),
            raw_key=data.get("rawKey", data.get("raw_key", "")),
            worktree=data.get("worktree", ""),
            branch=data.get("branch", ""),
            completion_summary=data.get("completionSummary", data.get("completion_summary", "")),
            evidence_paths=data.get("evidencePaths", data.get("evidence_paths", "")),
            worker_pid=data.get("workerPid", data.get("worker_pid", "")),
            error=data.get("error", ""),
            freely=data.get("freely"),
        )


# ── Helpers ──────────────────────────────────────────────────────────────

FREELY_SKILLS = [
    AgentSkill(
        id="freely-fix-execution",
        name="Bug Fix Execution",
        description="快速修复 bug 的高效策略：隔离验证→正式提交",
        tags=["fix", "bug", "development"],
        examples=["Fix authentication bug in login flow"],
    ),
    AgentSkill(
        id="freely-feature-execution",
        name="Feature Execution",
        description="新功能/大型改动的完整开发流程：预研→设计→实现→门禁→合并",
        tags=["feature", "development", "full-cycle"],
        examples=["Add user authentication to the app"],
    ),
    AgentSkill(
        id="freely-doc-B1_IBM-execution",
        name="B1_IBM Pre-Research",
        description="I→B→M 第一阶段：预研发散收敛产出 candidate",
        tags=["research", "brainstorm", "candidate"],
    ),
    AgentSkill(
        id="freely-doc-B2_IBM-execution",
        name="B2_IBM Design",
        description="I→B→M 第二阶段：实现设计产出 Map 交付 dev-loop",
        tags=["design", "implementation", "planning"],
    ),
    AgentSkill(
        id="freely-branch-management",
        name="Branch Management",
        description="管理 Freely 风格开发的完整自主分支生命周期",
        tags=["branch", "worktree", "git"],
    ),
    AgentSkill(
        id="freely-constitution-guard",
        name="Constitution Guard",
        description="强制执行宪法硬性约束：分支/worktree/架构/治理边界",
        tags=["governance", "compliance", "safety"],
    ),
    AgentSkill(
        id="freely-worktree-maintenance-governance",
        name="Worktree Maintenance",
        description="工位治理：核清单个 worktree 状态、制定安全 merge 顺序",
        tags=["worktree", "maintenance", "governance"],
    ),
]

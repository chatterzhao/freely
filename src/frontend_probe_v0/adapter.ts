import type { ClientCommand, ProbeSnapshot } from "./contracts";
import type { EventListener } from "./events";
import { mockSnapshot } from "./mockSnapshot";

export interface ProbeAdapter {
  /** List known project IDs — driven by runtime config, not hardcoded. */
  listProjects(): Promise<string[]>;
  requestSnapshot(projectId: string): Promise<ProbeSnapshot>;
  sendCommand(command: ClientCommand): Promise<void>;
}

export class MockProbeAdapter implements ProbeAdapter {
  private readonly listeners = new Set<EventListener>();
  private readonly snapshots = new Map<string, ProbeSnapshot>();

  async listProjects(): Promise<string[]> {
    const known = new Set(this.snapshots.keys());
    // Default projects always available even before any snapshot is loaded.
    for (const id of ["freely", "freely-sandbox", "frontend-probe-demo"]) {
      known.add(id);
    }
    return Array.from(known).sort();
  }

  async requestSnapshot(projectId: string): Promise<ProbeSnapshot> {
    return structuredClone(this.getSnapshot(projectId));
  }

  async sendCommand(command: ClientCommand): Promise<void> {
    if (command.type === "CreateOrResumeSession") {
      const snapshot = this.getSnapshot(command.projectId);
      const sessionId = command.sessionId ?? `session-${Date.now()}`;

      this.snapshots.set(command.projectId, {
        ...snapshot,
        activeSessions: [{ sessionId, status: "running" }],
        governanceSummary: [
          `session upserted via ${command.resumeHint ?? "probe-ui"}`,
          ...snapshot.governanceSummary,
        ].slice(0, 4),
        lastEventId: `event-${Date.now()}`,
      });

      const nextSnapshot = this.getSnapshot(command.projectId);
      this.emit({
        eventId: nextSnapshot.lastEventId,
        occurredAt: new Date().toISOString(),
        projectId: command.projectId,
        sessionId,
        source: "human-control",
        type: "SessionUpserted",
        status: "running",
      });
      this.emit({
        eventId: nextSnapshot.lastEventId,
        occurredAt: new Date().toISOString(),
        projectId: command.projectId,
        sessionId,
        source: "human-control",
        type: "AudioCueRequested",
        cueKey: "manager-started",
        actor: "manager",
        lifecycle: "started",
        reason: "session-created-or-resumed",
      });
      return;
    }

    if (command.type === "SendChatIntervention") {
      const snapshot = this.getSnapshot(command.projectId);

      this.snapshots.set(command.projectId, {
        ...snapshot,
        activeAgents: snapshot.activeAgents.map((agent, index) =>
          index === 0
            ? {
                ...agent,
                lastAction: `chat:${command.content.slice(0, 40)}`,
              }
            : agent,
        ),
        governanceSummary: [
          `chat intervention accepted for ${command.sessionId}`,
          ...snapshot.governanceSummary,
        ].slice(0, 4),
        lastEventId: `event-${Date.now()}`,
      });

      const nextSnapshot = this.getSnapshot(command.projectId);
      this.emit({
        eventId: nextSnapshot.lastEventId,
        occurredAt: new Date().toISOString(),
        projectId: command.projectId,
        sessionId: command.sessionId,
        source: "human-chat",
        type: "InputArbitrationRecorded",
        outcome: "accepted",
        details: command.content,
      });
      if (command.targetAgentId?.startsWith("worker")) {
        this.emit({
          eventId: nextSnapshot.lastEventId,
          occurredAt: new Date().toISOString(),
          projectId: command.projectId,
          sessionId: command.sessionId,
          source: "human-chat",
          type: "AudioCueRequested",
          cueKey: "worker-started",
          actor: "worker",
          lifecycle: "started",
          reason: "worker-targeted-chat-intervention",
        });
      }
      return;
    }

    if (command.type === "AttachTerminal") {
      const snapshot = this.getSnapshot(command.projectId);
      const nextTerminalTargets = [
        {
          terminalTarget: command.terminalTarget,
          sessionId: command.sessionId,
        },
        ...snapshot.terminalTargets.filter(
          (target) => target.terminalTarget !== command.terminalTarget,
        ),
      ];

      this.snapshots.set(command.projectId, {
        ...snapshot,
        terminalTargets: nextTerminalTargets,
        governanceSummary: [
          `terminal attached to ${command.terminalTarget}`,
          ...snapshot.governanceSummary,
        ].slice(0, 4),
        lastEventId: `event-${Date.now()}`,
      });

      const nextSnapshot = this.getSnapshot(command.projectId);
      this.emit({
        eventId: nextSnapshot.lastEventId,
        occurredAt: new Date().toISOString(),
        projectId: command.projectId,
        sessionId: command.sessionId,
        source: "human-control",
        type: "TerminalChunkAppended",
        terminalTarget: command.terminalTarget,
        chunk: `[mock:attach] attached to ${command.terminalTarget}`,
      });
      return;
    }

    if (command.type !== "ControlRun") {
      return;
    }

    const snapshot = this.getSnapshot(command.projectId);
    const activeActor =
      snapshot.activeAgents[0]?.agentId?.startsWith("worker") ? "worker" : "manager";
    const nextStatus =
      command.action === "terminate"
        ? "terminated"
        : command.action === "pause"
          ? "paused"
          : "in_dev";

    this.snapshots.set(command.projectId, {
      ...snapshot,
      activeRuns: snapshot.activeRuns.map((run) =>
        run.runId === command.runId ? { ...run, status: nextStatus } : run,
      ),
      activeAgents: snapshot.activeAgents.map((agent, index) =>
        index === 0
          ? {
              ...agent,
              lastAction: `control:${command.action}`,
              blocker: command.action === "pause" ? "paused by human-control" : undefined,
            }
            : agent,
        ),
      recoverySummary:
        command.action === "pause"
          ? [`run ${command.runId} paused by human-control`, ...snapshot.recoverySummary].slice(0, 4)
          : snapshot.recoverySummary,
      lastEventId: `event-${Date.now()}`,
    });

    const nextSnapshot = this.getSnapshot(command.projectId);
    const baseEvent = {
      eventId: nextSnapshot.lastEventId,
      occurredAt: new Date().toISOString(),
      projectId: command.projectId,
      sessionId: nextSnapshot.activeSessions[0]?.sessionId ?? "session-1",
      source: "human-control" as const,
    };

    this.emit({
      ...baseEvent,
      type: "RunStatusChanged",
      runId: command.runId,
      status: nextStatus,
    });
    this.emit({
      ...baseEvent,
      type: "AgentStatusChanged",
      agentId: nextSnapshot.activeAgents[0]?.agentId ?? "lead-agent",
      phase: "dev_loop",
      lastAction: `control:${command.action}`,
    });
    this.emit({
      ...baseEvent,
      type: "TerminalChunkAppended",
      terminalTarget:
        nextSnapshot.terminalTargets[0]?.terminalTarget ?? `${command.runId}:pty-0`,
      chunk: `[mock:${command.action}] run ${command.runId} -> ${nextStatus}`,
    });
    if (command.action !== "pause") {
      this.emit({
        ...baseEvent,
        type: "AudioCueRequested",
        cueKey:
          nextStatus === "terminated"
            ? `${activeActor}-completed`
            : `${activeActor}-started`,
        actor: activeActor,
        lifecycle: nextStatus === "terminated" ? "completed" : "started",
        reason: `run-${command.action}`,
      });
    }
  }

  subscribe(listener: EventListener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private emit(event: Parameters<EventListener>[0]) {
    this.listeners.forEach((listener) => {
      listener(event);
    });
  }

  private getSnapshot(projectId: string): ProbeSnapshot {
    const existing = this.snapshots.get(projectId);
    if (existing) {
      return existing;
    }

    const created = {
      ...structuredClone(mockSnapshot),
      projectSummary: {
        projectId,
        projectName: this.toProjectName(projectId),
      },
      activeSessions: [{ sessionId: `${projectId}-session-1`, status: "running" }],
      activeRuns: [{ runId: `${projectId}-run-1`, status: "in_dev" }],
      terminalTargets: [
        {
          terminalTarget: `${projectId}-run-1:pty-0`,
          sessionId: `${projectId}-session-1`,
        },
      ],
    } satisfies ProbeSnapshot;

    this.snapshots.set(projectId, created);
    return created;
  }

  private toProjectName(projectId: string): string {
    return projectId
      .split("-")
      .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
      .join(" ");
  }
}

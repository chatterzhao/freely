export type CommandSource =
  | "human-chat"
  | "human-control"
  | "auto-loop"
  | "recovery";

export type RunControlAction =
  | "start"
  | "pause"
  | "terminate"
  | "resume"
  | "retry";

export type ClientCommand =
  | {
      type: "CreateOrResumeSession";
      projectId: string;
      sessionId?: string;
      resumeHint?: string;
      commandSource: CommandSource;
    }
  | {
      type: "SendChatIntervention";
      projectId: string;
      sessionId: string;
      messageId: string;
      content: string;
      runId?: string;
      targetAgentId?: string;
    }
  | {
      type: "ControlRun";
      projectId: string;
      runId: string;
      action: RunControlAction;
      reason?: string;
    }
  | {
      type: "AttachTerminal";
      projectId: string;
      sessionId: string;
      terminalTarget: string;
      runId?: string;
      cursor?: string;
    }
  | {
      type: "RequestSnapshot";
      projectId: string;
      sessionId?: string;
      snapshotScope?: "project" | "session" | "run";
    };

export type BaseEvent = {
  eventId: string;
  occurredAt: string;
  projectId: string;
  sessionId: string;
  source: CommandSource | "system";
};

export type AudioCueActor = "manager" | "worker";

export type AudioCueLifecycle = "started" | "completed";

export type AudioCueKey =
  | "manager-started"
  | "manager-completed"
  | "worker-started"
  | "worker-completed";

export type ServerEvent =
  | (BaseEvent & { type: "SessionUpserted"; status: string })
  | (BaseEvent & { type: "RunStatusChanged"; runId: string; status: string })
  | (BaseEvent & {
      type: "AgentStatusChanged";
      agentId: string;
      phase: string;
      lastAction: string;
    })
  | (BaseEvent & {
      type: "TerminalChunkAppended";
      terminalTarget: string;
      chunk: string;
    })
  | (BaseEvent & {
      type: "GovernanceDecisionRecorded";
      decision: string;
      details: string;
    })
  | (BaseEvent & {
      type: "InputArbitrationRecorded";
      outcome: string;
      details: string;
    })
  | (BaseEvent & { type: "RecoveryStatusChanged"; runtimeState: string })
  | (BaseEvent & {
      type: "AudioCueRequested";
      cueKey: AudioCueKey;
      actor: AudioCueActor;
      lifecycle: AudioCueLifecycle;
      reason: string;
    });

export type ProbeSnapshot = {
  projectSummary: {
    projectId: string;
    projectName: string;
  };
  activeSessions: Array<{ sessionId: string; status: string }>;
  activeRuns: Array<{ runId: string; status: string }>;
  activeAgents: Array<{
    agentId: string;
    phase: string;
    lastAction: string;
    blocker?: string;
  }>;
  terminalTargets: Array<{ terminalTarget: string; sessionId: string }>;
  governanceSummary: string[];
  recoverySummary: string[];
  lastEventId: string;
};

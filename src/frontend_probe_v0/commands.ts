import type { ClientCommand, RunControlAction } from "./contracts";

export function createSnapshotRequest(projectId: string): ClientCommand {
  return {
    type: "RequestSnapshot",
    projectId,
    snapshotScope: "project",
  };
}

export function createOrResumeSessionCommand(
  projectId: string,
  sessionId?: string,
): ClientCommand {
  return {
    type: "CreateOrResumeSession",
    projectId,
    sessionId,
    commandSource: "human-control",
    resumeHint: sessionId ? "probe-ui-resume" : "probe-ui-create",
  };
}

export function createRunControlCommand(
  projectId: string,
  runId: string,
  action: RunControlAction,
): ClientCommand {
  return {
    type: "ControlRun",
    projectId,
    runId,
    action,
  };
}

export function createChatInterventionCommand(
  projectId: string,
  sessionId: string,
  content: string,
  runId?: string,
): ClientCommand {
  return {
    type: "SendChatIntervention",
    projectId,
    sessionId,
    messageId: `msg-${Date.now()}`,
    content,
    runId,
  };
}

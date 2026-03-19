import type { ProbeSnapshot } from "./contracts";

export const mockSnapshot: ProbeSnapshot = {
  projectSummary: {
    projectId: "freely",
    projectName: "Freely",
  },
  activeSessions: [{ sessionId: "session-1", status: "running" }],
  activeRuns: [{ runId: "run-1", status: "in_dev" }],
  activeAgents: [
    {
      agentId: "lead-agent",
      phase: "dev_loop",
      lastAction: "building probe shell",
    },
    {
      agentId: "worker-1",
      phase: "idle",
      lastAction: "awaiting next task",
    },
  ],
  terminalTargets: [{ terminalTarget: "run-1:pty-0", sessionId: "session-1" }],
  governanceSummary: ["laws-enforcer passed", "constitution-guard passed"],
  recoverySummary: [],
  lastEventId: "event-1",
};

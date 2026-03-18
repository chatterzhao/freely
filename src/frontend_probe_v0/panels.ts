import type { ProbeSnapshot } from "./contracts";

export type PanelId =
  | "control-bar"
  | "chat-intervention-panel"
  | "agent-roster"
  | "embedded-terminal";

export type PanelModel = {
  id: PanelId;
  title: string;
  summary: string;
};

export function buildPanelModels(snapshot: ProbeSnapshot): PanelModel[] {
  return [
    {
      id: "control-bar",
      title: "Control Bar",
      summary: `${snapshot.activeRuns.length} active run(s) ready for start/pause/terminate/resume/retry.`,
    },
    {
      id: "chat-intervention-panel",
      title: "Chat Intervention",
      summary: `Session count: ${snapshot.activeSessions.length}. Human input stays visible and traceable.`,
    },
    {
      id: "agent-roster",
      title: "Agent Roster",
      summary: `${snapshot.activeAgents.length} active agent(s) with phase and last-action visibility.`,
    },
    {
      id: "embedded-terminal",
      title: "Embedded Terminal",
      summary: `${snapshot.terminalTargets.length} terminal target(s) attachable from the current snapshot.`,
    },
  ];
}

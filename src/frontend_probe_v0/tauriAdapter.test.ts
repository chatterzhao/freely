// @ts-nocheck
import { describe, expect, it } from "bun:test";

import { TauriProbeAdapter } from "./tauriAdapter";

describe("TauriProbeAdapter", () => {
  it("wraps snapshot requests inside the payload arg expected by the tauri command", async () => {
    const calls: Array<{ command: string; payload?: Record<string, unknown> }> = [];
    const adapter = new TauriProbeAdapter(
      async (command, payload) => {
        calls.push({ command, payload });
        return {
          projectSummary: { projectId: "freely", projectName: "Freely" },
          activeSessions: [],
          activeRuns: [],
          activeAgents: [],
          terminalTargets: [],
          governanceSummary: [],
          recoverySummary: [],
          lastEventId: "event-1",
        };
      },
      async () => async () => {},
    );

    await adapter.requestSnapshot("freely");

    expect(calls).toEqual([
      {
        command: "probe_request_snapshot",
        payload: {
          payload: {
            projectId: "freely",
          },
        },
      },
    ]);
  });

  it("starts tauri event registration eagerly instead of waiting for the first subscription", async () => {
    const order: string[] = [];
    const adapter = new TauriProbeAdapter(
      async (command) => {
        order.push(`invoke:${command}`);
      },
      async () => {
        order.push("listen:start");
        order.push("listen:ready");
        return () => {};
      },
    );

    await adapter.sendCommand({
      type: "ControlRun",
      projectId: "freely",
      runId: "freely-run-1",
      action: "start",
    });
    expect(order).toEqual(["listen:start", "listen:ready", "invoke:probe_send_command"]);
  });
});

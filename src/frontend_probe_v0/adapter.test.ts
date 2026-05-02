// @ts-nocheck
import { describe, expect, it } from "bun:test";

import { MockProbeAdapter } from "./adapter";
import { createAttachTerminalCommand } from "./commands";

describe("MockProbeAdapter", () => {
  it("updates terminal attachment state and emits a terminal chunk when attaching", async () => {
    const adapter = new MockProbeAdapter();
    const events: string[] = [];
    const unsubscribe = adapter.subscribe((event) => {
      if (event.type === "TerminalChunkAppended") {
        events.push(`${event.terminalTarget}:${event.chunk}`);
      }
    });

    await adapter.sendCommand(
      createAttachTerminalCommand(
        "freely",
        "freely-session-2",
        "freely-run-2:pty-0",
        "freely-run-2",
      ),
    );

    const snapshot = await adapter.requestSnapshot("freely");
    unsubscribe();

    expect(snapshot.terminalTargets[0]).toEqual({
      terminalTarget: "freely-run-2:pty-0",
      sessionId: "freely-session-2",
    });
    expect(snapshot.governanceSummary[0]).toBe("terminal attached to freely-run-2:pty-0");
    expect(events).toEqual([
      "freely-run-2:pty-0:[mock:attach] attached to freely-run-2:pty-0",
    ]);
  });

  it("emits a worker-started audio cue when a worker-targeted chat is accepted", async () => {
    const adapter = new MockProbeAdapter();
    const audioEvents: string[] = [];
    const unsubscribe = adapter.subscribe((event) => {
      if (event.type === "AudioCueRequested") {
        audioEvents.push(`${event.cueKey}:${event.reason}`);
      }
    });

    await adapter.sendCommand({
      type: "SendChatIntervention",
      projectId: "freely",
      sessionId: "freely-session-1",
      messageId: "msg-1",
      content: "take this lane",
      targetAgentId: "worker-2",
    });

    unsubscribe();

    expect(audioEvents).toEqual([
      "worker-started:worker-targeted-chat-intervention",
    ]);
  });

  it("does not emit an audio cue for pause controls", async () => {
    const adapter = new MockProbeAdapter();
    const audioEvents: string[] = [];
    const unsubscribe = adapter.subscribe((event) => {
      if (event.type === "AudioCueRequested") {
        audioEvents.push(`${event.cueKey}:${event.reason}`);
      }
    });

    await adapter.sendCommand({
      type: "ControlRun",
      projectId: "freely",
      runId: "freely-run-1",
      action: "pause",
    });

    unsubscribe();

    expect(audioEvents).toEqual([]);
  });
});

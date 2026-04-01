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
});

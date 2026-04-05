// @ts-nocheck
import { describe, expect, it } from "bun:test";

import { getAudioCueKey } from "./audioCuePolicy";

describe("audioCuePolicy", () => {
  it("extracts the cue key from AudioCueRequested events", () => {
    expect(
      getAudioCueKey({
        type: "AudioCueRequested",
        eventId: "event-1",
        occurredAt: "2026-04-05T00:00:00Z",
        projectId: "freely",
        sessionId: "session-1",
        source: "system",
        cueKey: "worker-completed",
        actor: "worker",
        lifecycle: "completed",
        reason: "run-terminate",
      }),
    ).toBe("worker-completed");
  });

  it("ignores non-audio events", () => {
    expect(
      getAudioCueKey({
        type: "RunStatusChanged",
        eventId: "event-2",
        occurredAt: "2026-04-05T00:00:00Z",
        projectId: "freely",
        sessionId: "session-1",
        source: "system",
        runId: "run-1",
        status: "in_dev",
      }),
    ).toBeNull();
  });
});

import { useEffect, useRef, useState } from "react";

import type { ProbeAdapter } from "./adapter";
import {
  createChatInterventionCommand,
  createOrResumeSessionCommand,
  createRunControlCommand,
} from "./commands";
import type { ServerEvent, ProbeSnapshot } from "./contracts";

type ValidationStatus = "idle" | "running" | "passed" | "failed";
type ValidationStepName = "start" | "session" | "chat";
type ValidationStepState = "pending" | "passed" | "failed";

type ValidationSequenceState = {
  status: ValidationStatus;
  error: string | null;
  steps: Record<ValidationStepName, ValidationStepState>;
};

type ValidationSequenceOptions = {
  adapter: ProbeAdapter;
  events: ServerEvent[];
  projectId: string;
  runtimeMode: "mock" | "tauri";
  snapshot: ProbeSnapshot | null;
  validationMode?: "off" | "tauri-smoke";
};

const defaultState = (): ValidationSequenceState => ({
  status: "idle",
  error: null,
  steps: {
    start: "pending",
    session: "pending",
    chat: "pending",
  },
});

function delay(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

export function useTauriValidationSequence({
  adapter,
  projectId,
  runtimeMode,
  snapshot,
  validationMode = "off",
}: ValidationSequenceOptions) {
  const [state, setState] = useState<ValidationSequenceState>(() => defaultState());
  const snapshotRef = useRef(snapshot);
  const startedRef = useRef(false);

  snapshotRef.current = snapshot;

  useEffect(() => {
    if (validationMode !== "tauri-smoke" || runtimeMode !== "tauri" || !snapshot) {
      return;
    }
    if (startedRef.current) {
      return;
    }

    startedRef.current = true;
    const runId = snapshot.activeRuns[0]?.runId ?? `${projectId}-run-1`;
    const sessionId = `${projectId}-validation-session`;
    const validationMessage = "tauri validation ping";

    const refreshSnapshotUntil = async (
      predicate: (nextSnapshot: ProbeSnapshot) => boolean,
      label: string,
    ) => {
      const startedAt = Date.now();
      while (Date.now() - startedAt < 5000) {
        const nextSnapshot = await adapter.requestSnapshot(projectId);
        snapshotRef.current = nextSnapshot;
        if (predicate(nextSnapshot)) {
          return nextSnapshot;
        }
        await delay(100);
      }
      throw new Error(`timed out waiting for ${label}`);
    };

    const run = async () => {
      setState((current) => ({ ...current, status: "running", error: null }));

      await adapter.sendCommand(
        createRunControlCommand(projectId, runId, "start"),
      );
      await refreshSnapshotUntil(
        (nextSnapshot) =>
          nextSnapshot.activeRuns.some(
            (run) => run.runId === runId && run.status === "in_dev",
          ),
        "run status refresh after start",
      );
      setState((current) => ({
        ...current,
        steps: { ...current.steps, start: "passed" },
      }));

      await adapter.sendCommand(
        createOrResumeSessionCommand(projectId, sessionId),
      );
      await refreshSnapshotUntil(
        (nextSnapshot) =>
          nextSnapshot.activeSessions.some(
            (session) => session.sessionId === sessionId,
          ),
        "session refresh after validation resume",
      );
      setState((current) => ({
        ...current,
        steps: { ...current.steps, session: "passed" },
      }));

      await adapter.sendCommand(
        createChatInterventionCommand(
          projectId,
          sessionId,
          validationMessage,
          runId,
        ),
      );
      await refreshSnapshotUntil(
        (nextSnapshot) =>
          nextSnapshot.governanceSummary.some((summary) =>
            summary.includes("chat intervention accepted"),
          ),
        "snapshot refresh after validation chat",
      );
      setState((current) => ({
        ...current,
        status: "passed",
        steps: { ...current.steps, chat: "passed" },
      }));
    };

    void run().catch((error) => {
      const message = error instanceof Error ? error.message : String(error);
      setState((current) => ({
        ...current,
        status: "failed",
        error: message,
      }));
    });
  }, [adapter, projectId, runtimeMode, snapshot, validationMode]);

  return state;
}

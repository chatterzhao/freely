import { useEffect, useMemo, useState } from "react";

import type { ProbeAdapter } from "./adapter";
import { createAttachTerminalCommand } from "./commands";

export function useProbeTerminalAttach(
  projectId: string,
  sessionId: string | undefined,
  runId: string | undefined,
  terminalTargets: Array<{ terminalTarget: string; sessionId: string }>,
  adapter: ProbeAdapter,
) {
  const [attachedTarget, setAttachedTarget] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (terminalTargets.length === 0) {
      setAttachedTarget(null);
      return;
    }

    if (
      attachedTarget &&
      terminalTargets.some((target) => target.terminalTarget === attachedTarget)
    ) {
      return;
    }

    setAttachedTarget(terminalTargets[0]?.terminalTarget ?? null);
  }, [attachedTarget, terminalTargets]);

  return useMemo(
    () => ({
      attachedTarget,
      error,
      submitting,
      attach: async (terminalTarget: string) => {
        if (!sessionId) {
          setError("session required before attaching terminal");
          return;
        }

        setSubmitting(true);
        try {
          await adapter.sendCommand(
            createAttachTerminalCommand(projectId, sessionId, terminalTarget, runId),
          );
          setAttachedTarget(terminalTarget);
          setError(null);
        } catch (cause) {
          setError(cause instanceof Error ? cause.message : String(cause));
        } finally {
          setSubmitting(false);
        }
      },
    }),
    [adapter, attachedTarget, error, projectId, runId, sessionId, submitting],
  );
}

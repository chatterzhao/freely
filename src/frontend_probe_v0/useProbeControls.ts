import { useMemo, useState } from "react";

import type { ProbeAdapter } from "./adapter";
import { createRunControlCommand } from "./commands";

export function useProbeControls(
  projectId: string,
  runId: string | undefined,
  adapter: ProbeAdapter,
) {
  const [error, setError] = useState<string | null>(null);

  return useMemo(
    () => ({
      error,
      trigger: async (action: "start" | "pause" | "terminate" | "resume" | "retry") => {
        if (!runId) {
          return;
        }

        try {
          await adapter.sendCommand(createRunControlCommand(projectId, runId, action));
          setError(null);
        } catch (cause) {
          setError(cause instanceof Error ? cause.message : String(cause));
        }
      },
    }),
    [adapter, error, projectId, runId],
  );
}

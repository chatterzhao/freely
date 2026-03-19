import { useState } from "react";

import type { ProbeAdapter } from "./adapter";
import { createOrResumeSessionCommand } from "./commands";

export function useProbeSessionLifecycle(
  projectId: string,
  sessionId: string | undefined,
  adapter: ProbeAdapter,
) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createOrResume = async () => {
    setSubmitting(true);
    try {
      await adapter.sendCommand(createOrResumeSessionCommand(projectId, sessionId));
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
    } finally {
      setSubmitting(false);
    }
  };

  return {
    createOrResume,
    error,
    submitting,
  };
}

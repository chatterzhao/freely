import { useState } from "react";

import type { ProbeAdapter } from "./adapter";
import { createChatInterventionCommand } from "./commands";

export function useProbeChatIntervention(
  projectId: string,
  sessionId: string | undefined,
  runId: string | undefined,
  adapter: ProbeAdapter,
) {
  const [draft, setDraft] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    if (!sessionId || !draft.trim()) {
      return;
    }

    setSubmitting(true);
    try {
      await adapter.sendCommand(
        createChatInterventionCommand(projectId, sessionId, draft.trim(), runId),
      );
      setDraft("");
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
    } finally {
      setSubmitting(false);
    }
  };

  return {
    draft,
    error,
    setDraft,
    submit,
    submitting,
  };
}

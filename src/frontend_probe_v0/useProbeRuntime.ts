import { useEffect, useState } from "react";

import type { ProbeSnapshot } from "./contracts";
import type { ProbeAdapter } from "./adapter";
import { createProbeAdapter } from "./createAdapter";
import { isEventCapableAdapter } from "./events";

export function useProbeRuntime(
  projectId: string,
  adapter?: ProbeAdapter,
) {
  const [resolvedAdapter] = useState<ProbeAdapter>(() => adapter ?? createProbeAdapter());
  const [snapshot, setSnapshot] = useState<ProbeSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const refreshSnapshot = async () => {
      setLoading(true);
      try {
        const nextSnapshot = await resolvedAdapter.requestSnapshot(projectId);
        if (!cancelled) {
          setSnapshot(nextSnapshot);
          setError(null);
          setLoading(false);
        }
      } catch (cause) {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : String(cause));
          setLoading(false);
        }
      }
    };

    void refreshSnapshot();

    if (!isEventCapableAdapter(resolvedAdapter)) {
      return () => {
        cancelled = true;
      };
    }

    const unsubscribe = resolvedAdapter.subscribe(() => {
      if (!cancelled) {
        void refreshSnapshot();
      }
    });

    return () => {
      cancelled = true;
      unsubscribe();
    };
  }, [projectId, resolvedAdapter]);

  return {
    adapter: resolvedAdapter,
    error,
    snapshot,
    loading,
  };
}

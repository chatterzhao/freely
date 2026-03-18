import { useEffect, useState } from "react";

import type { ProbeAdapter } from "./adapter";
import type { ServerEvent } from "./contracts";
import { isEventCapableAdapter } from "./events";

export function useProbeEvents(adapter: ProbeAdapter) {
  const [events, setEvents] = useState<ServerEvent[]>([]);

  useEffect(() => {
    if (!isEventCapableAdapter(adapter)) {
      return;
    }

    return adapter.subscribe((event) => {
      setEvents((current) => [...current, event].slice(-20));
    });
  }, [adapter]);

  return events;
}

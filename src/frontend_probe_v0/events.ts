import type { ProbeAdapter } from "./adapter";
import type { ServerEvent } from "./contracts";

export type EventListener = (event: ServerEvent) => void;

export interface EventCapableProbeAdapter extends ProbeAdapter {
  subscribe(listener: EventListener): () => void;
}

export function isEventCapableAdapter(
  adapter: ProbeAdapter,
): adapter is EventCapableProbeAdapter {
  return "subscribe" in adapter;
}

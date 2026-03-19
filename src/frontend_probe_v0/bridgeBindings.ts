export type ProbeBridgeBindings = {
  requestSnapshotCommand: string;
  sendCommandCommand: string;
  serverEventName: string;
};

export const defaultProbeBridgeBindings: ProbeBridgeBindings = {
  requestSnapshotCommand: "probe_request_snapshot",
  sendCommandCommand: "probe_send_command",
  serverEventName: "probe_server_event",
};

export function resolveProbeBridgeBindings(
  overrides?: Partial<ProbeBridgeBindings> | null,
): ProbeBridgeBindings {
  return {
    ...defaultProbeBridgeBindings,
    ...overrides,
  };
}

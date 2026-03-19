import { MockProbeAdapter } from "./adapter";
import {
  resolveProbeBridgeBindings,
  type ProbeBridgeBindings,
} from "./bridgeBindings";
import { isEventCapableAdapter } from "./events";
import type { TauriRuntime } from "./tauriRuntime";

export function createMockTauriRuntime(
  overrides?: Partial<ProbeBridgeBindings> | null,
): TauriRuntime {
  const bindings = resolveProbeBridgeBindings(overrides);
  const adapter = new MockProbeAdapter();

  return {
    async invoke(command, payload) {
      if (command === bindings.requestSnapshotCommand) {
        return (await adapter.requestSnapshot(
          String(payload?.projectId ?? "freely"),
        )) as never;
      }

      if (command === bindings.sendCommandCommand) {
        await adapter.sendCommand(payload?.command as never);
        return undefined as never;
      }

      throw new Error(`Unsupported mock Tauri invoke command: ${command}`);
    },
    async listen(eventName, listener) {
      if (eventName !== bindings.serverEventName) {
        throw new Error(`Unsupported mock Tauri event: ${eventName}`);
      }

      if (!isEventCapableAdapter(adapter)) {
        return () => {};
      }

      return adapter.subscribe((event) => {
        listener({ payload: event });
      });
    },
  };
}

export function createBrokenTauriRuntime(message = "bridge offline"): TauriRuntime {
  return {
    async invoke() {
      throw new Error(message);
    },
    async listen() {
      return () => {};
    },
  };
}

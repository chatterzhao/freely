import { MockProbeAdapter, type ProbeAdapter } from "./adapter";
import type { ProbeBridgeBindings } from "./bridgeBindings";
import { TauriProbeAdapter } from "./tauriAdapter";
import type { TauriRuntime } from "./tauriRuntime";

export function createProbeAdapter(
  runtime?: TauriRuntime | null,
  bindings?: ProbeBridgeBindings,
): ProbeAdapter {
  if (runtime) {
    return new TauriProbeAdapter(runtime.invoke, runtime.listen, bindings);
  }

  return new MockProbeAdapter();
}

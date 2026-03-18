import { bootstrapProbeApp } from "./bootstrap";
import type { ProbeBridgeBindings } from "./bridgeBindings";
import { resolveProbeBridgeBindings } from "./bridgeBindings";
import { resolveTauriRuntime, type TauriInvoke, type TauriListen } from "./tauriRuntime";

declare global {
  interface Window {
    __TAURI__?: {
      invoke?: TauriInvoke;
      listen?: TauriListen;
      core?: {
        invoke?: TauriInvoke;
      };
      event?: {
        listen?: TauriListen;
      };
    };
    __FREELY_PROBE_BRIDGE__?: Partial<ProbeBridgeBindings>;
    __FREELY_PROBE_MANIFEST__?: typeof import("./bridgeManifest").probeBridgeManifest;
    __FREELY_PROBE_TRANSPORT__?: "mock" | "tauri-mock" | "tauri-broken";
  }
}

type DefaultProbeAppOptions = {
  projectId?: string;
};

export function createDefaultProbeApp(options?: DefaultProbeAppOptions) {
  return bootstrapProbeApp(resolveTauriRuntime(window.__TAURI__), {
    ...options,
    bridgeBindings: resolveProbeBridgeBindings(window.__FREELY_PROBE_BRIDGE__),
  });
}

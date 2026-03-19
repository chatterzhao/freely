import { AppShell } from "./AppShell";
import { resolveProbeBridgeBindings } from "./bridgeBindings";
import { probeBridgeManifest } from "./bridgeManifest";
import type { ProbeBridgeBindings } from "./bridgeBindings";
import { createProbeAdapter } from "./createAdapter";
import type { TauriRuntime } from "./tauriRuntime";

type BootstrapOptions = {
  projectId?: string;
  bridgeBindings?: ProbeBridgeBindings;
  transportMode?: "mock" | "tauri-mock" | "tauri-broken";
};

export function bootstrapProbeApp(
  runtime?: TauriRuntime | null,
  options: BootstrapOptions = {},
) {
  const bridgeBindings = resolveProbeBridgeBindings(options.bridgeBindings);
  const adapter = createProbeAdapter(runtime, bridgeBindings);
  const projectId = options.projectId ?? "freely";
  const runtimeMode = runtime ? "tauri" : "mock";
  const transportMode = options.transportMode ?? "mock";

  function BoundAppShell() {
    return (
      <AppShell
        adapter={adapter}
        bridgeBindings={bridgeBindings}
        bridgeContractVersion={probeBridgeManifest.contractVersion}
        projectId={projectId}
        runtimeMode={runtimeMode}
        transportMode={transportMode}
      />
    );
  }

  return {
    adapter,
    AppShell: BoundAppShell,
    bridgeBindings,
    bridgeContractVersion: probeBridgeManifest.contractVersion,
    projectId,
    runtimeMode,
    transportMode,
  };
}

import { createRoot } from "react-dom/client";

import { probeBridgeManifest } from "./bridgeManifest";
import { createBrokenTauriRuntime, createMockTauriRuntime } from "./mockTauriRuntime";
import { mountProbeIntoRoot } from "./host";

const container = document.getElementById("root");

if (!container) {
  throw new Error("Missing #root container for Frontend Probe v0");
}

const root = createRoot(container);

const searchParams = new URLSearchParams(window.location.search);
const transportParam = searchParams.get("transport");
const requestedTransport =
  window.__FREELY_PROBE_TRANSPORT__ ??
  (transportParam === "tauri-mock"
    ? "tauri-mock"
    : transportParam === "tauri-broken"
      ? "tauri-broken"
      : "mock");

window.__FREELY_PROBE_MANIFEST__ = probeBridgeManifest;

if (requestedTransport === "tauri-mock" && !window.__TAURI__) {
  window.__TAURI__ = createMockTauriRuntime(window.__FREELY_PROBE_BRIDGE__);
}

if (requestedTransport === "tauri-broken" && !window.__TAURI__) {
  window.__TAURI__ = createBrokenTauriRuntime();
}

mountProbeIntoRoot(root, {
  projectId: "freely",
  transportMode: requestedTransport,
});

import { createElement } from "react";

import { createDefaultProbeApp } from "./entry";

type RootLike = {
  render(component: unknown): void;
};

type HostOptions = {
  projectId?: string;
  transportMode?: "mock" | "tauri-mock" | "tauri-broken";
  validationMode?: "off" | "tauri-smoke";
};

export function mountProbeIntoRoot(root: RootLike, options?: HostOptions) {
  const { AppShell } = createDefaultProbeApp(options);
  root.render(createElement(AppShell));
}
